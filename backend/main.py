import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from pydantic import BaseModel

# Load environment variables
load_dotenv()

app = FastAPI()

# --- CORS CONFIGURATION ---
# This tells the backend to trust requests coming from your React app
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --------------------------

# Initialize AI components
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
index_name = os.getenv("PINECONE_INDEX_NAME")
vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)

class QueryRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(request: QueryRequest):
    retriever = vectorstore.as_retriever()
    template = """You are an expert AI assistant for the University of Melbourne's Computer Science department.
    Use the following pieces of context from the course handbook to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Keep the answer concise and helpful.

    Context: {context}
    Question: {question}
    Helpful Answer:"""
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)
    
    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=retriever,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )
    
    result = qa_chain.invoke({"query": request.question})
    return {"answer": result["result"]}