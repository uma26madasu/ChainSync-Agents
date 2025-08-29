# ChainSync AI Agent Deployment Guide

## Prerequisites
- Python 3.8+
- `pip` for package management
- (Optional) `.env` file for environment variables

## Installation
1. Clone the repository:
   ```sh
   git clone <repo-url>
   cd ChainSync-Agents
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set environment variables (or create a `.env` file):
   - `OPENAI_API_KEY`
   - `CHAINSYNC_API_URL` (optional)
   - `PYTHON_AGENT_PORT` (optional)
   - `LOG_LEVEL` (optional)

## Running the Application
Run the main application:
```sh
python main.py
```

## Testing
Run all tests:
```sh
python -m unittest discover tests
```

## Integration
- The Python AI Agent is designed to be integrated with MuleSoft or other orchestration layers.
- API endpoints and further integration logic can be added as needed.

---
*Update this guide as deployment or integration requirements change.*
