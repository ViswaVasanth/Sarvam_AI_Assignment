import os
#importing moudles
import requests
from bs4 import BeautifulSoup
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain import HuggingFaceHub
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


DOC_PATH = "iesc111.pdf"
CHROMA_PATH = "ncert" 

# load your pdf doc
loader = PyPDFLoader(DOC_PATH)
pages = loader.load()
import os
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

# split the doc into smaller chunks i.e. chunk_size=500
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = text_splitter.split_documents(pages)
embedding = HuggingFaceEmbeddings()
db = FAISS.from_documents(chunks, embedding)
llm=HuggingFaceHub(
    repo_id="google/flan-t5-large", 
    model_kwargs={"temperature":0.2, "max_length":256}
    )
chain = load_qa_chain(llm, chain_type="stuff")
query = "Explain Propagation of Sound ?"
# docs = db.similarity_search(query)
# chain_input = {"input_documents": docs, "question": query}
# result = chain.invoke(chain_input)
import re

def classify_query(query: str) -> str:
    # Identify if query is conversational (e.g., Hello, how are you?)
    if re.search(r"\b(hello|hi|hey|how are you|greetings)\b", query, re.IGNORECASE):
        return "greeting"
    
    # Identify if query is about calculations
    
    if re.search(r"\d+[\+\-\*\/]\d+", query):
      return "calculator"
    
    # Otherwise, assume it's a factual question requiring VectorDB search
    return "factual"
def query_rag(question):
  docs = db.similarity_search(query)
  chain_input = {"input_documents": docs, "question": query}
  response = chain.invoke(chain_input)
  return response["output_text"]
def calculator(query: str):
  # Parse and evaluate a simple math expression
  try:
      result = eval(query)
      return f"The result is {result}."
  except:
      return "Sorry, I couldn't compute that."

def agent(query: str):
    # Classify the query
    query_type = classify_query(query)
    
    if query_type == "greeting":
        return "Hello! How can I assist you today?"

    elif query_type == "calculator":
      return calculator(query)
    
    elif query_type == "factual":
        # Call the RAG (VectorDB) for factual answers
        return query_rag(query)
    
    else:
        return "I'm not sure how to help with that."
from flask import Flask, request, jsonify
app = Flask(__name__)
@app.route('/agent', methods=['POST'])
def agent_endpoint():
    # Get the user query and location (if provided)
    data = request.get_json()
    query = data.get("query")    
    # Get the response from the agent
    response = agent(query)
    
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)