import os
from agent.gitlab_api import scaffold_project

# Need to find the clone URL for Werd How's repo. 
# We'll just run scaffold_project and see if it fails.
project_id = "82559130" # Wait, 82559130 is the default in gitlab_api.py, but what is the ID of real-time-chat-app?
