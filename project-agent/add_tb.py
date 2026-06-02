import traceback
import re
filepath = r'C:\Users\admin\Desktop\Hackathon\project-agent\agent\server.py'
with open(filepath, 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace('print(f"Error during agent execution: {e}")', 'import traceback; print(f"Error during agent execution: {traceback.format_exc()}")')
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(c)
