import langchain
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb
from chromadb.utils import embedding_functions
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import BitsAndBytesConfig
import torch

with open("scraped_content.txt", "r", encoding="utf-8") as f:
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

flattened_chunk = [flattend for chunk in chunks for flattend in chunk]


CHROMA_DATA_PATH = "chroma/"
EMBED_MODEL = "llmrails/ember-v1"
COLLECTION_NAME = "chatbot_chunk"

client = chromadb.PersistentClient(path=CHROMA_DATA_PATH)

embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EMBED_MODEL
)

collection = client.create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_func,
    metadata={"hnsw:space": "cosine"},
)

documents = flattened_chunk
collection.add(
    documents=documents,
    ids=[f"id{i}" for i in range(len(documents))],
)


def retriever(query, collection=collection):
    query_results = collection.query(
        query_texts=[query],
        include=["documents", "distances"],
        n_results=5,
    )

    return query_results["documents"]


quantization_config = BitsAndBytesConfig(
    load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16
)

attn_implementation = "sdpa"  # scaled dot product attention
print(f"Using attention implementation: {attn_implementation}")

model_id = "google/gemma-2b-it"

tokenizer = AutoTokenizer.from_pretrained("google/gemma-2b-it")
llm_model = AutoModelForCausalLM.from_pretrained(
    pretrained_model_name_or_path=model_id,
    torch_dtype=torch.float16,
    quantization_config=quantization_config,
    low_cpu_mem_usage=False,
    attn_implementation=attn_implementation,
)


def prompt_formatter(query: str, context_items) -> str:
    context = "- " + "\n- ".join(
        [item for sublist in context_items for item in sublist]
    )

    base_prompt = """
        Based on the following context items, please answer the query.
        Give yourself room to think by extracting relevant passages from the context before answering the query.
        Don't return the thinking, only return the answer.
        Make sure your answers are as explanatory as possible.
        \nNow use the following context items to answer the user query:
        {context}
        \nRelevant passages: <extract relevant passages from the context here>
        User query: {query}
        Answer:
    """
    base_prompt = base_prompt.format(context=context, query=query)

    dialogue_template = [{"role": "user", "content": base_prompt}]

    prompt = tokenizer.apply_chat_template(
        conversation=dialogue_template, tokenize=False, add_generation_prompt=True
    )

    return prompt


def ask(
    query: str,
    temperature: float = 0.7,
    max_new_tokens: int = 256,
):

    context_items = retriever(query)

    prompt = prompt_formatter(query=query, context_items=context_items)

    input_ids = tokenizer(prompt, return_tensors="pt").to("cuda")

    outputs = llm_model.generate(
        **input_ids,
        temperature=temperature,
        do_sample=True,
        max_new_tokens=max_new_tokens,
    )

    output_text = tokenizer.decode(outputs[0])

    output_text = (
        output_text.replace(prompt, "").replace("<bos>", "").replace("<eos>", "")
    )

    return output_text


query = "atom kinds and types in metta"

print(ask(query=query, temperature=0.2))
