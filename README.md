# Django, React, HubSpot 

## Goals

### Back End:

* Setup a Django project [done]
* Create Models to store HubSpot Tokens [done]
* Build OAuth Integration with HubSpot [done]
* Build HubSpot Integration with the Owner API to read Owners [done]
* Build HubSpot Integration with the Deals API to read and write Deals [done]

### Front End:

* Setup a React project [done]
* Integrate the OAuth flow [done]
* Implement UI to consume the Back End endpoints for Owners (read) and Deals (read, write) [done]

## Usage

This project was written in a very short period of time, trying to achieve both BE and FE goals. For this very reason, it is not a "Production quality" project but a PoC.

```
$ git clone https://github.com/lvm/owners-n-deals/ challenge/
```

In order to setup the BE project, these steps are required:  
These will install the Python dependencies on a virtual environment, run Django migrations, and finally run Django's dev webserver.

```
$ cd challenge/
$ python -m venv env
$ source ./env/bin/activate
(env)$ pip install -r requirements.txt
(env)$ python manage.py migrate
(env)$ python manage.py createsuperuser
(env)$ python manage.py runserver
```


In order to setup the FE (sub) project, these other steps are required:  
These will install the JS/Node dependencies, finally run webpack to generate a .js file with the contents to load the different Apps _inside_ Django templates. 

```
$ cd challenge/frontend/
$ npm install
$ npm run dev
```


## Considerations

This PoC/Challenge was written as a "single user" service, meaning, Client ID, Client Secrets, Redirect URI and Scopes are _hardcoded_ in the `settings.py` file instead of using a Django Model to store this info.  
For this very same reason, in `backend/models.py` there's a Singleton that provides access to `Credentials`, that are used when requesting (O)authorization and refreshing the Access Token. Another detail for this Singleton, is that it uses a "frozen" DataClass, allowing not only to have an unique instance for these credentials but disallowing to edit its values.  
Following the same idea, only one `HubSpotToken` record/object is created (and updated) for each user (which ideally would be just one)

## Tech debt: Back End

### Better BE architecture

It would be ideal to integrate the apps, templates, settings and statics, into the project. This way, everything could be tightly coupled providing a better structure.

### Unit tests
 
No tests provided. Mocking HubSpot requests would be ideal but for time-reasons it was discarded. 

### Django Rest Framework

This project provides JSON endpoints but handled "manually" instead, providing JsonResponse responses.
The correct approach would've been to use DRF to handle Owners and Deals endpoints.

### Docker

Given the simple approach that has been taken to develop this PoC/Challenge, preparing a Docker "setup" represented extra work which for time-reasons was discarded.
In case Docker were added, it could provide (using docker-compose) access to a DB (such as PostgreSQL), Redis, and a separated Celery instance running workers/beat.

### Different environments

Only one environment (dev) is available. In order to extend this setup for more environments, it would simply require to:

* Rename `challenge/settings.py` to `challenge/settings/common.py`
* Create `challenge/settings/{env}.py`
* Export an Env var `DJANGO_SETTINGS_MODULE` pointing to the current environment

### Queues to handle asynchronously Object storage

Due to the missing Docker configuration, using Redis + Celery was discarded.
Ideally, async tasks could handle storing Tokens when finishing the OAuth flow (connect -> approve -> callback -> token is stored the first time) and when refreshing the token (POST request to 'refresh token endpoint' -> request new Token -> (new) token is updated)

## Tech debt: Front End

### Better architecture

This project has 3 "Apps" + its Components rendered through Django templates. An ideal scenario, would be to create a separated project not tied to the BE and create a single App + different "views" rendering each Component accordingly.

### Separate completely the FE app from the BE app

Following the previous item, tt would be ideal to completely separate the React project, allowing Login flow, OAuth flow, Owners and Deals listing and creation through a REST API. Once again, time was a crucial.
