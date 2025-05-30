import chainlit as cl 
from poc_crewai_developers.crew import PocCrewaiDevelopers
from datetime import datetime

@cl.on_chat_start
async def greet():
    await cl.Message(content="Crew is ready! ask me anything!").send()

@cl.on_message
async def reply(message: cl.Message):
    crew = PocCrewaiDevelopers()
    crew_instance = crew.crew()
    
    # Get the inputs from the message
    inputs = {
        'topic': message.content,
        'current_year': str(datetime.now().year)
    }
    
    # Run the crew with the inputs (not async)
    result = crew_instance.kickoff(inputs=inputs)
    
    # Send the result
    await cl.Message(content=str(result)).send()
