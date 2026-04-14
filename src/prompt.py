import google.generativeai as genai
# Configure API
genai.configure(api_key="api_key")

# Load Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")


# Your system prompt
system_prompt = (
    "You are a Medical assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise.\n\n"
)


# Function to run RAG
def ask_medibot(query):
    # Step 1: Retrieve documents
    docs = retriever.get_relevant_documents(query)

    # Step 2: Combine context
    context = "\n".join([doc.page_content for doc in docs])

    # Step 3: Create prompt
    prompt = f"""
    {system_prompt}
    
    Context:
    {context}
    
    Question:
    {query}
    """

    # Step 4: Generate answer
    response = model.generate_content(prompt)

    return response.text