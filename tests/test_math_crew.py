"""Tests for math crew module."""

from unittest.mock import MagicMock, patch

import pytest

from math_generator.math_concepts import GradeLevel, MathTopic
from math_generator.math_crew import MathProblemsCrew, generate_problems_for_grade


class TestMathProblemsCrew:
    """Tests for MathProblemsCrew class."""

    def test_create_crew_with_defaults(self) -> None:
        """Test creating crew with default parameters."""
        crew = MathProblemsCrew()
        assert crew.grade == GradeLevel.GRADE_1
        assert crew.topic == MathTopic.ADDITION
        assert crew.verbose is True

    def test_create_crew_with_custom_params(self) -> None:
        """Test creating crew with custom parameters."""
        crew = MathProblemsCrew(
            grade=GradeLevel.GRADE_3,
            topic=MathTopic.MULTIPLICATION,
            verbose=False,
        )
        assert crew.grade == GradeLevel.GRADE_3
        assert crew.topic == MathTopic.MULTIPLICATION
        assert crew.verbose is False

    def test_invalid_topic_for_grade_raises_error(self) -> None:
        """Test that invalid topic for grade raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            MathProblemsCrew(
                grade=GradeLevel.KINDERGARTEN,
                topic=MathTopic.DIVISION,
            )
        assert "not appropriate" in str(exc_info.value)

    def test_valid_topic_combinations(self) -> None:
        """Test valid topic and grade combinations."""
        valid_combinations = [
            (GradeLevel.KINDERGARTEN, MathTopic.COUNTING),
            (GradeLevel.GRADE_1, MathTopic.ADDITION),
            (GradeLevel.GRADE_2, MathTopic.SUBTRACTION),
            (GradeLevel.GRADE_3, MathTopic.MULTIPLICATION),
            (GradeLevel.GRADE_4, MathTopic.DIVISION),
            (GradeLevel.GRADE_5, MathTopic.FRACTIONS),
        ]
        for grade, topic in valid_combinations:
            crew = MathProblemsCrew(grade=grade, topic=topic)
            assert crew.grade == grade
            assert crew.topic == topic

    def test_create_agents(self) -> None:
        """Test that _create_agents returns all expected agents."""
        crew = MathProblemsCrew()
        agents = crew._create_agents()

        assert "concept_expert" in agents
        assert "problem_generator" in agents
        assert "problem_reviewer" in agents
        assert "hint_provider" in agents


class TestGenerateProblemsForGrade:
    """Tests for generate_problems_for_grade function."""

    @patch("math_generator.math_crew.MathProblemsCrew")
    def test_generates_for_all_topics(self, mock_crew_class: MagicMock) -> None:
        """Test that function generates problems for all grade-appropriate topics."""
        mock_crew = MagicMock()
        mock_crew.generate_problems.return_value = {"result": "test"}
        mock_crew_class.return_value = mock_crew

        result = generate_problems_for_grade(
            grade=GradeLevel.GRADE_1,
            num_problems_per_topic=2,
        )

        assert result["grade"] == "grade_1"
        assert "topics" in result
        # Grade 1 has multiple topics, so multiple calls should be made
        assert mock_crew.generate_problems.called

    def test_result_structure(self) -> None:
        """Test the structure of the returned result."""
        # Just test that the function can be called and returns expected structure
        with patch("math_generator.math_crew.MathProblemsCrew") as mock_crew_class:
            mock_crew = MagicMock()
            mock_crew.generate_problems.return_value = {"result": "test"}
            mock_crew_class.return_value = mock_crew

            result = generate_problems_for_grade(GradeLevel.KINDERGARTEN)

            assert isinstance(result, dict)
            assert "grade" in result
            assert "topics" in result


class TestCrewIntegration:
    """Integration tests for the crew (require mocking LLM calls)."""

    @patch("math_generator.math_crew.Crew")
    def test_generate_problems_creates_crew(self, mock_crew_class: MagicMock) -> None:
        """Test that generate_problems creates and runs a Crew."""
        mock_crew_instance = MagicMock()
        mock_crew_instance.kickoff.return_value = "Generated problems"
        mock_crew_class.return_value = mock_crew_instance

        crew = MathProblemsCrew(
            grade=GradeLevel.GRADE_1,
            topic=MathTopic.ADDITION,
            verbose=False,
        )
        result = crew.generate_problems(num_problems=3)

        mock_crew_class.assert_called_once()
        mock_crew_instance.kickoff.assert_called_once()
        assert "result" in result

    @patch("math_generator.math_crew.Crew")
    def test_explain_concept_creates_crew(self, mock_crew_class: MagicMock) -> None:
        """Test that explain_concept creates and runs a Crew."""
        mock_crew_instance = MagicMock()
        mock_crew_instance.kickoff.return_value = "Concept explanation"
        mock_crew_class.return_value = mock_crew_instance

        crew = MathProblemsCrew(
            grade=GradeLevel.GRADE_2,
            topic=MathTopic.SUBTRACTION,
            verbose=False,
        )
        result = crew.explain_concept()

        mock_crew_class.assert_called_once()
        assert "explanation" in result

    @patch("math_generator.math_crew.Crew")
    def test_generate_worksheet_creates_crew(self, mock_crew_class: MagicMock) -> None:
        """Test that generate_worksheet creates and runs a Crew."""
        mock_crew_instance = MagicMock()
        mock_crew_instance.kickoff.return_value = "Worksheet content"
        mock_crew_class.return_value = mock_crew_instance

        crew = MathProblemsCrew(
            grade=GradeLevel.GRADE_3,
            topic=MathTopic.MULTIPLICATION,
            verbose=False,
        )
        result = crew.generate_worksheet(num_problems=5)

        mock_crew_class.assert_called_once()
        assert "worksheet" in result

    @patch("math_generator.math_crew.Crew")
    def test_generate_problems_without_hints(self, mock_crew_class: MagicMock) -> None:
        """Test generating problems without hints."""
        mock_crew_instance = MagicMock()
        mock_crew_instance.kickoff.return_value = "Problems"
        mock_crew_class.return_value = mock_crew_instance

        crew = MathProblemsCrew()
        result = crew.generate_problems(
            num_problems=3,
            include_hints=False,
            include_review=False,
        )

        assert "result" in result

    @patch("math_generator.math_crew.Crew")
    def test_generate_problems_returns_metadata(self, mock_crew_class: MagicMock) -> None:
        """Test that generate_problems returns proper metadata."""
        mock_crew_instance = MagicMock()
        mock_crew_instance.kickoff.return_value = "Problems"
        mock_crew_class.return_value = mock_crew_instance

        crew = MathProblemsCrew(
            grade=GradeLevel.GRADE_4,
            topic=MathTopic.FRACTIONS,
        )
        result = crew.generate_problems(
            num_problems=5,
            difficulty=3,
        )

        assert result["grade"] == "grade_4"
        assert result["topic"] == "fractions"
        assert result["num_problems"] == 5
        assert result["difficulty"] == 3
