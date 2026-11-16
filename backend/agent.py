from evaluator import evaluate_lesson
from memory import create_table, save_evaluation
from learning import update_learning_hints, get_learning_hints
from improver import improve_lesson

def run_agent(initial_lesson, topic="Introduction to RAG", accuracy_status="PENDING", max_retries=2):
    """Run one initial evaluation and up to max_retries improvement attempts."""
    attempt = 1
    lesson = initial_lesson
    rejection_log = []
    create_table()

    while attempt <= max_retries + 1:
        results = evaluate_lesson(lesson, accuracy_status=accuracy_status)
        failed = [name for name, result in results.items() if result["status"] != "PASS"]

        if not failed:
            return {
                "status": "APPROVED",
                "attempts": attempt,
                "results": results,
                "rejection_log": rejection_log,
                "final_lesson": lesson,
            }

        rejection_log.append({"attempt": attempt, "failures": failed})
        final_status = "REJECTED" if attempt == max_retries + 1 else "NEEDS_IMPROVEMENT"
        save_evaluation(
            topic=topic,
            attempt=attempt,
            failed_criteria=", ".join(failed),
            feedback="Lesson needs improvement. See criterion feedback.",
            final_status=final_status,
        )

        update_learning_hints()
        hints = get_learning_hints()

        if attempt == max_retries + 1:
            return {
                "status": "REJECTED",
                "attempts": attempt,
                "failed_criteria": failed,
                "results": results,
                "rejection_log": rejection_log,
                "final_lesson": lesson,
                "learning_hints": hints,
            }

        lesson = improve_lesson(lesson, failed)
        attempt += 1
