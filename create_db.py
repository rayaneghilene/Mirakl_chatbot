from sentence_transformers import SentenceTransformer
import chromadb
from chromadb import Client
import argparse
from urllib.parse import urljoin, urlparse
import logging
import json


logging.getLogger("chromadb.segment.impl.metadata.sqlite").setLevel(logging.ERROR)
logging.getLogger("chromadb.segment.impl.vector.local_hnsw").setLevel(logging.ERROR)

model = SentenceTransformer('all-MiniLM-L6-v2')


def load_json(file_path):
    """Load data from a JSON file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def preprocess_text(text_list):
    """Preprocess a list of text data."""
    return [text.lower() for text in text_list]


def vectorize_text(text):
    return model.encode(text, convert_to_tensor=True).tolist()


def get_or_create_collection(client, collection_name):
    existing_collections = client.list_collections()

    for collection in existing_collections:
        print("collection name", collection.name)
        if collection.name == collection_name:
            logging.info(f"Collection '{collection_name}' already exists.")
            return client.get_collection(name=collection_name)

    logging.info(f"Collection '{collection_name}' does not exist. Creating it now.")
    return client.create_collection(name=collection_name)


def query_collection(collection, query_text, top_k=1):
    query_vector = vectorize_text(query_text)
    results = collection.query(
        query_embeddings=[query_vector]
    )
    
    ids = results['ids'][0]
    distances = results['distances'][0]
    metadatas = results['metadatas'][0]
    
    top_results = {
        'ids': ids[:top_k],
        'distances': distances[:top_k],
        'metadatas': metadatas[:top_k]
    }
    
    return top_results


def add_paragraphs_to_collection(collection, data):
    for page, content in data.items():
        for paragraph in content['content']['paragraphs']:
            paragraph_vector = vectorize_text(paragraph)
            collection.add(
                embeddings=[paragraph_vector],
                metadatas=[{"paragraph": paragraph, "url": content['url'], "id": f"para_{page}"}],
                ids=[f"doc_{page}"]
            )


def delete_collection(client, collection_name):
    try:
        # Retrieve the collection object
        collection = client.get_collection(name=collection_name)
        
        if collection:
            # Delete the collection
            client.delete_collection(name=collection_name)
            print(f"Collection '{collection_name}' has been deleted.")
        else:
            print(f"Collection '{collection_name}' does not exist.")
    
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    parser = argparse.ArgumentParser(description='Load data from a JSON file.')

    parser.add_argument('--json_file', type=str, default='/Users/rayaneghilene/Documents/Ollama/Mirakl_chatbot/scraped_data.json',
                    help='The file path to the scraped data in JSON format (default: Mirakl_chatbot/scraped_data.json).')
    parser.add_argument('--collection_name', type=str, default='mirakl_data',
                    help='The name of the collection (default: mirakl_data).')
    parser.add_argument('--query_text', type=str, default='what is the mission of Mirakl',
                    help='The default query (default: what is the mission of Mirakl).')
    

    args = parser.parse_args()
    print("args", args)
    json_file_path = args.json_file
    print("json_file_path", json_file_path)
    query_text = args.query_text
    collection_name = args.collection_name
    data = load_json(json_file_path)


    client = Client()

    delete_collection(client, collection_name)
    
    collection = get_or_create_collection(client, collection_name)
    add_paragraphs_to_collection(collection, data)


    results = query_collection(collection, query_text)

    print("Query Results:")
    for i in range(len(results['ids'])):
        print(f"Query: {query_text}")
        print(f"Response: {results['metadatas'][i]['paragraph']}")
        print("-------")

if __name__ == '__main__':
    main()
