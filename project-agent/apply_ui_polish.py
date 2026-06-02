import re

filepath = r"C:\Users\admin\Desktop\Hackathon\project-agent\web\src\app\page.tsx"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Roster Alignments & Badges
# Replace Name & Username min-w-[150px] with fixed w-[160px] shrink-0
content = content.replace(
    '<div className="flex flex-col min-w-[150px]">',
    '<div className="flex flex-col w-[160px] shrink-0">'
)

# Replace Badges min-w-[150px] with fixed w-[180px] shrink-0
content = content.replace(
    '<div className="flex shrink-0 gap-1.5 hidden md:flex min-w-[150px]">',
    '<div className="flex shrink-0 gap-1.5 hidden md:flex w-[180px]">'
)

# Replace skills style
content = content.replace(
    'className="text-[10px] bg-transparent border border-border/40 text-text-tertiary px-1.5 py-0.5 rounded hover:border-emerald-500/30 hover:text-emerald-300 transition-colors cursor-default whitespace-nowrap"',
    'className="text-[10px] bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 px-1.5 py-0.5 rounded cursor-default whitespace-nowrap"'
)


# 2. Dashboard Recent Repository Activity
start_marker = "              {/* Bottom Row: Recent Activity Feed */}"
end_marker = "            </div>\n          )}\n\n          {/* TAB: STANDUP */}"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_dashboard_block = '''              {/* Bottom Row: Recent Activity Feed */}
              {dashboardMetrics && (dashboardMetrics.recent_issues?.length > 0 || dashboardMetrics.recent_mrs?.length > 0) && (
                <div className="xl:col-span-2 flex flex-col gap-3 mt-4">
                  <h3 className="text-sm font-bold text-text-primary uppercase tracking-widest flex items-center gap-2 mb-2">
                    <Activity className="w-4 h-4 text-accent" />
                    Recent Repository Activity
                  </h3>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    {/* Recent Issues */}
                    {dashboardMetrics.recent_issues?.length > 0 && (
                      <div className="flex flex-col">
                        <h4 className="text-xs font-bold text-text-secondary uppercase tracking-widest mb-3 flex items-center gap-2 pl-1">
                          <AlertCircle className="w-3.5 h-3.5 text-amber-400" /> Latest Issues
                        </h4>
                        <div className="flex flex-col bg-surface/20 border border-border/40 rounded-xl overflow-hidden shadow-sm">
                          {dashboardMetrics.recent_issues.map((issue: any, idx: number) => (
                            <a key={idx} href={issue.web_url} target="_blank" rel="noreferrer" className="group flex items-center gap-3 p-3 border-b border-border/30 last:border-b-0 hover:bg-surface/50 transition-colors">
                              <div className="shrink-0 pl-1">
                                <div className="w-4 h-4 rounded-full border border-dashed border-amber-500/50 opacity-60 group-hover:opacity-100 transition-opacity" />
                              </div>
                              <div className="flex flex-col flex-1 min-w-0">
                                <span className="text-sm font-medium text-text-primary truncate group-hover:text-amber-400 transition-colors">{issue.title}</span>
                                <div className="flex items-center gap-2 text-[10px] text-text-tertiary font-mono">
                                  <span className="text-amber-500/60 font-bold">#{issue.iid}</span>
                                  <span>•</span>
                                  <span>@{issue.author}</span>
                                </div>
                              </div>
                              <div className="shrink-0 flex items-center gap-2">
                                {issue.labels && issue.labels.length > 0 && (
                                  <span className="hidden md:inline-block px-1.5 py-0.5 rounded bg-surface border border-border/50 text-[9px] uppercase text-text-secondary">
                                    {issue.labels[0]}
                                  </span>
                                )}
                                <span className="text-[10px] text-text-tertiary font-mono whitespace-nowrap pl-2 border-l border-border/30 ml-1">
                                  {new Date(issue.created_at).toLocaleDateString()}
                                </span>
                              </div>
                            </a>
                          ))}
                        </div>
                      </div>
                    )}
                    
                    {/* Recent MRs */}
                    {dashboardMetrics.recent_mrs?.length > 0 && (
                      <div className="flex flex-col">
                        <h4 className="text-xs font-bold text-text-secondary uppercase tracking-widest mb-3 flex items-center gap-2 pl-1">
                          <GitPullRequest className="w-3.5 h-3.5 text-blue-400" /> Latest Merge Requests
                        </h4>
                        <div className="flex flex-col bg-surface/20 border border-border/40 rounded-xl overflow-hidden shadow-sm">
                          {dashboardMetrics.recent_mrs.map((mr: any, idx: number) => (
                            <a key={idx} href={mr.web_url} target="_blank" rel="noreferrer" className="group flex items-center gap-3 p-3 border-b border-border/30 last:border-b-0 hover:bg-surface/50 transition-colors">
                              <div className="shrink-0 pl-1">
                                <GitPullRequest className="w-4 h-4 text-blue-500/50 group-hover:text-blue-400 transition-colors" />
                              </div>
                              <div className="flex flex-col flex-1 min-w-0">
                                <span className="text-sm font-medium text-text-primary truncate group-hover:text-blue-400 transition-colors">{mr.title}</span>
                                <div className="flex items-center gap-2 text-[10px] text-text-tertiary font-mono">
                                  <span className="text-blue-500/60 font-bold">!{mr.iid}</span>
                                  <span>•</span>
                                  <span>@{mr.author}</span>
                                </div>
                              </div>
                              <div className="shrink-0 flex items-center gap-2">
                                <span className={`w-1.5 h-1.5 rounded-full ${mr.state === 'merged' ? 'bg-purple-500' : mr.state === 'closed' ? 'bg-red-500' : 'bg-emerald-500'}`} />
                                <span className="text-[10px] text-text-tertiary font-mono whitespace-nowrap pl-2 border-l border-border/30 ml-1">
                                  {new Date(mr.created_at).toLocaleDateString()}
                                </span>
                              </div>
                            </a>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}
'''

    content = content[:start_idx] + new_dashboard_block + content[end_idx:]
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print("Success: Applied all Linear UI polishes.")
else:
    print("Error: Could not find start_marker or end_marker for Dashboard Activity.")
