import re

filepath = r"C:\Users\admin\Desktop\Hackathon\project-agent\agent\server.py"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

correct_chat_fn = r'''async def chat(request: ChatRequest):
    try:
        print(f"Executing Agent with query: {request.message}")
        
        import os
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        adk_exe = os.path.join(base_dir, ".venv", "Scripts", "adk.exe")
        env_file_path = os.path.join(base_dir, ".env")
        
        # Load env vars properly
        merged_env = os.environ.copy()
        merged_env["PYTHONIOENCODING"] = "utf-8"
        if os.path.exists(env_file_path):
            with open(env_file_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        merged_env[k] = v.strip("'\"")
                        
        final_query = request.message
        if request.project_id:
            final_query = f"[TARGET PROJECT ID: {request.project_id}]\n\n{final_query}"
            
        import asyncio
        import subprocess as sp
        
        process = await asyncio.create_subprocess_exec(
            adk_exe, "run", "project_agent", "--prompt", final_query, "--env", env_file_path,
            env=merged_env,
            cwd=base_dir,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT
        )
        
        output_chunks = []
        async def read_stream():
            while True:
                line = await process.stdout.readline()
                if not line:
                    break
                output_chunks.append(line.decode("utf-8", errors="ignore"))
                
        try:
            await asyncio.wait_for(read_stream(), timeout=110.0)
        except asyncio.TimeoutError:
            print("Agent execution timed out! Force killing...")
            sp.run(f"taskkill /F /T /PID {process.pid}", shell=True, capture_output=True)
            
        output = "".join(output_chunks).strip()
        final_response = output
        
        if "[project_agent]:" in final_response:
            final_response = final_response.split("[project_agent]:")[-1].strip()
        elif "Agent:" in final_response:
            final_response = final_response.split("Agent:")[-1].strip()
            
        if "{" not in final_response:
            raise HTTPException(status_code=504, detail="Agent timed out and returned no valid JSON.")
            
        print("Agent execution completed successfully.")
        return {"response": final_response}
            
    except Exception as e:
        import traceback
        print(f"Error during agent execution: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))'''

pattern = re.compile(r'async def chat\(request: ChatRequest\):.*?def start_server\(\):', re.DOTALL)
new_content = pattern.sub(lambda m: correct_chat_fn + "\n\ndef start_server():", content)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(new_content)
