# Mirakl Data Scraper and Vector Database Query

This project is a Python-based tool that scrapes data from the Mirakl website, processes it, and stores it in a JSON file, which is later loaded into vector database for efficient querying. It uses the Sentence Transformers library for text embeddings and ChromaDB for vector storage and retrieval.

## Features

- **Web Scraping**: Extracts data from a given website and stores it in a JSON file.
- **Vectorization**: Converts text data into vector embeddings using Sentence Transformers.
- **Database Management**: Interacts with ChromaDB to manage collections and store vectors.
- **Querying**: Retrieves relevant information from the vector database based on a query.

## Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.10 or higher
- Pip (Python package installer)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/rayaneghilene/Mirakl_chatbot.git
   cd Mirakl_chatbot
    ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

The ```scrape_website.py``` script will scrape data from a website and save it to a JSON file.

1. Run the Scraping Script:

    ```bash
    python scrape_data.py --base_url https://www.mirakl.com/ --output_file scraped_data.json
    ```


* **--base_url**: Base URL of the website to scrape (default: https://www.mirakl.com/).
* **--output_file**: Path to save the scraped data in JSON format (default: scraped_data.json).

2. Create the Vector database:
    ```bash
    python create_db.py --json_file path/to/your/scraped_data.json --collection_name your_collection_name --query_text "your query here"
    ```

* **--json_file** : Path to the JSON file containing the scraped data.
* **--collection_name**: Name of the ChromaDB collection.
* **--query_text**: The query text to search in the collection.

## Contributing
We welcome contributions from the community to enhance work. 
If you have ideas for features, improvements, or bug fixes, please submit a pull request or open an issue on GitHub.


## Support
For any questions, issues, or feedback, please reach out to rayane.ghilene@ensea.fr