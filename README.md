[![Circle CI](https://circleci.com/gh/jojacobsen/talentsoftomorrow.svg?style=svg&circle-token=8f459840b266a7a5aa538e429c3221f2977b9b56)](https://circleci.com/gh/jojacobsen/talentsoftomorrow)

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
$ python manage.py runserver --settings=talentsoftomorrow.settings_development
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


### 5.1 Endpoints

### 5.1.1 List of players
__Method:__ GET

__URL:__ /players/

__Headers:__
* Authorization: JWT ...
* Content-type: application/json


__Success response:__

| Status code | Body    | Explanation |
|:------------|:--------|:------------|
| 200         | _JSON_  | OK          |

__Error responses:__

TBD

| Status code | Body               | Explanation                                       |
|:------------|:-------------------|:--------------------------------------------------|
| 40x         | `{"error": "..."}` | Client Error - Don't repeat without modifications |
| 50x         | `{"error": "..."}` | Server Error                                      |

__JSON Response:__

```javascript
[
  {
    "id": 1,
    "user": {
      "id": 8,
      "username": "Ibra",
      "last_name": "",
      "first_name": "",
      "email": ""
    },
    "lab_key": "1234",
    "gender": "M",
    "birthday": "2016-03-18"
  },
  // ...
]
```

### 5.1.2 Detail view of player
__Method:__ GET

__URL:__ /player/{ player_id }

__Headers:__
* Authorization: JWT ...
* Content-type: application/json


__Success response:__

| Status code | Body    | Explanation |
|:------------|:--------|:------------|
| 200         | _JSON_  | OK          |

__Error responses:__

TBD

| Status code | Body               | Explanation                                       |
|:------------|:-------------------|:--------------------------------------------------|
| 40x         | `{"error": "..."}` | Client Error - Don't repeat without modifications |
| 50x         | `{"error": "..."}` | Server Error                                      |

__JSON Response:__

```javascript
{
  "id": 1,
  "user": {
    "id": 8,
    "username": "Ibra",
    "last_name": "",
    "first_name": "",
    "email": ""
  },
  "lab_key": "1234",
  "gender": "M",
  "birthday": "2016-03-18",
  "coaches": [
    {
      "id": 1,
      "club": {
        "id": 1,
        "user": {
          "id": 3,
          "username": "Arsenal",
          "last_name": "",
          "first_name": "",
          "email": ""
        }
      },
      "user": {
        "id": 5,
        "username": "Bruno",
        "last_name": "",
        "first_name": "",
        "email": ""
      }
    }
  ],
  "club": {
    "id": 1,
    "user": {
      "id": 3,
      "username": "Arsenal",
      "last_name": "",
      "first_name": "",
      "email": ""
    }
  }
}
```

### 5.1.3 Add new player
__Method:__ POST

__URL:__ /players/

__Headers:__
* Authorization: JWT ...
* Content-type: application/json


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

__Data:__

```javascript
[
  {
    "user": {"last_name": "Carlos", "first_name": "Roberto"},
    "gender": "M",
    "birthday": "2010-03-18",
    "coach": [1]
  },
  // ...
]
```


### 5.1.4 List of performances
__Method:__ GET

__URL:__ /performances/

__Headers:__
* Authorization: JWT ...
* Content-type: application/json


__Success response:__

| Status code | Body    | Explanation |
|:------------|:--------|:------------|
| 200         | _JSON_  | OK          |

__Error responses:__

TBD

| Status code | Body               | Explanation                                       |
|:------------|:-------------------|:--------------------------------------------------|
| 40x         | `{"error": "..."}` | Client Error - Don't repeat without modifications |
| 50x         | `{"error": "..."}` | Server Error                                      |

__JSON Response:__

```javascript
[
  {
    "id": 1,
    "value": "198.0000000000",
    "date": "2016-03-18",
    "description": "",
    "player": 1,
    "measurement": 2
  },
  {
    "id": 2,
    "value": "3.0000000000",
    "date": "2016-03-18",
    "description": "",
    "player": 2,
    "measurement": 1
  },
  // ...
]
```

### 5.1.5 Detail view of performance
__Method:__ GET

__URL:__ /performance/{ performance_id }

__Headers:__
* Authorization: JWT ...
* Content-type: application/json


__Success response:__

| Status code | Body    | Explanation |
|:------------|:--------|:------------|
| 200         | _JSON_  | OK          |

__Error responses:__

TBD

| Status code | Body               | Explanation                                       |
|:------------|:-------------------|:--------------------------------------------------|
| 40x         | `{"error": "..."}` | Client Error - Don't repeat without modifications |
| 50x         | `{"error": "..."}` | Server Error                                      |

__JSON Response:__

```javascript
{
  "id": 1,
  "value": "198.0000000000",
  "date": "2016-03-18",
  "description": "",
  "player": 1,
  "measurement": 2
}
```

### 5.1.6 Add new performances
__Method:__ POST

__URL:__ /performances/

__Headers:__
* Authorization: JWT ...
* Content-type: application/json


__Success response:__

| Status code | Body    | Explanation |
|:------------|:--------|:------------|
| 200         | _JSON_ | Created     |

__Error responses:__

TBD

| Status code | Body               | Explanation                                       |
|:------------|:-------------------|:--------------------------------------------------|
| 40x         | `{"error": "..."}` | Client Error - Don't repeat without modifications |
| 50x         | `{"error": "..."}` | Server Error                                      |

__Data:__

```javascript
[
  {
    "value": "224.0000000000",
    "player": 1,
    "date": "2016-12-2",
    "measurement": 2,
    "description": "had too long hairs today..."
  },
  // ...
]
```


__Return Object:__

```javescript
[
  {
    "id": 33,
    "value": "224.0000000000",
    "date": "2016-12-02",
    "description": "asdfdsafdsflkjlasdkjflkjadslkf",
    "player": 1,
    "measurement": 2
  },
  //...
]
```

### 5.1.7 List of coaches
__Method:__ GET

__URL:__ /coaches/

__Headers:__
* Authorization: JWT ...
* Content-type: application/json


__Success response:__

| Status code | Body    | Explanation |
|:------------|:--------|:------------|
| 200         | _JSON_  | OK          |

__Error responses:__

TBD

| Status code | Body               | Explanation                                       |
|:------------|:-------------------|:--------------------------------------------------|
| 40x         | `{"error": "..."}` | Client Error - Don't repeat without modifications |
| 50x         | `{"error": "..."}` | Server Error                                      |

__JSON Response:__

```javascript
[
  {
    "id": 1,
    "club": {
      "id": 1,
      "user": {
        "id": 3,
        "username": "Arsenal",
        "last_name": "",
        "first_name": "",
        "email": "admin@arsenal.cp,"
      }
    },
    "user": {
      "id": 5,
      "username": "Bruno",
      "last_name": "Labadia",
      "first_name": "Bruno",
      "email": "bruno@arsenal.com"
    }
  },
  // ...
]
```


### 5.1.8 List of measurements
__Method:__ GET

__URL:__ /measurements/

__Headers:__
* Authorization: JWT ...
* Content-type: application/json


__Success response:__

| Status code | Body    | Explanation |
|:------------|:--------|:------------|
| 200         | _JSON_  | OK          |

__Error responses:__

TBD

| Status code | Body               | Explanation                                       |
|:------------|:-------------------|:--------------------------------------------------|
| 40x         | `{"error": "..."}` | Client Error - Don't repeat without modifications |
| 50x         | `{"error": "..."}` | Server Error                                      |

__JSON Response:__

```javascript
[
  {
    "id": 1,
    "name": "Sprint (30m)",
    "unit": "s",
    "description": "balbla",
    "upper_limit": "20.0000000000",
    "lower_limit": "3.0000000000"
  },
  // ...
]
```


### 5.1.9 Get current user
__Method:__ GET

__URL:__ /user/

__Headers:__
* Authorization: JWT ...
* Content-type: application/json


__Success response:__

| Status code | Body    | Explanation |
|:------------|:--------|:------------|
| 200         | _JSON_  | OK          |

__Error responses:__

TBD

| Status code | Body               | Explanation                                       |
|:------------|:-------------------|:--------------------------------------------------|
| 40x         | `{"error": "..."}` | Client Error - Don't repeat without modifications |
| 50x         | `{"error": "..."}` | Server Error                                      |

__JSON Response:__

There are 3 different response types (Club, Coach and Player). All of them have almost the same structure. 

_Player_
```javascript
{
  "id": 2,
  "user": {
    "is_superuser": false,
    "is_staff": false,
    "is_active": true,
    "username": "Messi",
    "first_name": "",
    "last_name": "",
    "email": "",
    "groups": [
      {
        "id": 2,
        "name": "Player"
      }
    ],
    "date_joined": "2016-03-18T14:46:18Z",
    "last_login": null
  },
  "club": {
    "id": 2,
    "user": {
      "id": 2,
      "username": "Barca",
      "last_name": "",
      "first_name": "",
      "email": ""
    },
    "name": "FC Barcelona"
  },
  "gender": "M",
  "birthday": "2016-03-18"
}
```

_Club_
```javascript
{
  "id": 1,
  "user": {
    "is_superuser": false,
    "is_staff": false,
    "is_active": true,
    "username": "Arsenal",
    "first_name": "",
    "last_name": "",
    "email": "",
    "groups": [
      {
        "id": 3,
        "name": "Club"
      }
    ],
    "date_joined": "2016-03-18T14:27:23Z",
    "last_login": null
  },
  "name": "FC Arsenal London"
}
```

_Coach_
```javascript
{
  "id": 4,
  "club": {
    "id": 1,
    "user": {
      "id": 3,
      "username": "Arsenal",
      "last_name": "",
      "first_name": "",
      "email": ""
    },
    "name": "FC Arsenal London"
  },
  "user": {
    "is_superuser": false,
    "is_staff": false,
    "is_active": true,
    "username": "Jupp",
    "first_name": "Jupp",
    "last_name": "Heynckes",
    "email": "jh@fca.com",
    "groups": [
      {
        "id": 4,
        "name": "Coach"
      }
    ],
    "date_joined": "2016-03-18T14:44:30Z",
    "last_login": null
  }
}
```
### 5.2 Data

TBD


### 5.3 Implementation

##### Edge cases

## 6. Coach view

TBD

## 7. Club view

TBD

## 8. Player view

TBD