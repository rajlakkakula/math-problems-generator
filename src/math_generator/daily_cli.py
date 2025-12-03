"""CLI for daily curriculum generation."""

import argparse
import sys
from typing import Any

from math_generator.math_concepts import GradeLevel
from math_generator.daily_curriculum import DailyCurriculum, generate_daily_for_all_grades


def print_progress_summary(summary: dict[str, Any]) -> None:
    """Print a formatted progress summary.

    Args:
        summary: Progress summary dictionary.
    """
    print("\n" + "=" * 60)
    print(f"CURRICULUM PROGRESS: {summary['grade'].upper()}")
    print("=" * 60)
    print(f"Current Topic: {summary['current_topic']}")
    print(f"Topic {summary['current_topic_index'] + 1} of {summary['total_topics']}")
    print(f"Days Completed: {summary['days_completed']}")
    print(f"Progress: {summary['progress_percentage']:.1f}%")
    print(f"Topics Remaining: {summary['topics_remaining']}")

    if summary['recent_history']:
        print("\nRecent History:")
        print("-" * 60)
        for entry in summary['recent_history']:
            print(f"  Day {entry['day']} ({entry['date']}): {entry['topic']}")
            if entry.get('concept_guide_path'):
                print(f"    ✓ Concept Guide: {entry['concept_guide_path']}")
            if entry.get('worksheet_path'):
                print(f"    ✓ Worksheet: {entry['worksheet_path']}")
    print("=" * 60 + "\n")


def print_week_plan(plan: list[dict[str, Any]]) -> None:
    """Print a formatted week plan.

    Args:
        plan: List of daily plans.
    """
    print("\n" + "=" * 60)
    print("WEEKLY PLAN")
    print("=" * 60)
    for day_plan in plan:
        print(f"\nDay {day_plan['day']}: {day_plan['topic'].replace('_', ' ').title()}")
        print(f"  Topic {day_plan['topic_index']} of sequence")
        print(f"  Day {day_plan['day_in_topic']} of {day_plan['total_days_for_topic']}")
        print(f"  Focus: {day_plan['focus']}")
    print("=" * 60 + "\n")


def print_generation_result(result: dict[str, Any]) -> None:
    """Print formatted generation result.

    Args:
        result: Generation result dictionary.
    """
    if result.get("status") == "completed":
        print("\n" + "=" * 60)
        print(f"🎉 {result['message']}")
        print(f"Total Days Completed: {result['total_days']}")
        print("=" * 60 + "\n")
        return

    print("\n" + "=" * 60)
    print(f"DAILY CONTENT GENERATED: {result['grade'].upper()}")
    print("=" * 60)
    print(f"Date: {result['date']}")
    print(f"Day: {result['day']}")
    print(f"Topic: {result['topic'].replace('_', ' ').title()}")
    print(f"Topic Progress: {result['topic_sequence']} of {result['total_topics']}")

    if "concept_guide" in result:
        print("\n📚 Concept Guide:")
        print(f"  Description: {result['concept_guide'].get('description', 'N/A')}")
        print(f"  PDF: {result['concept_guide'].get('pdf_path', 'Not generated')}")

    if "worksheet" in result:
        print("\n📝 Practice Worksheet:")
        print(f"  Problems: {result['worksheet'].get('num_problems', 'N/A')}")
        print(f"  PDF: {result['worksheet'].get('pdf_path', 'Not generated')}")

    print("=" * 60 + "\n")


def main() -> int:
    """Main entry point for the daily curriculum CLI.

    Returns:
        Exit code (0 for success, non-zero for error).
    """
    parser = argparse.ArgumentParser(
        description="Generate daily math curriculum with sequential concept building",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate today's content for Grade 3
  python -m math_generator.daily_cli --grade grade_3

  # Generate for all grades
  python -m math_generator.daily_cli --all-grades

  # View progress for Grade 2
  python -m math_generator.daily_cli --grade grade_2 --status

  # View weekly plan for Grade 4
  python -m math_generator.daily_cli --grade grade_4 --week-plan

  # Reset progress for Grade 1
  python -m math_generator.daily_cli --grade grade_1 --reset

  # Generate with custom settings
  python -m math_generator.daily_cli --grade grade_5 --num-problems 15
        """,
    )

    parser.add_argument(
        "--grade",
        type=str,
        choices=[g.value for g in GradeLevel],
        help="Target grade level",
    )

    parser.add_argument(
        "--all-grades",
        action="store_true",
        help="Generate for all grade levels",
    )

    parser.add_argument(
        "--num-problems",
        type=int,
        default=10,
        help="Number of problems per worksheet (default: 10)",
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="output",
        help="Directory for output files (default: output)",
    )

    parser.add_argument(
        "--status",
        action="store_true",
        help="Show current progress status",
    )

    parser.add_argument(
        "--week-plan",
        action="store_true",
        help="Show weekly plan",
    )

    parser.add_argument(
        "--reset",
        action="store_true",
        help="Reset curriculum progress to beginning",
    )

    parser.add_argument(
        "--next-topic",
        action="store_true",
        help="Advance to next topic in sequence",
    )

    parser.add_argument(
        "--no-concept-guide",
        action="store_true",
        help="Skip generating concept guide",
    )

    parser.add_argument(
        "--no-worksheet",
        action="store_true",
        help="Skip generating worksheet",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show verbose output",
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.all_grades and not args.grade:
        parser.error("Either --grade or --all-grades must be specified")

    try:
        # Handle all grades generation
        if args.all_grades:
            if args.status or args.week_plan or args.reset or args.next_topic:
                print("Error: Status operations cannot be used with --all-grades")
                return 1

            results = generate_daily_for_all_grades(
                output_dir=args.output_dir,
                verbose=args.verbose,
            )

            print("\n" + "=" * 60)
            print("DAILY CONTENT GENERATED FOR ALL GRADES")
            print("=" * 60)
            for grade_value, result in results.items():
                print(f"\n{grade_value.upper()}:")
                if result.get("status") == "success":
                    print(f"  ✓ Topic: {result.get('topic')}")
                    print(f"  ✓ Day: {result.get('day')}")
                else:
                    print(f"  ℹ {result.get('message', 'No content generated')}")
            print("=" * 60 + "\n")

            return 0

        # Single grade operations
        grade = GradeLevel(args.grade)
        curriculum = DailyCurriculum(
            grade=grade,
            output_dir=args.output_dir,
            verbose=args.verbose,
        )

        # Handle status display
        if args.status:
            summary = curriculum.get_progress_summary()
            print_progress_summary(summary)
            return 0

        # Handle weekly plan
        if args.week_plan:
            plan = curriculum.generate_week_plan()
            print_week_plan(plan)
            return 0

        # Handle reset
        if args.reset:
            curriculum.reset_progress()
            print(f"\n✓ Progress reset for {grade.value}\n")
            summary = curriculum.get_progress_summary()
            print_progress_summary(summary)
            return 0

        # Handle next topic advancement
        if args.next_topic:
            if curriculum.advance_to_next_topic():
                print(f"\n✓ Advanced to next topic for {grade.value}\n")
                summary = curriculum.get_progress_summary()
                print_progress_summary(summary)
            else:
                print(f"\n⚠ Already at the last topic for {grade.value}\n")
            return 0

        # Generate daily content
        result = curriculum.generate_daily_content(
            num_problems=args.num_problems,
            generate_concept_guide=not args.no_concept_guide,
            generate_worksheet=not args.no_worksheet,
        )

        print_generation_result(result)

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
