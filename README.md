//Installing Rest Framework for Django

pip3 install djangorestframework
pip install markdown
pip install django-filter 

//Install PostgresSql

Download the PostgreSQL installer for Windows from the official website:
https://www.postgresql.org/download/windows/
Steps While Installing:
1.) Don't change the username
2.) Set the password as postgres@321
3.) Port Used will be 5432
4.) Rest Everything to be used as default setting

Configure Django With Postgres
1.)python3 -m  pip install psycopg2
2.)Run the Microservice (python3 DbOperations.py) and check the output is "Database connected successfully"
3.)Run python3 manage.py migrate
4.)Run python3 manage.py makemigrations

//Install Faker
python3 -Spam  pip install faker

