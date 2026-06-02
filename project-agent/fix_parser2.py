filepath = r"C:\Users\admin\Desktop\Hackathon\project-agent\web\src\app\page.tsx"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

old_logic = '''  let boardData: any = inputBoardData;
  
  if (!boardData && text) {
    try {
      const firstBrace = text.indexOf('{');
      const lastBrace = text.lastIndexOf('}');
      if (firstBrace !== -1 && lastBrace !== -1 && lastBrace >= firstBrace) {
        const jsonString = text.substring(firstBrace, lastBrace + 1);
        boardData = JSON.parse(jsonString);
      } else {
        boardData = JSON.parse(text);
      }
    } catch (e) {
      return <div className="font-mono text-sm whitespace-pre-wrap">{text}</div>;
    }
  }'''

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

content = content.replace(old_logic, new_logic)

old_return = '''  return (
    <div className="flex gap-6 overflow-x-auto custom-scrollbar pb-4 h-full items-start">
      {boardData.board.map((col: any, cIdx: number) => {'''

new_return = '''  return (
    <div className="flex flex-col gap-4 h-full w-full">
      <div className="flex gap-6 overflow-x-auto custom-scrollbar pb-4 items-start shrink-0">
        {boardData.board.map((col: any, cIdx: number) => {'''

content = content.replace(old_return, new_return)

old_close = '''      </div>
    </div>
  );
};'''

new_close = '''      </div>
      {remainingText && (
        <div className="mt-4 p-4 bg-surface/30 border border-border/50 rounded-xl font-mono text-sm whitespace-pre-wrap text-text-secondary overflow-y-auto custom-scrollbar flex-1">
          {remainingText}
        </div>
      )}
    </div>
  );
};'''

content = content.replace(old_close, new_close)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
