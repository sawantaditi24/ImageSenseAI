from sentence_transformers import SentenceTransformer

# Load the model once at startup
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_text_embedding(text: str):
    """
    Returns a list of floats (the embedding vector) for the given text.
    """
    return model.encode(text).tolist()
