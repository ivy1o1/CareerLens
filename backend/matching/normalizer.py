import re


def normalize_text(text: str) -> str:
    """
    Normalize text for reliable comparison.

    Example:
    "  Python Programming  " -> "python programming"
    """

    text = text.strip().lower()
    text = re.sub(r"\s+", " ", text)

    return text


def normalize_skill(skill: str) -> str:
    """
    Normalize a skill name.

    Example:
    "Python" -> "python"
    " REST APIs " -> "rest apis"
    """

    return normalize_text(skill)