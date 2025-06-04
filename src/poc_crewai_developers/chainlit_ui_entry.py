import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import chainlit as cl 
from poc_crewai_developers.crew import PocCrewaiDevelopers
from datetime import datetime
import json
from poc_crewai_developers.crew_chainlit_listener import ChainlitEventListener

crew_instance = None
crew_listener = None

def get_crew_instance():
    global crew_instance
    global crew_listener
    if crew_instance is None:
        crew_listener = ChainlitEventListener()
        crew_instance = PocCrewaiDevelopers().crew()

    return crew_instance

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
        crew_instance = get_crew_instance()
        #crew_instance.event_bus.register_listener(handle_crew_event)
        # result = crew_instance.kickoff(inputs=inputs)
        result = await cl.make_async(crew_instance.kickoff)(inputs=inputs)
        
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
            report = [task for task in result.tasks_output if task.name == "reporting_task"][0]
            await cl.Message(content=str(report.raw)).send()
            
    except Exception as e:
        await cl.Message(content=f"Error processing request: {str(e)}").send()

if __name__ == "__main__":
    from chainlit.cli import run_chainlit
    run_chainlit(__file__)
