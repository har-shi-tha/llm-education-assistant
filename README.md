# LLM-Based Adaptive Learning Assistant

A local AI-powered educational assistant built using Python and Ollama (Llama3).  
This project demonstrates LLM integration, prompt engineering, structured output validation, and interactive CLI-based assessment design.



 Overview

The LLM-Based Adaptive Learning Assistant is a local AI system that:

- Stores topic-based notes (persistent memory)
- Generates AI-powered multiple-choice quizzes
- Validates structured JSON outputs from LLM responses
- Provides interactive scoring and explanations
- Tracks learning progress
- Supports tutor-style AI Q&A mode

The system runs entirely locally using Ollama — no external API billing required.



 Key Features

- Topic-based note storage (SQLite-backed memory)
- AI-generated quizzes with interactive scoring
- Prompt engineering with JSON schema enforcement
- LLM output validation to reduce malformed responses
- CLI interface with structured formatting (Rich)
- Progress tracking system (todo / doing / done)
- Local deployment using Ollama (Llama3)



Tech Stack

- Python
- Ollama (Llama3 model)
- SQLite
- Rich (CLI formatting)
- Requests (LLM communication)
- Prompt Engineering
- Structured Output Validation (JSON Schema)



 Project Structure

edu_agent/
│
├── agent.py              # Main CLI application
├── quiz.py               # Quiz generation logic
├── llm.py                # Ollama API communication
├── memory.py             # Note storage (SQLite)
├── tracker.py            # Progress tracking
├── requirements.txt
├── README.md
└── .gitignore



 Installation & Setup

1) Install Ollama  
Download and install from:
https://ollama.com/download

Pull the required model:

    ollama pull llama3.2:3b

2) Create Virtual Environment (Windows PowerShell)

    py -m venv .venv
    .venv\Scripts\Activate.ps1

3) Install Dependencies

    pip install -r requirements.txt

If you do not have requirements.txt:

    pip install rich requests

---

## Running the Application

    python agent.py

You should see:

    Education Helper Agent ready.
    Commands:
    ...
    You:



 Available Commands

note: <topic> | <content>      -> Save a note  
search: <keyword>              -> Search saved notes  
quiz: <topic>                  -> Generate AI quiz and test yourself  
status: <topic> | todo/doing/done -> Track learning progress  
progress                       -> Show latest progress  
ask: <question>                -> AI tutor explanation mode  
help                           -> Show commands  
quit                           -> Exit program  



 Example Usage

    note: Gradient Descent | Update rule: w = w - alpha * gradient
    quiz: Gradient Descent
    ask: Explain gradient descent with a small numeric example



AI Design Considerations

- Structured JSON prompt design ensures predictable quiz formatting.
- Schema validation reduces hallucination-driven formatting errors.
- Output parsing logic handles non-JSON model responses.
- Prompt constraints improve logical consistency between answers and explanations.
- Designed to demonstrate practical LLM orchestration and reliability engineering.



 Future Improvements

- Add REST API layer (FastAPI)
- Add web interface (Streamlit or React)
- Add quiz performance analytics dashboard
- Add auto-validation and regeneration pipeline for incorrect questions



 Notes

- As this system uses a generative LLM, factual accuracy may vary.
- Designed as a demonstration of LLM integration and prompt engineering.
- Fully local deployment — no external API keys required.


