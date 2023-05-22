# Casting Agency Project
Udacity Full-Stack Web Developer Nanodegree Program Capstone Project


## Project Motivation
The Casting Agency Project models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process. 


This project is simply a workspace for practicing and showcasing different set of skills related with web development. These include data modelling, API design, authentication and authorization and cloud deployment.

## Getting Started

The project adheres to the PEP 8 style guide and follows common best practices, including:

* Variable and function names are clear.
* Endpoints are logically named.
* Code is commented appropriately.

### Key Dependencies & Platforms

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Auth0](https://auth0.com/docs/) is the authentication and authorization system we'll use to handle users with different roles with more secure and easy ways

- [PostgreSQL](https://www.postgresql.org/) this project is integrated with a popular relational database PostgreSQL, though other relational databases can be used with a little effort.

- [Render](https://render.com/) is the cloud platform used for deployment


### Running Locally

#### Installing Dependencies

##### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

##### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

#### Production Project Render link: 
https://capstone-casting.onrender.com

#### Running Tests
To run the tests, run
```bash
python test_app.py
```

#### Auth0 Setup

You need to setup an Auth0 account.

```bash
export AUTH0_DOMAIN="xxxxxxxxxx.auth0.com" # Choose your tenant domain
export ALGORITHMS="RS256"
export API_AUDIENCE="capstone_final" # Create an API in Auth0
```

##### Roles

Create three roles for users under `Users & Roles` section in Auth0

* Casting Assistant
	* Can view actors and movies
* Casting Director
	* All permissions a Casting Assistant has and…
	* Add or delete an actor from the database
	* Modify actors or movies
* Executive Producer
	* All permissions a Casting Director has and…
	* Add or delete a movie from the database

##### Permissions

Following permissions should be created under created API settings.

* `view:actors`
* `view:movies`
* `delete:actor`
* `delete:movie`
* `update:actor`
* `update:movie`
* `post:movie`
* `post:actor`

##### Set JWT Tokens in '.env' (for Production) & '.env_test' (for Test) files.

Use the following link to create users and sign them in. This way, you can generate the three required tokens 

```
https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}}


```



#### Launching The App

1. Initialize and activate a virtualenv:

   ```bash
   python -m venv venv
   ./venv/Scripts/activate
   ```

2. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```
3. Configure database variables to connect local postgres database in `.env.py`

    ```python
    DB_NAME="casting_prod"
	DB_USER="vikasgarg"
	DB_PASSWORD="vikas1"
    ```

For more details [look at the documentation (31.1.1.2. Connection URIs)](https://www.postgresql.org/docs/9.3/libpq-connect.html)

5.  To run the server locally, execute:

    ```bash
    export FLASK_APP=app.py
    export FLASK_DEBUG=True
    export FLASK_ENVIRONMENT=debug
    flask run --reload
    ```

## API Documentation

### Models
There are two models:
* Movie
	* name
	* release_date
* Actor
	* name
	* age
	* gender

### Error Handling

Errors are returned as JSON objects in the following format:
```json
{
    "success": False, 
    "error": 400,
    "message": "Bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 401: Not Authorized
- 403: Forbidden
- 404: Resource not Found
- 405: Method not Allowed
- 422: Request cannot be processed 
- 500: Internal server error

### Endpoints
	
#### GET /actors 
* Get all actors

* Requires `view:actors` permission

* **Example Request:** `curl 'http://localhost:5000/actors'`

* **Expected Result:**
    ```json
	{
		"actors": [
			{
				"age": 62,
				"gender": "M",
				"id": 1,
				"name": "Salman"
			},
			{
				"age": 56,
				"gender": "M",
				"id": 4,
				"name": "Ajay Devgan"
			},
			{
				"age": 37,
				"gender": "M",
				"id": 8,
				"name": "Ranvir Singh Upd"
			},
			{
				"age": 94,
				"gender": "M",
				"id": 15,
				"name": "Amrish Puri"
			}
		],
		"success": true
	}
	```

#### POST /actor
* Creates a new actor.

* Requires `post:actor` permission

* Requires the name, age and gender of the actor.

* **Example Request:** (Create)
    ```bash
	curl --location --request POST 'http://localhost:5000/actor' \
		--header 'Content-Type: application/json' \
		--data-raw 
		'{
			"age": 94,
			"gender": "M",
			"name": "Amrish Puri"
		}'
    ```
    
* **Example Response:**
    ```json
		{
		"actor": {
			"age": 94,
			"gender": "M",
			"id": 16,
			"name": "Amrish Puri"
		},
		"success": true
		}
    ```

#### DELETE /actor/<int:actor_id>


* Deletes the actor with given id 

* Require `delete:actor` permission

* **Example Request:** `curl --request DELETE 'http://localhost:5000/actor/1'`

* **Example Response:**
    ```json
		{
			"id": 1,
			"success": true
		}
    ```
	
#### PATCH /actor/<actor_id>
* Updates the actor where <actor_id> is the existing actor id

* Require `update:actor`

* Responds with a 404 error if <actor_id> is not found

* Update the given fields for Actor with id <actor_id>

* **Example Request:** 
	```bash
    curl --location --request PATCH 'http://localhost:5000/actor/8' \
		--header 'Content-Type: application/json' \
		--data-raw 
		'{
            "name": "Ranvir Singh"
        }'
  ```
  
* **Example Response:**
    ```json
	{
		"success": true, 
		"updated": {
      		"age": 37,
            "gender": "M",
            "id": 8,
            "name": "Ranvir Singh"
		}
	}
	```

#### GET /movies 
* Get all movies

* Require `view:movies` permission

* **Example Request:** `curl 'http://localhost:5000/movies'`

* **Expected Result:**
    ```json
		{
			"movies": [
				{
					"id": 4,
					"name": "Jab tak hain Jaan",
					"release_date": "2023-12-16"
				},
				{
					"id": 5,
					"name": "Shehjada",
					"release_date": "2022-10-08"
				},
				{
					"id": 7,
					"name": "Singh is King",
					"release_date": "2014-05-06"
				}
			],
			"success": true
		}    
	```


#### POST /movie
* Creates a new movie.

* Requires `post:movie` permission

* Requires the title and release date.

* **Example Request:** (Create)
    ```bash
	curl --location --request POST 'http://localhost:5000/movie' \
		--header 'Content-Type: application/json' \
		--data-raw 
		'{
			"name": "Padosan",
			"release_date": "1966-01-25T00:00:00"
		}'
    ```
    
* **Example Response:**
    ```json
		{
			"movie": 
			{
				"id": 13,
				"name": "Padosan",
				"release_date": "1966-01-25"
			},
			"success": true
		}	
    ```


#### DELETE /movie/<int:movie_id>
* Deletes the movie with given id 

* Require `delete:movie` permission

* **Example Request:** `curl --request DELETE 'http://localhost:5000/movie/7'`

* **Example Response:**
    ```json
		{
			"id": 7,
			"success": true
		}
    ```
    


#### PATCH /movie/<movie_id>
* Updates the movie where <movie_id> is the existing movie id

* Require `update:movie` permission

* Responds with a 404 error if <movie_id> is not found

* Update the corresponding fields for Movie with id <movie_id>

* **Example Request:** 
	```bash
    curl --location --request PATCH 'http://localhost:5000/movie/1' \
		--header 'Content-Type: application/json' \
		--data-raw 
		'{
    		"release_date": "2016-12-16T00:00:00"
	    }'
  ```
  
* **Example Response:**
    ```json
	{
		"movie": 
		{
			"id": 4,
			"name": "Jab tak hain Jaan",
			"release_date": "2016-12-16"
		},
		"success": true
	}	
    ```
	
