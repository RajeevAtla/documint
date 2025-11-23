# Technical Documentation Modernizer

An AI-powered system that modernizes technical documentation using LangGraph agents and Claude.

## Features
- Fetches documentation from any URL
- Identifies outdated content and practices
- Researches current best practices
- Generates modernized markdown documentation
- Provides quality assessment

## Setup

1. Install UV package manager:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Clone and setup:
   ```bash
   git clone <repo>
   cd doc-modernizer
   uv sync
   ```

3. Configure environment:
   ```bash
   cp .env.example .env
   # Add your GEMINI_API_KEY to .env
   ```

4. Run the application:
   ```bash
   uv run python src/app.py
   ```

5. Open browser to http://localhost:7860

## Architecture

The system uses a LangGraph state machine with these agents:
- **Fetcher**: Retrieves and converts HTML to markdown
- **Analyzer**: Identifies outdated sections and issues
- **Researcher**: Finds current best practices
- **Generator**: Creates modernized documentation
- **Quality Checker**: Validates output quality

## Usage

1. Enter a documentation URL
2. Click "Modernize"
3. Review the analysis, modernized content, and quality report
4. Download the modernized markdown

## Development

Run tests:
```bash
uv run pytest
```

Format code:
```bash
uv run black src/
uv run ruff check src/
```
