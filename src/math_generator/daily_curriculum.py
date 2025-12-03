"""Daily curriculum generator for sequential concept building."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from math_generator.math_concepts import GradeLevel, MathTopic, get_topics_for_grade
from math_generator.math_crew import MathProblemsCrew


class DailyCurriculum:
    """Manages sequential daily curriculum generation for a grade level."""

    def __init__(
        self,
        grade: GradeLevel,
        output_dir: str = "output",
        verbose: bool = False,
    ):
        """Initialize the daily curriculum generator.

        Args:
            grade: The target grade level.
            output_dir: Directory to save generated content and progress.
            verbose: Whether to show verbose output.
        """
        self.grade = grade
        self.output_dir = Path(output_dir)
        self.verbose = verbose
        self.progress_file = self.output_dir / f"curriculum_progress_{grade.value}.json"
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Get ordered topics for the grade level
        self.topics = get_topics_for_grade(grade)
        
        # Load or initialize progress
        self.progress = self._load_progress()

    def _load_progress(self) -> dict[str, Any]:
        """Load curriculum progress from file.

        Returns:
            Progress dictionary with current topic index and completion history.
        """
        if self.progress_file.exists():
            with open(self.progress_file, "r") as f:
                return json.load(f)
        
        # Initialize new progress
        return {
            "grade": self.grade.value,
            "current_topic_index": 0,
            "days_completed": 0,
            "history": [],
            "topics_order": [topic.value for topic in self.topics],
        }

    def _save_progress(self) -> None:
        """Save current progress to file."""
        with open(self.progress_file, "w") as f:
            json.dump(self.progress, f, indent=2)

    def get_current_topic(self) -> MathTopic | None:
        """Get the current topic to work on.

        Returns:
            Current MathTopic or None if all topics completed.
        """
        index = self.progress["current_topic_index"]
        if index >= len(self.topics):
            return None
        return self.topics[index]

    def advance_to_next_topic(self) -> bool:
        """Move to the next topic in the sequence.

        Returns:
            True if advanced, False if already at the end.
        """
        if self.progress["current_topic_index"] < len(self.topics) - 1:
            self.progress["current_topic_index"] += 1
            self._save_progress()
            return True
        return False

    def reset_progress(self) -> None:
        """Reset curriculum progress to the beginning."""
        self.progress["current_topic_index"] = 0
        self.progress["days_completed"] = 0
        self.progress["history"] = []
        self._save_progress()

    def generate_daily_content(
        self,
        num_problems: int = 10,
        generate_concept_guide: bool = True,
        generate_worksheet: bool = True,
    ) -> dict[str, Any]:
        """Generate daily content for the current topic.

        Args:
            num_problems: Number of problems to generate.
            generate_concept_guide: Whether to generate conceptual guide.
            generate_worksheet: Whether to generate practice worksheet.

        Returns:
            Dictionary containing paths to generated content and metadata.
        """
        current_topic = self.get_current_topic()
        
        if current_topic is None:
            return {
                "status": "completed",
                "message": f"All topics for {self.grade.value} have been completed!",
                "total_days": self.progress["days_completed"],
            }

        # Initialize crew for current topic
        crew = MathProblemsCrew(
            grade=self.grade,
            topic=current_topic,
            verbose=self.verbose,
            output_dir=str(self.output_dir),
        )

        results = {
            "status": "success",
            "grade": self.grade.value,
            "topic": current_topic.value,
            "day": self.progress["days_completed"] + 1,
            "topic_sequence": self.progress["current_topic_index"] + 1,
            "total_topics": len(self.topics),
            "date": datetime.now().strftime("%Y-%m-%d"),
        }

        # Generate concept guide (foundational learning)
        if generate_concept_guide:
            if self.verbose:
                print(f"\nGenerating concept guide for {current_topic.value}...")
            
            concept_result = crew.explain_concept(
                generate_pdf=True,
                frequency="daily",
            )
            results["concept_guide"] = {
                "pdf_path": concept_result.get("pdf_path"),
                "description": concept_result.get("description"),
            }

        # Generate practice worksheet
        if generate_worksheet:
            if self.verbose:
                print(f"\nGenerating practice worksheet for {current_topic.value}...")
            
            worksheet_result = crew.generate_worksheet(
                num_problems=num_problems,
                difficulty=self._calculate_difficulty(),
                generate_pdf=True,
                frequency="daily",
            )
            results["worksheet"] = {
                "pdf_path": worksheet_result.get("pdf_path"),
                "num_problems": num_problems,
            }

        # Update progress
        self.progress["days_completed"] += 1
        self.progress["history"].append({
            "day": self.progress["days_completed"],
            "date": results["date"],
            "topic": current_topic.value,
            "topic_index": self.progress["current_topic_index"],
            "concept_guide_path": results.get("concept_guide", {}).get("pdf_path"),
            "worksheet_path": results.get("worksheet", {}).get("pdf_path"),
        })
        self._save_progress()

        return results

    def _calculate_difficulty(self) -> int:
        """Calculate appropriate difficulty based on grade level.

        Returns:
            Difficulty level (1-5).
        """
        difficulty_map = {
            GradeLevel.KINDERGARTEN: 1,
            GradeLevel.GRADE_1: 1,
            GradeLevel.GRADE_2: 2,
            GradeLevel.GRADE_3: 3,
            GradeLevel.GRADE_4: 4,
            GradeLevel.GRADE_5: 5,
        }
        return difficulty_map.get(self.grade, 1)

    def get_progress_summary(self) -> dict[str, Any]:
        """Get a summary of curriculum progress.

        Returns:
            Dictionary with progress statistics and current state.
        """
        current_topic = self.get_current_topic()
        
        return {
            "grade": self.grade.value,
            "total_topics": len(self.topics),
            "current_topic_index": self.progress["current_topic_index"],
            "current_topic": current_topic.value if current_topic else "All completed",
            "days_completed": self.progress["days_completed"],
            "topics_remaining": len(self.topics) - self.progress["current_topic_index"],
            "progress_percentage": (
                self.progress["current_topic_index"] / len(self.topics) * 100
                if len(self.topics) > 0 else 100
            ),
            "recent_history": self.progress["history"][-5:] if self.progress["history"] else [],
        }

    def generate_week_plan(self, days_per_topic: int = 2) -> list[dict[str, Any]]:
        """Generate a weekly plan showing which topics will be covered.

        Args:
            days_per_topic: Number of days to spend on each topic.

        Returns:
            List of daily plans for the week.
        """
        week_plan = []
        current_index = self.progress["current_topic_index"]
        
        for day in range(1, 6):  # 5 school days
            topic_index = current_index + (day - 1) // days_per_topic
            
            if topic_index >= len(self.topics):
                break
                
            topic = self.topics[topic_index]
            day_in_topic = ((day - 1) % days_per_topic) + 1
            
            week_plan.append({
                "day": day,
                "topic": topic.value,
                "topic_index": topic_index + 1,
                "day_in_topic": day_in_topic,
                "total_days_for_topic": days_per_topic,
                "focus": "Concept Introduction" if day_in_topic == 1 else "Practice & Reinforcement",
            })
        
        return week_plan


def generate_daily_for_all_grades(
    output_dir: str = "output",
    grades: list[GradeLevel] | None = None,
    verbose: bool = False,
) -> dict[str, Any]:
    """Generate daily content for multiple grade levels.

    Args:
        output_dir: Directory to save generated content.
        grades: List of grade levels (if None, generates for all).
        verbose: Whether to show verbose output.

    Returns:
        Dictionary with results for each grade.
    """
    if grades is None:
        grades = list(GradeLevel)

    results = {}
    
    for grade in grades:
        if verbose:
            print(f"\n{'=' * 60}")
            print(f"Generating daily content for {grade.value}")
            print(f"{'=' * 60}")
        
        curriculum = DailyCurriculum(grade=grade, output_dir=output_dir, verbose=verbose)
        grade_result = curriculum.generate_daily_content()
        results[grade.value] = grade_result
        
        if verbose:
            print(f"\n✓ Completed {grade.value}")
            if grade_result.get("status") == "success":
                print(f"  - Topic: {grade_result.get('topic')}")
                print(f"  - Day: {grade_result.get('day')}")
                if "concept_guide" in grade_result:
                    print(f"  - Concept Guide: {grade_result['concept_guide'].get('pdf_path')}")
                if "worksheet" in grade_result:
                    print(f"  - Worksheet: {grade_result['worksheet'].get('pdf_path')}")
    
    return results
