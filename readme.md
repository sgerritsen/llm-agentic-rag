# LLM RAG, multi agent

Author: Simon Gerritsen

## Installation

1. Copy the .env.example and replace the environment variables.
2. Run `docker compose up --build --remove-orphans`
3. Ensure your python interpreter uses the python the build.
4. Check connection to the redis server.
5. Install Ollama and download `llama3.2`, and `mxbai-embed-large`
6. Depending on whether you want to run the **simple_rag_agent** or the **react_agent**, insert a question in `user_query` of the file.
7. Adjust the `description` in the `ToolMetadata`.
8. In order to retrieve the documents from Confluence, first run the `get_quality_manual_from_confluence.py` script. This may take a while, and there's a chance you'll be throttled. Take this into consideration. 
9. Run the `simple_rag_agent.py`, or `react_agent.py` script.
