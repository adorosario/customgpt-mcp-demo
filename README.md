# RAG Agent with OpenAI Agents SDK

This project uses Docker Compose to build and run a Python-based RAG agent that connects to your MCP SSE endpoint.

## Prerequisites

* Docker Engine (v20+)
* Docker Compose (v1.27+)

## Setup & Run

1. **Clone the repo**

   ```bash
   git clone https://github.com/your-org/your-repo.git
   cd your-repo
   ```

2. **Build the container**

   ```bash
   docker-compose build
   ```

3. **Run the agent**

   ```bash
   docker-compose up
   ```

   This will:

   * Build the `rag-agent` service using your `Dockerfile`.
   * Mount your code into `/app`.
   * Drop into Bash, then execute `python main.py` with `MCP_ENDPOINT` set.

4. **Stop the agent**
   In another terminal:

   ```bash
   docker-compose down
   ```

## Customization

* **Change the MCP endpoint**
  Edit `docker-compose.yml` and update the `MCP_ENDPOINT` environment variable.

* **Interactive shell**
  To get a Bash shell inside the container for debugging:

  ```bash
  docker-compose run --rm rag-agent bash
  ```

## File Overview

* **Dockerfile**
  Based on `python:3.10-slim`, installs dependencies, and sets up Bash as the shell.
* **docker-compose.yml**
  Defines a single `rag-agent` service that builds your image, mounts code, and runs `main.py`.
* **requirements.txt**
  Lists your Python dependencies (`openai-agents`, `openai`, etc.).
* **main.py**
  Your agent’s entrypoint script where you connect to the MCP server and perform RAG searches.


## Setup Instructions

1. Clone the repository
2. Copy `.env.example` to `.env` and fill in your API keys
3. Run with Docker: `docker compose run --rm rag-agent`

## Environment Variables Required
- `OPENAI_API_KEY`: Your OpenAI API key
- `MCP_ENDPOINT`: Your CustomGPT MCP endpoint URL
