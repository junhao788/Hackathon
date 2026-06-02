import re

filepath = r"C:\Users\admin\Desktop\Hackathon\project-agent\web\src\app\page.tsx"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add state variable
if 'const [syncingArchitect, setSyncingArchitect] = useState(false);' not in content:
    content = content.replace(
        'const [architectIdea, setArchitectIdea] = useState(\'\');',
        'const [architectIdea, setArchitectIdea] = useState(\'\');\n  const [syncingArchitect, setSyncingArchitect] = useState(false);'
    )

# 2. Add handleSyncArchitect function
sync_fn = '''  const handleSyncArchitect = async () => {
    if (!selectedProjectId || !architectResult) return;
    setSyncingArchitect(true);
    try {
      await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          message: `Please read the following JSON Kanban board, and use your GitLab MCP tools to create issues in the project for every card in the board. Check existing issues first. Board: ${architectResult}`, 
          project_id: selectedProjectId 
        })
      });
      alert('Tasks successfully pushed to GitLab! You can check your backlog.');
    } catch (e) {
      alert('Failed to push tasks.');
    }
    setSyncingArchitect(false);
  };

  const handleArchitect'''

content = content.replace('  const handleArchitect', sync_fn)

# 3. Add the button
header = '''                 <div className="flex items-center gap-3 mb-2">
                   <Zap className="w-6 h-6 text-yellow-400" />
                   <h2 className="text-xl font-semibold text-text-primary">Auto-Architect</h2>
                 </div>'''

new_header = '''                 <div className="flex items-center gap-3 mb-2">
                   <Zap className="w-6 h-6 text-yellow-400" />
                   <h2 className="text-xl font-semibold text-text-primary">Auto-Architect</h2>
                   {architectResult && (
                     <button onClick={handleSyncArchitect} disabled={syncingArchitect} className="ml-auto px-4 py-1.5 bg-yellow-400/20 text-yellow-400 text-sm font-semibold rounded-lg hover:bg-yellow-400/30 transition-colors">
                       {syncingArchitect ? 'Pushing Tasks...' : 'Push Tasks to GitLab'}
                     </button>
                   )}
                 </div>'''

content = content.replace(header, new_header)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
