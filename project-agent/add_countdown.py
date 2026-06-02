import re

filepath = r"C:\Users\admin\Desktop\Hackathon\project-agent\web\src\app\page.tsx"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# Add the SprintCountdown component right before `export default function Dashboard() {`
countdown_comp = '''const SprintCountdown = ({ createdAt }: { createdAt: number }) => {
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
};

export default function Dashboard() {'''

if 'const SprintCountdown =' not in content:
    content = content.replace('export default function Dashboard() {', countdown_comp)

# Replace the sprint title rendering
old_title = '''                          <div>
                            <h4 className="font-bold text-text-primary text-lg">Sprint {sprintHistory.length - idx}</h4>
                            <p className="text-xs text-text-secondary font-mono mt-1">{new Date(sprint.created_at * 1000).toLocaleString()}</p>
                          </div>'''

new_title = '''                          <div>
                            <div className="flex items-center">
                              <h4 className="font-bold text-text-primary text-lg">Sprint {sprintHistory.length - idx}</h4>
                              <SprintCountdown createdAt={sprint.created_at} />
                            </div>
                            <p className="text-xs text-text-secondary font-mono mt-1">{new Date(sprint.created_at * 1000).toLocaleString()}</p>
                          </div>'''

content = content.replace(old_title, new_title)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
