# LLM-Powered Intent Router Service

## Project Overview
This application implements a "Classify then Respond" system design pattern. It intelligently routes user requests to one of four specialized AI expert personas (Code, Data, Writing, Career) based on detected intent. This approach ensures higher accuracy and context-aware responses compared to monolithic prompt designs.

## Features
* **Intent Classification**: Uses a lightweight LLM call to categorize input into `code`, `data`, `writing`, `career`, or `unclear`.
* **Structured Output**: Ensures the classifier returns a strict JSON format with intent and confidence scores.
* **Expert Personas**: Four distinct, opinionated system prompts designed for high-quality generation.
* **Clarification Logic**: Automatically identifies unclear requests and asks for user clarification instead of guessing.
* **Robust Logging**: Every interaction is logged in JSON Lines (`.jsonl`) format for observability.

## Design Explanation
The system follows a two-step orchestration:
1.  **classify_intent**: The user message is sent to the LLM with a system prompt that enforces a JSON response schema.
2.  **route_and_respond**: Based on the JSON output, the system fetches the corresponding expert persona from `prompts.py` and generates the final response.

## Setup & Installation

### Prerequisites
* Python 3.11+
* Docker & Docker Desktop (for containerized execution)
* Groq API Key
```bash
### Local Setup
1. Clone the repository to your local machine.
2. Create a `.env` file in the root directory and add your key:
   ```text
   GROQ_API_KEY=your_actual_api_key_here
```
## Install dependencies:

```Bash
pip install -r requirements.txt
```
Run the application:

```Bash
python router.py
```
Running with Docker (Recommended)
This application is fully containerized. To build and run the service:

```Bash
docker-compose up --build
```
## Project Structure
**router.py:** Core logic for classification and routing.

**prompts.py:** Storage for specialized expert system prompts.

**route_log.jsonl:** The generated log file containing intent, confidence, and responses.

**.env.example:** Template for required environment variables.

**Dockerfile & docker-compose.yml:** Configuration for containerization.

## Evaluation Verification
**Core Requirements:** All 6 core requirements have been implemented and verified.

**Test Cases:** 15 varied test messages (ambiguous, technical, and professional) have been processed.

**Error Handling:** The system gracefully handles malformed JSON by defaulting to 'unclear' intent.

[click here to watch video](https://youtu.be/6owJWISiAyg)