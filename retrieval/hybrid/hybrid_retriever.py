"""
Hybrid Retriever Module
-----------------------
Combines dense vector retrieval and sparse BM25 retrieval
using Reciprocal Rank Fusion (RRF).

Hybrid retrieval improves search quality by combining:
- Semantic similarity from dense retrieval
- Exact keyword matching from sparse retrieval
"""

from typing import Any, Dict, List, Optional

from config.logging_config import get_logger
from retrieval.dense.vector_retriever import VectorRetriever
from retrieval.sparse.bm25_retriever import BM25Retriever


logger = get_logger(__name__)


class HybridRetriever:
    """
    Hybrid document retriever.

    Combines results from:
    1. Dense vector retrieval
    2. Sparse BM25 retrieval

    Results are merged using Reciprocal Rank Fusion (RRF).
    """

    def __init__(
        self,
        vector_retriever: VectorRetriever,
        bm25_retriever: BM25Retriever,
        rrf_k: int = 60,
    ) -> None:
        """
        Initialize the HybridRetriever.

        Args:
            vector_retriever: Dense vector retriever instance.
            bm25_retriever: Sparse BM25 retriever instance.
            rrf_k: Constant used in Reciprocal Rank Fusion.
        """

        self.vector_retriever = vector_retriever
        self.bm25_retriever = bm25_retriever
        self.rrf_k = rrf_k

        logger.info(
            "HybridRetriever initialized with RRF constant: %s",
            self.rrf_k,
        )

    @staticmethod
    def _get_document_id(
        document: Dict[str, Any],
        fallback_index: int,
    ) -> str:
        """
        Extract a unique document ID.

        Args:
            document: Retrieved document.
            fallback_index: Index used if no ID is available.

        Returns:
            Unique document identifier.
        """

        document_id = document.get("id")

        if document_id is None:
            document_id = document.get(
                "document_id",
                f"document_{fallback_index}",
            )

        return str(document_id)

    def _reciprocal_rank_fusion(
        self,
        dense_results: List[Dict[str, Any]],
        sparse_results: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Combine dense and sparse results using Reciprocal Rank Fusion.

        RRF score is calculated based on the rank of a document
        in each retrieval result list.

        Args:
            dense_results: Results from dense vector retrieval.
            sparse_results: Results from BM25 retrieval.

        Returns:
            Combined and ranked retrieval results.
        """

        fused_scores: Dict[str, float] = {}
        document_map: Dict[str, Dict[str, Any]] = {}

        result_sets = [
            dense_results,
            sparse_results,
        ]

        for results in result_sets:

            for rank, document in enumerate(
                results,
                start=1,
            ):

                document_id = self._get_document_id(
                    document=document,
                    fallback_index=rank,
                )

                if document_id not in fused_scores:
                    fused_scores[document_id] = 0.0
                    document_map[document_id] = document.copy()

                fused_scores[document_id] += (
                    1 / (self.rrf_k + rank)
                )

        fused_results = []

        for document_id, score in fused_scores.items():

            document = document_map[document_id].copy()

            document["rrf_score"] = score

            fused_results.append(document)

        fused_results.sort(
            key=lambda item: item["rrf_score"],
            reverse=True,
        )

        return fused_results

    def retrieve(
        self,
        query: str,
        query_embedding: List[float],
        top_k: int = 5,
        dense_top_k: Optional[int] = None,
        sparse_top_k: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve documents using hybrid search.

        Args:
            query: Original user query for BM25 retrieval.
            query_embedding: Query embedding for vector retrieval.
            top_k: Final number of fused documents to return.
            dense_top_k: Number of dense results to retrieve.
            sparse_top_k: Number of sparse results to retrieve.

        Returns:
            Top-K fused retrieval results.
        """

        if not query:
            logger.warning(
                "Empty query received for hybrid retrieval."
            )
            return []

        if not query_embedding:
            logger.warning(
                "Empty query embedding received."
            )
            return []

        dense_top_k = dense_top_k or top_k
        sparse_top_k = sparse_top_k or top_k

        try:
            # Dense semantic retrieval
            dense_results = self.vector_retriever.retrieve(
                query_embedding=query_embedding,
                top_k=dense_top_k,
            )

            # Sparse keyword retrieval
            sparse_results = self.bm25_retriever.retrieve(
                query=query,
                top_k=sparse_top_k,
            )

            # Combine results using RRF
            fused_results = self._reciprocal_rank_fusion(
                dense_results=dense_results,
                sparse_results=sparse_results,
            )

            final_results = fused_results[:top_k]

            logger.info(
                "Hybrid retrieval completed. "
                "Dense: %s | Sparse: %s | Final: %s",
                len(dense_results),
                len(sparse_results),
                len(final_results),
            )

            return final_results

        except Exception as error:
            logger.exception(
                "Hybrid retrieval failed: %s",
                error,
            )
            return []