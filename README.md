# Talents of Tomorrow Web Application (Developer documentation)

## 1. Overview

The Talents of Tomorrow Web Application is used by Talents of Tomorrow and its clients to collect and present data on the usage of its applications and services.

## 2. Requirements

* Python 3.5.1
* virtualenv
* PostgresSQL

## 3. Installation

Install virtualenv via pip:

```
$ pip install virtualenv
```

virtualenv venv will create a folder in the current directory with Python 3.5.1 as interpreter. To begin using the virtual environment, it needs to be activated.

```
$ virtualenv -p /Library/Frameworks/Python.framework/Versions/3.5/bin/python3.5 venv
$ source venv/bin/activate
```

Install the required packages using the same versions with following command:

```
$ pip install -r requirements.txt
```

This will help ensure consistency across installations, across deployments, and across developers.
Please remember to exclude the virtual environment folder from source control by adding it to the ignore list.

Create the db and add a user with following command:

```
$ createdb tot-db
$ psql
# CREATE USER test WITH PASSWORD 'test123';
# GRANT ALL PRIVILEGES ON DATABASE "tot-db" to test;
```

Create the tables in the database before we can use them. To do that, run the following command:

```
$ python manage.py makemigrations
$ python manage.py migrate
```

Afterwards create a user who can login to the admin site. Run the following command:

```
$ python manage.py createsuperuser
```

If the server is not running start it like so:

```
$ python manage.py runserver
```

## 4. Authentication

Talents of Tomorrow Web Application is using the JSON Web Token Authentication support for Django REST Framework.

If you want to know more about JWT, check out the following resources:

* [Auth with JSON Web Tokens](http://jpadilla.com/post/73791304724/auth-with-json-web-tokens)
* [JWT.io](http://jwt.io/)


You can easily test if the endpoint is working by doing the following in your terminal, if you had a user created with the username admin and password abc123.

```
$ curl -X POST -d "username=admin&password=abc123" http://localhost:8000/api-token-auth/
```

Alternatively, you can use all the content types supported by the Django REST framework to obtain the auth token. For example:

```
$ curl -X POST -H "Content-Type: application/json" -d '{"username":"admin","password":"abc123"}' http://localhost:8000/api-token-auth/
```

Now in order to access protected api urls you must include the Authorization: JWT <your_token> header.

```
$ curl -H "Authorization: JWT <your_token>" http://localhost:8000/protected-url/
```

### 4.1 Refresh Token

Pass in an existing token to the refresh endpoint as follows: {"token": EXISTING_TOKEN}. Note that only non-expired tokens will work. The JSON response looks the same as the normal obtain token endpoint {"token": NEW_TOKEN}.

```
$ curl -X POST -H "Content-Type: application/json" -d '{"token":"<EXISTING_TOKEN>"}' http://localhost:8000/api-token-refresh/
```

## 5. Talents of Tomorrow Web Application


### 5.1 Endpoint

__Method:__ POST

__URL:__ //

__Headers:__
* Authorization: Token ...
* Content-type: application/json

__Data:__

```javascript
[
  {
    'test': '9783502390848',                // String
    'test': '73',                           // String
  },
  // ...
]
```


__Success response:__

| Status code | Body    | Explanation |
|:------------|:--------|:------------|
| 201         | _Empty_ | Created     |

__Error responses:__

TBD

| Status code | Body               | Explanation                                       |
|:------------|:-------------------|:--------------------------------------------------|
| 40x         | `{"error": "..."}` | Client Error - Don't repeat without modifications |
| 50x         | `{"error": "..."}` | Server Error                                      |

### 3.2 Data

TBD


### 3.3 Implementation

##### Edge cases

## 3. Coach view

TBD

## 4. Club view

TBD

## 5. Player view

TBD