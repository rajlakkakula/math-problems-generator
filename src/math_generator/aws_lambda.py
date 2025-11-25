"""AWS Lambda handler for math problems generation."""

import json
from typing import Any

from math_generator.math_concepts import GradeLevel, MathTopic
from math_generator.math_crew import MathProblemsCrew


def lambda_handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """AWS Lambda handler for generating math problems.

    This handler processes API Gateway requests to generate math problems
    for elementary school students.

    Args:
        event: The Lambda event containing request data.
        context: The Lambda context (unused).

    Returns:
        API Gateway response with generated problems or error message.
    """
    try:
        # Parse request body
        body = event.get("body", "{}")
        if isinstance(body, str):
            body = json.loads(body) if body else {}

        # Get parameters from query string or body
        query_params = event.get("queryStringParameters", {}) or {}

        grade_str = body.get("grade") or query_params.get("grade", "grade_1")
        topic_str = body.get("topic") or query_params.get("topic", "addition")
        num_problems = int(body.get("num_problems") or query_params.get("num_problems", 5))
        difficulty = int(body.get("difficulty") or query_params.get("difficulty", 1))
        action = body.get("action") or query_params.get("action", "generate")

        # Validate and convert grade level
        try:
            grade = GradeLevel(grade_str)
        except ValueError:
            valid_grades = [g.value for g in GradeLevel]
            return _error_response(400, f"Invalid grade: {grade_str}. Valid grades: {valid_grades}")

        # Validate and convert topic
        try:
            topic = MathTopic(topic_str)
        except ValueError:
            valid_topics = [t.value for t in MathTopic]
            return _error_response(400, f"Invalid topic: {topic_str}. Valid topics: {valid_topics}")

        # Validate difficulty
        if not 1 <= difficulty <= 5:
            return _error_response(400, "Difficulty must be between 1 and 5")

        # Validate num_problems
        if not 1 <= num_problems <= 20:
            return _error_response(400, "Number of problems must be between 1 and 20")

        # Create the crew and execute the action
        crew = MathProblemsCrew(grade=grade, topic=topic, verbose=False)

        if action == "generate":
            result = crew.generate_problems(
                num_problems=num_problems,
                difficulty=difficulty,
                include_hints=True,
                include_review=True,
            )
        elif action == "explain":
            result = crew.explain_concept()
        elif action == "worksheet":
            result = crew.generate_worksheet(
                num_problems=num_problems,
                difficulty=difficulty,
            )
        else:
            return _error_response(
                400, f"Invalid action: {action}. Valid actions: generate, explain, worksheet"
            )

        return _success_response(result)

    except ValueError as e:
        return _error_response(400, str(e))
    except Exception as e:
        return _error_response(500, f"Internal server error: {str(e)}")


def _success_response(data: dict[str, Any]) -> dict[str, Any]:
    """Create a successful API Gateway response.

    Args:
        data: The response data.

    Returns:
        API Gateway response dictionary.
    """
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        },
        "body": json.dumps(data),
    }


def _error_response(status_code: int, message: str) -> dict[str, Any]:
    """Create an error API Gateway response.

    Args:
        status_code: HTTP status code.
        message: Error message.

    Returns:
        API Gateway response dictionary.
    """
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        },
        "body": json.dumps({"error": message}),
    }


# Additional handler for health checks
def health_check(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """Health check handler for the Lambda function.

    Args:
        event: The Lambda event (unused).
        context: The Lambda context (unused).

    Returns:
        API Gateway response indicating service health.
    """
    return _success_response(
        {
            "status": "healthy",
            "service": "math-problems-generator",
            "version": "0.1.0",
        }
    )
