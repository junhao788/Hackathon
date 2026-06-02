filepath = r"C:\Users\admin\Desktop\Hackathon\project-agent\web\src\app\page.tsx"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

changes = 0

# ============================================================
# 1. FIX SCROLLBAR: The Sprint History kanban board wrapper
#    needs a fixed height with overflow, not just h-[400px]
# ============================================================
old_sprint_hist_wrapper = '<div className="h-[400px]">'
new_sprint_hist_wrapper = '<div className="h-[450px] overflow-y-auto custom-scrollbar">'
if old_sprint_hist_wrapper in content:
    content = content.replace(old_sprint_hist_wrapper, new_sprint_hist_wrapper)
    changes += 1
    print("[1] Fixed Sprint History kanban board wrapper height/scroll")

# ============================================================
# 2. FIX SCROLLBAR: The outer Kanban column wrapper (shrink-0
#    prevents the columns from being scrollable vertically)
# ============================================================
old_kanban_outer = 'className="flex gap-6 overflow-x-auto custom-scrollbar pb-4 items-start shrink-0"'
new_kanban_outer = 'className="flex gap-6 overflow-x-auto custom-scrollbar pb-4 items-start flex-1 min-h-0"'
if old_kanban_outer in content:
    content = content.replace(old_kanban_outer, new_kanban_outer)
    changes += 1
    print("[2] Fixed Kanban outer wrapper shrink-0 -> flex-1 min-h-0")

# ============================================================
# 3. ADD TIME ESTIMATE BADGE to Kanban cards
#    Insert right after the description block, before assigned_to
# ============================================================
old_assigned_block = '''{card.assigned_to && (
                    <div className={`mt-3 flex items-center justify-between bg-surface/60 rounded-lg p-2 border border-border/50 ${card.checked ? 'opacity-50' : ''}`}>'''

time_badge_plus_assigned = '''{card.estimated_hours && (
                    <div className={`mt-3 flex items-center gap-1.5 ${card.checked ? 'opacity-50' : ''}`}>
                      <Clock className="w-3.5 h-3.5 text-amber-400" />
                      <span className="text-xs font-bold text-amber-300 font-mono">{card.estimated_hours}h</span>
                    </div>
                  )}
                  {card.assigned_to && (
                    <div className={`mt-3 flex items-center justify-between bg-surface/60 rounded-lg p-2 border border-border/50 ${card.checked ? 'opacity-50' : ''}`}>'''

if old_assigned_block in content:
    content = content.replace(old_assigned_block, time_badge_plus_assigned)
    changes += 1
    print("[3] Added time estimate badge to Kanban cards")

# ============================================================
# 4. ADD SPRINT CAPACITY HEADER to Kanban board
#    Show "28/35h used" progress bar above columns
# ============================================================
old_board_start = '''  if (!boardData || !boardData.board) {
     return <div className="font-mono text-sm whitespace-pre-wrap">{text || JSON.stringify(inputBoardData)}</div>;
  }

  return (
    <div className="flex flex-col gap-4 h-full w-full">'''

new_board_start = '''  if (!boardData || !boardData.board) {
     return <div className="font-mono text-sm whitespace-pre-wrap">{text || JSON.stringify(inputBoardData)}</div>;
  }

  const sprintCapacity = boardData.sprint_capacity_hours || 35;
  const sprintUsed = boardData.sprint_used_hours || 0;
  const capacityPct = Math.min((sprintUsed / sprintCapacity) * 100, 100);
  const capacityColor = capacityPct > 90 ? 'bg-red-500' : capacityPct > 70 ? 'bg-amber-500' : 'bg-emerald-500';

  return (
    <div className="flex flex-col gap-4 h-full w-full">
      {sprintUsed > 0 && (
        <div className="flex items-center gap-3 px-1 shrink-0">
          <Clock className="w-4 h-4 text-amber-400 shrink-0" />
          <div className="flex-1 h-2.5 bg-surface/60 rounded-full border border-border/50 overflow-hidden">
            <div className={`h-full ${capacityColor} rounded-full transition-all duration-500`} style={{ width: `${capacityPct}%` }} />
          </div>
          <span className="text-xs font-mono font-bold text-text-secondary shrink-0">{sprintUsed}/{sprintCapacity}h</span>
        </div>
      )}'''

if old_board_start in content:
    content = content.replace(old_board_start, new_board_start)
    changes += 1
    print("[4] Added Sprint capacity progress bar")

# ============================================================
# 5. FIX Zero-to-One issues list: add scroll + max height
# ============================================================
old_issues_list = '''                          {zeroResult.issues && (
                            <ul className="space-y-1">'''
new_issues_list = '''                          {zeroResult.issues && (
                            <ul className="space-y-1 max-h-[300px] overflow-y-auto custom-scrollbar pr-1">'''
if old_issues_list in content:
    content = content.replace(old_issues_list, new_issues_list)
    changes += 1
    print("[5] Fixed Zero-to-One issues list scroll")

# ============================================================
# 6. ADD estimated_hours display in Zero-to-One issues list
# ============================================================
old_issue_item = '''                                  {issue.assigned_to && (
                                    <span className="text-cyan-300 font-bold ml-auto shrink-0">→ @{issue.assigned_to}</span>
                                  )}'''
new_issue_item = '''                                  {issue.estimated_hours && (
                                    <span className="text-amber-300 font-mono shrink-0">{issue.estimated_hours}h</span>
                                  )}
                                  {issue.assigned_to && (
                                    <span className="text-cyan-300 font-bold ml-auto shrink-0">→ @{issue.assigned_to}</span>
                                  )}'''
if old_issue_item in content:
    content = content.replace(old_issue_item, new_issue_item)
    changes += 1
    print("[6] Added estimated_hours to Zero-to-One issues list items")

# ============================================================
# 7. ADD column total hours in Kanban column header
# ============================================================
old_col_count = '''{col.cards?.length || 0}
              </span>'''
new_col_count = '''{col.cards?.length || 0}
              </span>
              {col.cards?.some((c: any) => c.estimated_hours) && (
                <span className="text-[10px] font-mono px-1.5 py-0.5 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/30">
                  {col.cards.reduce((sum: number, c: any) => sum + (c.estimated_hours || 0), 0)}h
                </span>
              )}'''
if old_col_count in content:
    content = content.replace(old_col_count, new_col_count)
    changes += 1
    print("[7] Added column total hours badge in Kanban column header")

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print(f"\nDone! Applied {changes} changes.")
