from rich.console import Console
from rich.table import Table

from memory import init_db, add_note, search_notes
from tracker import set_status, get_latest_progress
from quiz import make_quiz
from llm import llm_text

console = Console()

HELP = """
Commands:
  note: <topic> | <content>           -> save a note
  search: <keyword>                  -> search notes
  quiz: <topic>                      -> generate an AI quiz and test you (A/B/C/D)
  status: <topic> | todo/doing/done  -> track progress
  progress                           -> show latest progress
  ask: <question>                    -> AI tutor mode (ONLY runs when you use ask:)
  help                               -> show commands
  quit                               -> exit

Examples:
  note: Linear Regression | y = wx + b. Trained by minimizing MSE.
  search: regression
  status: Linear Regression | doing
  quiz: Linear Regression
  ask: Explain gradient descent with a tiny numeric example
"""

def show_notes(results):
    if not results:
        console.print("[yellow]No matches found.[/yellow]")
        return

    table = Table(title="Matched Notes")
    table.add_column("Topic", style="bold")
    table.add_column("Created")
    table.add_column("Content", overflow="fold")

    for r in results:
        table.add_row(r["topic"], r["created_at"][:19], r["content"])

    console.print(table)

def show_progress(items):
    if not items:
        console.print("[yellow]No progress updates yet.[/yellow]")
        return

    table = Table(title="Progress (Latest)")
    table.add_column("Topic", style="bold")
    table.add_column("Status")
    table.add_column("Created")

    for x in items:
        table.add_row(x["topic"], x["status"], x["created_at"][:19])

    console.print(table)

def _ask_choice() -> str:
    while True:
        ans = console.input("Your answer (A/B/C/D): ").strip().upper()
        if ans in {"A", "B", "C", "D"}:
            return ans
        console.print("[red]Please enter only A, B, C, or D.[/red]")

def run_interactive_quiz(quiz_items):
    score = 0
    total = len(quiz_items)

    for i, q in enumerate(quiz_items, 1):
        question = q.get("question", "").strip()
        options = q.get("options") or []
        ans_idx = q.get("answer_index")
        explanation = q.get("explanation", "")

        console.print(f"\n[bold]Q{i}:[/bold] {question}")

        if len(options) == 4:
            for idx, opt in enumerate(options):
                # Print A/B/C/D and option text
                console.print(f"   {chr(65 + idx)}. {opt}")
        else:
            console.print("[yellow]This question is not in multiple-choice format.[/yellow]")
            if explanation:
                console.print(f"[cyan]Explanation:[/cyan] {explanation}")
            continue

        user_ans = _ask_choice()

        correct_letter = chr(65 + ans_idx) if isinstance(ans_idx, int) and 0 <= ans_idx <= 3 else None

        if correct_letter and user_ans == correct_letter:
            console.print("[green]Correct![/green]")
            score += 1
        else:
            console.print(f"[red]Incorrect.[/red] Correct answer: {correct_letter}")

        if explanation:
            console.print(f"[cyan]Explanation:[/cyan] {explanation}")

    console.print(f"\n[bold yellow]Final Score: {score}/{total}[/bold yellow]")

def tutor_answer(question: str) -> str:
    related = search_notes(question, limit=5)
    notes_block = "\n".join([f"- ({x['topic']}) {x['content']}" for x in related]) if related else "(No related notes.)"

    prompt = f"""
You are an Education Helper Tutor.

Use the saved notes if they help:
{notes_block}

User question:
{question}

Requirements:
- Explain simply first
- Then explain slightly deeper
- Include 1 small numeric example if applicable
- End with 2 short practice questions
"""
    return llm_text(prompt)

def main():
    init_db()
    console.print("[bold green]Education Helper Agent ready.[/bold green]")
    console.print(HELP)

    while True:
        user = console.input("\n[bold cyan]You:[/bold cyan] ").strip()
        if not user:
            continue

        low = user.lower()

        if low == "quit":
            break

        if low == "help":
            console.print(HELP)
            continue

        if low.startswith("note:"):
            try:
                _, rest = user.split("note:", 1)
                topic, content = rest.split("|", 1)
                console.print(add_note(topic, content))
            except Exception:
                console.print("[red]Format: note: <topic> | <content>[/red]")
            continue

        if low.startswith("search:"):
            q = user.split("search:", 1)[1].strip()
            show_notes(search_notes(q))
            continue

        if low.startswith("quiz:"):
            topic = user.split("quiz:", 1)[1].strip()
            quiz_items = make_quiz(topic, n=5)
            run_interactive_quiz(quiz_items)
            continue

        if low.startswith("status:"):
            try:
                _, rest = user.split("status:", 1)
                topic, status = rest.split("|", 1)
                console.print(set_status(topic, status))
            except Exception:
                console.print("[red]Format: status: <topic> | todo/doing/done[/red]")
            continue

        if low == "progress":
            show_progress(get_latest_progress())
            continue

        if low.startswith("ask:"):
            question = user.split("ask:", 1)[1].strip()
            try:
                console.print(tutor_answer(question))
            except Exception as e:
                console.print(f"[red]Tutor mode error:[/red] {e}")
            continue

        # Anything else: don't call AI (prevents accidental pasted code triggering tutor mode)
        console.print("[yellow]Unknown input.[/yellow] Type [bold]help[/bold] to see commands, or use [bold]ask:[/bold] for tutor mode.")
        continue

if __name__ == "__main__":
    main()