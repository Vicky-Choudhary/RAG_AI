from hashlib import sha256
from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_pages(
    pages: list[dict],
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> list[dict]:
    """Split page records into chunks while preserving document metadata."""

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    chunks = []

    for page in pages:
        texts = splitter.split_text(page["text"])

        for chunk_index, text in enumerate(texts):

            # Create a stable unique ID for the chunk
            chunk_key = (
                f"{page['document_id']}:"
                f"{page['document_version']}:"
                f"{page['page']}:"
                f"{chunk_index}:"
                f"v1"
            )

            chunk_id = sha256(chunk_key.encode()).hexdigest()

            chunks.append({
                # Chunk information
                "chunk_id": chunk_id,
                "chunk_index": chunk_index,
                "text": text,
                "page": page["page"],

                # Document information
                "document_id": page["document_id"],
                "source_uri": page["source_uri"],
                "content_hash": page["content_hash"],
                "document_version": page["document_version"],
                "ingested_at": page["ingested_at"],
            })

    return chunks