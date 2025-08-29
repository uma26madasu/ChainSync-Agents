# ChainSync AI Agent API Documentation

## Overview
ChainSync AI Agent is a multi-domain enterprise platform component that provides AI-powered analysis and risk assessment for facilities. It integrates with OpenAI and ChainSync APIs and is designed for extensibility and integration with MuleSoft.

## Configuration (`chainsync/config.py`)
- **OPENAI_API_KEY**: API key for OpenAI (required for production).
- **CHAINSYNC_API_URL**: URL for ChainSync API (default: `http://localhost:8081/api`).
- **CHAINSYNC_TIMEOUT**: Timeout for ChainSync API requests (default: 10 seconds).
- **PYTHON_AGENT_PORT**: Port for the Python agent server (default: 8000).
- **DEBUG**: Enable debug mode (default: False).
- **LOG_LEVEL**: Logging level (default: INFO).

## Main Application (`main.py`)
- Entry point for the ChainSync AI Agent.
- Validates configuration and initializes the AI agent.
- Runs demo tests:
  - **Domain Analysis**: Analyzes environmental risks and provides recommendations.
  - **Risk Assessment**: Retrieves facility data and calculates risk assessment.

## AI Agent (`chainsync/ai_agent.py`)
- Implements the `ChainSyncAIAgent` class (to be defined).
- Expected methods:
  - `analyze_with_domain_context(prompt, conversation_id, domain, facility_id)`
  - `get_facility_data_from_chainsync(facility_id)`
  - `calculate_risk_assessment(facility_data)`

## Domain Manager (`chainsync/domain_manager.py`)
- (To be implemented) Handles domain-specific logic and coordination.

## Version
- **2.0.0** by Uma Maheswararao Madasu



