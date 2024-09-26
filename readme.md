# LLM RAG, multi agent

Author: Simon Gerritsen

## Installation

1. Copy the .env.example and replace the environment variables.
2. Run `docker compose up --build --remove-orphans`
3. Ensure your python interpreter uses the python the build.
4. Check connection to the redis server.
5. Install Ollama and download `llama3.1`, and `mxbai-embed-large`
5. Depending on whether you want to run the **simple_rag_agent** or the **react_agent**, insert a question in `user_query` of the file.
6. Adjust the `description` in the `ToolMetadata`.
6. Run the `simple_rag_agent.py`, or `react_agent.py` script.
