from flask import Flask, render_template, request
from pymysql import connections
import os
import random
import argparse
import boto3
import shutil

app = Flask(__name__)

# Read MySQL DB config from env vars or default
DBHOST = os.environ.get("DBHOST", "localhost")
DBUSER = os.environ.get("DBUSER", "root")
DBPWD = os.environ.get("DBPWD", "password")
DATABASE = os.environ.get("DATABASE", "employees")
DBPORT = int(os.environ.get("DBPORT", 3306))

# Read background image info from env vars
BG_IMAGE_URL = os.environ.get("BG_IMAGE_URL")
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")
S3_OBJECT_KEY = os.environ.get("S3_OBJECT_KEY")

# Read name to display from env var
MY_NAME = os.environ.get("MY_NAME", "Salisha-Pratima-Ajay")

# Download image from S3 and copy to static
def download_background_image():
    try:
        s3 = boto3.client('s3')
        local_path = "/tmp/bg.jpg"
        print(f"Downloading background image from S3 bucket: {S3_BUCKET_NAME}, key: {S3_OBJECT_KEY}")
        s3.download_file(S3_BUCKET_NAME, S3_OBJECT_KEY, local_path)
        # Copy to static folder
        os.makedirs("static", exist_ok=True)
        shutil.copy(local_path, "static/bg.jpg")
        print(f"Background image downloaded and copied to static/bg.jpg")
    except Exception as e:
        print(f"Error downloading background image: {e}")

# Trigger image download at app startup
download_background_image()

# MySQL connection
db_conn = connections.Connection(
    host=DBHOST,
    port=DBPORT,
    user=DBUSER,
    password=DBPWD,
    db=DATABASE
)

table = 'employee'

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('addemp.html', name=MY_NAME)

@app.route("/about", methods=['GET','POST'])
def about():
    return render_template('about.html', name=MY_NAME)

@app.route("/addemp", methods=['POST'])
def AddEmp():
    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    primary_skill = request.form['primary_skill']
    location = request.form['location']

    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    try:
        cursor.execute(insert_sql, (emp_id, first_name, last_name, primary_skill, location))
        db_conn.commit()
        emp_name = f"{first_name} {last_name}"
    finally:
        cursor.close()

    print("New employee added:", emp_name)
    return render_template('addempoutput.html', name=emp_name)

@app.route("/getemp", methods=['GET', 'POST'])
def GetEmp():
    return render_template("getemp.html", name=MY_NAME)

@app.route("/fetchdata", methods=['GET','POST'])
def FetchData():
    emp_id = request.form['emp_id']
    output = {}

    select_sql = "SELECT emp_id, first_name, last_name, primary_skill, location FROM employee WHERE emp_id=%s"
    cursor = db_conn.cursor()

    try:
        cursor.execute(select_sql, (emp_id,))
        result = cursor.fetchone()
        output["emp_id"] = result[0]
        output["first_name"] = result[1]
        output["last_name"] = result[2]
        output["primary_skills"] = result[3]
        output["location"] = result[4]
    except Exception as e:
        print(f"Error fetching employee: {e}")
    finally:
        cursor.close()

    return render_template("getempoutput.html", id=output["emp_id"], fname=output["first_name"],
                           lname=output["last_name"], interest=output["primary_skills"],
                           location=output["location"], name=MY_NAME)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--color', required=False)
    args = parser.parse_args()

    print(f"App running on port 81. BG_IMAGE_URL = {BG_IMAGE_URL}")
    app.run(host='0.0.0.0', port=81, debug=True)
