from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from halo import Halo

from color import Color


def console_print(message: str, color_name: str = Color.WHITE) -> None:
    print(color_name + message + Color.reset())


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
    console_print("The database is up to date.", Color.LIGHT_GRAY)

    # response = query_engine.query("Who is Byte?")
    # print(response)
except (ValueError, TypeError) as e:
    spinner.fail()
    console_print(f"Task failed: {e}", Color.RED)

while True:
    # Get the question from the user
    user_question = input(
        Color.LIGHT_BLUE + "Please enter your question (or type 'quit' to exit):" + Color.reset() + "\n")

    # Check if the user wants to quit
    if user_question.lower() in ['quit', 'qq', 'bye', 'exit']:
        break

    spinner.start()

    # Use the user's question in the query
    response = query_engine.query(user_question)

    spinner.stop()

    # Print the response
    console_print(str(response) + "\n", Color.CYAN)

console_print("Thank you for using the query engine!\n", Color.LIGHT_GRAY)
