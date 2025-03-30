from flask import Flask, render_template
import os
import boto3
import shutil

app = Flask(__name__)

# Read background image info from env vars
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")
S3_OBJECT_KEY = os.environ.get("S3_OBJECT_KEY")

# Read name to display
MY_NAME = os.environ.get("MY_NAME", "Reh")

# Download image from S3 and copy to static
def download_background_image():
    try:
        s3 = boto3.client('s3')
        local_path = "/tmp/bg.jpg"
        print(f"Downloading image from S3: {S3_BUCKET_NAME}/{S3_OBJECT_KEY}")
        s3.download_file(S3_BUCKET_NAME, S3_OBJECT_KEY, local_path)
        os.makedirs("static", exist_ok=True)
        shutil.copy(local_path, "static/bg.jpg")
        print("Image downloaded and copied to static/bg.jpg")
    except Exception as e:
        print(f"Error downloading image: {e}")

# Download once on app start
download_background_image()

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('addemp.html', name=MY_NAME)

@app.route("/about", methods=['GET','POST'])
def about():
    return render_template('about.html', name=MY_NAME)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)
