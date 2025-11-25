"""CrewAI tasks for math problem generation."""

from crewai import Agent, Task

from math_generator.math_concepts import GradeLevel, MathTopic


def create_concept_explanation_task(
    agent: Agent,
    topic: MathTopic,
    grade: GradeLevel,
) -> Task:
    """Create a task for explaining a math concept.

    Args:
        agent: The agent to perform the task.
        topic: The math topic to explain.
        grade: The target grade level.

    Returns:
        A CrewAI Task for concept explanation.
    """
    topic_name = topic.value.replace("_", " ")
    grade_name = grade.value.replace("_", " ")

    description = f"""Explain the math concept of {topic_name} for {grade_name} students.

Your explanation should include:
1. A simple, age-appropriate definition
2. Why this concept is important
3. Real-world examples children can relate to
4. Common misconceptions to avoid
5. Tips for understanding the concept better

Keep the language simple and engaging for young learners."""

    expected_output = (
        f"A clear, engaging explanation of {topic_name} suitable for "
        f"{grade_name} students, including definition, importance, examples, and tips."
    )

    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
    )


def create_problem_generation_task(
    agent: Agent,
    topic: MathTopic,
    grade: GradeLevel,
    num_problems: int = 5,
    difficulty: int = 1,
) -> Task:
    """Create a task for generating math problems.

    Args:
        agent: The agent to perform the task.
        topic: The math topic for problems.
        grade: The target grade level.
        num_problems: Number of problems to generate.
        difficulty: Difficulty level (1-5).

    Returns:
        A CrewAI Task for problem generation.
    """
    topic_name = topic.value.replace("_", " ")
    grade_name = grade.value.replace("_", " ")

    description = f"""Generate {num_problems} math problems about {topic_name} \
for {grade_name} students at difficulty level {difficulty} (out of 5).

For each problem, provide:
1. The question (clear and age-appropriate)
2. The correct answer
3. A brief explanation of how to solve it

Guidelines:
- Use simple, clear language
- Include relatable scenarios (toys, animals, food, games)
- Vary the problem types within the topic
- Ensure mathematical accuracy
- Make problems progressively slightly harder

Format each problem as:
Problem [number]:
Question: [question text]
Answer: [answer]
Explanation: [step-by-step solution]"""

    expected_output = (
        f"{num_problems} well-formatted math problems about {topic_name} "
        f"appropriate for {grade_name} students, each with question, answer, and explanation."
    )

    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
    )


def create_problem_review_task(
    agent: Agent,
    topic: MathTopic,
    grade: GradeLevel,
    context: list[Task] | None = None,
) -> Task:
    """Create a task for reviewing generated problems.

    Args:
        agent: The agent to perform the task.
        topic: The math topic of the problems.
        grade: The target grade level.
        context: Previous tasks whose output to use as context.

    Returns:
        A CrewAI Task for problem review.
    """
    topic_name = topic.value.replace("_", " ")
    grade_name = grade.value.replace("_", " ")

    description = f"""Review the generated {topic_name} problems for {grade_name} students.

For each problem, verify:
1. Mathematical accuracy - Is the answer correct?
2. Age appropriateness - Is it suitable for {grade_name}?
3. Clarity - Is the question clearly worded?
4. Difficulty - Is it at the right level?
5. Educational value - Does it help learn the concept?

Provide:
- Overall quality assessment (pass/needs revision)
- Specific feedback for any problems that need improvement
- Suggested corrections if errors are found"""

    expected_output = (
        f"A detailed review of the {topic_name} problems, including "
        "quality assessment, accuracy verification, and improvement suggestions."
    )

    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
        context=context or [],
    )


def create_hint_generation_task(
    agent: Agent,
    topic: MathTopic,
    grade: GradeLevel,
    context: list[Task] | None = None,
) -> Task:
    """Create a task for generating hints for problems.

    Args:
        agent: The agent to perform the task.
        topic: The math topic of the problems.
        grade: The target grade level.
        context: Previous tasks whose output to use as context.

    Returns:
        A CrewAI Task for hint generation.
    """
    topic_name = topic.value.replace("_", " ")
    grade_name = grade.value.replace("_", " ")

    description = f"""Create helpful hints for the {topic_name} problems \
designed for {grade_name} students.

For each problem, create 2-3 hints that:
1. Guide students toward the solution without giving it away
2. Break down the problem into smaller steps
3. Use simple language appropriate for {grade_name}
4. Encourage critical thinking
5. Build confidence

Hints should be progressive:
- Hint 1: A gentle nudge in the right direction
- Hint 2: A more specific strategy
- Hint 3: A detailed step to help stuck students"""

    expected_output = (
        f"2-3 progressive hints for each {topic_name} problem, "
        f"designed to help {grade_name} students solve problems independently."
    )

    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
        context=context or [],
    )


def create_worksheet_compilation_task(
    agent: Agent,
    topic: MathTopic,
    grade: GradeLevel,
    context: list[Task] | None = None,
) -> Task:
    """Create a task for compiling a complete worksheet.

    Args:
        agent: The agent to perform the task.
        topic: The math topic for the worksheet.
        grade: The target grade level.
        context: Previous tasks whose output to use as context.

    Returns:
        A CrewAI Task for worksheet compilation.
    """
    topic_name = topic.value.replace("_", " ")
    grade_name = grade.value.replace("_", " ")

    description = f"""Compile a complete {topic_name} worksheet for {grade_name} students.

The worksheet should include:
1. A title and brief introduction
2. A quick concept review section
3. The practice problems (organized by difficulty)
4. An answer key section
5. A "Challenge Yourself" bonus section

Format the worksheet in a clear, printable format with:
- Clear section headers
- Numbered problems
- Space indicators for student work
- Encouraging messages throughout"""

    expected_output = (
        f"A complete, well-formatted {topic_name} worksheet for "
        f"{grade_name} students, including introduction, problems, and answer key."
    )

    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
        context=context or [],
    )
