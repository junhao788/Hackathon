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
                          <div className="flex flex-col bg-surface/20 border border-border/40 rounded-xl overflow-hidden shadow-sm">
                            {teamResult.filter((d: any) => d.in_project).map((dev: any, idx: number) => (
                              <div key={idx} className="group flex flex-col md:flex-row items-start md:items-center gap-4 p-3 border-b border-border/30 last:border-b-0 hover:bg-surface/50 transition-colors">
                                
                                {/* Identity Block */}
                                <div className="flex items-center gap-3 w-full md:w-[240px] shrink-0">
                                  <div className="w-8 h-8 rounded-full border border-emerald-500/30 flex items-center justify-center text-xs font-bold uppercase shadow-sm bg-emerald-900/40 text-emerald-400 shrink-0">
                                    {dev.name.split(' ').map((n: string) => n[0]).join('').substring(0, 2)}
                                  </div>
                                  <div className="flex flex-col min-w-0">
                                    <span className="text-sm font-medium text-text-primary truncate">{dev.name}</span>
                                    <span className="text-[10px] text-text-tertiary font-mono truncate">@{dev.username}</span>
                                  </div>
                                </div>
                                
                                {/* Role Badge */}
                                <div className="flex items-center w-full md:w-[150px] shrink-0">
                                  <span className="text-[10px] font-medium tracking-wide px-1.5 py-0.5 rounded-md border border-border/50 text-text-secondary bg-surface/40">
                                    {dev.role}
                                  </span>
                                </div>
                                
                                {/* Workload Summary */}
                                <div className="flex-1 min-w-0 flex flex-col justify-center">
                                  {dev.assigned_issues && dev.assigned_issues.length > 0 ? (
                                    <div className="flex flex-wrap items-center gap-2">
                                      <span className="text-[10px] font-bold text-accent bg-accent/10 px-1.5 py-0.5 rounded border border-accent/20 shrink-0">
                                        {dev.assigned_issues.length} Tasks
                                      </span>
                                      <div className="flex flex-wrap gap-1.5">
                                        {dev.assigned_issues.map((issue: any, iIdx: number) => (
                                          <a key={iIdx} href={issue.web_url} target="_blank" rel="noreferrer" className="flex items-center gap-1.5 px-2 py-0.5 rounded bg-surface border border-border/50 text-text-secondary hover:text-emerald-400 hover:border-emerald-500/30 transition-colors group/issue truncate max-w-[200px]">
                                            <span className="text-[10px] font-mono text-emerald-500/60 font-bold group-hover/issue:text-emerald-400">#{issue.iid}</span>
                                            <span className="text-[10px] truncate">{issue.title}</span>
                                          </a>
                                        ))}
                                      </div>
                                    </div>
                                  ) : (
                                    <span className="text-xs text-text-tertiary italic flex items-center gap-1">
                                      <CheckCircle2 className="w-3.5 h-3.5" /> No active tasks
                                    </span>
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
                          <div className="flex flex-col bg-surface/20 border border-border/40 rounded-xl overflow-hidden shadow-sm opacity-60 grayscale hover:opacity-100 hover:grayscale-0 transition-all duration-300">
                            {teamResult.filter((d: any) => d.in_project === false).map((dev: any, idx: number) => (
                              <div key={idx} className="group flex flex-col md:flex-row items-start md:items-center gap-4 p-3 border-b border-border/30 last:border-b-0 hover:bg-surface/50 transition-colors">
                                
                                {/* Identity Block */}
                                <div className="flex items-center gap-3 w-full md:w-[240px] shrink-0">
                                  <div className="w-8 h-8 rounded-full border border-border flex items-center justify-center text-xs font-bold uppercase shadow-sm bg-background text-text-tertiary shrink-0">
                                    {dev.name.split(' ').map((n: string) => n[0]).join('').substring(0, 2)}
                                  </div>
                                  <div className="flex flex-col min-w-0">
                                    <span className="text-sm font-medium text-text-secondary truncate">{dev.name}</span>
                                    <span className="text-[10px] text-text-tertiary font-mono truncate">@{dev.username}</span>
                                  </div>
                                </div>
                                
                                {/* Role Badge */}
                                <div className="flex items-center w-full md:w-[150px] shrink-0">
                                  <span className="text-[10px] font-medium tracking-wide px-1.5 py-0.5 rounded-md border border-border/50 text-text-tertiary bg-surface/40">
                                    {dev.role}
                                  </span>
                                </div>
                                
                                {/* Availability Notice */}
                                <div className="flex-1 flex items-center">
                                  <span className="text-[10px] font-mono text-text-tertiary/60">
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
    print("Success: Applied Linear UI for Team Workload.")
else:
    print("Error: Could not find start_marker or end_marker for Team Workload.")
