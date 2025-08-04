import os
import numpy as np
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DEFAULT_EMBEDDING_MODEL = "text-embedding-3-large"
DEFAULT_CHAT_MODEL = "gpt-4o-mini"

current_embedding_model = DEFAULT_EMBEDDING_MODEL
current_chat_model = DEFAULT_CHAT_MODEL

def get_current_embedding_model():
    return current_embedding_model

def get_current_chat_model():
    return current_chat_model

def set_embedding_model(model):
    global current_embedding_model
    current_embedding_model = model

def set_chat_model(model):
    global current_chat_model
    current_chat_model = model

def load_embeddings(embeddings_path, sentences_path):
    if not os.path.exists(embeddings_path):
        raise FileNotFoundError(f"Embeddings file not found at {embeddings_path}")
    if not os.path.exists(sentences_path):
        raise FileNotFoundError(f"Sentences file not found at {sentences_path}")
    
    embeddings = np.load(embeddings_path)
    with open(sentences_path, 'r', encoding='utf-8') as f:
        sentences = f.readlines()
    sentences = [s.strip() for s in sentences]
    
    if len(embeddings) != len(sentences):
        raise ValueError("Number of embeddings and sentences do not match.")
    
    print(f"Loaded {len(embeddings)} embeddings and {len(sentences)} sentences.")
    return embeddings, sentences

def get_query_embedding(query, model=None):
    if model is None:
        model = current_embedding_model
    try:
        response = client.embeddings.create(input=query, model=model)
        embedding = response.data[0].embedding
        return embedding
    except Exception as e:
        print(f"Error obtaining query embedding: {e}")
        raise e

def find_top_n_similar(query_embedding, embeddings, sentences, top_n=5, min_similarity=0.5):
    query_vec = np.array(query_embedding).reshape(1, -1)
    similarities = np.dot(embeddings, query_vec.T).flatten()
    top_indices = similarities.argsort()[::-1]
    top_similar = [(sentences[i], similarities[i]) for i in top_indices if similarities[i] >= min_similarity]
    return top_similar[:top_n]

def get_answer_without_embeddings(query, max_tokens=150, model=None):
    if model is None:
        model = current_chat_model
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query}
            ],
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating answer: {e}")
        raise e

def get_answer_with_embeddings(query, embeddings, sentences, max_tokens=150, model=None):
    if model is None:
        model = current_chat_model
    try:
        query_embedding = get_query_embedding(query)
        top_similar = find_top_n_similar(query_embedding, embeddings, sentences)
        context = "\n".join([sentence for sentence, _ in top_similar])
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Use the provided context to answer the question."},
                {"role": "user", "content": f"Context: {context}\n\nQuestion: {query}"}
            ],
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating answer with embeddings: {e}")
        raise e

def process_query(query, num_sentences=5, use_embeddings=True, max_tokens=150, return_context=False):
    result = {
        "chat_model": get_current_chat_model(),
        "embedding_model": get_current_embedding_model(),
        "query": query,
        "answer": None,
        "context_sentences": None
    }
    
    if use_embeddings:
        embeddings_path = './openai_large_embeddings/openai_large_combined_embeddings.npy'
        sentences_path = './openai_large_embeddings/openai_large_combined_sentences.txt'
        
        try:
            embeddings, sentences = load_embeddings(embeddings_path, sentences_path)
            query_embedding = get_query_embedding(query)
            top_similar = find_top_n_similar(query_embedding, embeddings, sentences, num_sentences)
            
            context = "\n".join([sentence for sentence, _ in top_similar])
            result["context_sentences"] = [sentence for sentence, _ in top_similar] if return_context else None
            
            response = client.chat.completions.create(
                model=current_chat_model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Use the provided context to answer the question."},
                    {"role": "user", "content": f"Context: {context}\n\nQuestion: {query}"}
                ],
                max_tokens=max_tokens
            )
            result["answer"] = response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error processing query with embeddings: {e}")
            result["error"] = str(e)
    else:
        try:
            response = client.chat.completions.create(
                model=current_chat_model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": query}
                ],
                max_tokens=max_tokens
            )
            result["answer"] = response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error processing query without embeddings: {e}")
            result["error"] = str(e)
    
    return result

def process_query_with_similarity(query, num_sentences=7, min_similarity=0.5, max_tokens=150):
    result = {
        "chat_model": get_current_chat_model(),
        "embedding_model": get_current_embedding_model(),
        "query": query,
        "similar_sentences": None,
        "final_answer": None
    }
    
    embeddings_path = './openai_large_embeddings/openai_large_combined_embeddings.npy'
    sentences_path = './openai_large_embeddings/openai_large_combined_sentences.txt'
    
    try:
        embeddings, sentences = load_embeddings(embeddings_path, sentences_path)
        query_embedding = get_query_embedding(query)
        top_similar = find_top_n_similar(query_embedding, embeddings, sentences, num_sentences, min_similarity)
        
        result["similar_sentences"] = [{"sentence": sentence, "similarity": score} for sentence, score in top_similar]
        
        context = "\n".join([sentence for sentence, _ in top_similar])
        
        response = client.chat.completions.create(
            model=current_chat_model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Rewrite the provided context into a coherent paragraph that answers the question."},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
            ],
            max_tokens=max_tokens
        )
        result["final_answer"] = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error processing query: {e}")
        result["error"] = str(e)
    
    return result