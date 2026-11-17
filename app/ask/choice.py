import re

from app.ask.schemas import AskCandidate


def parse_choice(query: str, candidates: list[AskCandidate]) -> AskCandidate | None:
    text = query.strip()
    lowered = text.lower()

    if re.fullmatch(r"\d+", text):
        index = int(text)
        for candidate in candidates:
            if candidate.index == index:
                return candidate
        return None

    for candidate in candidates:
        if lowered == candidate.tool.lower():
            return candidate

    return None
