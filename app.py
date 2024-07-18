from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from halo import Halo

from color import Color

# Create a spinner
spinner = Halo(text='Loading', spinner='dots')

try:
    # Start the spinner
    spinner.start()
    # bge-base embedding model
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-base-en-v1.5")
    Settings.llm = Ollama(model="llama3", request_timeout=360.0)

    documents = SimpleDirectoryReader("data").load_data()
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine()
    spinner.stop()
    print(Color.LIGHT_GRAY + "The database is up to date." + Color.reset())

    # response = query_engine.query("Who is Byte?")
    # print(response)
except Exception as e:
    spinner.fail(f"Task failed: {e}")

while True:
    # Get the question from the user
    user_question = input(
        Color.LIGHT_BLUE + "Please enter your question (or 'quit' to exit):" + Color.reset() + "\n")

    # Check if the user wants to quit
    if user_question.lower() in ['quit', 'qq', 'bye', 'exit']:
        break

    spinner.start()

    # Use the user's question in the query
    response = query_engine.query(user_question)

    spinner.stop()

    # Print the response
    print(Color.CYAN + str(response) + Color.reset() + "\n")

print(Color.LIGHT_GRAY + "\nThank you for using the query engine!\n" + Color.reset())
