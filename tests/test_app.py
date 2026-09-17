import unittest
from app import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_user_lookup_missing_param(self):
        response = self.client.get("/user")
        self.assertIn(response.status_code, [200, 500])

    def test_calc_simple_expression(self):
        response = self.client.get("/calc?expr=1+1")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
