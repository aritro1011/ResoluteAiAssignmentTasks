# AI-Powered Applications with RAG and LangChain Agents  

This repository contains two AI-driven projects:  

## Task 1: Multiple Document RAG QA on Streamlit  
- Implements a **Retrieval-Augmented Generation (RAG) QA system** using **ChromaDB** and **Google Gemini**.  
- Allows users to query multiple documents and receive AI-generated responses.  

## Task 3: LangChain-Based AI Agent for Code Generation & Execution  
- A **LangChain agent** that can **generate and execute Python code**.  
- Uses **Google Gemini** for natural language processing and integrates a secure Python execution tool.  

---

# Task 1: Multiple Document RAG QA on Streamlit  

### **Overview**  
This project enables users to **ask questions across multiple documents** and receive AI-powered responses using a RAG-based pipeline.  

### **Tech Stack**  
- **Frontend**: Streamlit  
- **Vector Database**: ChromaDB  
- **Embeddings**: Sentence-Transformers  
- **LLM**: Google Gemini  

### **Features**  
✅ Upload multiple documents (.pdf, .txt, .docx, etc.)  
✅ Convert documents into vector embeddings  
✅ Query documents and retrieve relevant content  
✅ Generate AI responses using Gemini  

### **Setup Instructions**  
#### 1️⃣ Install dependencies  
```bash
pip install streamlit chromadb sentence-transformers google-generativeai
```
#### 2️⃣ Run the Streamlit app
```bash
streamlit run app.py
```
