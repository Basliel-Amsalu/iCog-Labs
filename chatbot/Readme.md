# Metta Chat-bot

## Description
This project id a chat-bot project that is made to assist with metta programming language and is made by using a rag system and scrapped content from the metta documentation website.

## Results of embedding performance
Based on the evaluation of :
- `bert-base-uncased`
- `sentence-t5-base`
- `all-mpnet-base-v2`
- `llmrails/ember-v1`
- `thenlper/gte-base`

`llmrails/ember-v1` performed best when tested using cosine similarity so this model was chosen for embedding

## Data chunking
The data is chunked using the recursive text splitter method from langchain.
### To install langchain

    - pip install langchain

## vector database
The vector database used is `chromadb`
### To install chromadb

     - pip install chromadb

## LLM Model
The LLM model used is `gemma-2b`. This model is used to generate response for the query.
### To use gemma-2b
- First login to huggingface.com and gain access to gemma-2b by accepting conditions
- Then login to the huggingface cli using your API key from huggingface
- Then install the following
    
         - pip install transformers
         - pip install torch
## File structure
- `preprocess.ipynb` - preprocessing test data for embedding model evaluation
- `embedding_models/evaluate.py` - evaluation of five different embedding models for their performance using test data
- `scrapping.py` - where the metta documentation site is scrapped for content
- `data_processing.py` - where the data that is scrapped is chunked embedded and stored into vector database
- `chatbot.py` - main file for the chatbot



## Usage

1. Clone the repository.
2. `cd chatbot`.
3. `python chatbot.py`


