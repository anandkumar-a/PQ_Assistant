"""
End-to-end document ingestion pipeline.

Workflow:
    Document -> Extract -> Clean -> Metadata -> Chunk

This module orchestrates the complete ingestion process and returns
structured data ready for embedding generation.
"""

from pathlib import Path
from typing import Dict, Any, List

from ingestion.extractors.document_loader import DocumentLoader
from ingestion.cleaners.document_cleaner import DocumentCleaner
from ingestion.metadata.metadata_extractor import MetadataExtractor
from ingestion.chunkers.recursive_chunker import RecursiveChunker


class IngestionPipeline:
    """
    End-to-end ingestion pipeline.
    """

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 100,
    ):
        """
        Initialize the ingestion pipeline.

        Args:
            chunk_size: Maximum characters per chunk.
            chunk_overlap: Overlap between chunks.
        """

        self.loader = DocumentLoader()
        self.cleaner = DocumentCleaner()
        self.metadata_extractor = MetadataExtractor()
        self.chunker = RecursiveChunker(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def process(self, file_path: str) -> Dict[str, Any]:
        """
        Process a document from start to finish.

        Args:
            file_path: Path to the input document.

        Returns:
            Dictionary containing processed document information.
        """

        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # ---------------------------------------------------------
        # Load & Extract
        # ---------------------------------------------------------
        document = self.loader.load(str(file_path))

        # ---------------------------------------------------------
        # Clean
        # ---------------------------------------------------------
        cleaned_text = self.cleaner.clean(document.content)

        # ---------------------------------------------------------
        # Metadata
        # ---------------------------------------------------------
        metadata = self.metadata_extractor.extract(
            document=document,
            file_path=str(file_path),
        )

        # ---------------------------------------------------------
        # Chunk
        # ---------------------------------------------------------
        chunks = self.chunker.chunk(cleaned_text)

        chunk_objects: List[Dict[str, Any]] = []

        for index, chunk in enumerate(chunks):
            chunk_objects.append(
                {
                    "chunk_id": index,
                    "text": chunk,
                    "metadata": metadata,
                }
            )

        return {
            "file_name": file_path.name,
            "file_path": str(file_path),
            "metadata": metadata,
            "cleaned_text": cleaned_text,
            "num_chunks": len(chunk_objects),
            "chunks": chunk_objects,
        }


if __name__ == "__main__":
    pipeline = IngestionPipeline()

    result = pipeline.process("sample.pdf")

    print("=" * 60)
    print("Document Processed Successfully")
    print("=" * 60)
    print(f"File       : {result['file_name']}")
    print(f"Chunks     : {result['num_chunks']}")
    print(f"Metadata   : {result['metadata']}")
