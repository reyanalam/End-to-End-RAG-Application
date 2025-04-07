import os
import pinecone
from langchain_community.document_loaders import PyPDFLoader 
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from src.app.get_embedding import embed_text

load_dotenv("file.env")

def load_document(document_path):
    loader = PyPDFLoader(document_path)
    return loader.load()

def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=120,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)

def add_to_pinecone(document_path: str):
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

    cloud = os.environ.get('PINECONE_CLOUD', 'aws')
    region = os.environ.get('PINECONE_REGION', 'us-east-1')
    spec = ServerlessSpec(cloud=cloud, region=region)

    index_name = "rag"

    # Load and split documents
    documents = load_document(document_path)
    print(f"Loaded {len(documents)} documents")
    chunks = split_documents(documents)

    # Extract text from document chunks
    texts = [doc.page_content for doc in chunks]

    # Generate embeddings
    embeddings = embed_text(texts)
    print(f"Created {len(chunks)} chunks")
    print(f"First chunk: {chunks[0].page_content[:100]}")
    print(f"Generated {len(embeddings)} embeddings")
    print(f"First embedding: {embeddings[0][:10]}")
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=len(embeddings[0]),  # Get the correct embedding dimension
            metric="cosine",
            spec=spec
        )

    namespace = "wondervector5000"
    class CustomEmbedding:
            def embed_documents(self, texts):
                return embed_text(texts)
            def embed_query(self, text):
                return embed_text([text])[0]
            
    docsearch = PineconeVectorStore.from_documents(
        documents=chunks,  # Use split document chunks
        index_name=index_name,
        embedding=CustomEmbedding(),
        namespace=namespace,
    )
    print(docsearch)
    print(f"Added {document_path} to Pinecone")
    return docsearch

docsearch = add_to_pinecone(r"C:\Users\Reyan\Desktop\Projects\RAG\src\data\galaxy-design-client-guide.pdf")
