# Daily Math Curriculum Generator

## Overview

The Daily Math Curriculum Generator creates sequential, building-block learning materials for elementary school students. Each day generates:

1. **Conceptual Guide**: Detailed explanation of the math concept
2. **Practice Worksheet**: Problems with hints and answers

The system automatically tracks progress and presents topics in a logical sequence that builds on previously learned concepts.

## Features

- ✅ Sequential topic progression based on grade-level curriculum
- ✅ Daily concept guides with detailed explanations
- ✅ Practice worksheets with 10+ problems
- ✅ Automatic progress tracking
- ✅ PDF generation for all materials
- ✅ Support for all elementary grades (K-5)
- ✅ Built for Wake County, NC standards

## Quick Start

### Generate Today's Content for a Specific Grade

```bash
# Activate virtual environment
source .venv/bin/activate

# Generate for Grade 3
python -m math_generator.daily_cli --grade grade_3
```

This will:
- Generate a concept guide PDF
- Generate a practice worksheet PDF
- Save progress automatically
- Move to the next topic when appropriate

### Generate for All Grades

```bash
python -m math_generator.daily_cli --all-grades
```

## Usage Examples

### Check Progress

```bash
# View current progress for Grade 2
python -m math_generator.daily_cli --grade grade_2 --status
```

Output shows:
- Current topic
- Days completed
- Progress percentage
- Recent history

### View Weekly Plan

```bash
# See what topics will be covered this week
python -m math_generator.daily_cli --grade grade_4 --week-plan
```

### Custom Number of Problems

```bash
# Generate with 15 problems instead of default 10
python -m math_generator.daily_cli --grade grade_5 --num-problems 15
```

### Reset Progress

```bash
# Start over from the beginning
python -m math_generator.daily_cli --grade grade_1 --reset
```

### Advance to Next Topic

```bash
# Skip current topic and move to next
python -m math_generator.daily_cli --grade grade_3 --next-topic
```

### Generate Only Concept Guide or Worksheet

```bash
# Only concept guide (no worksheet)
python -m math_generator.daily_cli --grade grade_2 --no-worksheet

# Only worksheet (no concept guide)
python -m math_generator.daily_cli --grade grade_2 --no-concept-guide
```

## Topic Sequence by Grade

### Kindergarten
1. Counting
2. Addition
3. Subtraction
4. Patterns
5. Geometry

### Grade 1
1. Counting
2. Addition
3. Subtraction
4. Patterns
5. Geometry
6. Time
7. Measurement and Data
8. Money
9. Ratios

### Grade 2
1. Addition
2. Subtraction
3. Multiplication
4. Geometry
5. Time
6. Money
7. Measurement and Data
8. Word Problems
9. Data and Statistics
10. Patterns
11. Ratios

### Grade 3
1. Addition
2. Subtraction
3. Multiplication
4. Division
5. Fractions
6. Geometry
7. Time
8. Money
9. Word Problems
10. Data and Statistics
11. Measurement and Data

### Grade 4
1. Multiplication
2. Division
3. Fractions
4. Decimals
5. Geometry
6. Measurement and Data
7. Data and Statistics
8. Ratios
9. Word Problems
10. Money

### Grade 5
1. Multiplication
2. Division
3. Fractions
4. Decimals
5. Geometry
6. Measurement and Data
7. Ratios
8. Data and Statistics
9. Word Problems
10. Money

## Output Structure

```
output/
├── curriculum_progress_grade_3.json          # Progress tracking
├── concept_addition_grade_3_20251203.pdf     # Concept guide
├── daily_problems_addition_grade_3_20251203.pdf  # Practice worksheet
└── ...
```

## Progress Tracking

The system maintains a JSON file for each grade level tracking:
- Current topic index
- Total days completed
- Complete history of generated materials
- Topics order

Progress files: `output/curriculum_progress_{grade}.json`

## Python API Usage

```python
from math_generator.daily_curriculum import DailyCurriculum
from math_generator.math_concepts import GradeLevel

# Initialize curriculum for Grade 3
curriculum = DailyCurriculum(
    grade=GradeLevel.GRADE_3,
    output_dir="output",
    verbose=True
)

# Generate today's content
result = curriculum.generate_daily_content(
    num_problems=10,
    generate_concept_guide=True,
    generate_worksheet=True
)

# Check progress
summary = curriculum.get_progress_summary()
print(f"Current topic: {summary['current_topic']}")
print(f"Progress: {summary['progress_percentage']:.1f}%")

# Get weekly plan
plan = curriculum.generate_week_plan(days_per_topic=2)
for day in plan:
    print(f"Day {day['day']}: {day['topic']} - {day['focus']}")
```

## Best Practices

1. **Daily Generation**: Run once per day to build consistent learning habits
2. **Review Progress**: Check `--status` weekly to track advancement
3. **Plan Ahead**: Use `--week-plan` to prepare materials in advance
4. **Customize Problems**: Adjust `--num-problems` based on student needs
5. **Save PDFs**: Archive generated PDFs for future reference

## Automation

### Daily Cron Job (Linux/Mac)

Add to crontab:
```bash
# Generate daily content for Grade 3 at 6 AM
0 6 * * 1-5 cd /path/to/math-problems-generator && source .venv/bin/activate && python -m math_generator.daily_cli --grade grade_3
```

### Batch Script (All Grades)

Create `generate_daily.sh`:
```bash
#!/bin/bash
source .venv/bin/activate
python -m math_generator.daily_cli --all-grades
```

## Troubleshooting

### "Topic not appropriate for grade" Error
- The progress file might be corrupted
- Run `--reset` to reinitialize

### Missing PDFs
- Check `output/` directory permissions
- Ensure `.env` has valid `OPENAI_API_KEY`

### Slow Generation
- Reduce `--num-problems` 
- Use `--no-worksheet` for faster concept-only generation

## Configuration

### Environment Variables

Required in `.env`:
```
OPENAI_API_KEY=sk-...
```

Optional:
```
OPENAI_MODEL_NAME=gpt-4  # Default model
```

## Support

For issues or questions:
1. Check progress files in `output/`
2. Run with `--verbose` for detailed logging
3. Review generated PDFs for quality
4. Reset progress if needed with `--reset`
