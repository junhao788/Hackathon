import re

filepath = r"C:\Users\admin\Desktop\Hackathon\project-agent\web\src\app\page.tsx"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "                      {/* IN PROJECT SECTION */}"
end_marker = "                    </div>\n                  )}\n\n                 {/* Raw fallback */}"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_team_block = '''                      {/* IN PROJECT SECTION */}
                      <div className="mb-8">
                        <h3 className="text-base font-bold text-text-primary mb-4 flex items-center gap-2 uppercase tracking-wide">
                          <Activity className="w-5 h-5 text-accent" /> Active in Project ({teamResult.filter((d: any) => d.in_project).length})
                        </h3>
                        {teamResult.filter((d: any) => d.in_project).length === 0 ? (
                          <div className="bg-surface/30 border border-border/50 rounded-xl p-6 text-center text-text-tertiary text-sm">
                            No team members are currently assigned to this project.
                          </div>
                        ) : (
                          <div className="flex flex-col gap-6">
                            {teamResult.filter((d: any) => d.in_project).map((dev: any, idx: number) => (
                              <div key={idx} className="flex flex-col bg-surface/20 border border-border/40 rounded-xl overflow-hidden shadow-sm">
                                
                                {/* Tier 1: Assignee Header */}
                                <div className="flex items-center justify-between p-3 bg-surface/40 border-b border-border/30">
                                  <div className="flex items-center gap-4">
                                    <div className="w-8 h-8 rounded-full border border-emerald-500/30 flex items-center justify-center text-xs font-bold uppercase shadow-sm bg-emerald-900/40 text-emerald-400 shrink-0">
                                      {dev.name.split(' ').map((n: string) => n[0]).join('').substring(0, 2)}
                                    </div>
                                    <div className="flex flex-col">
                                      <span className="text-sm font-bold text-text-primary flex items-center gap-2">
                                        {dev.name} 
                                        <span className="text-[10px] font-medium tracking-wide px-1.5 py-0.5 rounded-md border border-border/50 text-text-secondary bg-surface/40">
                                          {dev.role}
                                        </span>
                                      </span>
                                      <span className="text-[10px] text-text-tertiary font-mono">@{dev.username}</span>
                                    </div>
                                  </div>
                                  <div className="pr-2">
                                    <span className="text-[10px] font-bold text-accent bg-accent/10 px-2 py-1 rounded border border-accent/20">
                                      {dev.assigned_issues?.length || 0} Tasks
                                    </span>
                                  </div>
                                </div>
                                
                                {/* Tier 2: Task List */}
                                <div className="flex flex-col">
                                  {dev.assigned_issues && dev.assigned_issues.length > 0 ? (
                                    dev.assigned_issues.map((issue: any, iIdx: number) => (
                                      <a key={iIdx} href={issue.web_url} target="_blank" rel="noreferrer" className="group flex items-center gap-3 px-4 py-2.5 border-b border-border/20 last:border-b-0 hover:bg-surface/30 transition-colors">
                                        {/* Indentation line & Icon */}
                                        <div className="flex items-center gap-3 shrink-0">
                                          <div className="w-4 h-px bg-border/40 ml-2"></div>
                                          <div className="w-3 h-3 rounded-full border border-dashed border-accent/50 opacity-60 group-hover:opacity-100 group-hover:border-solid transition-all bg-accent/10" />
                                        </div>
                                        {/* Task Info */}
                                        <div className="flex items-center gap-2 flex-1 min-w-0">
                                          <span className="text-xs font-mono text-accent/80 font-bold shrink-0">#{issue.iid}</span>
                                          <span className="text-xs text-text-secondary group-hover:text-text-primary transition-colors truncate">{issue.title}</span>
                                        </div>
                                      </a>
                                    ))
                                  ) : (
                                    <div className="flex items-center gap-3 px-4 py-3 text-text-tertiary text-xs italic bg-surface/10">
                                      <div className="w-4 h-px bg-border/40 ml-2 shrink-0"></div>
                                      <CheckCircle2 className="w-3.5 h-3.5 opacity-50 shrink-0 text-emerald-400" /> No active tasks assigned. Available for work!
                                    </div>
                                  )}
                                </div>
                              </div>
                            ))}
                          </div>
                        )}
                      </div>

                      {/* NOT IN PROJECT SECTION */}
                      <div>
                        <h3 className="text-base font-bold text-text-secondary mb-4 flex items-center gap-2 uppercase tracking-wide">
                          <Briefcase className="w-5 h-5" /> Available Company Talent ({teamResult.filter((d: any) => d.in_project === false).length})
                        </h3>
                        {teamResult.filter((d: any) => d.in_project === false).length === 0 ? (
                          <div className="bg-surface/30 border border-border/50 rounded-xl p-6 text-center text-text-tertiary text-sm">
                            All talent from your company roster is currently active in this project.
                          </div>
                        ) : (
                          <div className="flex flex-col bg-surface/10 border border-border/30 rounded-xl overflow-hidden shadow-sm opacity-60 hover:opacity-100 transition-all duration-300">
                            {teamResult.filter((d: any) => d.in_project === false).map((dev: any, idx: number) => (
                              <div key={idx} className="group flex items-center justify-between p-3 border-b border-border/20 last:border-b-0 hover:bg-surface/30 transition-colors">
                                <div className="flex items-center gap-4">
                                  <div className="w-8 h-8 rounded-full border border-border flex items-center justify-center text-xs font-bold uppercase shadow-sm bg-background text-text-tertiary shrink-0">
                                    {dev.name.split(' ').map((n: string) => n[0]).join('').substring(0, 2)}
                                  </div>
                                  <div className="flex flex-col">
                                    <span className="text-sm font-medium text-text-secondary">{dev.name}</span>
                                    <span className="text-[10px] text-text-tertiary font-mono">@{dev.username}</span>
                                  </div>
                                </div>
                                <div className="flex items-center gap-4">
                                  <span className="text-[10px] font-medium tracking-wide px-1.5 py-0.5 rounded-md border border-border/50 text-text-tertiary bg-surface/40">
                                    {dev.role}
                                  </span>
                                  <span className="text-[10px] font-mono text-text-tertiary/60 hidden md:block">
                                    // Not currently active in this project
                                  </span>
                                </div>
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
'''

    content = content[:start_idx] + new_team_block + content[end_idx:]
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print("Success: Applied Grouped List Layout for Team Workload.")
else:
    print("Error: Could not find start_marker or end_marker for Team Workload.")
