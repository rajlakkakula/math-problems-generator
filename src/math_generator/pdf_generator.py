"""PDF generation module for math problems and worksheets."""

import os
from datetime import datetime
from pathlib import Path
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from math_generator.math_concepts import GradeLevel, MathTopic


class MathPDFGenerator:
    """Generate structured PDF documents for math problems and concepts."""

    def __init__(self, output_dir: str = "output"):
        """Initialize the PDF generator.

        Args:
            output_dir: Directory to save generated PDFs.
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self) -> None:
        """Set up custom paragraph styles for the PDF."""
        # Title style
        self.styles.add(
            ParagraphStyle(
                name="CustomTitle",
                parent=self.styles["Title"],
                fontSize=24,
                textColor=colors.HexColor("#2E86AB"),
                spaceAfter=30,
                alignment=1,  # Center
            )
        )

        # Section heading style
        self.styles.add(
            ParagraphStyle(
                name="SectionHeading",
                parent=self.styles["Heading1"],
                fontSize=16,
                textColor=colors.HexColor("#A23B72"),
                spaceAfter=12,
                spaceBefore=12,
            )
        )

        # Problem style
        self.styles.add(
            ParagraphStyle(
                name="Problem",
                parent=self.styles["Normal"],
                fontSize=12,
                spaceAfter=8,
                leftIndent=20,
            )
        )

        # Answer style
        self.styles.add(
            ParagraphStyle(
                name="Answer",
                parent=self.styles["Normal"],
                fontSize=11,
                textColor=colors.HexColor("#18A558"),
                leftIndent=30,
                spaceAfter=6,
            )
        )

        # Hint style
        self.styles.add(
            ParagraphStyle(
                name="Hint",
                parent=self.styles["Normal"],
                fontSize=10,
                textColor=colors.HexColor("#F77F00"),
                leftIndent=30,
                spaceAfter=6,
                fontName="Helvetica-Oblique",
            )
        )

        # Concept style
        self.styles.add(
            ParagraphStyle(
                name="Concept",
                parent=self.styles["Normal"],
                fontSize=11,
                spaceAfter=10,
                leftIndent=15,
            )
        )

    def _get_filename(
        self,
        grade: str,
        topic: str,
        doc_type: str = "problems",
        frequency: str = "daily",
    ) -> str:
        """Generate a filename for the PDF.

        Args:
            grade: Grade level.
            topic: Math topic.
            doc_type: Type of document (problems, worksheet, concepts).
            frequency: Frequency indicator (daily, weekly).

        Returns:
            Filename string.
        """
        timestamp = datetime.now().strftime("%Y%m%d")
        safe_topic = topic.replace(" ", "_").replace("/", "_")
        return f"{grade}_{safe_topic}_{doc_type}_{frequency}_{timestamp}.pdf"

    def generate_problems_pdf(
        self,
        data: dict[str, Any],
        frequency: str = "daily",
        include_answers: bool = True,
        include_hints: bool = True,
    ) -> str:
        """Generate a PDF document for math problems.

        Args:
            data: Dictionary containing problem data from MathProblemsCrew.
            frequency: 'daily' or 'weekly' to indicate the frequency.
            include_answers: Whether to include answer key.
            include_hints: Whether to include hints.

        Returns:
            Path to the generated PDF file.
        """
        grade = data.get("grade", "unknown")
        topic = data.get("topic", "unknown")
        filename = self._get_filename(grade, topic, "problems", frequency)
        filepath = self.output_dir / filename

        # Create PDF document
        doc = SimpleDocTemplate(str(filepath), pagesize=letter)
        story = []

        # Title
        title_text = f"Math Problems - {topic.replace('_', ' ').title()}"
        story.append(Paragraph(title_text, self.styles["CustomTitle"]))

        # Metadata
        metadata = [
            f"<b>Grade:</b> {grade.replace('_', ' ').title()}",
            f"<b>Topic:</b> {topic.replace('_', ' ').title()}",
            f"<b>Date:</b> {datetime.now().strftime('%B %d, %Y')}",
            f"<b>Frequency:</b> {frequency.title()}",
        ]
        for meta in metadata:
            story.append(Paragraph(meta, self.styles["Normal"]))
        story.append(Spacer(1, 0.3 * inch))

        # Add problems section
        story.append(Paragraph("Practice Problems", self.styles["SectionHeading"]))
        story.append(Spacer(1, 0.2 * inch))

        # Get the actual problems from the first task output (problem generation task)
        if "tasks_output" in data and len(data["tasks_output"]) > 0:
            problems_text = data["tasks_output"][0]  # First task is problem generation
        else:
            problems_text = data.get("result", "")
        
        self._add_problems_from_text(story, problems_text)

        # Add hints section if requested
        if include_hints and "tasks_output" in data and len(data["tasks_output"]) >= 3:
            story.append(PageBreak())
            story.append(Paragraph("Hints & Tips", self.styles["SectionHeading"]))
            story.append(Spacer(1, 0.2 * inch))
            # Hints are in the last task output
            hints_text = data["tasks_output"][-1]
            self._add_hints_from_text(story, hints_text)

        # Add answer key if requested
        if include_answers:
            story.append(PageBreak())
            story.append(Paragraph("Answer Key", self.styles["SectionHeading"]))
            story.append(Spacer(1, 0.2 * inch))
            self._add_answers_from_text(story, problems_text)

        # Build PDF
        doc.build(story)
        return str(filepath)

    def generate_worksheet_pdf(
        self,
        data: dict[str, Any],
        frequency: str = "weekly",
    ) -> str:
        """Generate a PDF worksheet with concepts and problems.

        Args:
            data: Dictionary containing worksheet data from MathProblemsCrew.
            frequency: 'daily' or 'weekly' to indicate the frequency.

        Returns:
            Path to the generated PDF file.
        """
        grade = data.get("grade", "unknown")
        topic = data.get("topic", "unknown")
        filename = self._get_filename(grade, topic, "worksheet", frequency)
        filepath = self.output_dir / filename

        # Create PDF document
        doc = SimpleDocTemplate(str(filepath), pagesize=letter)
        story = []

        # Title
        title_text = f"{topic.replace('_', ' ').title()} Worksheet"
        story.append(Paragraph(title_text, self.styles["CustomTitle"]))

        # Student information section
        student_info = Table(
            [
                ["Name: _________________________", "Date: _________________________"],
                ["Grade: _________________________", "Score: _________________________"],
            ],
            colWidths=[3 * inch, 3 * inch],
        )
        student_info.setStyle(
            TableStyle(
                [
                    ("FONTSIZE", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                ]
            )
        )
        story.append(student_info)
        story.append(Spacer(1, 0.3 * inch))

        # Add worksheet content - use the actual worksheet result
        worksheet_text = data.get("worksheet", "")
        if not worksheet_text and "result" in data:
            worksheet_text = data["result"]
        
        self._add_worksheet_content(story, worksheet_text)

        # Build PDF
        doc.build(story)
        return str(filepath)

    def generate_concept_pdf(
        self,
        data: dict[str, Any],
        frequency: str = "weekly",
    ) -> str:
        """Generate a PDF for concept explanation.

        Args:
            data: Dictionary containing concept explanation data.
            frequency: 'daily' or 'weekly' to indicate the frequency.

        Returns:
            Path to the generated PDF file.
        """
        grade = data.get("grade", "unknown")
        topic = data.get("topic", "unknown")
        filename = self._get_filename(grade, topic, "concepts", frequency)
        filepath = self.output_dir / filename

        # Create PDF document
        doc = SimpleDocTemplate(str(filepath), pagesize=letter)
        story = []

        # Title
        title_text = f"Understanding {topic.replace('_', ' ').title()}"
        story.append(Paragraph(title_text, self.styles["CustomTitle"]))

        # Metadata
        metadata = [
            f"<b>Grade Level:</b> {grade.replace('_', ' ').title()}",
            f"<b>Date:</b> {datetime.now().strftime('%B %d, %Y')}",
        ]
        for meta in metadata:
            story.append(Paragraph(meta, self.styles["Normal"]))
        story.append(Spacer(1, 0.3 * inch))

        # Add concept explanation
        explanation = data.get("explanation", "")
        story.append(Paragraph("Concept Explanation", self.styles["SectionHeading"]))
        story.append(Spacer(1, 0.2 * inch))

        # Split explanation into paragraphs
        for para in explanation.split("\n\n"):
            if para.strip():
                story.append(Paragraph(para.strip(), self.styles["Concept"]))
                story.append(Spacer(1, 0.1 * inch))

        # Build PDF
        doc.build(story)
        return str(filepath)

    def _add_problems_from_text(self, story: list, text: str) -> None:
        """Parse and add problems from text to the story.

        Args:
            story: List of reportlab flowables.
            text: Text containing problems.
        """
        if not text:
            story.append(Paragraph("No problems generated.", self.styles["Normal"]))
            return

        # Split into lines and process
        lines = text.split("\n")
        current_problem = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if this is a new problem
            if line.startswith("Problem "):
                # Add previous problem if exists
                if current_problem:
                    problem_text = "\n".join(current_problem)
                    story.append(Paragraph(problem_text, self.styles["Problem"]))
                    story.append(Spacer(1, 0.15 * inch))
                    current_problem = []
                current_problem.append(f"<b>{line}</b>")
            elif line.startswith("Question:"):
                current_problem.append(line)
            elif line.startswith("Answer:"):
                # Don't add answers in the problems section
                pass
            elif line.startswith("Explanation:"):
                # Don't add explanations in the problems section
                pass
            else:
                # Add other lines that are part of the question
                if current_problem and not any(x in line.lower() for x in ['quality', 'verified', 'assessment']):
                    current_problem.append(line)
        
        # Add the last problem
        if current_problem:
            problem_text = "\n".join(current_problem)
            story.append(Paragraph(problem_text, self.styles["Problem"]))
            story.append(Spacer(1, 0.15 * inch))

    def _add_answers_from_text(self, story: list, text: str) -> None:
        """Parse and add answers from text to the story.

        Args:
            story: List of reportlab flowables.
            text: Text containing answers.
        """
        if not text:
            return
            
        lines = text.split("\n")
        current_problem_num = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Track problem numbers
            if line.startswith("Problem "):
                current_problem_num = line
                story.append(Paragraph(f"<b>{line}</b>", self.styles["Answer"]))
            elif line.startswith("Answer:"):
                story.append(Paragraph(line, self.styles["Answer"]))
            elif line.startswith("Explanation:"):
                # Get the full explanation
                story.append(Paragraph(line, self.styles["Answer"]))
            elif current_problem_num and line.startswith("Question:"):
                # Show the question in answer key too
                story.append(Paragraph(line, self.styles["Normal"]))

    def _add_hints_from_text(self, story: list, text: str) -> None:
        """Parse and add hints from text to the story.

        Args:
            story: List of reportlab flowables.
            text: Text containing hints.
        """
        if not text:
            return
            
        lines = text.split("\n")
        current_problem = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Track problem numbers
            if line.startswith("Problem "):
                if current_problem:
                    story.append(Spacer(1, 0.15 * inch))
                current_problem = line
                story.append(Paragraph(f"<b>{line}</b>", self.styles["Hint"]))
            elif line.startswith("Hint"):
                story.append(Paragraph(f"💡 {line}", self.styles["Hint"]))
            elif current_problem and line and not any(x in line.lower() for x in ['quality', 'assessment']):
                # Add continuation of hint text
                story.append(Paragraph(line, self.styles["Hint"]))

    def _add_worksheet_content(self, story: list, text: str) -> None:
        """Parse and add worksheet content to the story.

        Args:
            story: List of reportlab flowables.
            text: Worksheet text.
        """
        sections = text.split("\n\n")
        for section in sections:
            section = section.strip()
            if section:
                # Detect section headers
                if any(
                    keyword in section.lower()
                    for keyword in [
                        "introduction",
                        "review",
                        "problems",
                        "answer key",
                        "challenge",
                    ]
                ):
                    story.append(Paragraph(section, self.styles["SectionHeading"]))
                else:
                    story.append(Paragraph(section, self.styles["Normal"]))
                story.append(Spacer(1, 0.15 * inch))
