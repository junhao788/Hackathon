import re

filepath = r"C:\Users\admin\Desktop\Hackathon\project-agent\web\src\app\page.tsx"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

new_logic = '''  let boardData: any = inputBoardData;
  let remainingText = "";
  
  if (!boardData && text) {
    let jsonString = text;
    const jsonMatch = text.match(/```(?:json)?\\s*(\\{[\\s\\S]*?\\})\\s*```/);
    if (jsonMatch) {
      jsonString = jsonMatch[1];
      remainingText = text.replace(jsonMatch[0], '').trim();
      try { boardData = JSON.parse(jsonString); } catch(e) {}
    } else {
      const firstBrace = text.indexOf('{');
      if (firstBrace !== -1) {
        for (let i = text.length - 1; i >= firstBrace; i--) {
          if (text[i] === '}') {
            try {
              jsonString = text.substring(firstBrace, i + 1);
              boardData = JSON.parse(jsonString);
              remainingText = text.substring(0, firstBrace) + text.substring(i + 1);
              remainingText = remainingText.trim();
              break;
            } catch(e) {}
          }
        }
      }
    }
    
    if (!boardData) {
      try { boardData = JSON.parse(text); } catch (e) {
        return <div className="font-mono text-sm whitespace-pre-wrap">{text}</div>;
      }
    }
  }'''

# Replace the parsing logic
content = re.sub(
    r'let boardData: any = inputBoardData;[\s\S]*?if \(!boardData \|\| !boardData\.board\) \{',
    new_logic + '\n  \n  if (!boardData || !boardData.board) {',
    content
)

# Render remaining text below the board
render_return = '''  return (
    <div className="flex flex-col gap-4 h-full w-full">
      <div className="flex gap-6 overflow-x-auto custom-scrollbar pb-4 items-start shrink-0">
        {boardData.board.map((col: any, cIdx: number) => {'''

content = content.replace('  return (\n    <div className="flex gap-6 overflow-x-auto custom-scrollbar pb-4 h-full items-start">\n      {boardData.board.map((col: any, cIdx: number) => {', render_return)

# Add closing tag for flex-col and render remainingText
closing_div = '''      </div>
      {remainingText && (
        <div className="mt-4 p-4 bg-surface/30 border border-border/50 rounded-xl font-mono text-sm whitespace-pre-wrap text-text-secondary overflow-y-auto custom-scrollbar flex-1">
          {remainingText}
        </div>
      )}
    </div>
  );
};'''

content = re.sub(r'      </div>\n    </div>\n  \);\n\};', closing_div, content)


with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
