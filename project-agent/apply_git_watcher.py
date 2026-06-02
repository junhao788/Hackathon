import re
import os

filepath = r"C:\Users\admin\Desktop\Hackathon\project-agent\agent\server.py"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

watcher_code = '''
# ── Autonomous Git Watcher ──────────────────────────
import threading
import time
import requests
import asyncio

MR_LAST_UPDATED_MEMORY = {}

def gitlab_watcher_loop():
    print("🤖 Autonomous Git Watcher started. Patrolling for new code every 15 seconds...")
    from agent.gitlab_api import GITLAB_API_URL, HEADERS
    
    def get_known_project_ids():
        import os, json
        sprints_path = os.path.join(os.path.dirname(__file__), "sprint_history.json")
        if os.path.exists(sprints_path):
            with open(sprints_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return list(data.keys())
        return ["howwerd0898/project-managing-dashboard"] # Fallback default

    while True:
        try:
            pids = get_known_project_ids()
            for pid in pids:
                encoded_pid = pid.replace("/", "%2F")
                url = f"{GITLAB_API_URL}/projects/{encoded_pid}/merge_requests?state=opened"
                resp = requests.get(url, headers=HEADERS, timeout=10)
                if resp.status_code == 200:
                    mrs = resp.json()
                    for mr in mrs:
                        mr_iid = mr.get("iid")
                        updated_at = mr.get("updated_at")
                        
                        memory_key = f"{pid}-{mr_iid}"
                        
                        if memory_key not in MR_LAST_UPDATED_MEMORY:
                            # First time seeing it since server start, initialize memory
                            MR_LAST_UPDATED_MEMORY[memory_key] = updated_at
                        else:
                            if MR_LAST_UPDATED_MEMORY[memory_key] != updated_at:
                                print(f"🚨 ALERT! MR #{mr_iid} in project {pid} was updated! Intercepting code...")
                                MR_LAST_UPDATED_MEMORY[memory_key] = updated_at
                                
                                # Run the review
                                try:
                                    loop = asyncio.new_event_loop()
                                    asyncio.set_event_loop(loop)
                                    loop.run_until_complete(execute_manual_review(pid, mr_iid))
                                    loop.close()
                                except Exception as e:
                                    print(f"Error running auto-review: {e}")
        except Exception as e:
            pass # Silent fail on network errors during watch
        time.sleep(15)

# Start watcher on server boot
watcher_thread = threading.Thread(target=gitlab_watcher_loop, daemon=True)
watcher_thread.start()
'''

if "Autonomous Git Watcher started" not in content:
    content += "\n" + watcher_code
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print("Success: Added Autonomous Git Watcher.")
else:
    print("Watcher already exists.")
