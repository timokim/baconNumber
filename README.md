# baconNumber
Calculates the bacon number of a given actor

# How It Was Installed
## Env setup
```
python3 -m venv env
source env/bin/activate
pip install django
```

## Create project/app
```
django-admin startproject baconNumber
cd baconNumber
django-admin startapp myapp
```

## Apply changes / Run
```
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```

# How to work with the API
Use the browser to access the django server API via the following URLs:
```
localhost:8000/preprocess
localhost:8000/getBaconNumber/<actor_name>
```