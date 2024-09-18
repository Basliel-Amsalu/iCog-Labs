import numpy as np
import json
from sentence_transformers import SentenceTransformer
from transformers import BertTokenizer, BertModel, AutoTokenizer, AutoModelForMaskedLM
import torch
from sklearn.metrics.pairwise import cosine_similarity

# Set device to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load preprocessed SQuAD data
with open("../cleaned_squad_data.json", "r", encoding="utf-8") as file:
    squad_data = json.load(file)


validation_data = squad_data[:5000]

validation_contexts = [item["context"] for item in validation_data]
validation_questions = [item["question"] for item in validation_data]


models = {
    "bert-base-uncased": (
        BertTokenizer.from_pretrained("bert-base-uncased"),
        BertModel.from_pretrained("bert-base-uncased").to(device),
    ),
    "sentence-transformers/sentence-t5-base": SentenceTransformer(
        "sentence-transformers/sentence-t5-base"
    ).to(device),
    "sentence-transformers/all-mpnet-base-v2": SentenceTransformer(
        "sentence-transformers/all-mpnet-base-v2"
    ).to(device),
    "llmrails/ember-v1": SentenceTransformer("llmrails/ember-v1").to(device),
    "thenlper/gte-base": SentenceTransformer("thenlper/gte-base").to(device),
}


# Function to generate embeddings
def generate_sbert_embeddings(model, texts, batch_size=8, prompt_name=None):
    embeddings = []
    for start_idx in range(0, len(texts), batch_size):
        end_idx = min(start_idx + batch_size, len(texts))
        batch_texts = texts[start_idx:end_idx]
        if prompt_name:
            batch_embeddings = model.encode(
                batch_texts,
                convert_to_tensor=True,
                device=device,
                prompt_name=prompt_name,
            )
        else:
            batch_embeddings = model.encode(
                batch_texts, convert_to_tensor=True, device=device
            )
        embeddings.append(batch_embeddings)
    return torch.cat(embeddings).cpu().numpy()


# Function to generate embeddings using BERT, XLM-RoBERTa
def generate_transformer_embeddings(tokenizer, model, texts, batch_size=8):
    embeddings = []
    for start_idx in range(0, len(texts), batch_size):
        end_idx = min(start_idx + batch_size, len(texts))
        batch_texts = texts[start_idx:end_idx]
        inputs = tokenizer(
            batch_texts, padding=True, truncation=True, return_tensors="pt"
        ).to(device)
        with torch.no_grad():
            outputs = model(**inputs)
        embeddings.append(outputs.last_hidden_state.mean(dim=1))
    return torch.cat(embeddings).cpu().numpy()


# Evaluate the models
results = {}
for model_name, model in models.items():
    if (
        "sentence-transformers" in model_name
        or "llmrails" in model_name
        or "thenlper" in model_name
    ):
        print(model_name)
        context_embeddings = generate_sbert_embeddings(model, validation_contexts)
        question_embeddings = generate_sbert_embeddings(model, validation_questions)
    elif "bert" in model_name or "xlm-roberta" in model_name:
        print(model_name)
        tokenizer, model_instance = model
        context_embeddings = generate_transformer_embeddings(
            tokenizer, model_instance, validation_contexts
        )
        question_embeddings = generate_transformer_embeddings(
            tokenizer, model_instance, validation_questions
        )

    def find_most_similar(question_embedding, context_embeddings):
        similarities = cosine_similarity([question_embedding], context_embeddings)
        most_similar_index = np.argmax(similarities)
        return most_similar_index, similarities[0][most_similar_index]

    # Evaluate accuracy
    correct = 0
    reciprocal_ranks = []
    for i, question_embedding in enumerate(question_embeddings):
        most_similar_index, similarity = find_most_similar(
            question_embedding, context_embeddings
        )
        if validation_contexts[most_similar_index] == validation_contexts[i]:
            correct += 1
        rank = (
            1
            + np.where(
                np.argsort(
                    -cosine_similarity([question_embedding], context_embeddings)[0]
                )
                == i
            )[0][0]
        )
        reciprocal_ranks.append(1 / rank)

    accuracy = correct / len(validation_data)
    mrr = np.mean(reciprocal_ranks)
    results[model_name] = {"accuracy": accuracy, "mrr": mrr}
    print(results[model_name])


for model_name, metrics in results.items():
    print(f"Model: {model_name}")
    print(f"Accuracy: {metrics['accuracy'] * 100:.2f}%")
    print(f"Mean Reciprocal Rank (MRR): {metrics['mrr']:.2f}")
    print("-" * 30)
