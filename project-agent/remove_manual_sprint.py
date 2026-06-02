import re

filepath = r"C:\Users\admin\Desktop\Hackathon\project-agent\web\src\app\page.tsx"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "              <div className=\"dashboard-card min-h-[500px] flex flex-col\">\n                 <div className=\"flex justify-between items-center mb-6\">\n                   <div>\n                     <h2 className=\"text-xl font-semibold text-text-primary\">Sprint Planner</h2>"
end_marker = "                    {sprintPlan ? <AgentOutputCardRenderer text={sprintPlan} /> : <span className=\"text-text-tertiary font-mono text-sm\">No sprint plan generated yet.</span>}\n                 </div>\n              </div>"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    end_idx += len(end_marker)
    # Remove the block entirely
    content = content[:start_idx] + content[end_idx:]
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print("Success: Removed manual Sprint Planner dashboard card.")
else:
    print("Error: Could not find start or end marker.")
