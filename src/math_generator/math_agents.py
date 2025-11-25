"""CrewAI agents for math problem generation."""

from crewai import LLM, Agent

from math_generator.math_concepts import GradeLevel, MathTopic


def get_llm(model_id: str = "anthropic.claude-3-5-sonnet-20241022-v2:0") -> LLM:
    """Get the LLM instance for agents.

    Args:
        model_id: The AWS Bedrock model ID to use.

    Returns:
        An LLM instance configured for AWS Bedrock.
    """
    return LLM(
        model=f"bedrock/{model_id}",
        temperature=0.7,
    )


def create_math_concept_expert(
    grade: GradeLevel,
    topic: MathTopic,
    llm: LLM | None = None,
) -> Agent:
    """Create a math concept expert agent.

    This agent specializes in understanding and explaining math concepts
    appropriate for elementary school students.

    Args:
        grade: The target grade level.
        topic: The math topic to focus on.
        llm: Optional LLM instance. If not provided, uses default.

    Returns:
        A CrewAI Agent configured as a math concept expert.
    """
    if llm is None:
        llm = get_llm()

    topic_name = topic.value.replace("_", " ")
    grade_name = grade.value.replace("_", " ")

    goal = (
        f"Provide clear, age-appropriate explanations of {topic_name} "
        f"concepts for {grade_name} students."
    )
    backstory = (
        f"You are an experienced elementary school math teacher who specializes "
        f"in teaching {topic_name} to young students. You have a gift for "
        "making complex mathematical concepts simple and engaging. You understand the "
        f"developmental stages of children in {grade_name} and adapt "
        "your explanations accordingly. You always use encouraging language and provide "
        "relatable examples that children can understand."
    )

    return Agent(
        role="Math Concept Expert",
        goal=goal,
        backstory=backstory,
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )


def create_problem_generator(
    grade: GradeLevel,
    topic: MathTopic,
    llm: LLM | None = None,
) -> Agent:
    """Create a math problem generator agent.

    This agent generates age-appropriate math problems for the specified
    grade level and topic.

    Args:
        grade: The target grade level.
        topic: The math topic for problems.
        llm: Optional LLM instance. If not provided, uses default.

    Returns:
        A CrewAI Agent configured as a problem generator.
    """
    if llm is None:
        llm = get_llm()

    topic_name = topic.value.replace("_", " ")
    grade_name = grade.value.replace("_", " ")

    goal = (
        f"Generate engaging, educational math problems about "
        f"{topic_name} that are appropriate for {grade_name} students."
    )
    backstory = (
        "You are a curriculum designer who creates math worksheets and "
        f"practice problems for elementary school students. You specialize in creating "
        f"problems for {grade_name} students focusing on "
        f"{topic_name}. Your problems are creative, engaging, and "
        "progressively challenging while remaining age-appropriate. You include "
        "real-world scenarios that children can relate to, such as toys, animals, "
        "food, and everyday activities."
    )

    return Agent(
        role="Math Problem Generator",
        goal=goal,
        backstory=backstory,
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )


def create_problem_reviewer(
    grade: GradeLevel,
    llm: LLM | None = None,
) -> Agent:
    """Create a math problem reviewer agent.

    This agent reviews generated problems for accuracy, age-appropriateness,
    and educational value.

    Args:
        grade: The target grade level.
        llm: Optional LLM instance. If not provided, uses default.

    Returns:
        A CrewAI Agent configured as a problem reviewer.
    """
    if llm is None:
        llm = get_llm()

    grade_name = grade.value.replace("_", " ")

    goal = (
        "Review and validate math problems to ensure they are accurate, "
        f"age-appropriate for {grade_name}, and educationally sound."
    )
    backstory = (
        "You are a senior educational consultant who specializes in "
        "elementary math education. You review math problems to ensure they meet "
        f"curriculum standards for {grade_name} students. You check "
        "for mathematical accuracy, appropriate difficulty level, clear wording, "
        "and educational value. You provide constructive feedback to improve "
        "problems when necessary."
    )

    return Agent(
        role="Math Problem Reviewer",
        goal=goal,
        backstory=backstory,
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )


def create_hint_provider(
    grade: GradeLevel,
    llm: LLM | None = None,
) -> Agent:
    """Create a hint provider agent.

    This agent generates helpful hints and step-by-step explanations
    for math problems.

    Args:
        grade: The target grade level.
        llm: Optional LLM instance. If not provided, uses default.

    Returns:
        A CrewAI Agent configured as a hint provider.
    """
    if llm is None:
        llm = get_llm()

    grade_name = grade.value.replace("_", " ")
    goal = (
        "Create helpful, scaffolded hints and step-by-step explanations "
        f"that guide {grade_name} students to solve math problems "
        "without giving away the answer directly."
    )
    backstory = (
        "You are a patient math tutor who excels at helping struggling "
        "students understand math concepts. You create hints that break down problems "
        f"into manageable steps for {grade_name} students. Your hints "
        "encourage students to think critically while providing just enough guidance "
        "to keep them from getting frustrated. You use visual descriptions and "
        "relatable examples to help children understand."
    )

    return Agent(
        role="Math Hint Provider",
        goal=goal,
        backstory=backstory,
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )
