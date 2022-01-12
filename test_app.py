import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor

castingAssistantTokenValid = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5DWnJBb1pYeXNfaXVNZWlkeEJLWSJ9.eyJpc3MiOiJodHRwczovL2Rldi0wbTVia2IwdS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjFkZWE5MzkzNjRiMWQwMDZhZmQ1NjM0IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTY0MTk4MjQ4NywiZXhwIjoxNjQxOTg5Njg3LCJhenAiOiJKVzJJOWhCcHl1cElleGZhaXczZnhuT01ydDAyWjJrdyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.p_nQjSqst8_6BlZOxttpc-n7ovWG5pbg6wGof9fWujVB8bI4UugP1ZbMf2WDOx8jzJ8ZSgZYjpC01XGP1JP565drdNvssvq1wn_Fyo1WIZz-sJWhXICcRLcHfsdf-PE-BrTR6aRIM84ELwUiREep4PAb-ayZveTMSEpuNxMQL9xvRYb20wsB9Ut12zOUJhprrfzK7mOzEnmp-HBqkyWAPrW8mSmqBYSb3zuBl-NgwvNKelpIbXhnLnOgUnqC7G8Lm36QpHGtfiyHmPiViYUXr_U6fVShn0MGwjpS3cKl8J8ODqfK8BZ7erIujQ-ISSL8_vZ0YAyolc8HgdCSutX1nw'

castingDirectorTokenValid = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5DWnJBb1pYeXNfaXVNZWlkeEJLWSJ9.eyJpc3MiOiJodHRwczovL2Rldi0wbTVia2IwdS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjFkZWFlMGEzNjRiMWQwMDZhZmQ1NmJkIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTY0MTk4MzU1MCwiZXhwIjoxNjQxOTkwNzUwLCJhenAiOiJKVzJJOWhCcHl1cElleGZhaXczZnhuT01ydDAyWjJrdyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.E11Dw4mhaNU10u8ratmHQ74W_mg6VMhXQcWInf-DvZtMT2Lbq8eNSunuYqt944dkhBWP4HQpxgo624dYxGae1_7wbw0sA20UjfoEI2po9SrP11lBJUfF5vk6fNZ9qwucLrDjzmxlX6oDDNYwzmhUnEzLGEYJnbPm1SVInYU191WFjSWxwk_19LNIzAySZ_8YGBDZ48I2CY8EWUjkiXT12x4p45je8dbBAONQihuhkKtgespv8JfubCro4xLeA-JEw_uPVWlalvyEtIzWSVxeW5KLZIeqFCgqSNXCKJ5mfrh3MbjeXdN1jnwX17NHnB0y4QDXbGkoMbkLiUQpPwDdGg'

executiveProducerTokenValid = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5DWnJBb1pYeXNfaXVNZWlkeEJLWSJ9.eyJpc3MiOiJodHRwczovL2Rldi0wbTVia2IwdS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjFkZWFmYWVkMTg4ZDgwMDZlYTRjYzI4IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTY0MTk4Mzk5NSwiZXhwIjoxNjQxOTkxMTk1LCJhenAiOiJKVzJJOWhCcHl1cElleGZhaXczZnhuT01ydDAyWjJrdyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.UpXbWSNsnXFqKTpyF9mWB9IDMoSa3SOXE0oqqTx9TJcPhgZqqUgZ6pBhgASvse5C0Vmv3j1M0vBK_Fxr8D-a75IngHXesnO1GPbV0cHhC-MUn38CM0ywtE6HaBJROuWSm0Ki9INlYK2pkg9TqRClcuOitPb8iiNu1gEcG2UFvTJBHpqrqz8xDoNSN65AyuK_Qy8lqnrKlbEfxb6gxgK29I-kPttAAQWu05HoDidfxpmh3PbFkv0aqRBYw6k_tjXpGPq9l_dR8e6uwhzFLJKJVqpqhtCQiDF4QaOUMP8PlUuV4b-eQWrcmttiuBnCOcf9mh9PmmzjdiHkPmIFtgD-mQ'

noPermissionsToken = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5DWnJBb1pYeXNfaXVNZWlkeEJLWSJ9.eyJpc3MiOiJodHRwczovL2Rldi0wbTVia2IwdS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjFkZWFmYWVkMTg4ZDgwMDZlYTRjYzI4IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTY0MTk4MzkxOCwiZXhwIjoxNjQxOTkxMTE4LCJhenAiOiJKVzJJOWhCcHl1cElleGZhaXczZnhuT01ydDAyWjJrdyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOltdfQ.GJD9Y1qh6ebdDXQ2_diRH7Q51BfugkRvFrF5gTOAcs_l1QMtEED6vbW8V6QF5ang8GJebF6p6qCVCoxEi7I54J2ZwOCyI34zFo7vNcRsSIIad2Jhmmbw9t1UWBJrsvqw8HXuAyVG6jNBcZYtmwSl_UTFGqwiZHW2Uhm8u6GliesVvlKPBXYTvI4RbU00E2IbG02UeJ8_sTuzH9YIutCo1VR-gieVdKBEzF2KEoNzwy_UFfocIjj0y_ttS3of6p79qmUrSu7QBAtNi3ojxcmslIe1pZLYf0U-Ce38krN7I17U6GGMFWAw6FXXSWHaeuqEBQL3CzH78jUhJg6HseKrVg'

class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "postgres"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "postgres", "", "localhost:5432", self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

# First set of tests are for actors

    def test_get_actors_with_result(self):
        res = self.client().get('/actors', headers = {'Authorization': f'Bearer {castingAssistantTokenValid}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['actors']), 3)

    def test_post_actor_with_result(self):
        res = self.client().post('/actors',headers = {'Authorization': f'Bearer {castingDirectorTokenValid}'}, json ={
        'name':'Test_app actor name',
        'age': '35',
        'gender': 'Male'
        })
        data = json.loads(res.data)

        new_actor = Actor.query.filter(Actor.name == 'Test_app actor name').first()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor'], {
        'name':'Test_app actor name',
        'age': 35,
        'gender': 'Male',
        'id': new_actor.id
        })

        new_actor.delete()

    def test_post_actor_without_result(self):
        res = self.client().post('/actors',headers = {'Authorization': f'Bearer {castingDirectorTokenValid}'}, json ={
        'name':'Test_app actor name without age provided',
        'gender': 'Male'
        })
        data = json.loads(res.data)

        new_actor = Actor.query.filter(Actor.name == 'Test_app actor name without age provided').one_or_none()
        self.assertEqual(res.status_code, 422)
        self.assertTrue(new_actor is None)

    def test_delete_actor_with_results(self):
        actor_to_delete = Actor(age=32, gender='Male', name='test_actor_to_delete1')
        actor_to_delete.insert()
        id = actor_to_delete.id

        res = self.client().delete(f'/actors/{id}',headers = {'Authorization': f'Bearer {castingDirectorTokenValid}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], id)

    def test_delete_actor_without_results(self):
        res = self.client().delete(f'/actors/65343456',headers = {'Authorization': f'Bearer {castingDirectorTokenValid}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_patch_actor_with_result(self):
        actor_to_patch = Actor(age=32, gender='Male', name='test_actor_to_patch1')
        actor_to_patch.insert()
        id = actor_to_patch.id

        res = self.client().patch(f'/actors/{id}',headers = {'Authorization': f'Bearer {castingDirectorTokenValid}'}, json={
        'name':'test_actor_to_patch1_updated',
        'age': 33,
        'gender':'Female'
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['edited'], {
        'name':'test_actor_to_patch1_updated',
        'age': 33,
        'gender': 'Female',
        'id': id
        })

        actor_to_patch.delete()

    def test_patch_actor_without_result1_incomplete_data(self):
        actor_to_patch = Actor(age=41, gender='Male', name='test_actor_to_patch2')
        actor_to_patch.insert()
        id = actor_to_patch.id

        res = self.client().patch(f'/actors/{id}',headers = {'Authorization': f'Bearer {castingDirectorTokenValid}'}, json={
        'name':'test_actor_to_patch2_updated_no_gender',
        'age': 33
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        actor_to_patch.delete()

    def test_patch_actor_without_result2_not_found(self):
        res = self.client().patch(f'/actors/967578658765',headers = {'Authorization': f'Bearer {castingDirectorTokenValid}'}, json={
        'name':'test_actor_to_patch_not_found',
        'age': 33,
        'gender': 'Male'
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

# Second set of tests are for movies

    def test_get_movies_with_result(self):
        res = self.client().get('/movies', headers = {'Authorization': f'Bearer {castingAssistantTokenValid}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['movies']), 2)

    def test_post_movie_with_result(self):
        res = self.client().post('/movies',headers = {'Authorization': f'Bearer {executiveProducerTokenValid}'}, json ={
        'title':'test_app_movie_title',
        'releaseDate': '2020-06-25'
        })
        data = json.loads(res.data)

        new_movie = Movie.query.filter(Movie.title == 'test_app_movie_title').first()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie'], {
        'title':'test_app_movie_title',
        'releaseDate': 'Thu, 25 Jun 2020 00:00:00 GMT',
        'id': new_movie.id
        })

        new_movie.delete()

    def test_post_movie_without_result(self):
        res = self.client().post('/movies',headers = {'Authorization': f'Bearer {executiveProducerTokenValid}'}, json ={
        'title':'test_app_movie_title_releaseDate_not_provided'
        })
        data = json.loads(res.data)

        new_movie = Movie.query.filter(Movie.title == 'test_app_movie_title_releaseDate_not_provided').one_or_none()
        self.assertEqual(res.status_code, 422)
        self.assertTrue(new_movie is None)

    def test_delete_movie_with_results(self):
        movie_to_delete = Movie(releaseDate='2019-06-18', title='test_movie_to_delete1')
        movie_to_delete.insert()
        id = movie_to_delete.id

        res = self.client().delete(f'/movies/{id}',headers = {'Authorization': f'Bearer {executiveProducerTokenValid}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], id)

    def test_delete_movie_without_results(self):
        res = self.client().delete(f'/movies/65343456',headers = {'Authorization': f'Bearer {executiveProducerTokenValid}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_patch_movie_with_result(self):
        movie_to_patch = Movie(releaseDate='2020-06-20', title='test_movie_to_patch1')
        movie_to_patch.insert()
        id = movie_to_patch.id

        res = self.client().patch(f'/movies/{id}',headers = {'Authorization': f'Bearer {castingDirectorTokenValid}'}, json={
        'title':'test_movie_to_patch1_updated',
        'releaseDate': '2020-06-25'
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['edited'], {
        'title':'test_movie_to_patch1_updated',
        'releaseDate': 'Thu, 25 Jun 2020 00:00:00 GMT',
        'id': id
        })

        movie_to_patch.delete()

    def test_patch_movie_without_result1_incomplete_data(self):
        movie_to_patch = Movie(releaseDate='2019-03-18', title='test_movie_to_patch2')
        movie_to_patch.insert()
        id = movie_to_patch.id

        res = self.client().patch(f'/movies/{id}',headers = {'Authorization': f'Bearer {castingDirectorTokenValid}'}, json={
        'title':'test_movie_to_patch2_updated_no_releaseDate'
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        movie_to_patch.delete()

    def test_patch_movie_without_result2_not_found(self):
        res = self.client().patch(f'/movies/967578658765',headers = {'Authorization': f'Bearer {castingDirectorTokenValid}'}, json={
        'title':'test_movie_to_patch_not_found',
        'releaseDate': '2020-03-01'
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

# Third set of tests are for RBAC
    def test_casting_assistant_delete_movie_not_authorised(self):
        res = self.client().delete(f'/movies/1',headers = {'Authorization': f'Bearer {castingAssistantTokenValid}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)

    def test_casting_assistant_post_movie_not_authorised(self):
        res = self.client().post('/movies',headers = {'Authorization': f'Bearer {castingAssistantTokenValid}'}, json ={
        'title':'test_app_movie_title',
        'releaseDate': '2020-06-25'
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)

    def test_casting_director_delete_movie_not_authorised(self):
        res = self.client().delete(f'/movies/1',headers = {'Authorization': f'Bearer {castingDirectorTokenValid}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)

    def test_casting_director_post_movie_not_authorised(self):
        res = self.client().post('/movies',headers = {'Authorization': f'Bearer {castingDirectorTokenValid}'}, json ={
        'title':'test_app_movie_title',
        'releaseDate': '2020-06-25'
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)

    def test_executive_producer_get_actors_with_result(self):
        res = self.client().get('/actors', headers = {'Authorization': f'Bearer {executiveProducerTokenValid}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['actors']), 3)

    def test_get_actors_no_bearer_token(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
