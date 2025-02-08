# BU Chat

## Overview
BU Chat is an AI-powered chatbot built using Hugging Face Transformers (Ollama 3.2) and Python Flask. It enables efficient querying of the BU website’s content by leveraging a structured database setup.

## Problem Statement
The information on the BU website is extensive, making it difficult for users to find relevant details quickly due to numerous URL links and web pages.

## Tools Used
- **Hugging Face Transformers** → Ollama 3.2
- **Python Flask**
- **ChromeDriver**
- **Langchain**
- **Chroma**

## Setup Steps
1. **Upload BU Website Content**  
   Extract and store website data into an array for processing.
2. **Create Database**  
   Structure the extracted data into a queryable format.
3. **Implement Querying**  
   Enable searching and interaction with stored data.

## Development Time
- **Duration:** A weekend

## API Routes
- `POST /create_db` → Initializes the database and stores website content.
- `POST /query` → Processes user queries and retrieves relevant information.
- `POST /chat` → Facilitates AI-driven conversations with users.

## Usage
BU Chat allows users to efficiently navigate the BU website's content through natural language queries, reducing the need for manual searches.

