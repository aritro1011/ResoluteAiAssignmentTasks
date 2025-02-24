import os
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import google.generativeai as genai 
from docx import Document
import streamlit as st
from dotenv import load_dotenv  
from io import BytesIO
import fitz 


load_dotenv()  


embedding_model = SentenceTransformer('all-MiniLM-L6-v2')


client = chromadb.Client()


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def parse_pdf(file):
    text = ""
    pdf_data = file.read()  
    doc = fitz.open(stream=pdf_data, filetype="pdf")  
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text("text") 
    return text

def parse_docx(file):
    text = ""
    doc = Document(file)
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def preprocess_documents(files):
    document_texts = []
    
    for file in files:
        if file.type == "application/pdf":
            text = parse_pdf(file)
        elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = parse_docx(file)
        elif file.type == "text/plain":
            text = str(file.read(), "utf-8")
        else:
            continue 

        document_texts.append(text)


    embeddings = embedding_model.encode(document_texts, convert_to_tensor=True)
    embeddings = embeddings.tolist() 

    collection_name = "document_collection"
    
  
    collection = None
    try:
        collection = client.get_collection(name=collection_name)
    except Exception as e:
      
        print(f"Collection not found or error: {e}. Creating a new collection.")
    
    
    if collection is None:
        collection = client.create_collection(name=collection_name)

    collection.add(
        documents=document_texts,
        embeddings=embeddings,
        metadatas=[{"source": "file"}] * len(document_texts),
        ids=[str(i) for i in range(len(document_texts))]
    )

def retrieve_relevant_passages(query, k=3):
    query_embedding = embedding_model.encode([query], convert_to_tensor=True).tolist()

    collection = client.get_collection(name="document_collection")
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k
    )
    
  
    relevant_passages = results['documents']
    
 
    if isinstance(relevant_passages, list):
       
        relevant_passages = [str(item) for sublist in relevant_passages for item in (sublist if isinstance(sublist, list) else [sublist])]
    else:
        # In case it's not a list, just convert it to a string
        relevant_passages = [str(relevant_passages)]
    
   
    context = "\n\n".join(relevant_passages)
    
    return context

def generate_response(query, context):
    prompt = f"Given the following context, answer the question: {context}\n\nQuestion: {query}\nAnswer:"


    response = genai.GenerativeModel('gemini-1.5-flash').generate_content(prompt)
    
    return response.text.strip()

st.title("Document Chat with RAG (using Google Gemini & ChromaDB)")


uploaded_files = st.file_uploader("Upload documents (PDF, DOCX, TXT)", accept_multiple_files=True)

if uploaded_files:

    preprocess_documents(uploaded_files)
    st.write("Documents uploaded and processed.")

   
    user_input = st.text_input("Ask a question:")
    
    if user_input:  
       
        context = retrieve_relevant_passages(user_input)  # Get relevant passages as context
        answer = generate_response(user_input, context)
        st.write("Answer:", answer)


if st.button('Clear Session'):
   
    for key in list(st.session_state.keys()):
        del st.session_state[key]
   
    st.rerun()
