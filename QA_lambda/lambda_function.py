import torch
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
import requests
import logging
import warnings

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Ensure PyTorch uses only CPU
torch.set_num_threads(1)

# Initialize MongoDB
mongo_uri = os.getenv("MONGO_URI", "mongodb+srv://katipellypriyareddy123:teFyIZ97MLT5JKDN@estimator.w973e.mongodb.net/")
mongo_client = MongoClient(mongo_uri)
db = mongo_client['VAS']
collection = db['documents']

# Initialize Groq Client
groq_api_key = os.getenv("GROQ_API_KEY", "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")
client = None
if groq_api_key:
    from groq import Groq
    client = Groq(api_key=groq_api_key)

# Function to get embeddings
def get_embeddings(input_text):
    api_url = os.getenv("EMBEDDING_API_URL", "https://estimatortool.cognitiveservices.azure.com/openai/deployments/text-embedding-3-large/embeddings?api-version=2023-05-15")
    api_key = os.getenv("EMBEDDING_API_KEY", "E6RgCV8d17exZ3BAcNTLQ5EjbXwQycUkx3ViqKmYxgCVIDCZhJizJQQJ99ALACYeBjFXJ3w3AAAAACOGeHh7")

    headers = {"api-key": api_key, "Content-Type": "application/json"}
    payload = {"input": input_text, "model": "text-embedding-3-large"}

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        if "data" in data and len(data["data"]) > 0:
            return data["data"][0]["embedding"]
        else:
            raise ValueError("No embedding data found in the response.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch embeddings: {e}")
        return None

# Main Lambda handler


# Refine text with LLaMA
def refine_text_with_llama(raw_text):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": f"Refine this text:\n{raw_text}"}],
            temperature=0.7,
            max_tokens=1024,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error refining text: {e}")
        return None

# Generate an answer with LLaMA
def generate_answer_with_llama(question, context):
    try:
        prompt = f"Context:\n{context}\n\nQuestion:\n{question}\n\nAnswer fully:"
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=512,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error generating answer: {e}")
        return None

def lambda_handler(event, context):
    try:
        body = event
        question = body.get("question")
        role = body.get("role")

        if not question or not role:
            return {"statusCode": 400, "body": {"error": "Question and role are required"}}

        # Generate embedding
        question_embedding = torch.tensor(get_embeddings(question))
        if question_embedding is None:
            return {"statusCode": 500, "body": {"error": "Failed to generate question embedding"}}

        # Fetch related documents
        related_documents = list(collection.find({"roles": role}))
        if not related_documents:
            return {"statusCode": 404, "body": {"error": "No documents found for the specified role"}}

        # Find the most similar document
        max_similarity = -1
        best_document = None

        for doc in related_documents:
            try:
                doc_embedding = torch.tensor(doc["embedding"])
                similarity = torch.nn.functional.cosine_similarity(question_embedding, doc_embedding, dim=0).item()
                if similarity > max_similarity:
                    max_similarity = similarity
                    best_document = doc
            except Exception as e:
                logger.warning(f"Skipping document due to error: {e}")

        if best_document:
            refined_text = refine_text_with_llama(best_document["content"])
            answer = generate_answer_with_llama(question, refined_text)
            return {
                "statusCode": 200,
                "body": {"question": question, "answer": answer, "source_file": best_document["url"]}
            }

        return {"statusCode": 404, "body": {"error": "No relevant document found"}}

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {"statusCode": 500, "body": {"error": str(e)}}