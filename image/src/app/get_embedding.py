from langchain_community.embeddings import SentenceTransformerEmbeddings

def embed_text(text_chunks):
    """Generates embeddings for a list of text chunks using TF-IDF."""
    model_name = "all-MiniLM-L6-v2"
    
    # Wrap the model with SentenceTransformerEmbeddings
    embeddings = SentenceTransformerEmbeddings(model_name=model_name)
    
    # Generate embeddings for the input text chunks
    embeddings_list = embeddings.embed_documents(text_chunks)
    
    return embeddings_list


