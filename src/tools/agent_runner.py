"""Utility to run ADK agents properly using Runner and Session."""

import os
import asyncio
import uuid

try:
    from google.adk import Runner
    from google.adk.sessions import InMemorySessionService
    from google.genai.types import Content, Part
    from google.adk.agents import Agent
except ImportError:
    Runner = None
    InMemorySessionService = None
    Content = None
    Part = None
    Agent = None


# Global session service instance
_session_service = None
_user_id = "default_user"
_app_name = "multiagent-dev-system"


def get_session_service():
    """Get or create a SessionService instance.
    
    Returns:
        SessionService instance
    """
    global _session_service
    
    if InMemorySessionService is None:
        raise ImportError("google-adk is not installed")
    
    if _session_service is None:
        _session_service = InMemorySessionService()
    
    return _session_service


async def _run_agent_async(agent, input_text: str):
    """Run an agent asynchronously.
    
    Args:
        agent: Agent instance to run
        input_text: Input text for the agent
        
    Returns:
        Agent response as string
    """
    if Runner is None or Content is None or Part is None:
        raise ImportError("google-adk is not installed")
    
    session_service = get_session_service()
    
    session_service = get_session_service()
    
    # Check if agent is a ProxyAgent or compatible
    if hasattr(agent, 'query') and (type(agent).__name__ == 'ProxyAgent' or hasattr(agent, 'proxy_url')):
        # Direct execution for ProxyAgent
        response = agent.query(input_text)
        return response

    # Create runner with the agent and app_name
    # Runner requires both app_name and agent
    runner = Runner(
        app_name=_app_name,
        agent=agent,
        session_service=session_service
    )
    
    # Create a session (async)
    session = await session_service.create_session(
        app_name=_app_name,
        user_id=_user_id
    )
    
    # Create Content from input text
    part = Part(text=input_text)
    content = Content(parts=[part])
    
    # Run the agent - this returns a generator
    # Implement retry logic for rate limits
    max_retries = 3
    retry_delay = 30
    
    # Initialize output variables
    output_parts = []
    last_output = None
    
    for attempt in range(max_retries):
        try:
            events = runner.run(
                user_id=_user_id,
                session_id=session.id,
                new_message=content
            )
            
            # Collect all events and extract the final response
            for event in events:
                # Check different event types for output
                if hasattr(event, 'output') and event.output:
                    if hasattr(event.output, 'text'):
                        output_parts.append(event.output.text)
                        last_output = event.output.text
                    elif isinstance(event.output, str):
                        output_parts.append(event.output)
                        last_output = event.output
                elif hasattr(event, 'content') and event.content:
                    if hasattr(event.content, 'text'):
                        output_parts.append(event.content.text)
                        last_output = event.content.text
                    elif isinstance(event.content, str):
                        output_parts.append(event.content)
                        last_output = event.content
                elif hasattr(event, 'text') and event.text:
                    output_parts.append(event.text)
                    last_output = event.text
                elif isinstance(event, dict):
                    output = event.get('output') or event.get('content')
                    if output:
                        if isinstance(output, dict) and 'text' in output:
                            output_parts.append(output['text'])
                            last_output = output['text']
                        else:
                            output_parts.append(str(output))
                            last_output = str(output)
            
            # If we get here, it succeeded
            break
            
        except Exception as e:
            print(f"DEBUG: Caught exception type: {type(e)}")
            print(f"DEBUG: Exception message: {str(e)}")
            
            if "ResourceExhausted" in str(e) or "429" in str(e) or "429" in str(getattr(e, 'message', '')):
                print(f"⚠️ API Rate Limit hit. Waiting {retry_delay}s before retry {attempt + 1}/{max_retries}...")
                await asyncio.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                print("DEBUG: Re-raising non-rate-limit exception")
                raise e
    
    # Return the last meaningful output or join all parts
    if last_output:
        return last_output
    elif output_parts:
        return ' '.join(str(p) for p in output_parts if p)
    else:
        return "No output received"


def run_agent(agent, input_text: str, state=None):
    """Run an agent with the given input.
    
    Args:
        agent: Agent instance to run
        input_text: Input text for the agent
        state: Optional state object (not used with ADK's state system)
        
    Returns:
        Agent response as string
    """
    # Check if we're in an async context
    try:
        loop = asyncio.get_running_loop()
        # We're in an async context, need to use nest_asyncio or thread executor
        try:
            import nest_asyncio
            nest_asyncio.apply()
            return asyncio.run(_run_agent_async(agent, input_text))
        except ImportError:
            # Use thread executor to run async code from sync context
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, _run_agent_async(agent, input_text))
                return future.result(timeout=300)  # 5 minute timeout
    except RuntimeError:
        # No running loop, create a new one
        return asyncio.run(_run_agent_async(agent, input_text))

