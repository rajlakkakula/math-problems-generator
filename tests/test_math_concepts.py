"""Tests for math concepts module."""

import pytest

from math_generator.math_concepts import (
    GRADE_TOPICS,
    GradeLevel,
    MathConcept,
    MathProblem,
    MathProblemsSet,
    MathTopic,
    create_math_concept,
    get_concept_description,
    get_topics_for_grade,
)


class TestGradeLevel:
    """Tests for GradeLevel enum."""

    def test_all_grades_defined(self) -> None:
        """Test that all expected grade levels are defined."""
        expected_grades = [
            "kindergarten",
            "grade_1",
            "grade_2",
            "grade_3",
            "grade_4",
            "grade_5",
        ]
        actual_grades = [g.value for g in GradeLevel]
        assert actual_grades == expected_grades

    def test_grade_from_value(self) -> None:
        """Test creating grade from string value."""
        assert GradeLevel("grade_1") == GradeLevel.GRADE_1
        assert GradeLevel("kindergarten") == GradeLevel.KINDERGARTEN

    def test_invalid_grade(self) -> None:
        """Test that invalid grade raises ValueError."""
        with pytest.raises(ValueError):
            GradeLevel("grade_6")


class TestMathTopic:
    """Tests for MathTopic enum."""

    def test_all_topics_defined(self) -> None:
        """Test that all expected topics are defined."""
        expected_topics = [
            "counting",
            "addition",
            "subtraction",
            "multiplication",
            "division",
            "fractions",
            "ratios",
            "decimals",
            "geometry",
            "measurement_and_data",
            "word_problems",
            "patterns",
            "time",
            "money",
            "numbers_and_operations",
            "data_and_statistics",
        ]
        actual_topics = [t.value for t in MathTopic]
        assert actual_topics == expected_topics

    def test_topic_from_value(self) -> None:
        """Test creating topic from string value."""
        assert MathTopic("addition") == MathTopic.ADDITION
        assert MathTopic("multiplication") == MathTopic.MULTIPLICATION


class TestMathConcept:
    """Tests for MathConcept model."""

    def test_create_concept(self) -> None:
        """Test creating a math concept."""
        concept = MathConcept(
            topic=MathTopic.ADDITION,
            grade_level=GradeLevel.GRADE_1,
            description="Add numbers within 20",
            difficulty=1,
        )
        assert concept.topic == MathTopic.ADDITION
        assert concept.grade_level == GradeLevel.GRADE_1
        assert concept.description == "Add numbers within 20"
        assert concept.difficulty == 1
        assert concept.examples == []

    def test_concept_with_examples(self) -> None:
        """Test creating concept with examples."""
        concept = MathConcept(
            topic=MathTopic.ADDITION,
            grade_level=GradeLevel.GRADE_1,
            description="Add numbers",
            examples=["5 + 3 = 8", "7 + 2 = 9"],
        )
        assert len(concept.examples) == 2
        assert "5 + 3 = 8" in concept.examples

    def test_difficulty_validation(self) -> None:
        """Test that difficulty must be between 1 and 5."""
        with pytest.raises(ValueError):
            MathConcept(
                topic=MathTopic.ADDITION,
                grade_level=GradeLevel.GRADE_1,
                description="Test",
                difficulty=0,
            )

        with pytest.raises(ValueError):
            MathConcept(
                topic=MathTopic.ADDITION,
                grade_level=GradeLevel.GRADE_1,
                description="Test",
                difficulty=6,
            )


class TestMathProblem:
    """Tests for MathProblem model."""

    def test_create_problem(self) -> None:
        """Test creating a math problem."""
        problem = MathProblem(
            question="What is 5 + 3?",
            answer="8",
            topic=MathTopic.ADDITION,
            grade_level=GradeLevel.GRADE_1,
        )
        assert problem.question == "What is 5 + 3?"
        assert problem.answer == "8"
        assert problem.topic == MathTopic.ADDITION
        assert problem.grade_level == GradeLevel.GRADE_1
        assert problem.difficulty == 1
        assert problem.hints == []
        assert problem.explanation == ""

    def test_problem_with_hints(self) -> None:
        """Test creating problem with hints and explanation."""
        problem = MathProblem(
            question="What is 5 + 3?",
            answer="8",
            topic=MathTopic.ADDITION,
            grade_level=GradeLevel.GRADE_1,
            hints=["Count on from 5", "Use your fingers"],
            explanation="Start at 5 and count 3 more: 6, 7, 8",
        )
        assert len(problem.hints) == 2
        assert problem.explanation == "Start at 5 and count 3 more: 6, 7, 8"


class TestMathProblemsSet:
    """Tests for MathProblemsSet model."""

    def test_create_empty_set(self) -> None:
        """Test creating an empty problems set."""
        problems_set = MathProblemsSet(
            topic=MathTopic.ADDITION,
            grade_level=GradeLevel.GRADE_1,
        )
        assert len(problems_set.problems) == 0
        assert problems_set.total_problems == 0

    def test_create_set_with_problems(self) -> None:
        """Test creating a problems set with problems."""
        problems = [
            MathProblem(
                question="5 + 3 = ?",
                answer="8",
                topic=MathTopic.ADDITION,
                grade_level=GradeLevel.GRADE_1,
            ),
            MathProblem(
                question="2 + 4 = ?",
                answer="6",
                topic=MathTopic.ADDITION,
                grade_level=GradeLevel.GRADE_1,
            ),
        ]
        problems_set = MathProblemsSet(
            problems=problems,
            topic=MathTopic.ADDITION,
            grade_level=GradeLevel.GRADE_1,
            total_problems=2,
        )
        assert len(problems_set.problems) == 2
        assert problems_set.total_problems == 2


class TestGetTopicsForGrade:
    """Tests for get_topics_for_grade function."""

    def test_kindergarten_topics(self) -> None:
        """Test kindergarten topics."""
        topics = get_topics_for_grade(GradeLevel.KINDERGARTEN)
        assert MathTopic.COUNTING in topics
        assert MathTopic.ADDITION in topics
        assert MathTopic.SUBTRACTION in topics
        assert MathTopic.PATTERNS in topics
        # Advanced topics should not be in kindergarten
        assert MathTopic.MULTIPLICATION not in topics
        assert MathTopic.DIVISION not in topics
        assert MathTopic.FRACTIONS not in topics

    def test_grade_3_topics(self) -> None:
        """Test grade 3 topics."""
        topics = get_topics_for_grade(GradeLevel.GRADE_3)
        assert MathTopic.MULTIPLICATION in topics
        assert MathTopic.DIVISION in topics
        assert MathTopic.FRACTIONS in topics
        assert MathTopic.WORD_PROBLEMS in topics

    def test_grade_5_topics(self) -> None:
        """Test grade 5 topics."""
        topics = get_topics_for_grade(GradeLevel.GRADE_5)
        assert MathTopic.DECIMALS in topics
        assert MathTopic.FRACTIONS in topics
        assert MathTopic.GEOMETRY in topics

    def test_all_grades_have_topics(self) -> None:
        """Test that all grades have at least some topics."""
        for grade in GradeLevel:
            topics = get_topics_for_grade(grade)
            assert len(topics) > 0, f"Grade {grade.value} should have topics"


class TestGetConceptDescription:
    """Tests for get_concept_description function."""

    def test_addition_grade_1(self) -> None:
        """Test addition description for grade 1."""
        description = get_concept_description(MathTopic.ADDITION, GradeLevel.GRADE_1)
        assert "20" in description.lower() or "number" in description.lower()

    def test_multiplication_grade_3(self) -> None:
        """Test multiplication description for grade 3."""
        description = get_concept_description(MathTopic.MULTIPLICATION, GradeLevel.GRADE_3)
        assert len(description) > 0

    def test_fallback_description(self) -> None:
        """Test that unknown combinations get a fallback description."""
        # This should return a fallback description
        description = get_concept_description(MathTopic.DECIMALS, GradeLevel.KINDERGARTEN)
        assert len(description) > 0

    def test_ratios_grade_5(self) -> None:
        """Test ratios description for grade 5."""
        description = get_concept_description(MathTopic.RATIOS, GradeLevel.GRADE_5)
        assert "ratio" in description.lower() or "rate" in description.lower()
        assert len(description) > 0

    def test_data_and_statistics_grade_4(self) -> None:
        """Test data and statistics description for grade 4."""
        description = get_concept_description(MathTopic.DATA_AND_STATISTICS, GradeLevel.GRADE_4)
        assert len(description) > 0
        assert "data" in description.lower() or "plot" in description.lower()

    def test_numbers_and_operations_grade_3(self) -> None:
        """Test numbers and operations description for grade 3."""
        description = get_concept_description(MathTopic.NUMBERS_AND_OPERATIONS, GradeLevel.GRADE_3)
        assert len(description) > 0
        assert "number" in description.lower() or "operation" in description.lower()


class TestCreateMathConcept:
    """Tests for create_math_concept function."""

    def test_create_concept_for_grade_1(self) -> None:
        """Test creating concept for grade 1."""
        concept = create_math_concept(MathTopic.ADDITION, GradeLevel.GRADE_1)
        assert concept.topic == MathTopic.ADDITION
        assert concept.grade_level == GradeLevel.GRADE_1
        assert concept.difficulty == 1
        assert len(concept.description) > 0

    def test_create_concept_for_grade_5(self) -> None:
        """Test creating concept for grade 5."""
        concept = create_math_concept(MathTopic.FRACTIONS, GradeLevel.GRADE_5)
        assert concept.topic == MathTopic.FRACTIONS
        assert concept.grade_level == GradeLevel.GRADE_5
        assert concept.difficulty == 5

    def test_difficulty_increases_with_grade(self) -> None:
        """Test that difficulty increases with grade level."""
        concept_k = create_math_concept(MathTopic.ADDITION, GradeLevel.KINDERGARTEN)
        concept_5 = create_math_concept(MathTopic.ADDITION, GradeLevel.GRADE_4)
        assert concept_k.difficulty < concept_5.difficulty


class TestGradeTopicsMapping:
    """Tests for GRADE_TOPICS mapping."""

    def test_all_grades_mapped(self) -> None:
        """Test that all grades have a mapping."""
        for grade in GradeLevel:
            assert grade in GRADE_TOPICS

    def test_topics_are_valid(self) -> None:
        """Test that all mapped topics are valid MathTopic values."""
        for _grade, topics in GRADE_TOPICS.items():
            for topic in topics:
                assert isinstance(topic, MathTopic)

    def test_progression_of_topics(self) -> None:
        """Test that topics progress appropriately across grades."""
        # Counting should be in early grades but not later ones
        assert MathTopic.COUNTING in GRADE_TOPICS[GradeLevel.KINDERGARTEN]
        assert MathTopic.COUNTING in GRADE_TOPICS[GradeLevel.GRADE_1]
        assert MathTopic.COUNTING not in GRADE_TOPICS[GradeLevel.GRADE_5]

        # Division should not be in early grades
        assert MathTopic.DIVISION not in GRADE_TOPICS[GradeLevel.KINDERGARTEN]
        assert MathTopic.DIVISION not in GRADE_TOPICS[GradeLevel.GRADE_1]
        assert MathTopic.DIVISION in GRADE_TOPICS[GradeLevel.GRADE_3]
