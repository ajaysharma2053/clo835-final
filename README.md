RUNNING IT LOCALLY OR IN CLOUD9

-----------------------------------------------
#Building Images

docker build -t flask-app -f Dockerfile .
docker build -t mysql-db -f Dockerfile_mysql .

----------------------------------------------
#Creating Network

docker network create clo835-net

--------------------------------------
#Running MySQL image container

docker run --name mysql-db \
  --network clo835-net \
  -e MYSQL_ROOT_PASSWORD=pw \
  -p 3307:3306 \
  -d mysql-db
  
  
-----------------------------------
#Running App image container

docker run --name flask-app \
  --network clo835-net \
  -p 8080:81 \
  -e DBHOST=mysql-db \
  -e DBPORT=3306 \
  -e DBUSER=root \
  -e DBPWD=pw \
  -e DATABASE=employees \
  -e S3_BUCKET_NAME=clo835-background-imgs \
  -e S3_OBJECT_KEY=bg.jpg \
  -e MY_NAME="Salisha-Pratima-Ajay" \
  -v ~/.aws:/root/.aws \
  flask-app
--------------------------------------


ADDITONAL INSFORMATION

# Install the required MySQL package

sudo apt-get update -y
sudo apt-get install mysql-client -y

# Running application locally
pip3 install -r requirements.txt
sudo python3 app.py
# Building and running 2 tier web application locally
### Building mysql docker image 
```docker build -t my_db -f Dockerfile_mysql . ```

### Building application docker image 
```docker build -t my_app -f Dockerfile . ```

### Running mysql
```docker run -d -e MYSQL_ROOT_PASSWORD=pw  my_db```


### Get the IP of the database and export it as DBHOST variable
```docker inspect <container_id>```


### Example when running DB runs as a docker container and app is running locally
```
export DBHOST=127.0.0.1
export DBPORT=3307
```
### Example when running DB runs as a docker container and app is running locally
```
export DBHOST=172.17.0.2
export DBPORT=3306
```
```
export DBUSER=root
export DATABASE=employees
export DBPWD=pw
export APP_COLOR=blue
```
### Run the application, make sure it is visible in the browser
```docker run -p 8080:8080  -e DBHOST=$DBHOST -e DBPORT=$DBPORT -e  DBUSER=$DBUSER -e DBPWD=$DBPWD  my_app```
