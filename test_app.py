import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, db_drop_and_create_all, Actor, Movie, Stageshow, db_drop_and_create_all
from config import tokens
from sqlalchemy import desc
from datetime import date

# declaring the tokens used for testing.

assistant_auth_header = {
    'Authorization': tokens['assistant']
}

director_auth_header = {
    'Authorization': tokens['director']
}

producer_auth_header = {
    'Authorization': tokens['producer']
}


#AgencyTestCase

class capstoneTestCase(unittest.TestCase):


    def setUp(self):
        # self.database_path = os.environ['DATABASE_URL']
        # setup_db(self.app, self.database_path)

        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)
        # db_drop_and_create_all()
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        pass

    def test_success_new_actor(self):
        # create new actor - for 200
        json_create_actor = {
            'name' : 'sudha',
            'age' : 27
        } 

        res = self.client().post('/actors', json = json_create_actor, headers = director_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
    
    def test_error_401_new_actor(self):
        # create new actor for 401
        json_create_actor = {
            'name' : 'sudha',
            'age' : 27
        } 

        res = self.client().post('/actors', json = json_create_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_error_422_new_actor(self):
        # create new actor for 422
        json_create_actor = {
            'age' : 25
        } 

        res = self.client().post('/actors', json = json_create_actor, headers = director_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'no name provided.')


    def test_success_actors_withHeader(self):
        # get all actors
        res = self.client().get('/actors', headers = assistant_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)

    def test_error_401_all_actors_without_header(self):
        # get all actors without header
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')


    def test_success_patch_actor(self):
        json_patch = {
            'age' : 30
        } 
        res = self.client().patch('/actors/11', json = json_patch, headers = director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actor']) > 0)


    def test_error_404_patch_actor(self):
        json_edit_actor_with_new_age = {
            'age' : 30
        } 
        res = self.client().patch('/actors/123', json = json_edit_actor_with_new_age, headers = director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'Actor 123 Details not found in database. Please check the ID')



    def test_error_401_delete_actor(self):
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_error_403_delete_actor(self):
        res = self.client().delete('/actors/1', headers = assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unauthorized')

    def test_success_delete_actor(self):
        res = self.client().delete('/actors/34', headers = director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        #self.assertEqual(data['deleted'], '29')

    def test_error_404_delete_actor(self):
        res = self.client().delete('/actors/123', headers = director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'Actor 123 Details not found in database. Please check the ID')

    def test_error_422_create_new_movie(self):
        json_create_movie_without_name = {
            'release_date' : date.today()
        } 

        res = self.client().post('/movies', json = json_create_movie_without_name, headers = producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'no title provided.')


    def test_error_404_get_movies(self):
        res = self.client().get('/movies', headers = assistant_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'no movies found in database. please add entries')

    def test_success_create_new_movie(self):
        json_create_movie = {
            'title' : 'Saw Movie',
            'release_date' : '12-05-1992'
        } 

        res = self.client().post('/movies', json = json_create_movie, headers = producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        #self.assertEqual(data['created'], 2)

    def test_success_get_all_movies(self):
        res = self.client().get('/movies?page=1', headers = assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)

    def test_error_401_get_all_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')



    def test_success_edit_movie(self):
        json_edit_movie = {
            'release_date' : '11-02-2018'
        } 
        res = self.client().patch('/movies/1', json = json_edit_movie, headers = producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movie']) > 0)


    def test_error_404_edit_movie(self):
        json_edit_movie = {
            'release_date' : '12-03-2019'
        } 
        res = self.client().patch('/movies/64', json = json_edit_movie, headers = producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'Movie 64 Details not found in database. Please check the ID.')


    def test_error_401_delete_movie(self):
        res = self.client().delete('/movies/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_error_403_delete_movie(self):
        res = self.client().delete('/movies/2', headers = assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unauthorized')

    def test_success_delete_movie(self):
        res = self.client().delete('/movies/8', headers = producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        #self.assertEqual(data['deleted'], '2')

    def test_error_404_delete_movie(self):
        res = self.client().delete('/movies/53', headers = producer_auth_header) 
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'Movie 53 Details not found in database. Please check the ID.')


if __name__ == "__main__":
    unittest.main()