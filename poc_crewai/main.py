import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# To load environment variables from a .env file
from dotenv import load_dotenv
load_dotenv()

# Example: Set up an OpenAI LLM
# Make sure to set your OPENAI_API_KEY environment variable
llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4.1-nano-2025-04-14", # Or any other OpenAI model you prefer, e.g., "gpt-4"
)

# Define your agents
researcher = Agent(
    role='Senior Researcher',
    goal='Discover new insights on {topic}',
    backstory='You are a senior researcher at a leading tech think tank.',
    verbose=True,
    llm=llm,
    allow_delegation=False
)

writer = Agent(
    role='Content Writer',
    goal='Write a compelling blog post about {topic}',
    backstory='You are a renowned content writer, known for your insightful and engaging articles.',
    verbose=True,
    llm=llm,
    allow_delegation=False
)

# Define your tasks
research_task = Task(
    description='Investigate the latest advancements in {topic}.',
    expected_output='A comprehensive report on the latest advancements.',
    agent=researcher
)

write_task = Task(
    description='Based on the research, write an engaging blog post about {topic}.',
    expected_output='A 3-paragraph blog post about the latest advancements in {topic}.',
    agent=writer
)

# Create and run the crew
def run_crew(topic: str):
    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, write_task],
        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff(inputs={'topic': topic})
    print("\n\n######################")
    print("## Here is the result:")
    print("######################\n")
    print(result)
    return result

if __name__ == '__main__':
    # You can change the topic here
    topic_to_research = "AI in healthcare"
    print(f"Attempting to run crew for topic: {topic_to_research}")
    run_crew(topic_to_research)
