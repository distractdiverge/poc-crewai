import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import chainlit as cl 
from poc_crewai_developers.crew import PocCrewaiDevelopers
from datetime import datetime

# Initialize the crew once at startup
crew = PocCrewaiDevelopers()
crew_instance = crew.crew()

@cl.on_chat_start
async def greet():
    await cl.Message(content="Crew is ready! Type in a topic to research.").send()

@cl.step(type="tool")
async def tool_step(step: cl.Step):
    await cl.Message(content=step.tool_call).send()

@cl.on_message
async def reply(message: cl.Message):
    try:
        # Get the inputs from the message
        inputs = {
            'topic': message.content,
            'current_year': str(datetime.now().year)
        }
        
        # Run the crew with the inputs
        result = crew_instance.kickoff(inputs=inputs)
        
        # If result is a large object, summarize it
        if isinstance(result, dict) or isinstance(result, list):
            result_str = str(result)[:1000] + "..." if len(str(result)) > 1000 else str(result)
        else:
            result_str = str(result)
        
        # Send the result
        await cl.Message(content=result_str).send()
    except Exception as e:
        await cl.Message(content=f"Error processing request: {str(e)}").send()
