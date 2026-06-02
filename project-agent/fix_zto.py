import re

filepath = r"C:\Users\admin\Desktop\Hackathon\project-agent\web\src\app\page.tsx"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

old_logic = '''          if (parsed.zero_to_one) {
            setZeroResult(parsed.zero_to_one);
            
            // --- NEW: Automatically run Sprint Planner and save it ---
            setZeroProgress(p => [...p, '🚀 🏃‍♂️ Executing Sprint Planner...']);
            try {
              const sprintController = new AbortController();
              const sprintTimeout = setTimeout(() => sprintController.abort(), 125000);
              
              const sprintRes = await fetch('http://localhost:8000/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: 'Execute SPRINT PROTOCOL.', project_id: selectedProjectId }),
                signal: sprintController.signal
              });
              clearTimeout(sprintTimeout);
              
              const sprintData = await sprintRes.json();
              const sprintPlanResult = sprintData.response || "";
              
              setZeroProgress(p => [...p, '💾 Saving Sprint Plan to Database...']);
              let pureJson = sprintPlanResult;
              const jsonMatch = sprintPlanResult.match(/\\{[\\s\\S]*\\}/);
              if (jsonMatch) pureJson = jsonMatch[0];
              
              await fetch(`http://localhost:8000/api/sprints/${selectedProjectId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ sprint_data: pureJson })
              });'''

# If the emojis don't match, we will just use a regex substitution that replaces from `if (parsed.zero_to_one)` down to `sprint_data: pureJson })`

new_logic = '''          if (parsed.zero_to_one) {
            setZeroResult(parsed.zero_to_one);
            
            const newProjectId = parsed.zero_to_one.project_id || selectedProjectId;
            if (parsed.zero_to_one.project_id) {
               await fetchProjects();
               setTimeout(() => { setSelectedProjectId(newProjectId.toString()); }, 500);
            }

            // --- NEW: Automatically run Sprint Planner and save it ---
            setZeroProgress(p => [...p, '🚀 🏃‍♂️ Executing Sprint Planner...']);
            try {
              const sprintController = new AbortController();
              const sprintTimeout = setTimeout(() => sprintController.abort(), 125000);
              
              const sprintRes = await fetch('http://localhost:8000/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: 'Execute SPRINT PROTOCOL.', project_id: newProjectId }),
                signal: sprintController.signal
              });
              clearTimeout(sprintTimeout);
              
              const sprintData = await sprintRes.json();
              const sprintPlanResult = sprintData.response || "";
              
              setZeroProgress(p => [...p, '💾 Saving Sprint Plan to Database...']);
              let pureJson = sprintPlanResult;
              const jsonMatch = sprintPlanResult.match(/\\{[\\s\\S]*\\}/);
              if (jsonMatch) pureJson = jsonMatch[0];
              
              await fetch(`http://localhost:8000/api/sprints/${newProjectId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ sprint_data: pureJson })
              });'''

# Try exact string replace first by finding the segment
start_idx = content.find('if (parsed.zero_to_one) {')
end_idx = content.find('body: JSON.stringify({ sprint_data: pureJson })', start_idx)

if start_idx != -1 and end_idx != -1:
    end_idx = content.find('});', end_idx) + 3
    segment = content[start_idx:end_idx]
    content = content.replace(segment, new_logic)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print("Success")
else:
    print("Failed to find segment")
