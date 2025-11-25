# Math Problems Generator

This repository consists of codebase that generates math concepts and math problems for kids in elementary school using Python, LLM, CrewAI, AWS Cloud infrastructure.

## Features

- **Grade-Appropriate Content**: Generates math problems tailored for Kindergarten through Grade 5
- **Multiple Math Topics**: Supports counting, addition, subtraction, multiplication, division, fractions, decimals, geometry, measurement, word problems, patterns, time, and money
- **AI-Powered Generation**: Uses CrewAI with OpenAI (GPT-4) for intelligent problem creation
- **Concept Explanations**: Provides age-appropriate explanations of math concepts
- **Worksheet Generation**: Creates complete worksheets with problems, hints, and answer keys
- **AWS Lambda Deployment**: Ready for serverless deployment on AWS

## Installation

### Prerequisites

- Python 3.10 or higher
- OpenAI API key (for LLM features)

### Local Installation

```bash
# Clone the repository
git clone https://github.com/rajlakkakula/math-problems-generator.git
cd math-problems-generator

# Create and activate virtual environment using uv
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies using uv
uv pip install -r requirements.txt

# Install in development mode
uv pip install -e ".[dev]"

# Create .env file and add your OpenAI API key
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Alternative using pip (commented for reference):
# python -m venv venv
# source venv/bin/activate
# pip install -r requirements.txt
# pip install -e ".[dev]"
```

## Usage

### Command Line Interface

```bash
# Generate 5 addition problems for Grade 1 (automatically creates PDF)
math-generator --grade grade_1 --topic addition --num-problems 5

# Generate problems with weekly frequency indicator in PDF filename
math-generator --grade grade_2 --topic subtraction --frequency weekly

# Disable PDF generation (text output only)
math-generator --grade grade_1 --topic addition --no-pdf

# Specify custom output directory for PDFs
math-generator --grade grade_3 --topic multiplication --output-dir my_worksheets

# Explain multiplication concept for Grade 3 (generates concept PDF)
math-generator --grade grade_3 --topic multiplication --action explain

# Generate a complete worksheet (generates formatted worksheet PDF)
math-generator --grade grade_2 --topic subtraction --action worksheet

# List available topics for a grade
math-generator --grade grade_4 --list-topics

# List all grade levels
math-generator --list-grades

# Save text output to file (in addition to PDF)
math-generator --grade grade_1 --topic addition --output problems.txt

# Output in JSON format
math-generator --grade grade_1 --topic addition --format json
```

### Python API

```python
from math_generator import MathProblemsCrew, GradeLevel, MathTopic

# Create a crew for generating problems
crew = MathProblemsCrew(
    grade=GradeLevel.GRADE_2,
    topic=MathTopic.ADDITION,
    verbose=True,
    output_dir="output"  # Directory for PDF files
)

# Generate problems (automatically creates PDF)
result = crew.generate_problems(
    num_problems=5,
    difficulty=2,
    include_hints=True,
    include_review=True,
    generate_pdf=True,  # Default is True
    frequency="daily"   # or "weekly"
)
# Access PDF path: result["pdf_path"]

# Explain a concept (generates concept explanation PDF)
explanation = crew.explain_concept(
    generate_pdf=True,
    frequency="weekly"
)

# Generate a complete worksheet (generates formatted worksheet PDF)
worksheet = crew.generate_worksheet(
    num_problems=10,
    generate_pdf=True,
    frequency="weekly"
)
```

### PDF Output

All generated content is automatically compiled into professional PDF documents with:

- **Structured Format**: Clear sections for concepts, problems, hints, and answers
- **Color-Coded Content**: Different colors for problems, answers, and hints
- **Daily/Weekly Naming**: Files are named with timestamps and frequency indicators
- **Organized Storage**: All PDFs saved to the `output/` directory (customizable)

Example PDF filenames:
- `grade_1_addition_problems_daily_20251125.pdf`
- `grade_3_multiplication_worksheet_weekly_20251125.pdf`
- `grade_2_subtraction_concepts_weekly_20251125.pdf`

### AWS Lambda API

Deploy using AWS SAM:

```bash
# Build the application
sam build

# Deploy to AWS
sam deploy --guided
```

API Endpoints:

- `POST /generate` - Generate math problems
- `POST /explain` - Get concept explanations
- `POST /worksheet` - Generate complete worksheets
- `GET /health` - Health check endpoint

Request body example:
```json
{
    "grade": "grade_2",
    "topic": "multiplication",
    "num_problems": 5,
    "difficulty": 2,
    "action": "generate"
}
```

## Supported Grade Levels

| Grade Level | Value |
|-------------|-------|
| Kindergarten | `kindergarten` |
| Grade 1 | `grade_1` |
| Grade 2 | `grade_2` |
| Grade 3 | `grade_3` |
| Grade 4 | `grade_4` |
| Grade 5 | `grade_5` |

## Math Topics by Grade

| Topic | K | 1 | 2 | 3 | 4 | 5 |
|-------|---|---|---|---|---|---|
| Counting | ✓ | ✓ | | | | |
| Addition | ✓ | ✓ | ✓ | ✓ | | |
| Subtraction | ✓ | ✓ | ✓ | ✓ | | |
| Multiplication | | | ✓ | ✓ | ✓ | ✓ |
| Division | | | | ✓ | ✓ | ✓ |
| Fractions | | | | ✓ | ✓ | ✓ |
| Decimals | | | | | ✓ | ✓ |
| Geometry | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Measurement | | ✓ | ✓ | | ✓ | ✓ |
| Word Problems | | | ✓ | ✓ | ✓ | ✓ |
| Patterns | ✓ | ✓ | | | | |
| Time | | ✓ | ✓ | ✓ | | |
| Money | | | ✓ | ✓ | | |

## Project Structure

```
math-problems-generator/
├── src/
│   └── math_generator/
│       ├── __init__.py         # Package initialization
│       ├── math_concepts.py    # Math concepts and data models
│       ├── math_agents.py      # CrewAI agent definitions
│       ├── math_tasks.py       # CrewAI task definitions
│       ├── math_crew.py        # Crew orchestration
│       ├── aws_lambda.py       # AWS Lambda handler
│       └── main.py             # CLI entry point
├── tests/
│   ├── test_math_concepts.py   # Tests for math concepts
│   ├── test_math_agents.py     # Tests for agents
│   ├── test_math_tasks.py      # Tests for tasks
│   ├── test_math_crew.py       # Tests for crew
│   └── test_aws_lambda.py      # Tests for Lambda handler
├── template.yaml               # AWS SAM template
├── samconfig.toml              # SAM configuration
├── pyproject.toml              # Project configuration
├── requirements.txt            # Python dependencies
├── LICENSE                     # MIT License
└── README.md                   # This file
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=math_generator

# Run specific test file
pytest tests/test_math_concepts.py
```

### Linting

```bash
# Run ruff linter
ruff check src tests

# Auto-fix issues
ruff check --fix src tests

# Format code
ruff format src tests
```

### Type Checking

```bash
mypy src
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AWS_REGION` | AWS region for Bedrock | `us-east-1` |
| `BEDROCK_MODEL_ID` | Claude model ID | `anthropic.claude-3-5-sonnet-20241022-v2:0` |

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Prithviraj Lakkakula, Ph.D.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
