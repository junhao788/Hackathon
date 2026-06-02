import re

filepath = r"C:\Users\admin\Desktop\Hackathon\project-agent\web\src\app\page.tsx"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# Define boundaries for replacement
start_marker = "              {/* Roster Grid */}"
end_marker = "              {/* TAB: ARCHITECT */}"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_roster_block = '''              {/* Roster Stats Header */}
              {rosterMembers.length > 0 && (
                <div className="flex items-center justify-between mb-4 mt-2 px-2">
                  <div className="flex items-center gap-6">
                    <div className="flex items-center gap-2">
                      <span className="text-xs text-text-tertiary uppercase tracking-wider font-semibold">Total:</span>
                      <span className="text-sm font-bold font-mono text-emerald-400">{rosterMembers.length}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs text-text-tertiary uppercase tracking-wider font-semibold">Available:</span>
                      <span className="text-sm font-bold font-mono text-cyan-400">{rosterMembers.filter((m: any) => m.availability === 'High').length}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs text-text-tertiary uppercase tracking-wider font-semibold">Seniors:</span>
                      <span className="text-sm font-bold font-mono text-amber-400">{rosterMembers.filter((m: any) => m.experience_level === 'Senior' || m.experience_level === 'Lead').length}</span>
                    </div>
                  </div>
                  <button
                    onClick={fetchRoster}
                    className="text-xs text-text-tertiary hover:text-emerald-400 transition-colors flex items-center gap-1"
                  >
                    <Activity className="w-3 h-3" /> Refresh
                  </button>
                </div>
              )}

              {/* Roster Grid -> Linear List */}
              {loadingRoster ? (
                <div className="dashboard-card flex items-center justify-center py-20">
                  <div className="flex flex-col items-center gap-4 text-text-tertiary">
                    <div className="w-8 h-8 border-4 border-emerald-500/30 border-t-emerald-400 rounded-full animate-spin" />
                    <p className="text-sm animate-pulse">Loading company roster...</p>
                  </div>
                </div>
              ) : rosterMembers.length === 0 ? (
                <div className="dashboard-card flex flex-col items-center justify-center py-20 text-text-tertiary">
                  <Users className="w-16 h-16 opacity-15 mb-4" />
                  <p className="text-lg font-medium mb-1">Talent Pool is Empty</p>
                  <p className="text-sm">Click "Add Member" above to register your first team member.</p>
                </div>
              ) : (
                <div className="flex flex-col bg-surface/20 border border-border/40 rounded-xl overflow-hidden shadow-sm">
                  {rosterMembers.map((dev: any, idx: number) => {
                    const avatarColor = dev.experience_level === 'Senior' || dev.experience_level === 'Lead'
                      ? 'bg-amber-900/40 border-amber-500/30 text-amber-400'
                      : dev.experience_level === 'Mid'
                        ? 'bg-blue-900/40 border-blue-500/30 text-blue-400'
                        : 'bg-emerald-900/40 border-emerald-500/30 text-emerald-400';
                    
                    return (
                      <div key={dev.username} className={`group flex items-center gap-4 p-3 border-b border-border/30 last:border-b-0 hover:bg-surface/50 transition-colors`}>
                        
                        {/* Avatar */}
                        <div className="shrink-0 pl-1">
                          <div className={`w-8 h-8 rounded-full border flex items-center justify-center text-xs font-bold uppercase shadow-sm ${avatarColor}`}>
                            {dev.name.split(' ').map((n: string) => n[0]).join('').substring(0, 2)}
                          </div>
                        </div>
                        
                        {/* Name & Username */}
                        <div className="flex flex-col min-w-[150px]">
                          <span className="text-sm font-medium text-text-primary">{dev.name}</span>
                          <span className="text-xs text-text-tertiary font-mono">@{dev.username}</span>
                        </div>

                        {/* Badges (Role & Seniority) */}
                        <div className="flex shrink-0 gap-1.5 hidden md:flex min-w-[150px]">
                          <span className="text-[10px] font-medium tracking-wide px-1.5 py-0.5 rounded-md border border-border/50 text-text-secondary bg-surface/40">
                            {dev.role}
                          </span>
                          <span className="text-[10px] font-medium tracking-wide px-1.5 py-0.5 rounded-md border border-border/50 text-text-secondary bg-surface/40">
                            {dev.experience_level}
                          </span>
                        </div>

                        {/* Skills */}
                        <div className="flex-1 flex flex-wrap gap-1.5 hidden lg:flex min-w-0">
                          {(dev.skills || []).map((skill: string, sIdx: number) => (
                            <span key={sIdx} className="text-[10px] bg-transparent border border-border/40 text-text-tertiary px-1.5 py-0.5 rounded hover:border-emerald-500/30 hover:text-emerald-300 transition-colors cursor-default whitespace-nowrap">
                              {skill}
                            </span>
                          ))}
                        </div>

                        {/* Actions */}
                        <div className="shrink-0 flex items-center gap-1 pl-3 pr-2 opacity-0 group-hover:opacity-100 transition-opacity ml-auto">
                          <button
                            onClick={() => handleEditClick(dev)}
                            className="p-1.5 rounded hover:bg-emerald-500/20 text-text-tertiary hover:text-emerald-400 transition-colors"
                            title={`Edit @${dev.username}`}
                          >
                            <Pencil className="w-3.5 h-3.5" />
                          </button>
                          <button
                            onClick={() => handleDeleteMember(dev.username)}
                            disabled={deletingUsername === dev.username}
                            className="p-1.5 rounded hover:bg-red-500/20 text-text-tertiary hover:text-red-400 transition-colors"
                            title={`Remove @${dev.username}`}
                          >
                            {deletingUsername === dev.username
                              ? <div className="w-3.5 h-3.5 border-2 border-red-400/30 border-t-red-400 rounded-full animate-spin" />
                              : <Trash2 className="w-3.5 h-3.5" />
                            }
                          </button>
                        </div>

                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          )}

'''

    content = content[:start_idx] + new_roster_block + content[end_idx:]
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print("Success: Replaced Roster grid UI with Linear-style list UI")
else:
    print("Error: Could not find start_marker or end_marker")
