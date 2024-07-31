import langchain
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb
from chromadb.utils import embedding_functions

SCRAPED_CONTENT_PATH = "scraped_content.txt"
CHROMA_DATA_PATH = "chroma/"
EMBED_MODEL = "llmrails/ember-v1"
COLLECTION_NAME = "chatbot_chunk"

def process_content():
    with open(SCRAPED_CONTENT_PATH, "r", encoding="utf-8") as f:
        scraped_content = f.read()

    pages = scraped_content.split("\f")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=10,
        length_function=len,
        is_separator_regex=False,
    )

    chunks = []
    for page in pages:
        content_lines = page.strip().split("\n")
        content_lines = [
            line
            for line in content_lines
            if not line.startswith("URL:") and not line.startswith("=" * 80)
        ]
        content = "\n".join(content_lines)
        split_text = text_splitter.split_text(content)
        chunks.append(split_text)

    return [flattend for chunk in chunks for flattend in chunk]

def setup_collection():
    client = chromadb.PersistentClient(path=CHROMA_DATA_PATH)
    embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBED_MODEL
    )

    if COLLECTION_NAME in client.list_collections():
        collection = client.get_collection(COLLECTION_NAME)
    else:
        collection = client.create_collection(
            name=COLLECTION_NAME,
            embedding_function=embedding_func,
            metadata={"hnsw:space": "cosine"},
        )
        documents = process_content()
        collection.add(
            documents=documents,
            ids=[f"id{i}" for i in range(len(documents))],
        )

    return collection
