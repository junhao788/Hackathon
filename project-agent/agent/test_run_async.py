import asyncio
import os
import sys

# Add the project root to sys.path so we can import agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.agent import root_agent

async def test_agent():
    print("Testing run_async...")
    res = await root_agent.run_async("What is your name?")
    
    # Try to print whatever res is
    print("Type of res:", type(res))
    print("Result attributes:", dir(res))
    if hasattr(res, 'output'):
        print("Output:", res.output)
    else:
        print("Res itself:", res)

if __name__ == "__main__":
    asyncio.run(test_agent())
