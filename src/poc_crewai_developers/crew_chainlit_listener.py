from crewai.utilities.events import (
    CrewKickoffStartedEvent,
    CrewKickoffCompletedEvent,
    CrewKickoffFailedEvent,
    AgentExecutionStartedEvent,
    AgentExecutionCompletedEvent,
    AgentExecutionErrorEvent,
    TaskStartedEvent,
    TaskCompletedEvent,
    TaskEvaluationEvent,
    TaskFailedEvent,
    ToolUsageStartedEvent,
    ToolUsageFinishedEvent,
    ToolUsageErrorEvent,
)
from crewai.utilities.events.base_event_listener import BaseEventListener
import asyncio 
import chainlit as cl 



class ChainlitEventListener(BaseEventListener):
    def __init__(self):
        super().__init__()

    def _emit(self, message, author = None):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(cl.Message(content=message, author=author).send())

    def setup_listeners(self, crewai_event_bus):
        @crewai_event_bus.on(CrewKickoffStartedEvent)
        def on_crew_started(source, event):
            self._emit(f"Crew '{event.crew_name}' has started execution!")
        
        @crewai_event_bus.on(CrewKickoffCompletedEvent)
        def on_crew_completed(source, event):
            self._emit(f"Crew '{event.crew_name}' has completed execution!")
        
        @crewai_event_bus.on(CrewKickoffFailedEvent)
        def on_crew_failed(source, event):
            self._emit(f"Crew '{event.crew_name}' has failed execution!")
        
        @crewai_event_bus.on(AgentExecutionStartedEvent)
        def on_agent_execution_started(source, event):
            self._emit(f"Agent '{event.agent.role}' execution started", author=event.agent.role)

        @crewai_event_bus.on(AgentExecutionCompletedEvent)
        def on_agent_execution_completed(source, event):
            #TODO: Emit event.output (The final result of the agent)
            self._emit(f"Agent '{event.agent.role}' execution completed", author=event.agent.role)
            self._emit(f"{event.output}", author=event.agent.role)

        @crewai_event_bus.on(AgentExecutionErrorEvent)
        def on_agent_execution_error(source, event):
            self._emit(f"Agent '{event.agent.role}' execution error: {event.error}", author=event.agent.role)

        @crewai_event_bus.on(TaskStartedEvent)
        def on_task_started(source, event):
            # TODO: Emit 'source.description' (What task is being done)
            #self._emit(f"Task '{event.task.name}' started")
            self._emit(f"{event.agent.role}: {event.task.description}")

        @crewai_event_bus.on(TaskCompletedEvent)
        def on_task_completed(source, event):
            self._emit(f"Task '{event.task.name}' completed")
        
        @crewai_event_bus.on(TaskEvaluationEvent)
        def on_task_evaluation(source, event):
            self._emit(f"Task '{event.task.name}' evaluation: {event.evaluation}")
        
        @crewai_event_bus.on(TaskFailedEvent)
        def on_task_failed(source, event):
            self._emit(f"Task '{event.task.name}' failed: {event.error}")
        
        @crewai_event_bus.on(ToolUsageStartedEvent)
        def on_tool_started(source, event):
            self._emit(f"Starting tool: {event.tool_name}")
        
        @crewai_event_bus.on(ToolUsageFinishedEvent)
        def on_tool_finished(source, event):
            self._emit(f"Tool '{event.tool_name}' completed")
        
        @crewai_event_bus.on(ToolUsageErrorEvent)
        def on_tool_error(source, event):
            self._emit(f"Tool '{event.tool_name}' error: {event.error}")
        
        
        
        #if event.type == "tool_call":
        #    await cl.Message(content=f"**Tool Call**: {event.content}").send()
        #elif event.type == "agent_message":
        #    await cl.Message(content=f"**Agent Message**: {event.content}", author=event.agent_name).send()
        #elif event.type == "plan":
        #    await cl.Message(content=f"**Planning**: {event.content}", author=event.agent_name).send()
        #elif event.type == "self_check":
        #    await cl.Message(content=f"**Self-Check**: {event.content}", author=event.agent_name).send()
        #elif event.type == "task_start":
        #    await cl.Message(content=f"**Task Start**: {event.task_name}", author="System").send()
        #elif event.type == "task_end":
        #    await cl.Message(content=f"**Task End**: {event.task_name}", author="System").send()
