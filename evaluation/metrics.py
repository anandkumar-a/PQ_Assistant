"""
Evaluation metrics for PQ Assistant.

Contains retrieval and response evaluation metrics used
to measure the performance of the RAG pipeline.
"""

from typing import List


def precision_at_k(
    retrieved_documents: List[str],
    relevant_documents: List[str],
    k: int = 5,
) -> float:
    """
    Calculate Precision@K.

    Precision@K measures the proportion of retrieved documents
    in the top-K results that are relevant.

    Args:
        retrieved_documents: Documents returned by the retriever.
        relevant_documents: Ground-truth relevant documents.
        k: Number of top results to consider.

    Returns:
        Precision@K score between 0.0 and 1.0.
    """

    if k <= 0 or not retrieved_documents:
        return 0.0

    retrieved = retrieved_documents[:k]
    relevant = set(relevant_documents)

    relevant_count = sum(
        1 for document in retrieved if document in relevant
    )

    return relevant_count / len(retrieved)


def recall_at_k(
    retrieved_documents: List[str],
    relevant_documents: List[str],
    k: int = 5,
) -> float:
    """
    Calculate Recall@K.

    Recall@K measures how many of the relevant documents
    were successfully retrieved within the top-K results.

    Args:
        retrieved_documents: Documents returned by the retriever.
        relevant_documents: Ground-truth relevant documents.
        k: Number of top results to consider.

    Returns:
        Recall@K score between 0.0 and 1.0.
    """

    if k <= 0 or not relevant_documents:
        return 0.0

    retrieved = set(retrieved_documents[:k])
    relevant = set(relevant_documents)

    return len(retrieved.intersection(relevant)) / len(relevant)


def reciprocal_rank(
    retrieved_documents: List[str],
    relevant_documents: List[str],
) -> float:
    """
    Calculate Reciprocal Rank.

    Reciprocal Rank is the inverse of the rank position
    of the first relevant document.

    Example:
        First relevant document at rank 1 -> 1.0
        First relevant document at rank 2 -> 0.5
        First relevant document at rank 3 -> 0.333

    Args:
        retrieved_documents: Documents returned by the retriever.
        relevant_documents: Ground-truth relevant documents.

    Returns:
        Reciprocal Rank score between 0.0 and 1.0.
    """

    relevant = set(relevant_documents)

    for rank, document in enumerate(retrieved_documents, start=1):
        if document in relevant:
            return 1.0 / rank

    return 0.0


def mean_reciprocal_rank(
    retrieval_results: List[List[str]],
    relevant_documents: List[List[str]],
) -> float:
    """
    Calculate Mean Reciprocal Rank (MRR).

    MRR is the average reciprocal rank across multiple queries.

    Args:
        retrieval_results: Retrieved documents for each query.
        relevant_documents: Relevant documents for each query.

    Returns:
        MRR score between 0.0 and 1.0.
    """

    if not retrieval_results or not relevant_documents:
        return 0.0

    reciprocal_ranks = []

    for retrieved, relevant in zip(
        retrieval_results,
        relevant_documents,
    ):
        reciprocal_ranks.append(
            reciprocal_rank(retrieved, relevant)
        )

    if not reciprocal_ranks:
        return 0.0

    return sum(reciprocal_ranks) / len(reciprocal_ranks)


def hit_at_k(
    retrieved_documents: List[str],
    relevant_documents: List[str],
    k: int = 5,
) -> float:
    """
    Calculate Hit@K.

    Returns 1.0 if at least one relevant document appears
    within the top-K results; otherwise returns 0.0.

    Args:
        retrieved_documents: Documents returned by the retriever.
        relevant_documents: Ground-truth relevant documents.
        k: Number of top results to consider.

    Returns:
        Hit@K score of 0.0 or 1.0.
    """

    if k <= 0 or not relevant_documents:
        return 0.0

    retrieved = set(retrieved_documents[:k])
    relevant = set(relevant_documents)

    return 1.0 if retrieved.intersection(relevant) else 0.0