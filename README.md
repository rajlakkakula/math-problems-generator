# Math Problems Generator

This repository consists of codebase that generates math concepts and math problems for kids in elementary school using Python, LLM, CrewAI, AWS Cloud infrastructure.

## Features

- **Grade-Appropriate Content**: Generates math problems tailored for Kindergarten through Grade 5
- **Multiple Math Topics**: Supports counting, addition, subtraction, multiplication, division, fractions, decimals, geometry, measurement, word problems, patterns, time, and money
- **AI-Powered Generation**: Uses CrewAI with AWS Bedrock (Claude) for intelligent problem creation
- **Concept Explanations**: Provides age-appropriate explanations of math concepts
- **Worksheet Generation**: Creates complete worksheets with problems, hints, and answer keys
- **AWS Lambda Deployment**: Ready for serverless deployment on AWS

## Installation

### Prerequisites

- Python 3.10 or higher
- AWS account with Bedrock access (for LLM features)
- AWS CLI configured with appropriate credentials

### Local Installation

```bash
# Clone the repository
git clone https://github.com/rajlakkakula/math-problems-generator.git
cd math-problems-generator

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e ".[dev]"
```

## Usage

### Command Line Interface

```bash
# Generate 5 addition problems for Grade 1
math-generator --grade grade_1 --topic addition --num-problems 5

# Explain multiplication concept for Grade 3
math-generator --grade grade_3 --topic multiplication --action explain

# Generate a complete worksheet
math-generator --grade grade_2 --topic subtraction --action worksheet

# List available topics for a grade
math-generator --grade grade_4 --list-topics

# List all grade levels
math-generator --list-grades

# Save output to file
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
    verbose=True
)

# Generate problems
result = crew.generate_problems(
    num_problems=5,
    difficulty=2,
    include_hints=True,
    include_review=True
)

# Explain a concept
explanation = crew.explain_concept()

# Generate a complete worksheet
worksheet = crew.generate_worksheet(num_problems=10)
```

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
