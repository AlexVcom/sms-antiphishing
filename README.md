# SMS Anti-Phishing Service

Service for filtering phishing SMS messages.

## Features
- Real-time phishing URL detection using WebRisk API
- User opt-in/opt-out management via SMS commands
- URL caching to minimize API calls
- Redis-based preference storage
- Comprehensive test suite

## Getting Started

### Prerequisites
- Docker and Docker Compose
- WebRisk API key

### Running Locally
1. Create `.env` file from template:
   ```bash
   cp .env.example .env