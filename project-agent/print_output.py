filepath = r"C:\Users\admin\Desktop\Hackathon\project-agent\agent\server.py"
with open(filepath, 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('raise HTTPException(status_code=504, detail="Agent returned no valid JSON. It may have failed or timed out.")', 
    'print(f"AGENT OUTPUT:\\n{output}"); raise HTTPException(status_code=504, detail="Agent returned no valid JSON. Check server logs.")')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(c)
