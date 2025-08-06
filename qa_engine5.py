# qa_engine5.py

import os
import numpy as np

# Try to import OpenAI, but handle missing API key gracefully
try:
    from openai import OpenAI
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        client = OpenAI(api_key=api_key)
    else:
        print("Warning: OPENAI_API_KEY not set. QA features will be limited.")
        client = None
except Exception as e:
    print(f"Warning: OpenAI import failed: {e}")
    client = None

class QAEngine:
    def __init__(self, sentences_file, embeddings_file):
        self.sentences_file = sentences_file
        self.embeddings_file = embeddings_file
        self.sentences = []
        self.embeddings = None
        self.client = client
        self.load_data()

    def load_data(self):
        try:
            with open(self.sentences_file, 'r', encoding='utf-8') as f:
                self.sentences = [line.strip() for line in f]
            self.embeddings = np.load(self.embeddings_file)
        except FileNotFoundError:
            pass
        except Exception:
            pass
        
    def find_relevant_sentences(self, query, top_k=3):
        if self.embeddings is None or not self.sentences:
            return []

        try:
            results = self.query_embeddings(query, top_k)
            relevant_sentences = [sentence for sentence, _ in results]
            return relevant_sentences
        except Exception as e:
            print(f"Error finding relevant sentences: {e}")
            return []
        
    def query_embeddings(self, query, top_k=10):
        try:
            if not self.client:
                return []
            
            query_embedding = self.client.embeddings.create(
                input=[query],
                model="text-embedding-3-large"
            ).data[0].embedding

            similarities = np.dot(self.embeddings, query_embedding) / (
                np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_embedding)
            )
            top_indices = similarities.argsort()[-top_k:][::-1]
            results = [(self.sentences[idx], similarities[idx]) for idx in top_indices]

            return results[:top_k]
        except Exception as e:
            print(f"Error in query_embeddings: {e}")
            return []
        
    def extract_answer(self, results, num_sentences=1):
        """
        Extract a coherent answer from the most relevant results.
        This version strips out tagging and metadata from sentences.
        """
        combined_answer = ""
        seen_sentences = set()

        for i, (sentence, similarity) in enumerate(results[:num_sentences]):
            # Assuming each sentence is in the format: "filename|tags|sentence_number|content"
            content = sentence.split('|', 3)[-1]  # Get the last part after the 3rd '|'
            content = content.strip()

            if content not in seen_sentences:
                seen_sentences.add(content)
                combined_answer += content + " "

        return combined_answer.strip() if combined_answer else "No valid answer found."

    def get_answer(self, question, num_sentences=7, response_mode="general"):
        results = self.query_embeddings(question)
        if not results:
            return "No relevant results found."

        context = self.extract_answer(results, num_sentences)

        if response_mode == "general":
            return get_general_response(question, context, max_tokens=800)
        elif response_mode == "andy":
            return get_andy_response(question, context, max_tokens=800)
        else:
            return "Invalid response mode. Please choose 'general' or 'andy'."

def get_embedding(text):
    response = client.embeddings.create(
        input=[text],
        model="text-embedding-3-large"
    )
    # Extract the embedding from the response
    return response.data[0].embedding

def get_general_response(query, context, max_tokens=800):
    prompt = f"""
    You are an AI assistant providing detailed information based on the given context. Your responses should be:
    1. Comprehensive and informative
    2. Based on the provided context, with some elaboration where appropriate
    3. Typically 7 sentences long
    4. Structured logically, with a clear flow of information

    Context: {context}

    Question: {query}

    Provide a detailed response:
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful, fact-based AI assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        temperature=0.5
    )

    full_response = response.choices[0].message.content.strip()
    
    # Check if the response is complete (ends with a period)
    while not full_response.endswith('.'):
        # If not complete, make another API call to continue the response
        continuation_prompt = f"Continue the previous response: {full_response}"
        continuation_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful, fact-based AI assistant."},
                {"role": "user", "content": continuation_prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.5
        )
        full_response += " " + continuation_response.choices[0].message.content.strip()

    return full_response

def get_andy_response(query, context, max_tokens=800):
    prompt = f"""
    You are Andy, a fund manager with several decades in the industry with a degree in financial and economics. Your responses should be:
    1. In the first person, expressing personal views confidently
    2. Detailed and insightful, typically 7 sentences long
    3. Based on the provided context, but feel free to extrapolate and provide your own analysis
    4. Don't use phrases like "Based on the information provided" or "The context suggests"
    5. Structured with a clear introduction, main points, and a brief conclusion
    6. This is meant to be a conversation, dont end with "in conclusion","in summary" or any phrase that would unlikey to be spoken

    Your tone should be:
    - Knowledgeable but approachable
    - Slightly informal, as if speaking to a colleague
    - Confident in your analysis and opinions

    Context: {context}

    Question: {query}

    Provide a detailed answer as Andy:
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are Andy, a knowledgeable and confident AI assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7
        )

        full_response = response.choices[0].message.content.strip()

        # Check if the response is complete (ends with a period)
        while not full_response.endswith('.'):
            # If not complete, make another API call to continue the response
            continuation_prompt = f"Continue the previous response as Andy: {full_response}"
            continuation_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are Andy, a knowledgeable and confident AI assistant."},
                    {"role": "user", "content": continuation_prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            full_response += " " + continuation_response.choices[0].message.content.strip()

        # Remove any summarization phrases at the beginning
        summarization_phrases = ["In conclusion,", "To summarize,", "To conclude,", "In summary,"]
        for phrase in summarization_phrases:
            if full_response.lower().startswith(phrase.lower()):
                full_response = full_response[len(phrase):].strip()

        return full_response

    except Exception as e:
        print(f"Error in get_andy_response: {e}")
        return "I'm sorry, I encountered an error while processing your question."

def detect_intent(query):
    query_lower = query.lower()
    andy_keywords = ["andy", "your view", "your opinion", "what do you think", "your thoughts"]
    general_keywords = ["report", "summary", "overview", "details", "information about"]

    if any(keyword in query_lower for keyword in andy_keywords):
        return "andy"
    elif any(keyword in query_lower for keyword in general_keywords):
        return "general"
    else:
        return "general"
