"""
Response Generator Agent
------------------------

Generates grounded responses for the PQ Assistant using
the user query and retrieved knowledge base documents.
"""

import logging
from typing import Any, Dict, List, Optional


logger = logging.getLogger(__name__)


class ResponseGeneratorAgent:
    """
    Agent responsible for generating grounded answers from
    retrieved documents.
    """

    def __init__(
        self,
        llm=None,
        max_context_documents: int = 5,
    ):
        """
        Initialize the Response Generator Agent.

        Args:
            llm:
                Configured LLM instance.
            max_context_documents:
                Maximum number of retrieved documents to use
                when building the context.
        """

        self.llm = llm
        self.max_context_documents = max_context_documents

    def build_context(
        self,
        retrieved_documents: List[Dict[str, Any]],
    ) -> str:
        """
        Convert retrieved documents into a structured context
        for the LLM.

        Args:
            retrieved_documents:
                List of documents returned by the Retrieval Agent.

        Returns:
            Formatted context string.
        """

        if not retrieved_documents:
            return "No relevant documents were retrieved."

        context_parts = []

        for index, document in enumerate(
            retrieved_documents[:self.max_context_documents],
            start=1,
        ):
            content = (
                document.get("content")
                or document.get("text")
                or document.get("document")
                or ""
            )

            metadata = document.get(
                "metadata",
                {},
            )

            source = metadata.get(
                "source",
                f"Document {index}",
            )

            context_parts.append(
                f"""
[Document {index}]
Source: {source}

Content:
{content}
"""
            )

        return "\n".join(context_parts)

    def build_prompt(
        self,
        query: str,
        context: str,
        intent: Optional[str] = None,
    ) -> str:
        """
        Build the RAG prompt for response generation.

        Args:
            query:
                Original user query.
            context:
                Relevant retrieved knowledge.
            intent:
                Detected user intent.

        Returns:
            Formatted prompt.
        """

        return f"""
You are an intelligent Product Query Assistant for an
industrial enterprise.

Your responsibility is to answer user questions accurately
using ONLY the information provided in the retrieved context.

Rules:
1. Do not invent information.
2. Do not provide unsupported technical instructions.
3. If the context does not contain enough information,
   clearly say that the information is not available.
4. Use fault codes, part numbers, and technical details
   exactly as they appear in the context.
5. Provide a clear and structured response.
6. If troubleshooting steps are available, present them
   step by step.

User Intent:
{intent or "general_query"}

User Query:
{query}

Retrieved Context:
{context}

Generate a helpful, accurate, and concise answer.
"""

    def generate(
        self,
        query: str,
        retrieved_documents: List[Dict[str, Any]],
        intent: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Generate a response using the configured LLM.

        Args:
            query:
                Original user query.
            retrieved_documents:
                Documents retrieved from the knowledge base.
            intent:
                Intent detected by the Query Understanding Agent.

        Returns:
            Dictionary containing generated response details.
        """

        if self.llm is None:
            raise ValueError(
                "LLM has not been initialized."
            )

        context = self.build_context(
            retrieved_documents
        )

        prompt = self.build_prompt(
            query=query,
            context=context,
            intent=intent,
        )

        logger.info(
            "Generating response for query: %s",
            query,
        )

        try:
            response = self.llm.invoke(prompt)

            if hasattr(response, "content"):
                answer = response.content
            else:
                answer = str(response)

            logger.info(
                "Response generated successfully."
            )

            return {
                "query": query,
                "intent": intent,
                "answer": answer,
                "context": context,
                "documents_used": len(
                    retrieved_documents[
                        :self.max_context_documents
                    ]
                ),
            }

        except Exception as error:

            logger.exception(
                "Response generation failed."
            )

            raise RuntimeError(
                f"Response generation failed: {str(error)}"
            ) from error

    def process(
        self,
        query_data: Dict[str, Any],
        retrieval_result: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Execute the complete response generation process.

        Args:
            query_data:
                Output from QueryUnderstandingAgent.
            retrieval_result:
                Output from RetrievalAgent.

        Returns:
            Generated response information.
        """

        query = query_data.get(
            "original_query",
            "",
        )

        intent = query_data.get(
            "intent",
            "general_query",
        )

        retrieved_documents = retrieval_result.get(
            "retrieved_documents",
            [],
        )

        return self.generate(
            query=query,
            retrieved_documents=retrieved_documents,
            intent=intent,
        )