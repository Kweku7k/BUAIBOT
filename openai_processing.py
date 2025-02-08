from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
import os

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
You are a helpful and engaging assistant. Use the following context to answer the user's question naturally and conversationally. If the context is unclear, rely on general knowledge to provide a thoughtful response.

Context:
{context}

Now, respond in a friendly and engaging way:
"""

def get_embeddings():
    """Returns an embedding model (OpenAI) compatible with Chroma."""
    return OpenAIEmbeddings(model="text-embedding-ada-002")  # OpenAI's embedding model

def query_database(db, query_text, k=3):
    """Queries the Chroma database for the most relevant documents."""
    try:
        results = db.similarity_search_with_relevance_scores(query_text, k=k)
        return results if results else None
    except Exception as e:
        print(f"Error querying database: {str(e)}")
        return None

def generate_response(model, prompt):
    """Generates a response using OpenAI's GPT model."""
    try:
        return model.invoke(prompt)
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return None

def process_query(query_text="Where is the school located?"):
    """Main function that processes a query text using a RAG system."""
    try:
        # Load OpenAI embeddings
        embedding_functions = get_embeddings()
        if not embedding_functions:
            return

        # Connect to Chroma database
        try:
            db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_functions)
        except Exception as e:
            print(f"Error connecting to Chroma database: {str(e)}")
            return

        results = query_database(db, query_text)

        # Handle case where no results are found
        if not results:
            print("No relevant results found.")
            return

        print("----RESULTS----")
        print(results)
        print("----RESULTS[0]----")
        print(results[0])

        # Extract the first result's score
        first_result = results[0]
        if isinstance(first_result, tuple) and len(first_result) >= 2:
            first_score = first_result[1]
        else:
            print("Unexpected result format.")
            return

        print("----RESULTS[0][1]----")
        print(first_score)

        # Filter out low-relevance results
        if first_score < 0.07:
            print("No results with sufficient relevance found.")
            return

        # Extract context text from retrieved documents
        context_text = "\n\n---".join([doc.page_content if hasattr(doc, "page_content") else str(doc) for doc, _score in results])

        # Format the prompt
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=query_text)

        # Use OpenAI's GPT model
        model = ChatOpenAI(model_name="gpt-3.5-turbo")  # Change to "gpt-3.5-turbo" if needed
        response_text = generate_response(model, prompt)

        # Ensure response is valid before proceeding
        if not response_text:
            print("Failed to generate a response.")
            return

        # Extract sources
        sources = [doc.metadata.get("source", "Unknown") for doc, _score in results]

        formatted_response = f"Response: {response_text}\nSource: {sources}"
        print("formatted_response")
        print(formatted_response)
        return response_text

    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    process_query()