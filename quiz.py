import json
from typing import List, Dict, Any
from memory import search_notes
from llm import llm_text


def _extract_json(text: str) -> str:
    """
    Ollama models sometimes add extra text before/after JSON.
    This extracts the first JSON object {...} from the response.
    """
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return ""
    return text[start:end + 1]


def make_quiz(topic: str, n: int = 5) -> List[Dict[str, Any]]:
    notes = search_notes(topic, limit=10)
    notes_text = "\n".join([f"- {x['content']}" for x in notes]) if notes else "(No saved notes found.)"

    prompt = f"""
You are generating a quiz for learning.

Create exactly {n} DIFFERENT multiple-choice questions on: {topic}

Use these notes if helpful:
{notes_text}

Return ONLY JSON (no markdown, no extra text) in this exact schema:
{{
  "quiz": [
    {{
      "question": "string",
      "options": ["option A", "option B", "option C", "option D"],
      "answer_index": 0,
      "explanation": "1-2 lines that directly justify the correct option"
    }}
  ]
}}

Hard rules (must follow):
- Exactly 4 options per question
- DO NOT include "A.", "B.", "C.", "D." inside the option strings
- answer_index must be 0, 1, 2, or 3
- The correct answer MUST match the explanation exactly
- Options must be mutually exclusive (no overlap like "30s" vs "mid-30s")
- No repeated questions
- Mix difficulty: easy / medium / hard

If you include numeric/fact questions:
- Use clear ranges instead of vague decades (example: "20–29", "30–39", "40–49", "50+")
- If you are not confident about an exact fact, ask a conceptual question instead

Quality check (before you output JSON):
- For every question, verify: the explanation supports ONLY the chosen option.
"""

    raw = llm_text(prompt)
    json_text = _extract_json(raw)

    try:
        data = json.loads(json_text)
        quiz = data.get("quiz", [])

        cleaned: List[Dict[str, Any]] = []
        for q in quiz:
            question = str(q.get("question", "")).strip()
            options = q.get("options", [])
            answer_index = q.get("answer_index", None)
            explanation = str(q.get("explanation", "")).strip()

            # Validate core schema
            if not question:
                continue
            if not isinstance(options, list) or len(options) != 4:
                continue
            if not isinstance(answer_index, int) or answer_index not in (0, 1, 2, 3):
                continue

            # Clean options
            options_clean = [str(o).strip() for o in options]

            # Reject if options include A/B/C/D prefixes (we print labels ourselves)
            bad_prefixes = ("A.", "B.", "C.", "D.", "A:", "B:", "C:", "D:")
            if any(opt.startswith(bad_prefixes) for opt in options_clean):
                continue

            cleaned.append({
                "question": question,
                "options": options_clean,
                "answer_index": answer_index,
                "explanation": explanation,
            })

        # If we got good questions, return them
        if cleaned:
            return cleaned

    except Exception:
        pass

    # Fallback: show raw output for debugging in the UI
    return [{
        "question": "Quiz generation failed (non-JSON or invalid schema). Raw model output below:",
        "options": [],
        "answer_index": None,
        "explanation": raw
    }]