import re

filepath = r"C:\Users\admin\Desktop\Hackathon\project-agent\agent\gitlab_api.py"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

correct_function = r'''def scaffold_project(project_id: str, clone_url: str, framework: str) -> dict:
    """
    Scaffolds a new project using the specified framework and pushes it to GitLab.
    Supported frameworks: react-ts, nextjs, vue-ts, python-fastapi, node-express,
                          fullstack-react-fastapi, fullstack-vue-fastapi, fullstack-react-express
    """
    import subprocess
    import tempfile
    import shutil
    import os
    
    auth_url = clone_url.replace("https://", f"https://oauth2:{GITLAB_TOKEN}@")
    temp_dir = tempfile.mkdtemp()
    
    try:
        subprocess.run(f"git clone {auth_url} .", cwd=temp_dir, shell=True, check=True, timeout=30)
        
        # Clear all files (like README.md from repo initialization) except .git so npm create doesn't abort
        for item in os.listdir(temp_dir):
            if item != ".git":
                item_path = os.path.join(temp_dir, item)
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)
                    
        if framework == "react-ts":
            subprocess.run("npm create vite@latest . -- --template react-ts", cwd=temp_dir, shell=True, check=True, timeout=60)
        elif framework == "vue-ts":
            subprocess.run("npm create vite@latest . -- --template vue-ts", cwd=temp_dir, shell=True, check=True, timeout=60)
        elif framework == "nextjs":
            subprocess.run("npx create-next-app@latest . --ts --tailwind --eslint --app --src-dir --import-alias \"@/*\" --use-npm", cwd=temp_dir, shell=True, check=True, timeout=60)
        elif framework == "python-fastapi":
            with open(os.path.join(temp_dir, "app.py"), "w") as f:
                f.write("from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get('/')\ndef read_root():\n    return {'Hello': 'World'}\n")
            with open(os.path.join(temp_dir, "requirements.txt"), "w") as f:
                f.write("fastapi\nuvicorn\n")
        elif framework == "node-express":
            subprocess.run("npm init -y", cwd=temp_dir, shell=True, check=True, timeout=30)
            subprocess.run("npm install express", cwd=temp_dir, shell=True, check=True, timeout=60)
            with open(os.path.join(temp_dir, "index.js"), "w") as f:
                f.write("const express = require('express');\nconst app = express();\n\napp.get('/', (req, res) => res.send('Hello World'));\n\napp.listen(3000, () => console.log('Server ready'));\n")
        elif framework.startswith("fullstack-"):
            frontend_dir = os.path.join(temp_dir, "frontend")
            backend_dir = os.path.join(temp_dir, "backend")
            os.mkdir(frontend_dir)
            os.mkdir(backend_dir)
            
            if "react" in framework:
                subprocess.run("npm create vite@latest . -- --template react-ts", cwd=frontend_dir, shell=True, check=True, timeout=60)
            elif "vue" in framework:
                subprocess.run("npm create vite@latest . -- --template vue-ts", cwd=frontend_dir, shell=True, check=True, timeout=60)
                
            if "fastapi" in framework:
                with open(os.path.join(backend_dir, "app.py"), "w") as f:
                    f.write("from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get('/')\ndef read_root():\n    return {'Hello': 'World'}\n")
                with open(os.path.join(backend_dir, "requirements.txt"), "w") as f:
                    f.write("fastapi\nuvicorn\n")
            elif "express" in framework:
                subprocess.run("npm init -y", cwd=backend_dir, shell=True, check=True, timeout=30)
                subprocess.run("npm install express", cwd=backend_dir, shell=True, check=True, timeout=60)
                with open(os.path.join(backend_dir, "index.js"), "w") as f:
                    f.write("const express = require('express');\nconst app = express();\n\napp.get('/', (req, res) => res.send('Hello World'));\n\napp.listen(3000, () => console.log('Server ready'));\n")
        
        subprocess.run("git config user.name \"Project Agent AI\"", cwd=temp_dir, shell=True)
        subprocess.run("git config user.email \"agent@example.com\"", cwd=temp_dir, shell=True)
        
        subprocess.run("git add .", cwd=temp_dir, shell=True, check=True, timeout=30)
        subprocess.run("git commit -m \"Initial scaffold from Project Agent AI\"", cwd=temp_dir, shell=True, check=True, timeout=30)
        subprocess.run("git branch -M main", cwd=temp_dir, shell=True, timeout=10)
        subprocess.run("git push -u origin main --force", cwd=temp_dir, shell=True, check=True, timeout=30)
        
        return {"status": "success", "message": f"Successfully scaffolded {framework} and pushed to repository."}
    except Exception as e:'''

pattern = re.compile(r'def scaffold_project.*?except Exception as e:', re.DOTALL)
new_content = pattern.sub(lambda m: correct_function, content)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(new_content)
