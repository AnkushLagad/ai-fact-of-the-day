import json
import unittest
from unittest.mock import Mock, patch

import lambda_function


class GenerateFactTests(unittest.TestCase):
    def test_generate_fact_returns_text_and_category(self):
        with patch(
            "lambda_function.random.choice",
            return_value="space and astronomy",
        ) as choose_category:
            with patch("lambda_function.bedrock.invoke_model") as invoke_model:
                response_body = Mock()
                response_body.read.return_value = json.dumps({
                    "output": {
                        "message": {
                            "content": [{"text": "  Saturn could float in water.  "}]
                        }
                    }
                }).encode("utf-8")
                invoke_model.return_value = {"body": response_body}

                fact, category = lambda_function.generate_fact()

        self.assertEqual(fact, "Saturn could float in water.")
        self.assertEqual(category, "space and astronomy")
        self.assertEqual(invoke_model.call_args.kwargs["modelId"], lambda_function.MODEL_ID)
        choose_category.assert_called_once()


class HtmlPageTests(unittest.TestCase):
    def test_generated_text_is_escaped_and_controls_are_present(self):
        page = lambda_function.build_html_page(
            '<script>alert("fact")</script>',
            "science & technology",
        )

        self.assertIn("&lt;script&gt;alert(&quot;fact&quot;)&lt;/script&gt;", page)
        self.assertIn("Science &amp; Technology", page)
        self.assertNotIn('<script>alert("fact")</script>', page)
        self.assertIn('id="copy-fact"', page)
        self.assertIn('href="/"', page)


class HandlerTests(unittest.TestCase):
    def test_handler_returns_html_and_disables_caching(self):
        with patch(
            "lambda_function.generate_fact",
            return_value=("A sample fact.", "mathematics"),
        ) as generate_fact:
            response = lambda_function.handler({}, None)

        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(response["headers"]["Content-Type"], "text/html; charset=utf-8")
        self.assertEqual(response["headers"]["Cache-Control"], "no-store")
        self.assertIn("A sample fact.", response["body"])
        generate_fact.assert_called_once()

    def test_handler_logs_failure_without_exposing_it_to_visitors(self):
        with patch(
            "lambda_function.generate_fact",
            side_effect=RuntimeError("private failure detail"),
        ) as generate_fact:
            with self.assertLogs(lambda_function.logger, level="ERROR"):
                response = lambda_function.handler({}, None)

        self.assertEqual(response["statusCode"], 500)
        self.assertIn("try again in a moment", response["body"])
        self.assertNotIn("private failure detail", response["body"])
        generate_fact.assert_called_once()


if __name__ == "__main__":
    unittest.main()
