# Sarvam_AI_Assignment
# Smart Agent Query System

## Overview

The Smart Agent Query System is a solution designed to handle user queries through a web API and a Gradio interface. It uses a combination of natural language processing and machine learning to classify queries, perform calculations, and provide answers from a knowledge base. Additionally, it converts textual responses into audio using the Sarvam AI API.

## Features

- **Query Classification**: Determines if a query is a greeting, a calculation, or a factual question.
- **Document Retrieval**: Utilizes a document database to fetch relevant information for factual questions.
- **Calculation Handling**: Evaluates and returns results for mathematical expressions.
- **Text-to-Speech Conversion**: Converts text responses into audio files using the Sarvam AI API.
- **Gradio Interface**: Provides a web-based interface for users to interact with the system.

## Setup

### Prerequisites

- Python 3.8 or later
- Flask
- Gradio
- Requests
- BeautifulSoup4
- langchain
- Sarvam AI API key

### Installation

1. **Clone the Repository**

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. **Install Required Packages**

    Install the necessary Python packages using `pip`:

    ```bash
    pip install flask gradio requests beautifulsoup4 langchain
    ```

3. **Set Up Environment Variables**

    Set your Hugging Face API token in an environment variable. Replace `YOUR_HUGGINGFACE_API_TOKEN` with your actual token.

    ```bash
    export HUGGINGFACEHUB_API_TOKEN=YOUR_HUGGINGFACE_API_TOKEN
    ```

4. **Run the Flask API**

    Start the Flask server:

    ```bash
    python Sarvam_exp.py
    ```

5. **Run the Gradio Interface**

    In a separate terminal, execute:

    ```bash
    python Sarvam_Deployment.py
    ```


## Usage

### Interacting with the API

Send a POST request to `http://127.0.0.1:8000/agent` with a JSON payload containing the query:

```json
{
    "query": "Explain Propagation of Sound?"
}
