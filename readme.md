# LLM RAG, multi agent

Author: Simon Gerritsen

## Installation

1. Copy the .env.example and replace the environment variables.
2. Run `docker compose up --build --remove-orphans`
3. Ensure your python interpreter uses the containerized python build.
4. Check connection to the redis server.
5. From the ollama container, run `ollama pull llama3.2 mxbai-embed-large`
6. Depending on whether you want to run the **simple_rag_agent** or the **react_agent**, insert a question in `user_query` of the file.
   - When using **react_agent** Adjust the `description` in the `ToolMetadata` to your needs.
7. Run the `simple_rag_agent.py`, or `react_agent.py` script.
