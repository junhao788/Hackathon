import asyncio
from agent.agent import root_agent
from google.adk.agents.context import Context

async def test_protocol():
    ctx = Context()
    print("Testing SPRINT PROTOCOL...")
    
    response = ""
    async for event in root_agent.run(ctx=ctx, node_input="Execute SPRINT PROTOCOL."):
        response += str(event) + "\n"
        
    print("\n--- FINAL RESPONSE ---")
    print(response)

if __name__ == "__main__":
    asyncio.run(test_protocol())
