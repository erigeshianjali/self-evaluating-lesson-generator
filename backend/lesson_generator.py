def generate_lesson(topic: str) -> str:
    """Generate a transparent, rule-based demonstration lesson for the RAG project topic."""
    if "rag" not in topic.lower() and "retrieval-augmented generation" not in topic.lower():
        raise ValueError("This deadline-ready demo currently supports the topic 'Introduction to RAG'.")

    return f"""
Introduction:
This lesson introduces {topic}, often shortened to RAG.

Definition:
Retrieval-Augmented Generation (RAG) is an approach that combines information retrieval with text generation.
A system first retrieves relevant information and then gives that information to a language model as context.

Importance:
RAG can help an AI application answer questions using a selected collection of documents.
This is useful when an application needs to refer to information outside the model's built-in parameters.

How It Works:
1. A user submits a question.
2. The system searches a collection of documents.
3. It retrieves passages that may be relevant to the question.
4. The passages are added to the language model's context.
5. The language model generates an answer using the question and retrieved context.

Example:
A student asks a college chatbot about the attendance policy.
The system searches the college policy documents and retrieves a relevant paragraph.
The language model uses that paragraph as context when preparing its answer.

Advantages:
1. RAG can connect a language model to external documents.
2. The document collection can be updated without retraining the language model.
3. Retrieved passages can help people inspect the information used for an answer.

Limitations:
1. The system may retrieve irrelevant or outdated passages.
2. The language model may misunderstand the retrieved information.
3. RAG does not guarantee that every generated answer is correct.

Conclusion:
RAG combines retrieval and generation so an AI application can use external information.
Its results still depend on the quality of the documents, retrieval process, and generated response.
"""
