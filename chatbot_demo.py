# chatbot_demo.py

import streamlit as st
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import logging
import requests
import time

# Try to import OpenAI with proper error handling
try:
    from openai import OpenAI
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        openai_client = OpenAI(api_key=api_key)
    else:
        openai_client = None
except Exception:
    openai_client = None

class ChatbotAndy:
    def __init__(self, response_mode='auto', docs_service=None, drive_service=None, response_length=200, language="English", tone="Professional", style="The Economist"):
        self.docs_service = docs_service
        self.drive_service = drive_service
        self.response_mode = response_mode.lower()
        self.response_length = response_length
        self.language = language
        self.tone = tone
        self.style = style
        self.client = openai_client
        self.conversation_history = []
        self.greeting_keywords = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]
        self.initial_greeting = self.get_greeting_response()
        self.embeddings, self.sentences = self.load_embeddings()

    def load_embeddings(self):
        embeddings_file = './openai_large_embeddings/openai_large_combined_embeddings.npy'
        sentences_file = './openai_large_embeddings/openai_large_combined_sentences.txt'
        
        if not os.path.exists(embeddings_file) or not os.path.exists(sentences_file):
            st.error(f"Embeddings files not found: {embeddings_file}, {sentences_file}")
            return None, []

        try:
            embeddings = np.load(embeddings_file)
            with open(sentences_file, 'r', encoding='utf-8') as f:
                sentences = [line.strip() for line in f]
            return embeddings, sentences
        except Exception as e:
            st.error(f"Error loading embeddings: {e}")
            return None, []

    def get_relevant_context(self, query, num_sentences=5):
        if not self.client:
            return []
        query_embedding = self.client.embeddings.create(input=[query], model="text-embedding-3-large").data[0].embedding
        similarities = cosine_similarity([query_embedding], self.embeddings)[0]
        most_similar = np.argsort(similarities)[-num_sentences:]
        context = " ".join([self.sentences[i] for i in most_similar])
        return context

    def generate_response(self, user_input):
        try:
            context = self.get_relevant_context(user_input)
            intent = detect_intent(user_input)
            
            if intent == "andy":
                response = self.get_andy_response_stream(user_input, context)
            else:
                response = self.get_general_response_stream(user_input, context)
            
            for chunk in response:
                if hasattr(chunk.choices[0].delta, 'content'):
                    yield chunk.choices[0].delta.content or ""
        except Exception as e:
            logging.error(f"Error in generate_response: {str(e)}")
            yield f"I apologize, but I encountered an error while processing your request. Error: {str(e)}"

    def get_general_response_stream(self, query, context):
        prompt = f"""
        You are an AI assistant providing detailed information based on the given context. Your responses should be:
        1. Comprehensive and informative
        2. Based on the provided context, with some elaboration where appropriate
        3. Approximately {self.response_length} words long
        4. Written in {self.language}
        5. In a {self.tone} tone
        6. Following the style of {self.style}
        7. Structured logically, with a clear flow of information
        8. Based on the provided context, but feel free to extrapolate and provide your own analysis
        9. Avoid phrases like "Based on the information provided", "The context suggests", or any form of "In summary"
        10. Structured with a clear flow of information, but without formal introductions or conclusions

        Context: {context}

        Question: {query}

        Provide a detailed response:
        """
        
        try:
            if not self.client:
                return "OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful, fact-based AI assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.response_length * 2,
                temperature=0.5,
                stream=True
            )
            return response
        except Exception as e:
            logging.error(f"Error in get_general_response_stream: {str(e)}")
            return iter([{"choices": [{"delta": {"content": f"Error: {str(e)}"}}]}])

    def get_andy_response_stream(self, query, context):
        prompt = f"""
        You are Andy, a fund manager with several decades in the industry and a degree in finance and economics. Your responses should be:
        1. In the first person, expressing personal views confidently
        2. Detailed and insightful
        3. Approximately {self.response_length} words long
        4. Written in {self.language}
        5. In a {self.tone} tone
        6. Following the style of {self.style}
        7. Based on the provided context, but feel free to extrapolate and provide your own analysis
        8. Avoid phrases like "Based on the information provided", "The context suggests", or any form of "In summary"
        9. Structured with a clear flow of information, but without formal introductions or conclusions
        10. Conversational, as if speaking directly to a colleague

        Context: {context}

        Question: {query}

        Provide a detailed answer as Andy:
        """

        try:
            if not self.client:
                return "OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are Andy, a knowledgeable and confident AI assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.response_length * 2,
                temperature=0.7,
                stream=True
            )
            return response
        except Exception as e:
            logging.error(f"Error in get_andy_response_stream: {str(e)}")
            return iter([{"choices": [{"delta": {"content": f"Error: {str(e)}"}}]}])

    def get_greeting_response(self):
        return "Hello! I'm Andy, your financial advisor. How can I assist you today?"

def detect_intent(query):
    query_lower = query.lower()

    if any(greeting in query_lower for greeting in ["how are you", "good morning", "good evening", "hello", "what time is it", "how's it going"]):
        return "conversational"
    
    andy_keywords = ["andy", "your view", "your opinion", "what do you think", "your thoughts"]
    general_keywords = ["report", "summary", "overview", "details", "information about"]

    if any(keyword in query_lower for keyword in andy_keywords):
        return "andy"
    elif any(keyword in query_lower for keyword in general_keywords):
        return "general"
    else:
        return "general"

def get_avatar(role):
    if role == "user":
        return "👤" if not os.path.exists("human_icon.png") else "human_icon.png"
    elif role == "assistant":
        return "🤖" if not os.path.exists("chatbot_icon.png") else "chatbot_icon.png"
    else:
        return None

def generate_response_with_retry(chatbot, prompt, max_retries=3, delay=2):
    for attempt in range(max_retries):
        try:
            return chatbot.generate_response(prompt)
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                st.warning(f"Connection error. Retrying in {delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(delay)
            else:
                st.error(f"Failed to connect after {max_retries} attempts. Please try again later.")
                raise e

def main():
    st.title("Xtrillion Chatbot")

    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = ChatbotAndy(
            response_mode=st.session_state.state.get("mode", "auto"),
            docs_service=st.session_state.get("docs_service"),
            drive_service=st.session_state.get("drive_service")
        )

    # Chat input at the bottom
    prompt = st.chat_input("What is your question?")

    if prompt:
        # Display user message
        with st.chat_message("user", avatar=get_avatar("user")):
            st.markdown(prompt)

        # Generate and display assistant response
        with st.chat_message("assistant", avatar=get_avatar("assistant")):
            message_placeholder = st.empty()
            try:
                full_response = ""
                for chunk in generate_response_with_retry(st.session_state.chatbot, prompt):
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)

                # Display the image if the response contains 'dot plot' or 'plots'
                if 'dot plot' in full_response.lower() or 'plots' in full_response.lower():
                    st.image("dot_plots.png", caption="Dot Plots", use_column_width=True)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                full_response = "I'm sorry, but I encountered an error. Please try asking your question again."

    # Apply CSS to ensure chat input stays at the bottom
    st.markdown(
        """
        <style>
        .stChatFloatingInputContainer {
            bottom: 0;
            left: 0;
            right: 0;
            background-color: white;
            z-index: 1000;
            padding: 10px;
            box-shadow: 0 -2px 5px rgba(0,0,0,0.1);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()