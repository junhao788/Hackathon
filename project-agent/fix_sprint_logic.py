import re

filepath = r"C:\Users\admin\Desktop\Hackathon\project-agent\web\src\app\page.tsx"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

old_fn = '''  const handleGenerateSprint = async () => {
    setLoadingSprint(true);
    setSprintPlan('Executing SPRINT PROTOCOL...');
    try {
      const res = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: 'Execute SPRINT PROTOCOL.', project_id: selectedProjectId })
      });'''

new_fn = '''  const handleGenerateSprint = async () => {
    setLoadingSprint(true);
    setSprintPlan('Executing SPRINT PROTOCOL...');
    
    let promptMsg = 'Execute SPRINT PROTOCOL.';
    if (sprintHistory && sprintHistory.length > 0) {
      const latestSprint = sprintHistory[0];
      const tasksInSprint = [];
      if (latestSprint.board) {
        latestSprint.board.forEach((col: any) => {
          if (col.cards) col.cards.forEach((card: any) => tasksInSprint.push(card.title));
        });
      }
      if (tasksInSprint.length > 0) {
        promptMsg += ` IMPORTANT: There is currently an active Sprint. You MUST NOT include the following tasks in the new sprint plan because they are already being worked on: ${JSON.stringify(tasksInSprint)}. Select the NEXT highest priority open issues from the backlog for this new sprint.`;
      }
    }

    try {
      const res = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: promptMsg, project_id: selectedProjectId })
      });'''

content = content.replace(old_fn, new_fn)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
