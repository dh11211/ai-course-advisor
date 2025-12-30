import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

# Load environment variables from .env file
load_dotenv()

# --- 1. Load and Chunk the Document ---
print("Loading and chunking document...")
loader = TextLoader("data/course_handbook.txt")
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documents)

# --- 2. Create Embeddings and Upload to Pinecone ---
# Get the OpenAI embeddings model
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

# Get the name of the Pinecone index from environment variables
index_name = os.getenv("PINECONE_INDEX_NAME", "ai-course-advisor")

# This is the main command that does all the work:
# 1. It takes our text chunks.
# 2. It uses the OpenAI embeddings model to convert them to vectors.
# 3. It connects to our Pinecone index.
# 4. It uploads the vectors and their corresponding text to the index.
PineconeVectorStore.from_documents(
    documents=chunks, 
    embedding=embeddings, 
    index_name=index_name
)

print(f"✅ Ingestion complete! Data uploaded to index: {index_name}")