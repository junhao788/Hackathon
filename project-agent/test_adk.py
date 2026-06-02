import asyncio
from google.adk.agents import Agent

async def main():
    agent = Agent(name="test", model="gemini-2.5-flash", instruction="Say hello.")
    
    # Try using __call__
    print("Testing __call__...")
    try:
        res = await agent("Hello")
        print(res)
    except Exception as e:
        print("Error with __call__:", e)
        
    print("\nTesting run() generator...")
    try:
        from google.adk.core.context import Context
        async for event in agent.run(ctx=Context(), node_input="Hello"):
            print("Event:", event)
    except Exception as e:
        print("Error with run():", e)

if __name__ == "__main__":
    asyncio.run(main())
