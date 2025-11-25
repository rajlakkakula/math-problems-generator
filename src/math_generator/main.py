"""Main entry point for the math problems generator CLI."""

import argparse
import json
import sys
from typing import Any

from math_generator.math_concepts import (
    GradeLevel,
    MathTopic,
    create_math_concept,
    get_topics_for_grade,
)
from math_generator.math_crew import MathProblemsCrew


def parse_args() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description="Generate math problems for elementary school kids",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate 5 addition problems for Grade 1
  math-generator --grade grade_1 --topic addition --num-problems 5

  # Explain multiplication concept for Grade 3
  math-generator --grade grade_3 --topic multiplication --action explain

  # Generate a complete worksheet
  math-generator --grade grade_2 --topic subtraction --action worksheet

  # List available topics for a grade
  math-generator --grade grade_4 --list-topics
        """,
    )

    parser.add_argument(
        "--grade",
        type=str,
        choices=[g.value for g in GradeLevel],
        default="grade_1",
        help="Target grade level (default: grade_1)",
    )

    parser.add_argument(
        "--topic",
        type=str,
        choices=[t.value for t in MathTopic],
        default="addition",
        help="Math topic (default: addition)",
    )

    parser.add_argument(
        "--num-problems",
        type=int,
        default=5,
        help="Number of problems to generate (default: 5)",
    )

    parser.add_argument(
        "--difficulty",
        type=int,
        choices=[1, 2, 3, 4, 5],
        default=1,
        help="Difficulty level 1-5 (default: 1)",
    )

    parser.add_argument(
        "--action",
        type=str,
        choices=["generate", "explain", "worksheet"],
        default="generate",
        help="Action to perform (default: generate)",
    )

    parser.add_argument(
        "--no-hints",
        action="store_true",
        help="Skip generating hints for problems",
    )

    parser.add_argument(
        "--no-review",
        action="store_true",
        help="Skip reviewing problems for quality",
    )

    parser.add_argument(
        "--list-topics",
        action="store_true",
        help="List available topics for the specified grade",
    )

    parser.add_argument(
        "--list-grades",
        action="store_true",
        help="List all available grade levels",
    )

    parser.add_argument(
        "--output",
        type=str,
        help="Output file path (default: stdout)",
    )

    parser.add_argument(
        "--format",
        type=str,
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show verbose output from agents",
    )

    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress all output except results",
    )

    return parser.parse_args()


def list_grades() -> None:
    """Print all available grade levels."""
    print("Available grade levels:")
    print("-" * 30)
    for grade in GradeLevel:
        print(f"  {grade.value}")


def list_topics_for_grade(grade: GradeLevel) -> None:
    """Print available topics for a grade level.

    Args:
        grade: The grade level to list topics for.
    """
    topics = get_topics_for_grade(grade)
    print(f"Available topics for {grade.value}:")
    print("-" * 30)
    for topic in topics:
        concept = create_math_concept(topic, grade)
        print(f"  {topic.value}: {concept.description}")


def format_output(result: dict[str, Any], output_format: str) -> str:
    """Format the result for output.

    Args:
        result: The result dictionary.
        output_format: Either 'text' or 'json'.

    Returns:
        Formatted string output.
    """
    if output_format == "json":
        return json.dumps(result, indent=2)

    # Text format
    lines = []
    lines.append("=" * 60)
    lines.append(f"Grade: {result.get('grade', 'N/A')}")
    lines.append(f"Topic: {result.get('topic', 'N/A')}")
    lines.append("=" * 60)

    if "explanation" in result:
        lines.append("\nConcept Explanation:")
        lines.append("-" * 40)
        lines.append(result["explanation"])

    if "result" in result:
        lines.append("\nGenerated Content:")
        lines.append("-" * 40)
        lines.append(result["result"])

    if "worksheet" in result:
        lines.append("\nWorksheet:")
        lines.append("-" * 40)
        lines.append(result["worksheet"])

    if "tasks_output" in result:
        lines.append("\nDetailed Output:")
        lines.append("-" * 40)
        for i, output in enumerate(result["tasks_output"], 1):
            lines.append(f"\nTask {i} Output:")
            lines.append(output)

    lines.append("\n" + "=" * 60)
    return "\n".join(lines)


def main() -> int:
    """Main entry point for the CLI.

    Returns:
        Exit code (0 for success, non-zero for error).
    """
    args = parse_args()

    # Handle listing options
    if args.list_grades:
        list_grades()
        return 0

    grade = GradeLevel(args.grade)

    if args.list_topics:
        list_topics_for_grade(grade)
        return 0

    # Validate topic for grade
    topic = MathTopic(args.topic)
    valid_topics = get_topics_for_grade(grade)

    if topic not in valid_topics:
        print(f"Error: Topic '{topic.value}' is not available for {grade.value}")
        print("Available topics:")
        list_topics_for_grade(grade)
        return 1

    # Create the crew
    try:
        if not args.quiet:
            print(f"Initializing math problems generator for {grade.value} - {topic.value}...")

        crew = MathProblemsCrew(
            grade=grade,
            topic=topic,
            verbose=args.verbose,
        )

        # Execute the requested action
        if args.action == "generate":
            if not args.quiet:
                print(f"Generating {args.num_problems} problems...")
            result = crew.generate_problems(
                num_problems=args.num_problems,
                difficulty=args.difficulty,
                include_hints=not args.no_hints,
                include_review=not args.no_review,
            )
        elif args.action == "explain":
            if not args.quiet:
                print("Generating concept explanation...")
            result = crew.explain_concept()
        elif args.action == "worksheet":
            if not args.quiet:
                print(f"Generating worksheet with {args.num_problems} problems...")
            result = crew.generate_worksheet(
                num_problems=args.num_problems,
                difficulty=args.difficulty,
            )
        else:
            print(f"Error: Unknown action '{args.action}'")
            return 1

        # Format and output the result
        output = format_output(result, args.format)

        if args.output:
            with open(args.output, "w") as f:
                f.write(output)
            if not args.quiet:
                print(f"Output written to {args.output}")
        else:
            print(output)

        return 0

    except ValueError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        if args.verbose:
            import traceback

            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
