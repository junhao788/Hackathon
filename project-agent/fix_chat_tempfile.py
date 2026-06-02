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
            
        import subprocess as sp
        import tempfile
        
        # We redirect stdout and stderr to a real file instead of a pipe.
        # This completely avoids the Windows pipe inheritance hang caused by grandchild node.js processes!
        # It also avoids the asyncio NotImplementedError for subprocesses on Windows SelectorEventLoop.
        
        temp_fd, temp_out_path = tempfile.mkstemp(text=True)
        os.close(temp_fd) # Close it so we can open it via standard open()
        
        try:
            with open(temp_out_path, 'w', encoding='utf-8') as out_f:
                # We use synchronous subprocess.run! Since it writes to a file, it will return the 
                # moment adk_exe finishes, without waiting for hanging grandchildren.
                sp.run(
                    [adk_exe, "run", "project_agent", "--prompt", final_query, "--env", env_file_path],
                    env=merged_env,
                    cwd=base_dir,
                    stdout=out_f,
                    stderr=sp.STDOUT,
                    timeout=110
                )
        except sp.TimeoutExpired:
            print("Agent execution timed out after 110 seconds! Recovering output from temp file...")
        except Exception as e:
            print(f"Subprocess run failed: {e}")
            
        # Read the output regardless of timeout or success
        with open(temp_out_path, 'r', encoding='utf-8', errors='ignore') as in_f:
            output = in_f.read()
            
        # Cleanup the temp file. If the node.js process is still running and holds it open, 
        # Windows might throw PermissionError, so we ignore it.
        try:
            os.remove(temp_out_path)
        except Exception:
            pass
            
        final_response = output.strip()
        
        if "[project_agent]:" in final_response:
            final_response = final_response.split("[project_agent]:")[-1].strip()
        elif "Agent:" in final_response:
            final_response = final_response.split("Agent:")[-1].strip()
            
        if "{" not in final_response:
            # Check if this is an HTTPException caught by the outer try-except
            from fastapi import HTTPException
            raise HTTPException(status_code=504, detail="Agent returned no valid JSON. It may have failed or timed out.")
            
        print("Agent execution completed successfully.")
        return {"response": final_response}
            
    except Exception as e:
        import traceback
        print(f"Error during agent execution: {traceback.format_exc()}")
        from fastapi import HTTPException
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))'''

pattern = re.compile(r'async def chat\(request: ChatRequest\):.*?def start_server\(\):', re.DOTALL)
new_content = pattern.sub(lambda m: correct_chat_fn + "\n\ndef start_server():", content)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(new_content)
