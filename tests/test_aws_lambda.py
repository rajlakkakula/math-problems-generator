"""Tests for AWS Lambda handler."""

import json
from unittest.mock import MagicMock, patch

from math_generator.aws_lambda import (
    _error_response,
    _success_response,
    health_check,
    lambda_handler,
)


class TestSuccessResponse:
    """Tests for _success_response function."""

    def test_returns_200_status(self) -> None:
        """Test that success response returns 200 status."""
        response = _success_response({"key": "value"})
        assert response["statusCode"] == 200

    def test_returns_cors_headers(self) -> None:
        """Test that success response includes CORS headers."""
        response = _success_response({})
        assert "Access-Control-Allow-Origin" in response["headers"]
        assert response["headers"]["Access-Control-Allow-Origin"] == "*"

    def test_returns_json_body(self) -> None:
        """Test that success response returns JSON body."""
        data = {"result": "test", "count": 5}
        response = _success_response(data)
        body = json.loads(response["body"])
        assert body == data


class TestErrorResponse:
    """Tests for _error_response function."""

    def test_returns_specified_status(self) -> None:
        """Test that error response returns specified status code."""
        response = _error_response(400, "Bad request")
        assert response["statusCode"] == 400

        response = _error_response(500, "Server error")
        assert response["statusCode"] == 500

    def test_returns_error_message(self) -> None:
        """Test that error response includes error message."""
        response = _error_response(400, "Invalid parameter")
        body = json.loads(response["body"])
        assert body["error"] == "Invalid parameter"

    def test_returns_cors_headers(self) -> None:
        """Test that error response includes CORS headers."""
        response = _error_response(500, "Error")
        assert "Access-Control-Allow-Origin" in response["headers"]


class TestHealthCheck:
    """Tests for health_check function."""

    def test_returns_healthy_status(self) -> None:
        """Test that health check returns healthy status."""
        response = health_check({}, None)
        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["status"] == "healthy"

    def test_returns_service_info(self) -> None:
        """Test that health check returns service information."""
        response = health_check({}, None)
        body = json.loads(response["body"])
        assert body["service"] == "math-problems-generator"
        assert "version" in body


class TestLambdaHandler:
    """Tests for lambda_handler function."""

    @patch("math_generator.aws_lambda.MathProblemsCrew")
    def test_handler_with_valid_request(self, mock_crew_class: MagicMock) -> None:
        """Test handler with valid request parameters."""
        mock_crew = MagicMock()
        mock_crew.generate_problems.return_value = {"result": "problems"}
        mock_crew_class.return_value = mock_crew

        event = {
            "body": json.dumps(
                {
                    "grade": "grade_1",
                    "topic": "addition",
                    "num_problems": 5,
                }
            )
        }
        response = lambda_handler(event, None)

        assert response["statusCode"] == 200
        mock_crew.generate_problems.assert_called_once()

    @patch("math_generator.aws_lambda.MathProblemsCrew")
    def test_handler_with_query_params(self, mock_crew_class: MagicMock) -> None:
        """Test handler with query string parameters."""
        mock_crew = MagicMock()
        mock_crew.generate_problems.return_value = {"result": "problems"}
        mock_crew_class.return_value = mock_crew

        event = {
            "queryStringParameters": {
                "grade": "grade_2",
                "topic": "subtraction",
            }
        }
        response = lambda_handler(event, None)

        assert response["statusCode"] == 200

    def test_handler_with_invalid_grade(self) -> None:
        """Test handler with invalid grade parameter."""
        event = {
            "body": json.dumps(
                {
                    "grade": "grade_99",
                    "topic": "addition",
                }
            )
        }
        response = lambda_handler(event, None)

        assert response["statusCode"] == 400
        body = json.loads(response["body"])
        assert "invalid grade" in body["error"].lower()

    def test_handler_with_invalid_topic(self) -> None:
        """Test handler with invalid topic parameter."""
        event = {
            "body": json.dumps(
                {
                    "grade": "grade_1",
                    "topic": "quantum_physics",
                }
            )
        }
        response = lambda_handler(event, None)

        assert response["statusCode"] == 400
        body = json.loads(response["body"])
        assert "invalid topic" in body["error"].lower()

    def test_handler_with_invalid_difficulty(self) -> None:
        """Test handler with invalid difficulty parameter."""
        event = {
            "body": json.dumps(
                {
                    "grade": "grade_1",
                    "topic": "addition",
                    "difficulty": 10,
                }
            )
        }
        response = lambda_handler(event, None)

        assert response["statusCode"] == 400
        body = json.loads(response["body"])
        assert "difficulty" in body["error"].lower()

    def test_handler_with_invalid_num_problems(self) -> None:
        """Test handler with invalid num_problems parameter."""
        event = {
            "body": json.dumps(
                {
                    "grade": "grade_1",
                    "topic": "addition",
                    "num_problems": 100,
                }
            )
        }
        response = lambda_handler(event, None)

        assert response["statusCode"] == 400
        body = json.loads(response["body"])
        assert "number of problems" in body["error"].lower()

    @patch("math_generator.aws_lambda.MathProblemsCrew")
    def test_handler_explain_action(self, mock_crew_class: MagicMock) -> None:
        """Test handler with explain action."""
        mock_crew = MagicMock()
        mock_crew.explain_concept.return_value = {"explanation": "test"}
        mock_crew_class.return_value = mock_crew

        event = {
            "body": json.dumps(
                {
                    "grade": "grade_1",
                    "topic": "addition",
                    "action": "explain",
                }
            )
        }
        response = lambda_handler(event, None)

        assert response["statusCode"] == 200
        mock_crew.explain_concept.assert_called_once()

    @patch("math_generator.aws_lambda.MathProblemsCrew")
    def test_handler_worksheet_action(self, mock_crew_class: MagicMock) -> None:
        """Test handler with worksheet action."""
        mock_crew = MagicMock()
        mock_crew.generate_worksheet.return_value = {"worksheet": "test"}
        mock_crew_class.return_value = mock_crew

        event = {
            "body": json.dumps(
                {
                    "grade": "grade_1",
                    "topic": "addition",
                    "action": "worksheet",
                }
            )
        }
        response = lambda_handler(event, None)

        assert response["statusCode"] == 200
        mock_crew.generate_worksheet.assert_called_once()

    def test_handler_with_invalid_action(self) -> None:
        """Test handler with invalid action parameter."""
        event = {
            "body": json.dumps(
                {
                    "grade": "grade_1",
                    "topic": "addition",
                    "action": "invalid_action",
                }
            )
        }
        response = lambda_handler(event, None)

        assert response["statusCode"] == 400
        body = json.loads(response["body"])
        assert "invalid action" in body["error"].lower()

    @patch("math_generator.aws_lambda.MathProblemsCrew")
    def test_handler_with_empty_body(self, mock_crew_class: MagicMock) -> None:
        """Test handler with empty request body uses defaults."""
        mock_crew = MagicMock()
        mock_crew.generate_problems.return_value = {"result": "problems"}
        mock_crew_class.return_value = mock_crew

        event = {"body": ""}
        response = lambda_handler(event, None)

        assert response["statusCode"] == 200

    @patch("math_generator.aws_lambda.MathProblemsCrew")
    def test_handler_with_missing_body(self, mock_crew_class: MagicMock) -> None:
        """Test handler with missing body uses defaults."""
        mock_crew = MagicMock()
        mock_crew.generate_problems.return_value = {"result": "problems"}
        mock_crew_class.return_value = mock_crew

        event = {}
        response = lambda_handler(event, None)

        assert response["statusCode"] == 200

    def test_handler_with_topic_not_valid_for_grade(self) -> None:
        """Test handler when topic is not valid for the grade."""
        event = {
            "body": json.dumps(
                {
                    "grade": "kindergarten",
                    "topic": "division",
                }
            )
        }
        response = lambda_handler(event, None)

        assert response["statusCode"] == 400
        body = json.loads(response["body"])
        assert "error" in body
