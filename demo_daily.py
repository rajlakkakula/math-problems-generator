#!/usr/bin/env python
"""Quick demo of the daily curriculum generator."""

from math_generator.daily_curriculum import DailyCurriculum
from math_generator.math_concepts import GradeLevel


def demo():
    """Run a quick demonstration of the daily curriculum system."""
    print("\n" + "=" * 70)
    print("DAILY MATH CURRICULUM GENERATOR - DEMO")
    print("=" * 70)

    # Demo for Grade 3
    grade = GradeLevel.GRADE_3
    print(f"\nInitializing curriculum for {grade.value}...")

    curriculum = DailyCurriculum(grade=grade, verbose=True)

    # Show current progress
    print("\n" + "-" * 70)
    print("CURRENT PROGRESS")
    print("-" * 70)
    summary = curriculum.get_progress_summary()
    print(f"Grade: {summary['grade']}")
    print(f"Current Topic: {summary['current_topic']}")
    print(f"Topic {summary['current_topic_index'] + 1} of {summary['total_topics']}")
    print(f"Days Completed: {summary['days_completed']}")
    print(f"Progress: {summary['progress_percentage']:.1f}%")

    # Show weekly plan
    print("\n" + "-" * 70)
    print("WEEKLY PLAN (2 days per topic)")
    print("-" * 70)
    plan = curriculum.generate_week_plan(days_per_topic=2)
    for day_plan in plan:
        print(f"Day {day_plan['day']}: {day_plan['topic'].replace('_', ' ').title()}")
        print(f"  Focus: {day_plan['focus']}")

    # Show what would be generated
    print("\n" + "-" * 70)
    print("WHAT WILL BE GENERATED TODAY")
    print("-" * 70)
    current_topic = curriculum.get_current_topic()
    if current_topic:
        print(f"📚 Concept Guide for: {current_topic.value.replace('_', ' ').title()}")
        print(f"📝 Practice Worksheet with 10 problems")
        print(f"💾 Progress will be saved automatically")
        print(f"\nOutput location: output/")

    print("\n" + "=" * 70)
    print("To generate today's content, run:")
    print(f"  python -m math_generator.daily_cli --grade {grade.value}")
    print("\nTo generate for all grades:")
    print("  python -m math_generator.daily_cli --all-grades")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    demo()
