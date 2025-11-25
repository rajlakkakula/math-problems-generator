"""Tests for PDF generator module."""

import os
from pathlib import Path

import pytest

from math_generator.pdf_generator import MathPDFGenerator


class TestMathPDFGenerator:
    """Tests for MathPDFGenerator class."""

    @pytest.fixture
    def pdf_generator(self, tmp_path: Path) -> MathPDFGenerator:
        """Create a PDF generator with temporary output directory.

        Args:
            tmp_path: Pytest temporary path fixture.

        Returns:
            MathPDFGenerator instance.
        """
        return MathPDFGenerator(output_dir=str(tmp_path))

    @pytest.fixture
    def sample_problems_data(self) -> dict:
        """Create sample problem data for testing.

        Returns:
            Sample problem data dictionary.
        """
        return {
            "grade": "grade_1",
            "topic": "addition",
            "num_problems": 3,
            "difficulty": 1,
            "result": """Problem 1:
Question: If you have 2 apples and get 3 more apples, how many apples do you have?
Answer: 5
Explanation: Start with 2, add 3 more: 2 + 3 = 5

Problem 2:
Question: Sarah has 4 crayons. Her friend gives her 2 more. How many crayons does Sarah have now?
Answer: 6
Explanation: 4 + 2 = 6 crayons

Problem 3:
Question: There are 5 birds on a tree. 1 more bird lands on the tree. How many birds are there now?
Answer: 6
Explanation: 5 + 1 = 6 birds""",
            "tasks_output": [
                "Generated 3 problems",
                "Hint 1: Count the starting number first...",
            ],
        }

    @pytest.fixture
    def sample_concept_data(self) -> dict:
        """Create sample concept data for testing.

        Returns:
            Sample concept data dictionary.
        """
        return {
            "grade": "grade_1",
            "topic": "addition",
            "description": "Basic addition with single digits",
            "explanation": """Addition is when we put numbers together to make a bigger number.

When we add, we are combining groups of things. For example, if you have 2 cookies and get 1 more cookie, you now have 3 cookies total.

We use the plus sign (+) to show addition. The equal sign (=) shows what the answer is.

Example: 2 + 1 = 3""",
        }

    @pytest.fixture
    def sample_worksheet_data(self) -> dict:
        """Create sample worksheet data for testing.

        Returns:
            Sample worksheet data dictionary.
        """
        return {
            "grade": "grade_2",
            "topic": "subtraction",
            "num_problems": 5,
            "difficulty": 2,
            "worksheet": """Introduction
Welcome to your subtraction worksheet!

Review
Subtraction means taking away from a number.

Problems
1. 10 - 3 = ?
2. 8 - 5 = ?

Answer Key
1. 7
2. 3""",
        }

    def test_pdf_generator_initialization(self, tmp_path: Path) -> None:
        """Test PDF generator initialization."""
        generator = MathPDFGenerator(output_dir=str(tmp_path))
        assert generator.output_dir == tmp_path
        assert tmp_path.exists()

    def test_generate_problems_pdf(
        self, pdf_generator: MathPDFGenerator, sample_problems_data: dict
    ) -> None:
        """Test generating a problems PDF."""
        pdf_path = pdf_generator.generate_problems_pdf(
            data=sample_problems_data, frequency="daily"
        )

        assert os.path.exists(pdf_path)
        assert pdf_path.endswith(".pdf")
        assert "grade_1" in pdf_path
        assert "addition" in pdf_path
        assert "problems" in pdf_path
        assert "daily" in pdf_path

    def test_generate_problems_pdf_without_hints(
        self, pdf_generator: MathPDFGenerator, sample_problems_data: dict
    ) -> None:
        """Test generating problems PDF without hints."""
        pdf_path = pdf_generator.generate_problems_pdf(
            data=sample_problems_data, frequency="daily", include_hints=False
        )

        assert os.path.exists(pdf_path)

    def test_generate_problems_pdf_without_answers(
        self, pdf_generator: MathPDFGenerator, sample_problems_data: dict
    ) -> None:
        """Test generating problems PDF without answers."""
        pdf_path = pdf_generator.generate_problems_pdf(
            data=sample_problems_data, frequency="daily", include_answers=False
        )

        assert os.path.exists(pdf_path)

    def test_generate_concept_pdf(
        self, pdf_generator: MathPDFGenerator, sample_concept_data: dict
    ) -> None:
        """Test generating a concept explanation PDF."""
        pdf_path = pdf_generator.generate_concept_pdf(
            data=sample_concept_data, frequency="weekly"
        )

        assert os.path.exists(pdf_path)
        assert "concepts" in pdf_path
        assert "weekly" in pdf_path

    def test_generate_worksheet_pdf(
        self, pdf_generator: MathPDFGenerator, sample_worksheet_data: dict
    ) -> None:
        """Test generating a worksheet PDF."""
        pdf_path = pdf_generator.generate_worksheet_pdf(
            data=sample_worksheet_data, frequency="weekly"
        )

        assert os.path.exists(pdf_path)
        assert "worksheet" in pdf_path
        assert "grade_2" in pdf_path
        assert "subtraction" in pdf_path

    def test_filename_generation(self, pdf_generator: MathPDFGenerator) -> None:
        """Test filename generation with various parameters."""
        filename = pdf_generator._get_filename(
            grade="grade_1", topic="addition", doc_type="problems", frequency="daily"
        )

        assert "grade_1" in filename
        assert "addition" in filename
        assert "problems" in filename
        assert "daily" in filename
        assert filename.endswith(".pdf")

    def test_filename_with_special_characters(
        self, pdf_generator: MathPDFGenerator
    ) -> None:
        """Test filename generation with special characters in topic."""
        filename = pdf_generator._get_filename(
            grade="grade_3",
            topic="word problems",
            doc_type="worksheet",
            frequency="weekly",
        )

        assert "word_problems" in filename
        assert "/" not in filename
        assert " " not in filename

    def test_weekly_frequency(
        self, pdf_generator: MathPDFGenerator, sample_problems_data: dict
    ) -> None:
        """Test PDF generation with weekly frequency."""
        pdf_path = pdf_generator.generate_problems_pdf(
            data=sample_problems_data, frequency="weekly"
        )

        assert "weekly" in pdf_path
        assert os.path.exists(pdf_path)

    def test_custom_output_directory(self, tmp_path: Path) -> None:
        """Test PDF generator with custom output directory."""
        custom_dir = tmp_path / "custom_output"
        generator = MathPDFGenerator(output_dir=str(custom_dir))

        assert custom_dir.exists()
        assert generator.output_dir == custom_dir
