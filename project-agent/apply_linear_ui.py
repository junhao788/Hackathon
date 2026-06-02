import re

filepath = r"C:\Users\admin\Desktop\Hackathon\project-agent\web\src\app\page.tsx"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# Find the start of the return block for AgentOutputCardRenderer
start_str = '''  return (
    <div className="flex flex-col gap-4 h-full w-full">'''
end_str = '''  );
};

const SprintCountdown ='''

start_idx = content.find(start_str)
end_idx = content.find(end_str)

if start_idx != -1 and end_idx != -1:
    new_return_block = '''  return (
    <div className="flex flex-col gap-6 w-full h-full pb-4">
      {/* Capacity Header */}
      {sprintUsed > 0 && (
        <div className="flex items-center gap-3 px-2 shrink-0">
          <Clock className="w-4 h-4 text-amber-400 shrink-0" />
          <div className="flex-1 h-2.5 bg-surface/60 rounded-full border border-border/50 overflow-hidden">
            <div className={`h-full ${capacityColor} rounded-full transition-all duration-500`} style={{ width: `${capacityPct}%` }} />
          </div>
          <span className="text-xs font-mono font-bold text-text-secondary shrink-0">{sprintUsed}/{sprintCapacity}h</span>
        </div>
      )}
      
      {/* List Groups container */}
      <div className="flex flex-col gap-8 overflow-y-auto custom-scrollbar pr-2 pb-8 flex-1 min-h-0">
        {boardData.board.map((col: any, cIdx: number) => {
          const colors = getColumnColor(col.columnName);
          const colHours = col.cards?.reduce((sum: number, c: any) => sum + (c.estimated_hours || 0), 0) || 0;
          
          return (
            <div key={cIdx} className="flex flex-col">
              {/* Minimalist Group Header */}
              <div className="flex items-center gap-3 mb-3 pl-2">
                <h3 className={`text-xs font-bold tracking-widest uppercase flex items-center gap-2 ${colors.text}`}>
                  {getColumnIcon(col.columnName)}
                  {col.columnName}
                </h3>
                <span className="text-text-tertiary text-xs">•</span>
                <span className="text-text-secondary text-xs font-medium">{col.cards?.length || 0} issues</span>
                {colHours > 0 && (
                  <>
                    <span className="text-text-tertiary text-xs">•</span>
                    <span className="text-amber-500 text-xs font-mono">{colHours}h</span>
                  </>
                )}
              </div>
              
              {/* Linear-style List Container */}
              <div className="flex flex-col bg-surface/20 border border-border/40 rounded-xl overflow-hidden shadow-sm">
                {col.cards && col.cards.map((card: any, cardIdx: number) => (
                  <div key={cardIdx} className={`group flex items-center gap-3 p-3 border-b border-border/30 last:border-b-0 hover:bg-surface/50 transition-colors cursor-default ${card.checked ? 'opacity-60 bg-surface/10' : ''}`}>
                    {/* Status Icon */}
                    <div className="shrink-0 pl-1">
                      {card.checked ? (
                         <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                      ) : (
                         <div className={`w-4 h-4 rounded-full border border-dashed ${colors.text.replace('text-', 'border-')} opacity-50 group-hover:opacity-100 transition-opacity`} />
                      )}
                    </div>
                    
                    {/* Title */}
                    <div className="flex-1 min-w-0">
                       <p className={`text-sm font-medium text-text-primary truncate ${card.checked ? 'line-through text-text-secondary' : ''}`}>
                         {card.title}
                       </p>
                    </div>
                    
                    {/* Badges */}
                    {card.badges && card.badges.length > 0 && (
                      <div className="flex shrink-0 gap-1.5 hidden md:flex">
                        {card.badges.map((badge: string, bIdx: number) => (
                          <span key={bIdx} className={`text-[10px] font-medium tracking-wide px-1.5 py-0.5 rounded-md border border-border/50 text-text-secondary bg-surface/40 group-hover:border-border/80 transition-colors`}>
                            {badge}
                          </span>
                        ))}
                      </div>
                    )}
                    
                    {/* Time Estimate */}
                    {card.estimated_hours && (
                      <div className="shrink-0 flex items-center justify-end min-w-[32px] ml-2">
                        <span className="text-xs font-mono text-amber-500/80 group-hover:text-amber-400 transition-colors">{card.estimated_hours}h</span>
                      </div>
                    )}
                    
                    {/* Assignee */}
                    {card.assigned_to && (
                      <div className="shrink-0 flex items-center gap-2 pl-3 ml-3 border-l border-border/40">
                         <div className="w-5 h-5 rounded-full bg-cyan-900/40 border border-cyan-500/30 flex items-center justify-center">
                            <span className="text-[10px] font-bold text-cyan-400 uppercase">{card.assigned_to.charAt(0)}</span>
                         </div>
                         <span className="text-xs text-text-secondary hidden lg:inline-block truncate max-w-[80px]">
                           {card.assigned_to}
                         </span>
                      </div>
                    )}
                  </div>
                ))}
                
                {(!col.cards || col.cards.length === 0) && (
                  <div className="p-4 flex items-center gap-2 text-text-tertiary text-xs italic">
                    <div className="w-4 h-4 rounded-full border border-dashed border-border/40 shrink-0 opacity-40 ml-1" />
                    No issues in this group
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
      
      {remainingText && (
        <div className="mt-2 p-3 bg-surface/20 border border-border/40 rounded-lg font-mono text-xs whitespace-pre-wrap text-text-secondary overflow-y-auto custom-scrollbar shrink-0 max-h-32">
          {remainingText}
        </div>
      )}
    </div>'''

    content = content[:start_idx] + new_return_block + "\n" + content[end_idx:]
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print("Success: Replaced Kanban UI with Linear-style UI")
else:
    print("Error: Could not find start_str or end_str")
