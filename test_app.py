import os
import json
import unittest
from ast import Pass
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from settings import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST
from database.models import db, setup_db, create_tables_for_test, Movie, Actor
from app import create_app

CASTING_ASSISTANT_TOKEN = os.getenv('CASTING_ASSISTANT_TOKEN')
CASTING_DIRECTOR_TOKEN = os.getenv('CASTING_DIRECTOR_TOKEN')
EXECUTIVE_PRODUCER_TOKEN = os.getenv('EXECUTIVE_PRODUCER_TOKEN')

# Actors Testing Class 
class ActorsTestCase(unittest.TestCase):
    print("This class includes test cases for Actors API endpoints")

    def setUp(self):
        self.assistant = CASTING_ASSISTANT_TOKEN
        self.director = CASTING_DIRECTOR_TOKEN
        self.producer = EXECUTIVE_PRODUCER_TOKEN

        self.app = create_app()
        self.client = self.app.test_client()
        setup_db(self.app)
        with self.app.app_context():
            create_tables_for_test()

    # Get all Actors Test Case 
    def test_get_all_actors_postitive(self):
        test_actor = {"name": "VK", "age": 36, "gender": "M"}
        res = self.client.post("/actor", headers={"Authorization": "Bearer {}".format(self.producer)}, json=test_actor)
        res = self.client.get("/actors", headers={"Authorization": "Bearer {}".format(self.producer)})
        data = json.loads(res.data)
        self.assertTrue(data['success'], "Success attribute of response json = False")
        self.assertGreaterEqual(len(data['actors']), 1, "No Actors returned")

    # Post an Actor Test Case
    def test_post_an_actor_positive(self):
        test_actor = {"name": "Salman", "age": 62, "gender": "M"}
        res = self.client.post("/actor", headers={"Authorization": "Bearer {}".format(self.producer)}, json=test_actor)
        data = json.loads(res.data)
        self.assertTrue(data['success'], "Success attribute of response json = False")
        id = Actor.query.get(data['actor']['id'])
        test_actor["id"] = data['actor']['id']
        self.assertEqual(id.serialized_actor(), test_actor, "Actor in test case and the actor posted in DB are not same")

    # Update an Actor Test Case - positive
    def test_patch_an_actor(self):
        test_actor = {"name": "Ranvir Singh", "age": 37, "gender": "M"}
        res = self.client.post("/actor", headers={"Authorization": "Bearer {}".format(self.producer)}, json=test_actor)
        id = json.loads(res.data)['actor']['id']
        test_actor_upd = {"name": "Ranvir Singh Upd", "age": 37, "gender": "M"}
        res_upd = self.client.patch(f'/actor/{id}', json=test_actor_upd, headers={"Authorization": "Bearer {}".format(self.producer)})
        data = json.loads(res_upd.data)
        self.assertTrue(data['success'], "Success attribute of response json = False")
        test_actor["age"] = test_actor_upd['age']
        test_actor["name"] = test_actor_upd['name']
        test_actor["gender"] = test_actor_upd['gender']
        test_actor["id"] = id
        self.assertEqual(data["actor"], test_actor, "Actor in test case and the actor posted in DB are not same")

    # # Update Test Case for Actor - Negative #
    # def test_patch_an_actor_negative(self):
    #     id = 999
    #     test_actor_upd = {"name": "Vikas Garg"}
    #     res_upd = self.client.patch(f'/actor/{id}', json=test_actor_upd, headers={"Authorization": "Bearer {}".format(self.producer)})
    #     data = json.loads(res_upd.data)
    #     self.assertFalse(data['success'], "success attribute in response json was true")
    #     self.assertEqual(int(data['error']), 404, "error code is not 404")

    # Delete Test Case for Actor - Positive
    def test_delete_an_actor(self):
        test_actor = {"name": "Aishwairya Rai", "age": 57, "gender": "F"}
        res = self.client.post("/actor", json=test_actor, headers={"Authorization": "Bearer {}".format(self.producer)})
        id = json.loads(res.data)['actor']['id']
        res_upd = self.client.delete(f'/actor/{id}', headers={"Authorization": "Bearer {}".format(self.producer)})
        data = json.loads(res_upd.data)
        self.assertTrue(data['success'], "success attribute in response json was false")
        self.assertEqual(data['id'], id, "Actor inserted hasn't been deleted")

    # # Delete Test Case for Actor - Negative
    # def test_delete_an_actor_negative(self):
    #     id = 999
    #     res_upd = self.client.delete(f'/actor/{id}', headers={"Authorization": "Bearer {}".format(self.producer)})
    #     data = json.loads(res_upd.data)
    #     self.assertFalse(data['success'], "success attribute in response json was true")
    #     self.assertEqual(int(data['error']), 404, "error code is not 404")

# Movies Class Rest Cases 

class MoviesTestCase(unittest.TestCase):
    print("This class includes test cases for Movies API endpoints")

    def setUp(self):
        self.assistant = CASTING_ASSISTANT_TOKEN
        self.director = CASTING_DIRECTOR_TOKEN
        self.producer = EXECUTIVE_PRODUCER_TOKEN
        self.db_path = 'postgresql://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)

        self.app = create_app(self.db_path)
        self.client = self.app.test_client()
        # setup_db(self.app)
        self.app.app_context().push()

    def tearDown(self):
        db.session.close()

    # Get all Movies Test Case - positive
    def test_get_all_movies_postitive(self):
        test_movie = {"name": "Dear Zindagi", "release_date": "2018-06-04"}
        res = self.client.post("/movies", headers={"Authorization": "Bearer {}".format(self.producer)}, json=test_movie)
        res = self.client.get("/movies", headers={"Authorization": "Bearer {}".format(self.producer)})
        data = json.loads(res.data)
        self.assertTrue(data['success'], "Success attribute of response json = False")
        self.assertGreaterEqual(len(data['movies']), 1, "No Movies returned")

    # Post a Movie Test Case
    def test_post_an_movie_positive(self):
        test_movie = {"name": "Shehjada", "release_date": "2022-10-08"}
        res = self.client.post("/movie", headers={"Authorization": "Bearer {}".format(self.producer)}, json=test_movie)
        data = json.loads(res.data)
        self.assertTrue(data['success'], "Success attribute of response json = False")
        id = Movie.query.get(data['movie']['id'])
        test_movie["id"] = data['movie']['id']
        self.assertEqual(id.serialized_movie(), test_movie, "Movie in test case and the movie posted in DB are not same")

    # Update an Movie Test Case
    def test_patch_an_movie(self):
        test_movie = {"name": "Badmaash Company", "release_date": "2008-12-01"}
        res = self.client.post("/movie", headers={"Authorization": "Bearer {}".format(self.producer)}, json=test_movie)
        id = json.loads(res.data)['movie']['id']
        test_movie_upd = {"name": "Badmaash Company 2", "release_date": "2016-10-01"}
        res_upd = self.client.patch(f'/movie/{id}', json=test_movie_upd, headers={"Authorization": "Bearer {}".format(self.producer)})
        data = json.loads(res_upd.data)
        self.assertTrue(data['success'], "Success attribute of response json = False")
        test_movie["name"] = test_movie_upd['name']
        test_movie["release_date"] = test_movie_upd['release_date']
        test_movie["id"] = id
        self.assertEqual(data["movie"], test_movie, "Movie in test case and the movie posted in DB are not same")

    # # Update Test Case for Movie - Negative #
    # def test_patch_an_movie_negative(self):
    #     id = 999
    #     test_movie_upd = {"name": "Time Pass"}
    #     res_upd = self.client.patch(f'/movie/{id}', json=test_movie_upd, headers={"Authorization": "Bearer {}".format(self.producer)})
    #     data = json.loads(res_upd.data)
    #     self.assertFalse(data['success'], "success attribute in response json was true")
    #     self.assertEqual(int(data['error']), 404, "error code is not 404")

    # Delete Test Case for Movie - Positive
    def test_delete_an_movie(self):
        test_movie = {"name": "Funtoosh", "release_date": "2006-12-01"}
        res = self.client.post("/movie", json=test_movie, headers={"Authorization": "Bearer {}".format(self.producer)})
        id = json.loads(res.data)['movie']['id']
        res_upd = self.client.delete(f'/movie/{id}', headers={"Authorization": "Bearer {}".format(self.producer)})
        data = json.loads(res_upd.data)
        self.assertTrue(data['success'], "success attribute in response json was false")
        self.assertEqual(data['id'], id, "Movie inserted hasn't been deleted")

#     # Delete Test Case for Movie - Negative
#     def test_delete_an_movie_negative(self):
#         id = 999
#         res_upd = self.client.delete(f'/movie/{id}', headers={"Authorization": "Bearer {}".format(self.producer)})
#         data = json.loads(res_upd.data)
#         self.assertFalse(data['success'], "success attribute in response json was true")
#         self.assertEqual(int(data['error']), 404, "error code is not 404")

# Auth Test Cases for Casting Assistant, Director and Producer 
class AuthTestCase(unittest.TestCase):
    print("This class include testcases for the different level of RBAC access")

    def setUp(self):
        self.assistant = CASTING_ASSISTANT_TOKEN
        self.director = CASTING_DIRECTOR_TOKEN
        self.producer = EXECUTIVE_PRODUCER_TOKEN
        self.db_path = 'postgresql://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)

        self.app = create_app(self.db_path)
        self.client = self.app.test_client()
        self.app.app_context().push()

    def tearDown(self):
        db.session.close()

    # Authorization Test Cases for Casting Assisstant
    def test_get_all_movies_casting_assistant(self):
        test_movie = {"name": "Singh is King", "release_date": "2014-05-06"}
        res = self.client.post("/movies", json=test_movie, headers={"Authorization": "Bearer {}".format(self.producer)})
        res = self.client.get("/movies", headers={"Authorization": "Bearer {}".format(self.assistant)})
        data = json.loads(res.data)
        self.assertTrue(data['success'], "Success attribute of response json = False")
        self.assertGreaterEqual(len(data['movies']), 1, "No Movies returned")

    def test_get_all_actors_casting_assistant(self):
        test_actor = {"name": "Ajay Devgan", "age": "56", "gender": "M"}
        res = self.client.post("/actors", json=test_actor, headers={"Authorization": "Bearer {}".format(self.producer)})
        res = self.client.get("/actors", headers={"Authorization": "Bearer {}".format(self.assistant)})
        data = json.loads(res.data)
        self.assertTrue(data['success'], "Success attribute of response json = False")
        self.assertGreaterEqual(len(data['actors']), 1, "No Actors returned")

    # def test_delete_an_actor_casting_assistant(self):
    #     test_actor = {"name": "Ajay Devgan", "age": "56", "gender": "M"}
    #     res = self.client.post("/actor", json=test_actor, headers={"Authorization": "Bearer {}".format(self.producer)})
    #     id = json.loads(res.data)['actor']['id']
    #     res_upd = self.client.delete(f'/actor/{id}', headers={"Authorization": "Bearer {}".format(self.assistant)})
    #     data = json.loads(res_upd.data)
    #     self.assertFalse(data['success'], "success attribute in response json was True")
    #     self.assertEqual(int(data['error']), 403, "error code is not 403")

    # Auth Test Cases for Casting Director
    # def test_post_a_movies_casting_director(self):
    #     test_movie = {"name": "Singh is King", "release_date": "2014-05-06"}
    #     res = self.client.post("/movie", json=test_movie, headers={"Authorization": "Bearer {}".format(self.director)})
    #     data = json.loads(res.data)
    #     self.assertFalse(data['success'], "success attribute in response json was True")
    #     self.assertEqual(int(data['error']), 403, "error code is not 403")

    def test_post_an_actor_casting_director(self):
        test_actor = {"name": "Ajay Devgan", "age": 56, "gender": "M"}
        res = self.client.post("/actor", json=test_actor, headers={"Authorization": "Bearer {}".format(self.director)})
        data = json.loads(res.data)
        self.assertTrue(data['success'], "success attribute in response json was false")
        id = Actor.query.get(data['actor']['id'])
        test_actor["id"] = data['actor']['id']
        self.assertEqual(id.serialized_actor(), test_actor, "Actor in test case and the Actor posted in DB are not same")

    # def test_delete_a_movie_casting_director(self):
    #     test_movie = {"name": "Singh is King", "release_date": "2014-05-06"}
    #     res = self.client.post("/movie", json=test_movie, headers={"Authorization": "Bearer {}".format(self.producer)})
    #     id = json.loads(res.data)['movie']['id']
    #     res_upd = self.client.delete(f'/movie/{id}', headers={"Authorization": "Bearer {}".format(self.director)})
    #     data = json.loads(res_upd.data)
    #     self.assertFalse(data['success'], "success attribute in response json was True")
    #     self.assertEqual(int(data['error']), 403, "error code is not 403")

    def test_delete_an_actor_casting_director(self):
        test_actor = {"name": "Ajay Devgan", "age": "56", "gender": "M"}
        res = self.client.post("/actor", json=test_actor, headers={"Authorization": "Bearer {}".format(self.producer)})
        id = json.loads(res.data)['actor']['id']
        res_upd = self.client.delete(f'/actor/{id}', headers={"Authorization": "Bearer {}".format(self.director)})
        data = json.loads(res_upd.data)
        self.assertTrue(data['success'], "success attribute in response json was false")
        self.assertEqual(data['id'], id, "Actor inserted hasn't been deleted")

    # Authorization Test Cases for Executive Producer 
    def test_post_a_movies_executive_producer(self):
        test_movie = {"name": "Singh is King", "release_date": "2014-05-06"}
        res = self.client.post("/movie", json=test_movie, headers={"Authorization": "Bearer {}".format(self.producer)})
        data = json.loads(res.data)
        self.assertTrue(data['success'], "success attribute in response json was false")
        id = Movie.query.get(data['movie']['id'])
        test_movie["id"] = data['movie']['id']
        self.assertEqual(id.serialized_movie(), test_movie, "Movie in test case and the Movie posted in DB are not same")

    def test_post_an_actor_executive_producer(self):
        test_actor = {"name": "Ajay Devgan", "age": 56, "gender": "M"}
        res = self.client.post("/actor", json=test_actor, headers={"Authorization": "Bearer {}".format(self.producer)})
        data = json.loads(res.data)
        self.assertTrue(data['success'], "success attribute in response json was false")
        id = Actor.query.get(data['actor']['id'])
        test_actor["id"] = data['actor']['id']
        self.assertEqual(id.serialized_actor(), test_actor, "Actor in test case and the Actor posted in DB are not same")

    def test_delete_a_movie_executive_producer(self):
        test_movie = {"name": "Singh is King", "release_date": "2014-05-06"}
        res = self.client.post("/movie", json=test_movie, headers={"Authorization": "Bearer {}".format(self.producer)})
        id = json.loads(res.data)['movie']['id']
        res_upd = self.client.delete(f'/movie/{id}', headers={"Authorization": "Bearer {}".format(self.producer)})
        data = json.loads(res_upd.data)
        self.assertTrue(data['success'], "success attribute in response json was false")
        self.assertEqual(data['id'], id, "Movie inserted hasn't been deleted")

    def test_delete_an_actor_executive_producer(self):
        test_actor = {"name": "Ajay Devgan", "age": "56", "gender": "M"}
        res = self.client.post("/actor", json=test_actor, headers={"Authorization": "Bearer {}".format(self.producer)})
        id = json.loads(res.data)['actor']['id']
        res_upd = self.client.delete(f'/actor/{id}', headers={"Authorization": "Bearer {}".format(self.producer)})
        data = json.loads(res_upd.data)
        self.assertTrue(data['success'], "success attribute in response json was false")
        self.assertEqual(data['id'], id, "Actor inserted hasn't been deleted")

if __name__ == "__main__":
    unittest.main()
