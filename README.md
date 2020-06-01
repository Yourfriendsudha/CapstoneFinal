

1. Install the dependencies:
```bash
$ pip install -r requirements.txt
```
For local testing use the postgres db/ or sqlite

3. Used Database : postgres for local testing. change the credentails accordingly to your local db setup.
 ```python
database_setup = {
    "database_name" : "postgres",
    "user_name" : "postgres", # default postgres user name
    "password" : "admin1", 
    "port" : "localhost:5432" # default postgres port
}
```

4. if Sqlite is to be used, uncomment the below in models.py and comment the postgres database url

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))


5. Setup Auth0
3 new roles producer, director, assistant has been created in the Auth0 and the bearer tokens are mentioned in

simply take the existing bearer tokens in `config.py`.


6. Run the development server:
  ```bash 
  $ FLASK_APP=api.py  FLASK_ENV=development FLASK_DEBUG=true flask run
  ```

7. To execute tests, run. if the DB is empty , few testcases may give not found error. initialise db with data and
modify the testcases for specific testcase for edit/delete/patch
```bash 
$ python test_app.py
```

8. Import  the postman collection json to run the postman test cases for each role.



##  Roles ans permisions

They are 3 Roles with distinct permission sets:

1. Casting Assistant:
  - GET /actors (view:actors): Can see all actors
  - GET /movies (view:movies): Can see all movies
2. Casting Director (everything from Casting Assistant plus)
  - POST /actors (post:actor): Can create new Actors
  - PATCH /actors (patch:actor): Can edit existing Actors
  - DELETE /actors (delete:actor): Can remove existing Actors from database
  - PATCH /movies (patch:movie): Can edit existing Movies
3. Exectutive Dircector (everything from Casting Director plus)
  - POST /movies (post:movie): Can create new Movies
  - DELETE /movies (delete:movie): Can remove existing Motives from database

In your API Calls, add them as Header, with `Authorization` as key and the `Bearer token` as value. Don´t forget to also
prepend `Bearer` to the token (seperated by space).

