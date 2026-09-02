import unittest

from issue_tracker.main import app


class OpenAPIAuthTests(unittest.TestCase):
    def test_user_profile_uses_cookie_security_scheme(self) -> None:
        schema = app.openapi()
        operation = schema["paths"]["/user-profile/"]["get"]

        self.assertNotIn("parameters", operation)
        self.assertEqual(operation["security"], [{"APIKeyCookie": []}])


if __name__ == "__main__":
    unittest.main()
