import re

filepath = r"C:\Users\admin\Desktop\Hackathon\project-agent\web\src\app\page.tsx"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Remove state variable
content = content.replace(
    'const [architectIdea, setArchitectIdea] = useState(\'\');\n  const [syncingArchitect, setSyncingArchitect] = useState(false);',
    'const [architectIdea, setArchitectIdea] = useState(\'\');'
)

# 2. Remove handleSyncArchitect function
content = re.sub(r'  const handleSyncArchitect = async \(\) => \{[\s\S]*?setSyncingArchitect\(false\);\n  \};\n\n  const handleArchitect', '  const handleArchitect', content)

# 3. Remove the button
old_header = '''                 <div className="flex items-center gap-3 mb-2">
                   <Zap className="w-6 h-6 text-yellow-400" />
                   <h2 className="text-xl font-semibold text-text-primary">Auto-Architect</h2>
                   {architectResult && (
                     <button onClick={handleSyncArchitect} disabled={syncingArchitect} className="ml-auto px-4 py-1.5 bg-yellow-400/20 text-yellow-400 text-sm font-semibold rounded-lg hover:bg-yellow-400/30 transition-colors">
                       {syncingArchitect ? 'Pushing Tasks...' : 'Push Tasks to GitLab'}
                     </button>
                   )}
                 </div>'''

new_header = '''                 <div className="flex items-center gap-3 mb-2">
                   <Zap className="w-6 h-6 text-yellow-400" />
                   <h2 className="text-xl font-semibold text-text-primary">Auto-Architect</h2>
                 </div>'''

content = content.replace(old_header, new_header)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
