"""Tests for math tasks module."""

from unittest.mock import MagicMock, patch

import pytest

from math_generator.math_concepts import GradeLevel, MathTopic
from math_generator.math_tasks import (
    create_concept_explanation_task,
    create_hint_generation_task,
    create_problem_generation_task,
    create_problem_review_task,
    create_worksheet_compilation_task,
)


@pytest.fixture
def mock_agent() -> MagicMock:
    """Create a mock agent for testing."""
    mock = MagicMock()
    mock.role = "Test Agent"
    return mock


class TestCreateConceptExplanationTask:
    """Tests for create_concept_explanation_task function."""

    @patch("math_generator.math_tasks.Task")
    def test_create_task_with_basic_params(
        self, mock_task_class: MagicMock, mock_agent: MagicMock
    ) -> None:
        """Test creating concept explanation task."""
        create_concept_explanation_task(
            agent=mock_agent,
            topic=MathTopic.ADDITION,
            grade=GradeLevel.GRADE_1,
        )
        mock_task_class.assert_called_once()
        call_kwargs = mock_task_class.call_args.kwargs
        assert "addition" in call_kwargs["description"].lower()
        assert "grade 1" in call_kwargs["description"].lower()
        assert call_kwargs["agent"] == mock_agent

    @patch("math_generator.math_tasks.Task")
    def test_task_expected_output(self, mock_task_class: MagicMock, mock_agent: MagicMock) -> None:
        """Test that task has appropriate expected output."""
        create_concept_explanation_task(
            agent=mock_agent,
            topic=MathTopic.MULTIPLICATION,
            grade=GradeLevel.GRADE_3,
        )
        call_kwargs = mock_task_class.call_args.kwargs
        assert "multiplication" in call_kwargs["expected_output"].lower()
        assert "grade 3" in call_kwargs["expected_output"].lower()

    @patch("math_generator.math_tasks.Task")
    def test_task_for_different_topics(
        self, mock_task_class: MagicMock, mock_agent: MagicMock
    ) -> None:
        """Test creating tasks for different topics."""
        for topic in [MathTopic.FRACTIONS, MathTopic.GEOMETRY, MathTopic.TIME]:
            mock_task_class.reset_mock()
            create_concept_explanation_task(
                agent=mock_agent,
                topic=topic,
                grade=GradeLevel.GRADE_3,
            )
            call_kwargs = mock_task_class.call_args.kwargs
            topic_name = topic.value.replace("_", " ")
            assert topic_name in call_kwargs["description"].lower()


class TestCreateProblemGenerationTask:
    """Tests for create_problem_generation_task function."""

    @patch("math_generator.math_tasks.Task")
    def test_create_task_with_defaults(
        self, mock_task_class: MagicMock, mock_agent: MagicMock
    ) -> None:
        """Test creating problem generation task with defaults."""
        create_problem_generation_task(
            agent=mock_agent,
            topic=MathTopic.ADDITION,
            grade=GradeLevel.GRADE_1,
        )
        call_kwargs = mock_task_class.call_args.kwargs
        assert call_kwargs["agent"] == mock_agent
        assert "5" in call_kwargs["description"]  # Default num_problems

    @patch("math_generator.math_tasks.Task")
    def test_create_task_with_custom_params(
        self, mock_task_class: MagicMock, mock_agent: MagicMock
    ) -> None:
        """Test creating task with custom parameters."""
        create_problem_generation_task(
            agent=mock_agent,
            topic=MathTopic.SUBTRACTION,
            grade=GradeLevel.GRADE_2,
            num_problems=10,
            difficulty=3,
        )
        call_kwargs = mock_task_class.call_args.kwargs
        assert "10" in call_kwargs["description"]
        assert "subtraction" in call_kwargs["description"].lower()

    @patch("math_generator.math_tasks.Task")
    def test_task_includes_formatting_guidelines(
        self, mock_task_class: MagicMock, mock_agent: MagicMock
    ) -> None:
        """Test that task includes formatting guidelines."""
        create_problem_generation_task(
            agent=mock_agent,
            topic=MathTopic.ADDITION,
            grade=GradeLevel.GRADE_1,
        )
        call_kwargs = mock_task_class.call_args.kwargs
        assert "question" in call_kwargs["description"].lower()
        assert "answer" in call_kwargs["description"].lower()
        assert "explanation" in call_kwargs["description"].lower()


class TestCreateProblemReviewTask:
    """Tests for create_problem_review_task function."""

    @patch("math_generator.math_tasks.Task")
    def test_create_review_task(self, mock_task_class: MagicMock, mock_agent: MagicMock) -> None:
        """Test creating problem review task."""
        create_problem_review_task(
            agent=mock_agent,
            topic=MathTopic.ADDITION,
            grade=GradeLevel.GRADE_1,
        )
        call_kwargs = mock_task_class.call_args.kwargs
        assert call_kwargs["agent"] == mock_agent
        assert "review" in call_kwargs["description"].lower()
        assert "accuracy" in call_kwargs["description"].lower()

    @patch("math_generator.math_tasks.Task")
    def test_review_task_with_context(
        self, mock_task_class: MagicMock, mock_agent: MagicMock
    ) -> None:
        """Test creating review task with context."""
        context_task = MagicMock()
        create_problem_review_task(
            agent=mock_agent,
            topic=MathTopic.ADDITION,
            grade=GradeLevel.GRADE_1,
            context=[context_task],
        )
        call_kwargs = mock_task_class.call_args.kwargs
        assert context_task in call_kwargs["context"]


class TestCreateHintGenerationTask:
    """Tests for create_hint_generation_task function."""

    @patch("math_generator.math_tasks.Task")
    def test_create_hint_task(self, mock_task_class: MagicMock, mock_agent: MagicMock) -> None:
        """Test creating hint generation task."""
        create_hint_generation_task(
            agent=mock_agent,
            topic=MathTopic.MULTIPLICATION,
            grade=GradeLevel.GRADE_3,
        )
        call_kwargs = mock_task_class.call_args.kwargs
        assert call_kwargs["agent"] == mock_agent
        assert "hint" in call_kwargs["description"].lower()
        assert "multiplication" in call_kwargs["description"].lower()

    @patch("math_generator.math_tasks.Task")
    def test_hint_task_mentions_progressive_hints(
        self, mock_task_class: MagicMock, mock_agent: MagicMock
    ) -> None:
        """Test that hint task mentions progressive hints."""
        create_hint_generation_task(
            agent=mock_agent,
            topic=MathTopic.ADDITION,
            grade=GradeLevel.GRADE_1,
        )
        call_kwargs = mock_task_class.call_args.kwargs
        assert "hint 1" in call_kwargs["description"].lower()
        assert "hint 2" in call_kwargs["description"].lower()


class TestCreateWorksheetCompilationTask:
    """Tests for create_worksheet_compilation_task function."""

    @patch("math_generator.math_tasks.Task")
    def test_create_worksheet_task(self, mock_task_class: MagicMock, mock_agent: MagicMock) -> None:
        """Test creating worksheet compilation task."""
        create_worksheet_compilation_task(
            agent=mock_agent,
            topic=MathTopic.SUBTRACTION,
            grade=GradeLevel.GRADE_2,
        )
        call_kwargs = mock_task_class.call_args.kwargs
        assert call_kwargs["agent"] == mock_agent
        assert "worksheet" in call_kwargs["description"].lower()
        assert "subtraction" in call_kwargs["description"].lower()

    @patch("math_generator.math_tasks.Task")
    def test_worksheet_task_includes_sections(
        self, mock_task_class: MagicMock, mock_agent: MagicMock
    ) -> None:
        """Test that worksheet task mentions required sections."""
        create_worksheet_compilation_task(
            agent=mock_agent,
            topic=MathTopic.ADDITION,
            grade=GradeLevel.GRADE_1,
        )
        call_kwargs = mock_task_class.call_args.kwargs
        assert "title" in call_kwargs["description"].lower()
        assert "answer key" in call_kwargs["description"].lower()

    @patch("math_generator.math_tasks.Task")
    def test_worksheet_task_with_context(
        self, mock_task_class: MagicMock, mock_agent: MagicMock
    ) -> None:
        """Test creating worksheet task with multiple context tasks."""
        context_tasks = [MagicMock(), MagicMock(), MagicMock()]
        create_worksheet_compilation_task(
            agent=mock_agent,
            topic=MathTopic.ADDITION,
            grade=GradeLevel.GRADE_1,
            context=context_tasks,
        )
        call_kwargs = mock_task_class.call_args.kwargs
        assert len(call_kwargs["context"]) == 3
