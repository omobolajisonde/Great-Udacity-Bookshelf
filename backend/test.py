import unittest
from backend.models import setup_db
from flaskr import create_app

class ResourceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name="test_db"
        self.database_path="postgres://{}:{}@{}:{}/{}".format("bolaji","bolaji","localhost",5432,self.database_name)
        setup_db(self.app,self.database_path)

    def tearDown(self):
        """Executed after each test"""
        pass
    def test_given_behaviour(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)

if __name__ == "__main__":
    unittest.main()