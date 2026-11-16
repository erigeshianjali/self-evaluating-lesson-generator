def improve_lesson(lesson, failed_criteria):
    """Add predefined RAG-specific material for the project demonstration."""
    improved = lesson

    additions = {
        "teaches_by_example": """
Example:
A student asks a college chatbot about the attendance policy.
The system searches the college policy document and retrieves the relevant paragraph.
The language model uses that paragraph to prepare an answer for the student.
""",
        "covers_key_points": """
Importance:
RAG allows an AI application to use information from external documents.
This is useful when answers need to refer to a particular collection of information.

How It Works:
1. A user asks a question.
2. The system searches its available documents.
3. It retrieves text that may be relevant.
4. The retrieved text is supplied as context to a language model.
5. The language model generates a response using that context.

Advantages:
1. It can use information from external documents.
2. The document collection can be updated separately from the language model.
3. Retrieved passages can help reviewers trace where an answer came from.

Limitations:
1. Retrieval can return irrelevant passages.
2. Old or incorrect documents can lead to poor answers.
3. A language model can still misunderstand the retrieved context or generate errors.
""",
        "no_unexplained_jargon": """
Retriever:
A retriever is a component that searches a collection of information and returns relevant items.
""",
        "coherent_flow": """
Introduction:
This lesson introduces Retrieval-Augmented Generation and explains its main steps.
""",
    }

    for criterion, content in additions.items():
        if criterion in failed_criteria:
            marker = content.strip().splitlines()[0]
            if marker.lower() not in improved.lower():
                improved += "\n" + content

    if "accuracy_and_grounding" in failed_criteria and "Accuracy Verification Required:" not in improved:
        improved += """
Accuracy Verification Required:
A human reviewer must compare factual claims with trusted source material.
Do not treat keyword overlap as proof of factual correctness.
"""
    return improved
