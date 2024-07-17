from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama

# bge-base embedding model
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
Settings.llm = Ollama(model="llama3", request_timeout=360.0)

documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
# response = query_engine.query("Who is Byte?")
# print(response)

while True:
    # Get the question from the user
    user_question = input("\nPlease enter your question (or 'quit' to exit):\n")

    # Check if the user wants to quit
    if user_question.lower() in ['quit', 'qq', 'bye', 'exit']:
        break

    # Use the user's question in the query
    response = query_engine.query(user_question)

    # Print the response
    print("\033[96m" + str(response) + "\033[0m")

print("\nThank you for using the query engine!")
