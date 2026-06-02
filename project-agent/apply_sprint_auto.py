import re

filepath = r"C:\Users\admin\Desktop\Hackathon\project-agent\web\src\app\page.tsx"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# =====================================================
# CHANGE 1: Update SprintCountdown to accept onExpired callback
# =====================================================
old_countdown = '''const SprintCountdown = ({ createdAt }: { createdAt: number }) => {
  const [timeLeft, setTimeLeft] = useState('');
  
  useEffect(() => {
    const updateCountdown = () => {
      const endsAt = (createdAt * 1000) + (7 * 24 * 60 * 60 * 1000); // 7 days later
      const now = Date.now();
      const diff = endsAt - now;
      
      if (diff <= 0) {
        setTimeLeft('Sprint Ended');
        return;
      }
      
      const d = Math.floor(diff / (1000 * 60 * 60 * 24));
      const h = Math.floor((diff / (1000 * 60 * 60)) % 24);
      const m = Math.floor((diff / 1000 / 60) % 60);
      const s = Math.floor((diff / 1000) % 60);
      
      setTimeLeft(`${d}d ${h}h ${m}m ${s}s remaining`);
    };
    
    updateCountdown();
    const interval = setInterval(updateCountdown, 1000);
    return () => clearInterval(interval);
  }, [createdAt]);

  return <span className="ml-3 px-2 py-0.5 bg-accent/20 text-accent text-xs rounded-md font-mono border border-accent/30 animate-pulse flex items-center gap-1.5"><Clock className="w-3 h-3" />{timeLeft}</span>;
};'''

new_countdown = '''const SprintCountdown = ({ createdAt, onExpired }: { createdAt: number; onExpired?: () => void }) => {
  const [timeLeft, setTimeLeft] = useState('');
  const [hasExpired, setHasExpired] = useState(false);
  const expiredCallbackRef = useRef(false);
  
  useEffect(() => {
    const updateCountdown = () => {
      const endsAt = (createdAt * 1000) + (7 * 24 * 60 * 60 * 1000); // 7 days later
      const now = Date.now();
      const diff = endsAt - now;
      
      if (diff <= 0) {
        setTimeLeft('Sprint Ended');
        setHasExpired(true);
        if (onExpired && !expiredCallbackRef.current) {
          expiredCallbackRef.current = true;
          onExpired();
        }
        return;
      }
      
      const d = Math.floor(diff / (1000 * 60 * 60 * 24));
      const h = Math.floor((diff / (1000 * 60 * 60)) % 24);
      const m = Math.floor((diff / 1000 / 60) % 60);
      const s = Math.floor((diff / 1000) % 60);
      
      setTimeLeft(`${d}d ${h}h ${m}m ${s}s remaining`);
    };
    
    updateCountdown();
    const interval = setInterval(updateCountdown, 1000);
    return () => clearInterval(interval);
  }, [createdAt, onExpired]);

  if (hasExpired) {
    return <span className="ml-3 px-2 py-0.5 bg-red-500/20 text-red-400 text-xs rounded-md font-mono border border-red-500/30 flex items-center gap-1.5"><Clock className="w-3 h-3" />Sprint Ended</span>;
  }

  return <span className="ml-3 px-2 py-0.5 bg-accent/20 text-accent text-xs rounded-md font-mono border border-accent/30 animate-pulse flex items-center gap-1.5"><Clock className="w-3 h-3" />{timeLeft}</span>;
};'''

content = content.replace(old_countdown, new_countdown)

# =====================================================
# CHANGE 2: Add useRef import if not already there
# =====================================================
if 'useRef' not in content:
    content = content.replace(
        "import { useState, useEffect } from 'react';",
        "import { useState, useEffect, useRef } from 'react';"
    )
    content = content.replace(
        "import { useState, useEffect,",
        "import { useState, useEffect, useRef,"
    )

# If useRef still not found, try another pattern
if 'useRef' not in content:
    content = content.replace(
        "} from 'react';",
        ", useRef } from 'react';",
        1  # Only first occurrence
    )

# =====================================================
# CHANGE 3: Add handleCompleteAndAutoGenerate function
# after handleSaveSprint function
# =====================================================
auto_gen_function = '''
  // ── Auto-Generate Next Sprint (Carryover Logic) ──────────────────────
  const [autoGeneratingSprintId, setAutoGeneratingSprintId] = useState<string | null>(null);
  
  const handleCompleteAndAutoGenerate = async (expiredSprint: any) => {
    if (!selectedProjectId || autoGeneratingSprintId) return;
    
    const sprintId = expiredSprint?.sprint_id;
    if (!sprintId) return;
    
    // Prevent duplicate auto-generations
    setAutoGeneratingSprintId(sprintId);
    setLoadingSprint(true);
    setSprintPlan('⚡ Sprint expired! AI is automatically generating the next Sprint with carryover tasks...');
    
    // Collect unchecked (incomplete) tasks from the expired sprint
    const carryoverTasks: string[] = [];
    if (expiredSprint.board) {
      expiredSprint.board.forEach((col: any) => {
        if (col.cards) {
          col.cards.forEach((card: any) => {
            if (!card.checked) {
              carryoverTasks.push(card.title);
            }
          });
        }
      });
    }
    
    let promptMsg = 'Execute SPRINT PROTOCOL.';
    
    if (carryoverTasks.length > 0) {
      promptMsg += ` [SYSTEM DIRECTIVE - CARRYOVER]: The previous Sprint has ENDED. The following ${carryoverTasks.length} tasks were NOT completed and MUST be carried over into this new Sprint. You MUST include ALL of them, tag each with a "CARRYOVER ⚠️" badge, and place them in P0 CRITICAL priority: ${JSON.stringify(carryoverTasks)}. Then fill the remaining capacity with new open issues from the backlog.`;
    } else {
      promptMsg += ' The previous Sprint was fully completed! Generate a fresh Sprint from the remaining open issues backlog.';
    }
    
    try {
      const res = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: promptMsg, project_id: selectedProjectId })
      });
      const data = await res.json();
      const sprintPlanResult = data.response || "";
      
      // Auto-save the new sprint
      let pureJson = sprintPlanResult;
      const jsonMatch = sprintPlanResult.match(/\\{[\\s\\S]*\\}/);
      if (jsonMatch) pureJson = jsonMatch[0];
      
      await fetch(`http://localhost:8000/api/sprints/${selectedProjectId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sprint_data: pureJson })
      });
      
      await fetchSprintHistory();
      setSprintPlan(null);
    } catch (e) {
      setSprintPlan('Error auto-generating next Sprint.');
    }
    setLoadingSprint(false);
    setAutoGeneratingSprintId(null);
  };

'''

# Insert the auto-gen function after handleSaveSprint
save_sprint_end = "    setSavingSprint(false);\n  };\n\n  const handleSyncSprint"
content = content.replace(
    save_sprint_end,
    "    setSavingSprint(false);\n  };\n" + auto_gen_function + "  const handleSyncSprint"
)

# =====================================================
# CHANGE 4: Update SprintCountdown usage in Sprint History to pass onExpired
# =====================================================
old_countdown_usage = '<SprintCountdown createdAt={sprint.created_at} />'
new_countdown_usage = '<SprintCountdown createdAt={sprint.created_at} onExpired={() => handleCompleteAndAutoGenerate(sprint)} />'
content = content.replace(old_countdown_usage, new_countdown_usage)

# =====================================================
# CHANGE 5: Add a "Complete Sprint (Test)" button next to "Sync AI Progress"
# =====================================================
old_sync_button_block = """                          <button
                            onClick={() => handleSyncSprint(sprint)}
                            disabled={syncingSprintId === sprint.sprint_id}
                            className={`px-4 py-2 text-sm font-bold rounded-lg transition-all flex items-center gap-2 shadow-lg shadow-emerald-500/10 ${
                              syncingSprintId === sprint.sprint_id
                                ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/50 cursor-not-allowed'
                                : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 hover:bg-emerald-500/20 hover:shadow-emerald-500/30'
                            }`}
                          >
                            <Bot className={`w-4 h-4 ${syncingSprintId === sprint.sprint_id ? 'animate-pulse' : ''}`} />
                            {syncingSprintId === sprint.sprint_id ? 'AI Syncing...' : 'Sync AI Progress'}
                          </button>"""

new_sync_button_block = """                          <div className="flex gap-2">
                            <button
                              onClick={() => handleCompleteAndAutoGenerate(sprint)}
                              disabled={autoGeneratingSprintId === sprint.sprint_id || loadingSprint}
                              className={`px-3 py-2 text-sm font-bold rounded-lg transition-all flex items-center gap-2 ${
                                autoGeneratingSprintId === sprint.sprint_id
                                  ? 'bg-red-500/20 text-red-300 border border-red-500/50 cursor-not-allowed'
                                  : 'bg-red-500/10 text-red-400 border border-red-500/30 hover:bg-red-500/20'
                              }`}
                            >
                              <Zap className={`w-4 h-4 ${autoGeneratingSprintId === sprint.sprint_id ? 'animate-pulse' : ''}`} />
                              {autoGeneratingSprintId === sprint.sprint_id ? 'Auto-Planning...' : 'Complete & Auto-Plan Next'}
                            </button>
                            <button
                              onClick={() => handleSyncSprint(sprint)}
                              disabled={syncingSprintId === sprint.sprint_id}
                              className={`px-3 py-2 text-sm font-bold rounded-lg transition-all flex items-center gap-2 shadow-lg shadow-emerald-500/10 ${
                                syncingSprintId === sprint.sprint_id
                                  ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/50 cursor-not-allowed'
                                  : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 hover:bg-emerald-500/20 hover:shadow-emerald-500/30'
                              }`}
                            >
                              <Bot className={`w-4 h-4 ${syncingSprintId === sprint.sprint_id ? 'animate-pulse' : ''}`} />
                              {syncingSprintId === sprint.sprint_id ? 'AI Syncing...' : 'Sync AI Progress'}
                            </button>
                          </div>"""

content = content.replace(old_sync_button_block, new_sync_button_block)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("Success: Applied Sprint Auto-Generation with Carryover logic.")
