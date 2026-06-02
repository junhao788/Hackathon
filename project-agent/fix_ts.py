import re

filepath = r"C:\Users\admin\Desktop\Hackathon\project-agent\web\src\app\page.tsx"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Fix remainingText in StandupRenderer
content = content.replace(
    'let standupData: any = null;\n  try {\n    const jsonMatch = text.match(/\\{[\\s\\S]*\\}/);\n    if (jsonMatch) {\n      const parsed = JSON.parse(jsonMatch[0]);\n      if (parsed.standup) standupData = parsed.standup;\n    }',
    'let standupData: any = null;\n  let remainingText = "";\n  try {\n    const jsonMatch = text.match(/\\{[\\s\\S]*\\}/);\n    if (jsonMatch) {\n      const parsed = JSON.parse(jsonMatch[0]);\n      if (parsed.standup) standupData = parsed.standup;\n      remainingText = text.replace(jsonMatch[0], "").trim();\n    }'
)

# 2. Fix missing github_username in newMember reset
content = content.replace(
    "setNewMember({ name: '', username: '', role: 'Developer', skills: '', experience_level: 'Mid', availability: 'High' });",
    "setNewMember({ name: '', username: '', github_username: '', role: 'Developer', skills: '', experience_level: 'Mid', availability: 'High' });"
)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
print("Applied TS fixes.")
