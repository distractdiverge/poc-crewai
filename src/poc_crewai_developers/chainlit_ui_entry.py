import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import chainlit as cl 
from poc_crewai_developers.crew import PocCrewaiDevelopers
from datetime import datetime
import json

# Initialize the crew once at startup
crew = PocCrewaiDevelopers()
crew_instance = crew.crew()

async def handle_crew_event(event):
    """Handle CrewAI events and convert them to Chainlit messages"""
    if event.type == "tool_call":
        await cl.Message(content=f"**Tool Call**: {event.content}").send()
    elif event.type == "agent_message":
        await cl.Message(content=f"**Agent Message**: {event.content}", author=event.agent_name).send()
    elif event.type == "plan":
        await cl.Message(content=f"**Planning**: {event.content}", author=event.agent_name).send()
    elif event.type == "self_check":
        await cl.Message(content=f"**Self-Check**: {event.content}", author=event.agent_name).send()
    elif event.type == "task_start":
        await cl.Message(content=f"**Task Start**: {event.task_name}", author="System").send()
    elif event.type == "task_end":
        await cl.Message(content=f"**Task End**: {event.task_name}", author="System").send()

@cl.on_chat_start
async def greet():
    await cl.Message(content="Crew is ready! Type in a topic to research.").send()

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
        
        # Process the result and display all steps
        if isinstance(result, dict):
            # Display each agent's output
            for agent_name, agent_output in result.items():
                if isinstance(agent_output, dict):
                    content = agent_output.get("content", "")
                    
                    # Display planning steps if available
                    if "Plan:" in content:
                        await cl.Message(
                            content=f"**{agent_name} Planning:**\n{content}",
                            author=agent_name
                        ).send()
                    
                    # Display self-checks if available
                    if "Self-Check:" in content:
                        await cl.Message(
                            content=f"**{agent_name} Self-Check:**\n{content}",
                            author=agent_name
                        ).send()
                    
                    # Display the main content
                    await cl.Message(
                        content=f"**{agent_name} Output:**\n{json.dumps(agent_output, indent=2)}",
                        author=agent_name
                    ).send()
        else:
            # If result is not a dict, just display it as is
            await cl.Message(content=str(result)).send()
            
    except Exception as e:
        await cl.Message(content=f"Error processing request: {str(e)}").send()
