"""CrewAI crew orchestration for math problem generation."""

from typing import Any

from crewai import LLM, Crew, Process

from math_generator.math_agents import (
    create_hint_provider,
    create_math_concept_expert,
    create_problem_generator,
    create_problem_reviewer,
    get_llm,
)
from math_generator.pdf_generator import MathPDFGenerator
from math_generator.math_concepts import (
    GradeLevel,
    MathTopic,
    get_concept_description,
    get_topics_for_grade,
)
from math_generator.math_tasks import (
    create_concept_explanation_task,
    create_hint_generation_task,
    create_problem_generation_task,
    create_problem_review_task,
    create_worksheet_compilation_task,
)


class MathProblemsCrew:
    """Orchestrates the math problems generation crew."""

    def __init__(
        self,
        grade: GradeLevel = GradeLevel.GRADE_1,
        topic: MathTopic = MathTopic.ADDITION,
        llm: LLM | None = None,
        verbose: bool = True,
        output_dir: str = "output",
    ):
        """Initialize the math problems crew.

        Args:
            grade: The target grade level for problems.
            topic: The math topic to focus on.
            llm: Optional LLM instance. If not provided, uses default.
            verbose: Whether to show verbose output.
            output_dir: Directory to save generated PDFs.
        """
        self.grade = grade
        self.topic = topic
        self.llm = llm or get_llm()
        self.verbose = verbose
        self.pdf_generator = MathPDFGenerator(output_dir=output_dir)

        # Validate that topic is appropriate for grade
        valid_topics = get_topics_for_grade(grade)
        if topic not in valid_topics:
            valid_topic_names = [t.value for t in valid_topics]
            raise ValueError(
                f"Topic '{topic.value}' is not appropriate for {grade.value}. "
                f"Valid topics: {valid_topic_names}"
            )

    def _create_agents(self) -> dict[str, Any]:
        """Create all agents for the crew.

        Returns:
            Dictionary of agent name to Agent instance.
        """
        return {
            "concept_expert": create_math_concept_expert(self.grade, self.topic, self.llm),
            "problem_generator": create_problem_generator(self.grade, self.topic, self.llm),
            "problem_reviewer": create_problem_reviewer(self.grade, self.llm),
            "hint_provider": create_hint_provider(self.grade, self.llm),
        }

    def generate_problems(
        self,
        num_problems: int = 5,
        difficulty: int = 1,
        include_hints: bool = True,
        include_review: bool = True,
        generate_pdf: bool = True,
        frequency: str = "daily",
    ) -> dict[str, Any]:
        """Generate math problems using the crew.

        Args:
            num_problems: Number of problems to generate.
            difficulty: Difficulty level (1-5).
            include_hints: Whether to generate hints for problems.
            include_review: Whether to review problems for quality.
            generate_pdf: Whether to generate a PDF file.
            frequency: 'daily' or 'weekly' for PDF filename.

        Returns:
            Dictionary containing generated problems, metadata, and PDF path if generated.
        """
        agents = self._create_agents()
        tasks = []

        # Create problem generation task
        generation_task = create_problem_generation_task(
            agent=agents["problem_generator"],
            topic=self.topic,
            grade=self.grade,
            num_problems=num_problems,
            difficulty=difficulty,
        )
        tasks.append(generation_task)

        # Optionally add review task
        if include_review:
            review_task = create_problem_review_task(
                agent=agents["problem_reviewer"],
                topic=self.topic,
                grade=self.grade,
                context=[generation_task],
            )
            tasks.append(review_task)

        # Optionally add hint generation task
        if include_hints:
            hint_task = create_hint_generation_task(
                agent=agents["hint_provider"],
                topic=self.topic,
                grade=self.grade,
                context=[generation_task],
            )
            tasks.append(hint_task)

        # Create and run the crew
        crew = Crew(
            agents=list(agents.values()),
            tasks=tasks,
            process=Process.sequential,
            verbose=self.verbose,
        )

        result = crew.kickoff()

        result_data = {
            "grade": self.grade.value,
            "topic": self.topic.value,
            "num_problems": num_problems,
            "difficulty": difficulty,
            "result": str(result),
            "tasks_output": [str(task.output) for task in tasks if task.output],
        }

        # Generate PDF if requested
        if generate_pdf:
            pdf_path = self.pdf_generator.generate_problems_pdf(
                data=result_data,
                frequency=frequency,
                include_answers=True,
                include_hints=include_hints,
            )
            result_data["pdf_path"] = pdf_path

        return result_data

    def explain_concept(self, generate_pdf: bool = True, frequency: str = "weekly") -> dict[str, Any]:
        """Generate a concept explanation.

        Args:
            generate_pdf: Whether to generate a PDF file.
            frequency: 'daily' or 'weekly' for PDF filename.

        Returns:
            Dictionary containing the concept explanation and PDF path if generated.
        """
        agents = self._create_agents()

        concept_task = create_concept_explanation_task(
            agent=agents["concept_expert"],
            topic=self.topic,
            grade=self.grade,
        )

        crew = Crew(
            agents=[agents["concept_expert"]],
            tasks=[concept_task],
            process=Process.sequential,
            verbose=self.verbose,
        )

        result = crew.kickoff()

        result_data = {
            "grade": self.grade.value,
            "topic": self.topic.value,
            "description": get_concept_description(self.topic, self.grade),
            "explanation": str(result),
        }

        # Generate PDF if requested
        if generate_pdf:
            pdf_path = self.pdf_generator.generate_concept_pdf(
                data=result_data, frequency=frequency
            )
            result_data["pdf_path"] = pdf_path

        return result_data

    def generate_worksheet(
        self,
        num_problems: int = 10,
        difficulty: int = 1,
        generate_pdf: bool = True,
        frequency: str = "weekly",
    ) -> dict[str, Any]:
        """Generate a complete worksheet.

        Args:
            num_problems: Number of problems for the worksheet.
            difficulty: Difficulty level (1-5).
            generate_pdf: Whether to generate a PDF file.
            frequency: 'daily' or 'weekly' for PDF filename.

        Returns:
            Dictionary containing the complete worksheet and PDF path if generated.
        """
        agents = self._create_agents()
        tasks = []

        # Generate concept explanation
        concept_task = create_concept_explanation_task(
            agent=agents["concept_expert"],
            topic=self.topic,
            grade=self.grade,
        )
        tasks.append(concept_task)

        # Generate problems
        generation_task = create_problem_generation_task(
            agent=agents["problem_generator"],
            topic=self.topic,
            grade=self.grade,
            num_problems=num_problems,
            difficulty=difficulty,
        )
        tasks.append(generation_task)

        # Review problems
        review_task = create_problem_review_task(
            agent=agents["problem_reviewer"],
            topic=self.topic,
            grade=self.grade,
            context=[generation_task],
        )
        tasks.append(review_task)

        # Generate hints
        hint_task = create_hint_generation_task(
            agent=agents["hint_provider"],
            topic=self.topic,
            grade=self.grade,
            context=[generation_task],
        )
        tasks.append(hint_task)

        # Compile worksheet
        worksheet_task = create_worksheet_compilation_task(
            agent=agents["concept_expert"],
            topic=self.topic,
            grade=self.grade,
            context=[concept_task, generation_task, review_task, hint_task],
        )
        tasks.append(worksheet_task)

        # Create and run the crew
        crew = Crew(
            agents=list(agents.values()),
            tasks=tasks,
            process=Process.sequential,
            verbose=self.verbose,
        )

        result = crew.kickoff()

        result_data = {
            "grade": self.grade.value,
            "topic": self.topic.value,
            "num_problems": num_problems,
            "difficulty": difficulty,
            "worksheet": str(result),
        }

        # Generate PDF if requested
        if generate_pdf:
            pdf_path = self.pdf_generator.generate_worksheet_pdf(
                data=result_data, frequency=frequency
            )
            result_data["pdf_path"] = pdf_path

        return result_data


def generate_problems_for_grade(
    grade: GradeLevel,
    num_problems_per_topic: int = 3,
    llm: LLM | None = None,
) -> dict[str, Any]:
    """Generate problems for all appropriate topics for a grade.

    Args:
        grade: The target grade level.
        num_problems_per_topic: Number of problems per topic.
        llm: Optional LLM instance.

    Returns:
        Dictionary containing problems for all topics.
    """
    topics = get_topics_for_grade(grade)
    results: dict[str, Any] = {
        "grade": grade.value,
        "topics": {},
    }

    for topic in topics:
        crew = MathProblemsCrew(grade=grade, topic=topic, llm=llm, verbose=False)
        topic_result = crew.generate_problems(
            num_problems=num_problems_per_topic,
            include_hints=True,
            include_review=True,
        )
        results["topics"][topic.value] = topic_result

    return results
