#!/usr/bin/env python
"""Example script demonstrating PDF generation for math problems."""

from math_generator import MathProblemsCrew, GradeLevel, MathTopic

print("=" * 60)
print("Math Problems Generator - PDF Generation Examples")
print("=" * 60)

# Example 1: Daily problems with PDF
print("\n1. Generating daily addition problems for Grade 1...")
crew1 = MathProblemsCrew(
    grade=GradeLevel.GRADE_1,
    topic=MathTopic.ADDITION,
    verbose=False,
    output_dir="output"
)

result1 = crew1.generate_problems(
    num_problems=5,
    difficulty=1,
    include_hints=True,
    include_review=True,
    generate_pdf=True,
    frequency="daily"
)

print(f"✓ PDF generated: {result1.get('pdf_path', 'N/A')}")

# Example 2: Weekly worksheet
print("\n2. Generating weekly multiplication worksheet for Grade 3...")
crew2 = MathProblemsCrew(
    grade=GradeLevel.GRADE_3,
    topic=MathTopic.MULTIPLICATION,
    verbose=False,
    output_dir="output"
)

result2 = crew2.generate_worksheet(
    num_problems=10,
    difficulty=2,
    generate_pdf=True,
    frequency="weekly"
)

print(f"✓ Worksheet PDF generated: {result2.get('pdf_path', 'N/A')}")

# Example 3: Concept explanation
print("\n3. Generating concept explanation for fractions (Grade 4)...")
crew3 = MathProblemsCrew(
    grade=GradeLevel.GRADE_4,
    topic=MathTopic.FRACTIONS,
    verbose=False,
    output_dir="output"
)

result3 = crew3.explain_concept(
    generate_pdf=True,
    frequency="weekly"
)

print(f"✓ Concept PDF generated: {result3.get('pdf_path', 'N/A')}")

print("\n" + "=" * 60)
print("All PDFs generated successfully!")
print("Check the 'output/' directory for the generated files.")
print("=" * 60)
