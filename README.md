# Blog Content Writer AI

An AI-powered blog content generation tool built with Streamlit and LangChain. This application helps users create high-quality blog posts by leveraging multiple search sources and advanced language models.

## Features

- **AI-Powered Content Generation**: Uses Groq's advanced language models (Llama, Gemma) to generate blog content
- **Multi-Source Research**: Integrates Wikipedia, Google Search (via SerpAPI), and Tavily Search for comprehensive research
- **Customizable Output**: Adjustable word limits and specific writing instructions
- **Interactive Chat Interface**: Streamlit-based UI with conversation history
- **Keyword Integration**: Optional keyword-based research for more targeted content
- **Docker Support**: Containerized deployment for easy setup

## Prerequisites

- Python 3.12 or higher
- Groq API key (required for AI generation)
- Optional: SerpAPI key and Tavily API key for enhanced search capabilities

## Installation

### Option 1: Local Setup

1. Clone or download the project files
2. Create a virtual environment:
   ```bash
   python -m venv envs
   source envs/bin/activate  # On Windows: envs\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   export GROQ_API_KEY="your-groq-api-key-here"
   # Optional:
   # export SERPAPI_API_KEY="your-serpapi-key-here"
   # export TAVILY_API_KEY="your-tavily-key-here"
   ```

### Option 2: Docker Setup

1. Build the Docker image:
   ```bash
   docker build -t blog-creator .
   ```

2. Run the container:
   ```bash
   docker run -p 8501:8501 -e GROQ_API_KEY="your-groq-api-key-here" blog-creator
   ```

## Usage

1. Start the application:
   ```bash
   streamlit run BlogCreator.py
   ```

2. Open your browser to `http://localhost:8501`

3. Enter your blog topic in the main text input

4. Configure options in the sidebar:
   - **Model Selection**: Choose from available Groq models (Llama 4, Gemma 2, etc.)
   - **Wikipedia Search**: Toggle to include Wikipedia research
   - **Keyword**: Add specific keywords for targeted research
   - **Word Limit**: Set desired blog length
   - **Specific Instructions**: Add custom writing guidelines

5. Click "Submit" to generate your blog content

## Configuration

### API Keys

The application requires a Groq API key for content generation. Optional search APIs enhance research capabilities:

- **GROQ_API_KEY**: Required for AI model access
- **SERPAPI_API_KEY**: For Google search integration
- **TAVILY_API_KEY**: For advanced web search

### Model Options

Available models:
- `meta-llama/llama-4-maverick-17b-128e-instruct`
- `gemma2-9b-it`
- `llama-3.3-70b-versatile`
- `llama3-70b-8192`

## Project Structure

```
BlogCreator.py          # Main Streamlit application
requirements.txt         # Python dependencies
Dockerfile              # Docker container configuration
envs/                   # Virtual environment (created during setup)
README.md              # This file
```

## Dependencies

Key libraries used:
- **Streamlit**: Web application framework
- **LangChain**: AI orchestration and prompt management
- **LangChain-Groq**: Groq model integration
- **Wikipedia API**: Wikipedia search functionality
- **SerpAPI/Tavily**: Web search capabilities

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. Please check the license file for details.

## Support

For issues or questions:
1. Check the configuration of your API keys
2. Ensure all dependencies are installed
3. Verify your Python version (3.12+ recommended)
4. Check the Streamlit logs for error messages
