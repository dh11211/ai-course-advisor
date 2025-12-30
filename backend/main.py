import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Updated imports for LangChain 0.1+
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA

load_dotenv()

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    # Add your production frontend URL here once deployed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Model
class QuestionRequest(BaseModel):
    question: str

# Setup LangChain (Initialize once)
api_key = os.environ.get("OPENAI_API_KEY")
pinecone_api_key = os.environ.get("PINECONE_API_KEY")
index_name = os.getenv("PINECONE_INDEX_NAME")

if not api_key:
    raise ValueError("OPENAI_API_KEY is not set")
if not pinecone_api_key:
    raise ValueError("PINECONE_API_KEY is not set")

embeddings = OpenAIEmbeddings(openai_api_key=api_key)
vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)
llm = ChatOpenAI(temperature=0.3, model_name="gpt-4", openai_api_key=api_key)

# Template
SYSTEM_TEMPLATE = """You are an expert academic advisor for the University of Melbourne.
Use the following pieces of context to answer the student's question.
If the answer is not in the context, say you don't know—do not hallucinate.

Context:
{context}

Question: {question}
Answer:"""

PROMPT = PromptTemplate(
    template=SYSTEM_TEMPLATE, input_variables=["context", "question"]
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
    chain_type_kwargs={"prompt": PROMPT},
    return_source_documents=True
)

@app.get("/")
def read_root():
    return {"message": "UniMelb AI Course Advisor API is running"}

@app.post("/ask")
def ask_question(request: QuestionRequest):
    result = qa_chain.invoke({"query": request.question})
    
    # Optional: Log or process source documents
    # source_docs = result.get("source_documents", [])
    
    return {"answer": result["result"]}