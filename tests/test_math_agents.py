"""Tests for math agents module."""

from math_generator.math_agents import (
    create_hint_provider,
    create_math_concept_expert,
    create_problem_generator,
    create_problem_reviewer,
    get_llm,
)
from math_generator.math_concepts import GradeLevel, MathTopic


class TestGetLLM:
    """Tests for get_llm function."""

    def test_get_llm_returns_llm_instance(self) -> None:
        """Test that get_llm returns an LLM instance."""
        llm = get_llm()
        assert llm is not None
        assert llm.model == "bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0"

    def test_get_llm_with_custom_model(self) -> None:
        """Test get_llm with custom model ID."""
        llm = get_llm(model_id="anthropic.claude-3-haiku-20240307-v1:0")
        assert "haiku" in llm.model


class TestCreateMathConceptExpert:
    """Tests for create_math_concept_expert function."""

    def test_create_agent_with_defaults(self) -> None:
        """Test creating agent with default parameters."""
        agent = create_math_concept_expert(
            grade=GradeLevel.GRADE_1,
            topic=MathTopic.ADDITION,
        )
        assert agent.role == "Math Concept Expert"
        assert "addition" in agent.goal.lower()
        assert "grade 1" in agent.goal.lower()

    def test_create_agent_with_custom_llm(self) -> None:
        """Test creating agent with custom LLM."""
        custom_llm = get_llm()
        agent = create_math_concept_expert(
            grade=GradeLevel.GRADE_3,
            topic=MathTopic.MULTIPLICATION,
            llm=custom_llm,
        )
        assert agent.llm == custom_llm

    def test_agent_backstory_contains_grade_info(self) -> None:
        """Test that agent backstory mentions the grade level."""
        agent = create_math_concept_expert(
            grade=GradeLevel.GRADE_2,
            topic=MathTopic.SUBTRACTION,
        )
        assert "grade 2" in agent.backstory.lower()
        assert "subtraction" in agent.backstory.lower()


class TestCreateProblemGenerator:
    """Tests for create_problem_generator function."""

    def test_create_agent_with_defaults(self) -> None:
        """Test creating problem generator with default parameters."""
        agent = create_problem_generator(
            grade=GradeLevel.GRADE_1,
            topic=MathTopic.ADDITION,
        )
        assert agent.role == "Math Problem Generator"
        assert "addition" in agent.goal.lower()

    def test_agent_for_different_topics(self) -> None:
        """Test creating agents for different topics."""
        topics = [MathTopic.ADDITION, MathTopic.MULTIPLICATION, MathTopic.FRACTIONS]
        for topic in topics:
            agent = create_problem_generator(
                grade=GradeLevel.GRADE_3,
                topic=topic,
            )
            assert topic.value.replace("_", " ") in agent.goal.lower()


class TestCreateProblemReviewer:
    """Tests for create_problem_reviewer function."""

    def test_create_reviewer_agent(self) -> None:
        """Test creating problem reviewer agent."""
        agent = create_problem_reviewer(grade=GradeLevel.GRADE_1)
        assert agent.role == "Math Problem Reviewer"
        assert "grade 1" in agent.goal.lower()

    def test_reviewer_for_different_grades(self) -> None:
        """Test creating reviewers for different grades."""
        for grade in GradeLevel:
            agent = create_problem_reviewer(grade=grade)
            grade_name = grade.value.replace("_", " ")
            assert grade_name in agent.goal.lower()


class TestCreateHintProvider:
    """Tests for create_hint_provider function."""

    def test_create_hint_provider_agent(self) -> None:
        """Test creating hint provider agent."""
        agent = create_hint_provider(grade=GradeLevel.GRADE_2)
        assert agent.role == "Math Hint Provider"
        assert "grade 2" in agent.goal.lower()

    def test_hint_provider_backstory(self) -> None:
        """Test that hint provider has appropriate backstory."""
        agent = create_hint_provider(grade=GradeLevel.GRADE_1)
        assert "hint" in agent.backstory.lower() or "tutor" in agent.backstory.lower()


class TestAgentProperties:
    """Tests for common agent properties."""

    def test_all_agents_have_verbose_true(self) -> None:
        """Test that all agents have verbose set to True by default."""
        agents = [
            create_math_concept_expert(GradeLevel.GRADE_1, MathTopic.ADDITION),
            create_problem_generator(GradeLevel.GRADE_1, MathTopic.ADDITION),
            create_problem_reviewer(GradeLevel.GRADE_1),
            create_hint_provider(GradeLevel.GRADE_1),
        ]
        for agent in agents:
            assert agent.verbose is True

    def test_all_agents_have_delegation_disabled(self) -> None:
        """Test that all agents have allow_delegation set to False."""
        agents = [
            create_math_concept_expert(GradeLevel.GRADE_1, MathTopic.ADDITION),
            create_problem_generator(GradeLevel.GRADE_1, MathTopic.ADDITION),
            create_problem_reviewer(GradeLevel.GRADE_1),
            create_hint_provider(GradeLevel.GRADE_1),
        ]
        for agent in agents:
            assert agent.allow_delegation is False
