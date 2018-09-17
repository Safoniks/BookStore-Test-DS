docker-compose up --build -d

docker-compose exec web_app python3 manage.py migrate

docker-compose exec web_app python3 manage.py loaddata initial_data


--> http://0.0.0.0:8007/

docker-compose exec web_app python3 manage.py get_books -o desc