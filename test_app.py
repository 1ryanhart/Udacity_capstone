import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor

castingAssistantTokenValid = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5DWnJBb1pYeXNfaXVNZWlkeEJLWSJ9.eyJpc3MiOiJodHRwczovL2Rldi0wbTVia2IwdS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjFkZWE5MzkzNjRiMWQwMDZhZmQ1NjM0IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTY0MTk4OTg1NywiZXhwIjoxNjQxOTk3MDU3LCJhenAiOiJKVzJJOWhCcHl1cElleGZhaXczZnhuT01ydDAyWjJrdyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.geu4mpuzjLY9E0dOEdYa4540LGX9m8u_riYQHv3s51iezKzLc0AaIoBvRriFpzM_qdtIFpj3GmTAH0qLQl9xkGO_3BdwfmZMnlbo69Sa6DeCcAE26UneW2UfUSPIZMrjLs9N9mRiWFTDE73v9G7PsfHFpKf0V5t00GrZ0VDP2hO6VZrvrX6qcmtw92EAmQ9GZKr_MEU4oUvSHTK0qimrBepo6QPdbVGbUPZn-XAwUDHEuTsbtxa8CtLHbhK1fHoicu5eIQoeEMjmz6vHuOxl77RSkalxZUchLMCHG3LpIOLPvD-jB3BiY0IIMl4Y0uKEPPZ27jrOh3U01kaD1UjJQg'

castingDirectorTokenValid = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5DWnJBb1pYeXNfaXVNZWlkeEJLWSJ9.eyJpc3MiOiJodHRwczovL2Rldi0wbTVia2IwdS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjFkZWFlMGEzNjRiMWQwMDZhZmQ1NmJkIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTY0MTk4OTkyMywiZXhwIjoxNjQxOTk3MTIzLCJhenAiOiJKVzJJOWhCcHl1cElleGZhaXczZnhuT01ydDAyWjJrdyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.LolK-XxYyisSGR3rEbd3Dcs90_FGRPYg1q8geLd88uq9T8a1Q7n0903Ci1h2aknHavWxwIkvtTHJMc1lHAl_HMUWS6A22dUB9ShHiF8mBsbB0YGrCjt5M23WO4F4SRk26dE4R8O82hfwU0HUbMyIK9FTXNIwwgb2d_8hOllXBjsc_Q0rIbdEaQvilizeINJvcOKlNK2tWpTlOdBKUTpd_-JUo2EpjTUhiSSO0l_CPwcndKbW7kmENOSDweQ-jMx4M0jo9YAONkPhqRqkijUY5aqCGJ23qzwxsduO44m_cQHH5ZIaWwrnHW8wnwv2zrsMfaKK7-MtRBdWgnztqSr6vA'

executiveProducerTokenValid = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5DWnJBb1pYeXNfaXVNZWlkeEJLWSJ9.eyJpc3MiOiJodHRwczovL2Rldi0wbTVia2IwdS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjFkZWFmYWVkMTg4ZDgwMDZlYTRjYzI4IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTY0MTk4OTk4NiwiZXhwIjoxNjQxOTk3MTg2LCJhenAiOiJKVzJJOWhCcHl1cElleGZhaXczZnhuT01ydDAyWjJrdyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.MNwaTaYJq0-JHOosUOt47IUySNiNV8fCDcN67K1-QlxfVY1vQOLH2eWNU-hT0Y-ycB9vOr1BYoi98fYpgsemKeQQgujx9fqdgvV1Kl4X7QfVYPZRo5ZrSJw85TdxNkEY4AptO-mJuozjxPONOR1Fjy_4RORrGtRin8ONjuRFGzQkjI_5aT97Nb3HeRPhrxvE1TIe8D-PUi-SKDmvtP2FAoUBAmnzbuOMMBXmK8BCnixPrrOVIi5nm1VWygwW6D0i9LV76QaezQAh8d9LgwH54LJJtV0sIH1zuwrUg2BudrrZrtbLkEL0EhGd5ASrPBaaI8VFWOuWVRu72B0jh74dIQ'

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
