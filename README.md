# CrewAI Proof of Concept

This project is a proof of concept for using CrewAI with `uv` for dependency management.

## Project Goals

Your original description mentioned:
"A Simple proof of concept that uses crew ai to simulate a development team."

And for the second phase:
"The larger / later role will be to simulate multiple teams, and apply the patterns from team topologies to the crew ai teams."

I've integrated these into the goals below.

1.  **Phase 1 (Current):** Simulate a simple development team using CrewAI.
2.  **Phase 2 (Future):** Simulate multiple teams and apply patterns from Team Topologies to the CrewAI teams.

## Setup

1.  **Clone the repository (if you haven't already):**
    ```bash
    # If you've already cloned, navigate to the project directory:
    cd poc-crewai 
    # Otherwise, clone it:
    # git clone <your-repo-url>
    # cd poc-crewai
    ```

2.  **Set up the virtual environment and install dependencies:**
    Make sure you have `uv` installed. If not, you can install it by following the instructions [here](https://github.com/astral-sh/uv).
    ```bash
    uv venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    uv pip install -e .
    ```

3.  **Set up your API keys:**
    Create a `.env` file in the project root (i.e., `/Users/allielapinski/git/poc-crewai/.env`) and add your API keys. For example, if you are using Groq for the LLM:
    ```env
    GROQ_API_KEY=your_groq_api_key_here
    ```
    The `main.py` is currently set up to use Groq, but you can modify it to use other LLM providers (e.g., OpenAI, Anthropic). Remember to install the corresponding Python package (e.g., `langchain-openai`) via `uv pip install langchain-openai` and update `main.py`.

## Running the Project

To run the example crew:

```bash
source .venv/bin/activate  # If you haven't already activated the venv
python -m poc_crewai.main
```

You can change the topic researched by the crew by editing the `topic_to_research` variable in `poc_crewai/main.py`.

