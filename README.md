## Install packages
pip install -r requirements.txt
## Install Postgres
Make sure postgres is installed on machine and service is running
## Create Database
createdb -h localhost -p port -U username tododb
## Run app
python app.py
Running the app will automatically create the tables in the postgres database

## Using postman try different endpoints
localhost:5000/todo


localhost:5000/todo/<todo_id>


localhost:5000/todo/<todo_id>/comments


localhost:5000/todo/<todo_id>/comments/<comment_id>'
