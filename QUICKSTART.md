# Quick Start Guide: Daily Math Curriculum

## What You Get

Each day, the system generates:
1. **📚 Concept Guide PDF** - Detailed explanation of today's math topic
2. **📝 Practice Worksheet PDF** - 10+ problems with hints and answer key

Topics progress sequentially, building on previous concepts.

## Simple Daily Workflow

### Option 1: Single Grade (Recommended for Teachers)

```bash
# Morning: Generate today's materials for your class
source .venv/bin/activate
python -m math_generator.daily_cli --grade grade_3
```

Output:
- `concept_addition_grade_3_20251203.pdf` - Teaching guide
- `daily_problems_addition_grade_3_20251203.pdf` - Student worksheet

### Option 2: All Grades (For Administrators)

```bash
# Generate for all K-5 grades at once
python -m math_generator.daily_cli --all-grades
```

## Check Your Progress

```bash
# See where you are in the curriculum
python -m math_generator.daily_cli --grade grade_3 --status
```

Shows:
- Current topic (e.g., "Addition")
- Days completed
- Progress percentage
- Recent history

## Plan Ahead

```bash
# See what's coming this week
python -m math_generator.daily_cli --grade grade_3 --week-plan
```

Output:
```
Day 1: Addition - Concept Introduction
Day 2: Addition - Practice & Reinforcement
Day 3: Subtraction - Concept Introduction
Day 4: Subtraction - Practice & Reinforcement
Day 5: Multiplication - Concept Introduction
```

## Customize

```bash
# More problems (15 instead of 10)
python -m math_generator.daily_cli --grade grade_4 --num-problems 15

# Only concept guide (skip worksheet)
python -m math_generator.daily_cli --grade grade_2 --no-worksheet

# Only worksheet (skip concept guide)
python -m math_generator.daily_cli --grade grade_5 --no-concept-guide
```

## Reset or Skip

```bash
# Start over from beginning
python -m math_generator.daily_cli --grade grade_1 --reset

# Skip to next topic
python -m math_generator.daily_cli --grade grade_3 --next-topic
```

## Automation (Optional)

### Mac/Linux - Generate Daily at 6 AM

1. Open terminal
2. Run: `crontab -e`
3. Add this line:
```
0 6 * * 1-5 cd /path/to/math-problems-generator && source .venv/bin/activate && python -m math_generator.daily_cli --grade grade_3
```

## Topic Sequences

### Grade 3 Example (11 topics)
1. Addition → 2. Subtraction → 3. Multiplication → 4. Division → 5. Fractions → 6. Geometry → 7. Time → 8. Money → 9. Word Problems → 10. Data & Statistics → 11. Measurement & Data

**See DAILY_CURRICULUM.md for all grade sequences**

## Files Generated

```
output/
├── curriculum_progress_grade_3.json          # Auto-saved progress
├── concept_addition_grade_3_20251203.pdf     # Today's concept guide
└── daily_problems_addition_grade_3_20251203.pdf  # Today's worksheet
```

## Troubleshooting

**"Missing OPENAI_API_KEY"**
- Check `.env` file has: `OPENAI_API_KEY=sk-...`

**"Topic not appropriate for grade"**
- Run: `python -m math_generator.daily_cli --grade grade_3 --reset`

**PDFs not generating**
- Check: `output/` directory exists and is writable
- Run with: `--verbose` flag to see details

## Need Help?

```bash
# See all options
python -m math_generator.daily_cli --help

# Run demo
python demo_daily.py
```

## Complete Documentation

- **DAILY_CURRICULUM.md** - Full documentation
- **README.md** - Project overview
- **PDF_GENERATION.md** - PDF format details

---

**Built for Wake County, NC elementary math standards**
