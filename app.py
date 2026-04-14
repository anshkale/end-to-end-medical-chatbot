from flask import Flask, render_template, request
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import google.generativeai as genai
import os

app = Flask(__name__)

# Load env
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Load model (IMPORTANT FIX)
model = genai.GenerativeModel("gemini-2.5-flash")

# Load embeddings
embeddings = download_hugging_face_embeddings()

# Pinecone index
index_name = "medical-chatbot"

docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# System prompt
system_prompt = (
    "You are a Medical assistant for question-answering tasks. "
    "Use the following context to answer the question. "
    "If you don't know, say you don't know. "
    "Keep answer concise (max 3 sentences).\n\n"
)

# RAG function
def ask_medibot(query):
    docs = retriever.get_relevant_documents(query)
    context = "\n".join([doc.page_content for doc in docs])

    prompt = f"""
    {system_prompt}

    Context:
    {context}

    Question:
    {query}
    """

    response = model.generate_content(prompt)
    return response.text


@app.route("/")
def index():
    return render_template('chat.html')


@app.route("/get", methods=["POST"])
def chat():
    msg = request.form["msg"]
    print("User:", msg)

    answer = ask_medibot(msg)

    print("Bot:", answer)
    return str(answer)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)