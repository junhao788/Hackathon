import re

filepath = r"C:\Users\admin\Desktop\Hackathon\project-agent\web\src\app\page.tsx"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

old_logic = '''    let promptMsg = 'Execute SPRINT PROTOCOL.';
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
    }'''

new_logic = '''    let promptMsg = 'Execute SPRINT PROTOCOL.';
    if (sprintHistory && sprintHistory.length > 0) {
      const activeTasks: string[] = [];
      let hasExpiredSprints = false;

      sprintHistory.forEach((sprint: any) => {
        const isActive = (Date.now() - (sprint.created_at * 1000)) < (7 * 24 * 60 * 60 * 1000);
        if (isActive) {
          if (sprint.board) {
            sprint.board.forEach((col: any) => {
              if (col.cards) {
                col.cards.forEach((card: any) => {
                  if (!card.checked) activeTasks.push(card.title);
                });
              }
            });
          }
        } else {
          hasExpiredSprints = true;
        }
      });

      if (activeTasks.length > 0) {
        promptMsg += ` IMPORTANT: There are active Sprints currently running. You MUST NOT include the following tasks in the new sprint plan because they are already scheduled: ${JSON.stringify(activeTasks)}. Select completely different open issues.`;
      }
      
      if (hasExpiredSprints) {
        promptMsg += ` Additionally, previous Sprints have ended. If there are any open issues that were NOT completed in those expired Sprints, you SHOULD prioritize them and ROLL THEM OVER into this new Sprint.`;
      }
    }'''

content = content.replace(old_logic, new_logic)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
