"""Math concepts and topics for elementary school kids."""

from enum import Enum

from pydantic import BaseModel, Field


class GradeLevel(str, Enum):
    """Grade levels for elementary school."""

    KINDERGARTEN = "kindergarten"
    GRADE_1 = "grade_1"
    GRADE_2 = "grade_2"
    GRADE_3 = "grade_3"
    GRADE_4 = "grade_4"
    GRADE_5 = "grade_5"


class MathTopic(str, Enum):
    """Math topics covered in elementary school."""

    COUNTING = "counting"
    ADDITION = "addition"
    SUBTRACTION = "subtraction"
    MULTIPLICATION = "multiplication"
    DIVISION = "division"
    FRACTIONS = "fractions"
    RATIOS = "ratios"
    DECIMALS = "decimals"
    GEOMETRY = "geometry"
    MEASUREMENT_AND_DATA = "measurement_and_data"
    WORD_PROBLEMS = "word_problems"
    PATTERNS = "patterns"
    TIME = "time"
    MONEY = "money"
    NUMBERS_AND_OPERATIONS = "numbers_and_operations"
    DATA_AND_STATISTICS = "data_and_statistics"


class MathConcept(BaseModel):
    """A math concept with its properties."""

    topic: MathTopic = Field(description="The math topic category")
    grade_level: GradeLevel = Field(description="The target grade level")
    description: str = Field(description="Description of the concept")
    examples: list[str] = Field(default_factory=list, description="Example problems")
    difficulty: int = Field(
        default=1, ge=1, le=5, description="Difficulty level from 1 (easiest) to 5 (hardest)"
    )


class MathProblem(BaseModel):
    """A generated math problem."""

    question: str = Field(description="The math problem question")
    answer: str = Field(description="The correct answer")
    topic: MathTopic = Field(description="The math topic")
    grade_level: GradeLevel = Field(description="The target grade level")
    difficulty: int = Field(default=1, ge=1, le=5, description="Difficulty level")
    hints: list[str] = Field(default_factory=list, description="Hints to help solve the problem")
    explanation: str = Field(default="", description="Step-by-step explanation")


class MathProblemsSet(BaseModel):
    """A set of generated math problems."""

    problems: list[MathProblem] = Field(default_factory=list, description="List of math problems")
    topic: MathTopic = Field(description="The math topic for this set")
    grade_level: GradeLevel = Field(description="The target grade level")
    total_problems: int = Field(default=0, description="Total number of problems")


# Grade-appropriate topics mapping
GRADE_TOPICS: dict[GradeLevel, list[MathTopic]] = {
    GradeLevel.KINDERGARTEN: [
        MathTopic.COUNTING,
        MathTopic.ADDITION,
        MathTopic.SUBTRACTION,
        MathTopic.PATTERNS,
        MathTopic.GEOMETRY,
    ],
    GradeLevel.GRADE_1: [
        MathTopic.COUNTING,
        MathTopic.ADDITION,
        MathTopic.SUBTRACTION,
        MathTopic.PATTERNS,
        MathTopic.GEOMETRY,
        MathTopic.TIME,
        MathTopic.MEASUREMENT_AND_DATA,
        MathTopic.MONEY,
        MathTopic.RATIOS
    ],
    GradeLevel.GRADE_2: [
        MathTopic.ADDITION,
        MathTopic.SUBTRACTION,
        MathTopic.MULTIPLICATION,
        MathTopic.GEOMETRY,
        MathTopic.TIME,
        MathTopic.MONEY,
        MathTopic.MEASUREMENT_AND_DATA,
        MathTopic.WORD_PROBLEMS,
        MathTopic.DATA_AND_STATISTICS,
        MathTopic.PATTERNS,
        MathTopic.RATIOS
    ],
    GradeLevel.GRADE_3: [
        MathTopic.ADDITION,
        MathTopic.SUBTRACTION,
        MathTopic.MULTIPLICATION,
        MathTopic.DIVISION,
        MathTopic.FRACTIONS,
        MathTopic.GEOMETRY,
        MathTopic.TIME,
        MathTopic.MONEY,
        MathTopic.WORD_PROBLEMS,
        MathTopic.DATA_AND_STATISTICS,
        MathTopic.MEASUREMENT_AND_DATA,
    ],
    GradeLevel.GRADE_4: [
        MathTopic.MULTIPLICATION,
        MathTopic.DIVISION,
        MathTopic.FRACTIONS,
        MathTopic.DECIMALS,
        MathTopic.GEOMETRY,
        MathTopic.MEASUREMENT_AND_DATA,
        MathTopic.DATA_AND_STATISTICS,
        MathTopic.RATIOS,
        MathTopic.WORD_PROBLEMS,
        MathTopic.MONEY
    ],
    GradeLevel.GRADE_5: [
        MathTopic.MULTIPLICATION,
        MathTopic.DIVISION,
        MathTopic.FRACTIONS,
        MathTopic.DECIMALS,
        MathTopic.GEOMETRY,
        MathTopic.MEASUREMENT_AND_DATA,
        MathTopic.RATIOS,
        MathTopic.DATA_AND_STATISTICS,
        MathTopic.WORD_PROBLEMS,
        MathTopic.MONEY
    ],
}


def get_topics_for_grade(grade: GradeLevel) -> list[MathTopic]:
    """Get the list of appropriate math topics for a given grade level.

    Args:
        grade: The grade level to get topics for.

    Returns:
        List of MathTopic values appropriate for the grade.
    """
    return GRADE_TOPICS.get(grade, [])


def get_concept_description(topic: MathTopic, grade: GradeLevel) -> str:
    """Get a description of a math concept for a specific grade level.

    Args:
        topic: The math topic.
        grade: The target grade level.

    Returns:
        A description of the concept appropriate for the grade level.
    """
    descriptions: dict[MathTopic, dict[GradeLevel, str]] = {
        MathTopic.COUNTING: {
            GradeLevel.KINDERGARTEN: "Count objects from 1 to 20",
            GradeLevel.GRADE_1: "Count objects from 1 to 100 and skip counting by 2s, 5s, and 10s",
        },
        MathTopic.ADDITION: {
            GradeLevel.KINDERGARTEN: "Add numbers within 10",
            GradeLevel.GRADE_1: "Add numbers within 20",
            GradeLevel.GRADE_2: "Add two-digit numbers with regrouping",
            GradeLevel.GRADE_3: "Add three-digit numbers with regrouping",
            GradeLevel.GRADE_4: "Add multi-digit numbers including decimals",
        },
        MathTopic.SUBTRACTION: {
            GradeLevel.KINDERGARTEN: "Subtract numbers within 10",
            GradeLevel.GRADE_1: "Subtract numbers within 20",
            GradeLevel.GRADE_2: "Subtract two-digit numbers with regrouping",
            GradeLevel.GRADE_3: "Subtract three-digit numbers with regrouping",
        },
        MathTopic.MULTIPLICATION: {
            GradeLevel.GRADE_2: "Introduction to multiplication with arrays",
            GradeLevel.GRADE_3: "Multiply single-digit numbers (times tables up to 10)",
            GradeLevel.GRADE_4: "Multiply multi-digit numbers",
            GradeLevel.GRADE_5: "Multiply multi-digit numbers and decimals",
        },
        MathTopic.DIVISION: {
            GradeLevel.GRADE_3: "Introduction to division with simple facts",
            GradeLevel.GRADE_4: "Divide multi-digit numbers by single-digit divisors",
            GradeLevel.GRADE_5: "Divide multi-digit numbers by multi-digit divisors",
        },
        MathTopic.FRACTIONS: {
            GradeLevel.GRADE_3: "Introduction to fractions: halves, thirds, fourths",
            GradeLevel.GRADE_4: "Add and subtract fractions with like denominators",
            GradeLevel.GRADE_5: "Add and subtract fractions with unlike denominators",
        },
        MathTopic.DECIMALS: {
            GradeLevel.GRADE_4: "Introduction to decimals: tenths and hundredths",
            GradeLevel.GRADE_5: "Add, subtract, multiply, and divide decimals",
        },
        MathTopic.GEOMETRY: {
            GradeLevel.KINDERGARTEN: "Identify basic shapes: circle, square, triangle",
            GradeLevel.GRADE_1: "Identify and describe 2D and 3D shapes",
            GradeLevel.GRADE_2: "Identify shapes and their attributes",
            GradeLevel.GRADE_3: "Calculate perimeter of shapes",
            GradeLevel.GRADE_4: "Calculate area and perimeter",
            GradeLevel.GRADE_5: "Calculate volume and surface area",
        },
        MathTopic.MEASUREMENT_AND_DATA: {
            GradeLevel.GRADE_1: "Compare and order objects by length",
            GradeLevel.GRADE_2: "Measure length using standard units",
            GradeLevel.GRADE_4: "Convert between units of measurement",
            GradeLevel.GRADE_5: "Convert between metric and customary units",
        },
        MathTopic.WORD_PROBLEMS: {
            GradeLevel.GRADE_2: "Simple word problems with addition and subtraction",
            GradeLevel.GRADE_3: "Word problems with multiplication and division",
            GradeLevel.GRADE_4: "Multi-step word problems",
            GradeLevel.GRADE_5: "Complex multi-step word problems",
        },
        MathTopic.PATTERNS: {
            GradeLevel.KINDERGARTEN: "Recognize and extend simple patterns (AB, ABC)",
            GradeLevel.GRADE_1: "Create and extend number patterns",
        },
        MathTopic.TIME: {
            GradeLevel.GRADE_1: "Tell time to the hour and half hour",
            GradeLevel.GRADE_2: "Tell time to the nearest 5 minutes",
            GradeLevel.GRADE_3: "Tell time to the nearest minute and calculate elapsed time",
        },
        MathTopic.MONEY: {
            GradeLevel.GRADE_2: "Identify coins and count money",
            GradeLevel.GRADE_3: "Count money and make change",
            GradeLevel.GRADE_4: "Solve word problems involving money and decimals",
            GradeLevel.GRADE_5: "Calculate with money including tax and discounts",
        },
        MathTopic.RATIOS: {
            GradeLevel.GRADE_1: "Introduction to comparing quantities (more, less, equal)",
            GradeLevel.GRADE_2: "Simple comparisons and basic ratios concepts",
            GradeLevel.GRADE_4: "Introduction to ratios and proportional relationships",
            GradeLevel.GRADE_5: "Solve problems involving ratios and rates",
        },
        MathTopic.NUMBERS_AND_OPERATIONS: {
            GradeLevel.KINDERGARTEN: "Understand numbers 0-20 and basic operations",
            GradeLevel.GRADE_1: "Place value and number operations within 100",
            GradeLevel.GRADE_2: "Place value to 1000 and number properties",
            GradeLevel.GRADE_3: "Place value and operations with larger numbers",
            GradeLevel.GRADE_4: "Multi-digit operations and number theory",
            GradeLevel.GRADE_5: "Operations with whole numbers, decimals, and fractions",
        },
        MathTopic.DATA_AND_STATISTICS: {
            GradeLevel.GRADE_2: "Read and interpret simple graphs and charts",
            GradeLevel.GRADE_3: "Create and analyze bar graphs and picture graphs",
            GradeLevel.GRADE_4: "Interpret line plots and solve problems using data",
            GradeLevel.GRADE_5: "Analyze data sets and calculate mean, median, and mode",
        },
    }

    topic_descriptions = descriptions.get(topic, {})
    return topic_descriptions.get(grade, f"{topic.value.replace('_', ' ').title()} concepts")


def create_math_concept(topic: MathTopic, grade: GradeLevel) -> MathConcept:
    """Create a MathConcept instance for a given topic and grade.

    Args:
        topic: The math topic.
        grade: The target grade level.

    Returns:
        A MathConcept instance with appropriate properties.
    """
    # Calculate difficulty based on grade level
    grade_difficulties: dict[GradeLevel, int] = {
        GradeLevel.KINDERGARTEN: 1,
        GradeLevel.GRADE_1: 1,
        GradeLevel.GRADE_2: 2,
        GradeLevel.GRADE_3: 3,
        GradeLevel.GRADE_4: 4,
        GradeLevel.GRADE_5: 5,
    }

    return MathConcept(
        topic=topic,
        grade_level=grade,
        description=get_concept_description(topic, grade),
        difficulty=grade_difficulties.get(grade, 1),
    )
