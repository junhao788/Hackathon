import re

filepath = r"C:\Users\admin\Desktop\Hackathon\project-agent\web\src\app\page.tsx"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "              {/* Bottom Row: Recent Activity Feed */}"
end_marker = "            </div>\n          )}\n\n          {/* TAB: STANDUP */}"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_dashboard_block = '''              {/* Bottom Row: Recent Activity Feed (Terminal Log) */}
              {dashboardMetrics && (dashboardMetrics.recent_issues?.length > 0 || dashboardMetrics.recent_mrs?.length > 0) && (
                (() => {
                  const combinedActivity = [
                    ...(dashboardMetrics.recent_issues || []).map((i: any) => ({ type: 'ISSUE', data: i })),
                    ...(dashboardMetrics.recent_mrs || []).map((m: any) => ({ type: 'MR', data: m }))
                  ].sort((a, b) => new Date(b.data.created_at).getTime() - new Date(a.data.created_at).getTime());
                  
                  return (
                    <div className="xl:col-span-2 flex flex-col mt-4">
                      <div className="flex items-center gap-3 px-4 py-2.5 bg-[#0a0a0a] border border-border/60 rounded-t-xl border-b-0">
                        <div className="flex gap-1.5">
                          <div className="w-3 h-3 rounded-full bg-red-500/80"></div>
                          <div className="w-3 h-3 rounded-full bg-amber-500/80"></div>
                          <div className="w-3 h-3 rounded-full bg-emerald-500/80"></div>
                        </div>
                        <span className="text-xs font-mono text-text-tertiary">agent@cmd:~/repo/activity-log</span>
                      </div>
                      <div className="bg-[#0a0a0a] border border-border/60 rounded-b-xl overflow-hidden shadow-2xl p-4 font-mono text-xs flex flex-col h-[400px] overflow-y-auto custom-scrollbar">
                        {combinedActivity.map((event, idx) => {
                          const dateObj = new Date(event.data.created_at);
                          const dateStr = `${dateObj.getFullYear()}-${String(dateObj.getMonth()+1).padStart(2, '0')}-${String(dateObj.getDate()).padStart(2, '0')} ${String(dateObj.getHours()).padStart(2, '0')}:${String(dateObj.getMinutes()).padStart(2, '0')}`;
                          
                          const isIssue = event.type === 'ISSUE';
                          const tagColor = isIssue ? 'text-amber-400' : 'text-blue-400';
                          const tagText = isIssue ? 'ISSUE' : ' MR  ';
                          const idPrefix = isIssue ? '#' : '!';
                          const actionWord = isIssue ? 'opened' : (event.data.state === 'merged' ? 'merged' : event.data.state === 'closed' ? 'closed' : 'opened');
                          
                          return (
                            <a 
                              key={idx} 
                              href={event.data.web_url} 
                              target="_blank" 
                              rel="noreferrer"
                              className="group flex flex-wrap md:flex-nowrap items-start md:items-center gap-x-3 gap-y-1 py-1.5 px-2 rounded hover:bg-white/5 transition-colors text-text-secondary"
                            >
                              <span className="text-text-tertiary/60 shrink-0 select-none">[{dateStr}]</span>
                              <span className={`shrink-0 select-none font-bold ${tagColor}`}>[{tagText}]</span>
                              <div className="flex-1 min-w-0 flex items-center gap-2 truncate">
                                <span className="text-emerald-400 shrink-0">@{event.data.author}</span>
                                <span className="shrink-0 text-text-tertiary select-none">{actionWord}</span>
                                <span className={`${tagColor} font-bold shrink-0`}>{idPrefix}{event.data.iid}:</span>
                                <span className="text-text-primary group-hover:text-white transition-colors truncate">{event.data.title}</span>
                              </div>
                            </a>
                          );
                        })}
                        <div className="mt-4 flex items-center gap-2 px-2 animate-pulse text-text-tertiary select-none">
                          <span className="text-emerald-400">➜</span>
                          <span className="text-blue-400">~</span>
                          <span className="w-2 h-4 bg-text-primary/70 inline-block" />
                        </div>
                      </div>
                    </div>
                  );
                })()
              )}
'''

    content = content[:start_idx] + new_dashboard_block + content[end_idx:]
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print("Success: Applied Terminal Log UI.")
else:
    print("Error: Could not find start_marker or end_marker.")
