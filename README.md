# Capstone project

### Project motivation

This project is the final project for the Udacity Full Stack Web Developer nanodegree.

### UL location of hosted API

The app is hosted on Heroku at this link https://capstone1ryanhart.herokuapp.com/

### Installing Dependencies for the Backend

1. **Python 3.8** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.

### Authentication

Auth0 is used for authentication. The following link is for the log in/register page:
https://dev-0m5bkb0u.us.auth0.com/authorize?audience=casting&response_type=token&client_id=JW2I9hBpyupIexfaiw3fxnOMrt02Z2kw&redirect_uri=http://192.168.0.61:8080

Three roles have been created:
#### Casting Assistant
Can view actors and movies
Sample user:
- castingassistant@fakeemail.com
- Udacitypassword1!
#### Casting Director
All permissions a Casting Assistant has and… Add or delete an actor from the database Modify actors or movies
Sample user:
- castingdirector@fakeemail.com
- Udacitypassword1!
#### Executive Producer
All permissions a Casting Director has and… Add or delete a movie from the database
Sample user:
- executiveproducer@fakeemail.com
- Udacitypassword1!

### Endpoints
#### GET /movies
- Returns a list of movies objects
- Request Arguments: Header with authorisation `get:movies`
- Sample: `curl -H "Authorization: Bearer <ACCESS TOKEN>" https://capstone1ryanhart.herokuapp.com/movies`
``` {
  "movies": [
    {
      "id": 1,
      "releaseDate": "Wed, 28 May 2014 00:00:00 GMT",
      "title": "Another movie name"
    },
    {
      "id": 3,
      "releaseDate": "Fri, 21 Feb 2020 00:00:00 GMT",
      "title": "Second movie title"
    }
  ],
  "success": true
}
```
#### GET /actors
- Returns a list of actor objects
- Request Arguments: Header with authorisation `get:actors`
- Sample: `curl -H "Authorization: Bearer <ACCESS TOKEN>" https://capstone1ryanhart.herokuapp.com/actors`
``` {
  "actors": [
    {
      "age": 52,
      "gender": "Male",
      "id": 1,
      "name": "Tom Cruise"
    },
    {
      "age": 21,
      "gender": "male",
      "id": 10,
      "name": "new actor name"
    },
    {
      "age": 30,
      "gender": "male",
      "id": 2,
      "name": "John Doe"
    }
  ],
  "success": true
}
```

#### DELETE /movies
- Deletes the movie of the given id if it exists
- Request Arguments: movie id, header with authorisation `delete:movies`
- Returns a the id of the deleted movie and success value  
- Sample: `curl -X -H "Authorization: Bearer <ACCESS TOKEN>" DELETE https://capstone1ryanhart.herokuapp.com/movies/3`
```
{
  "success": true,
  "deleted": 3
}
```

#### DELETE /actors
- Deletes the actor of the given id if it exists
- Request Arguments: actor id, header with authorisation `delete:actors`
- Returns a the id of the deleted actor and success value  
- Sample: `curl -X -H "Authorization: Bearer <ACCESS TOKEN>" DELETE https://capstone1ryanhart.herokuapp.com/actors/3`
```
{
  "success": true,
  "deleted": 3
}
```

#### POST /movies
- Creates a new movie with the given title and creation date
- Request Arguments: title, creation date, header with authorisation `post:movies`
- Returns a the movie object and success value  
- Sample: `curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <ACCESS TOKEN>" -d '{"title": "Another new movie name", "releaseDate":"2022-01-01"}' https://capstone1ryanhart.herokuapp.com/movies`
```
{
  "movie":
    {
      "id":1,
      "releaseDate":"Sat, 01 Jan 2022 00:00:00 GMT",
      "title":"First movie name"}
    ,
  "success":true
}
```

#### POST /actors
- Creates a new movie with the given title and creation date
- Request Arguments: title, creation date, header with authorisation `post:actors`
- Returns a the movie object and success value  
- Sample: `curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <ACCESS TOKEN>" -d '{"title": "Another new movie name", "releaseDate":"2022-01-01"}' https://capstone1ryanhart.herokuapp.com/movies`
```
{
  "movie":
    {
      "id":1,
      "releaseDate":"Sat, 01 Jan 2022 00:00:00 GMT",
      "title":"First movie name"}
    ,
  "success":true
}
```

#### PATCH /movies
- Modifies an existing movie to the given title and creation date
- Request Arguments: movie id, creation date, header with authorisation `patch:movies`
- Returns the edited movie object and success value  
- Sample: `curl -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer <ACCESS TOKEN>" -d '{"title": "updated movie title", "releaseDate": "2022-01-01"}' https://capstone1ryanhart.herokuapp.com/movies/3`
```
{
  "edited":
    {
      "id":3,
      "releaseDate":"Sat, 01 Jan 2022 00:00:00 GMT",
      "title":"updated movie title"}
    ,
  "success":true
}
```

#### PATCH /actors
- Modifies an existing actor to the given name, age and gender
- Request Arguments: actor id, name, age, gender, header with authorisation `patch:actors`
- Returns the edited actor object and success value  
- Sample: `curl -X PATCH -H 'Content-Type: application/json' -H "Authorization: Bearer <ACCESS TOKEN>" -d '{"name": "John Doe", "age": "30", "gender": "male"}' http://192.168.0.61:8080/actors/2`
```
{
  "edited":
    {
      "id":2,
      "name":"John Doe",
      "age":"30",
      "gender":"male"}
    ,
  "success":true
}
```

## Testing
To run the tests, run
```
python test_app.py
```
