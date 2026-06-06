# OmniLead 🚀
The first fully autonomous AI Tech Lead & Project Manager for your GitLab ecosystem.
## Why We Built This (Our Motivation)
In modern software development, Tech Leads and Project Managers spend **up to 40% of their time on administrative overhead** rather than actual engineering.
- They manually bootstrap repositories and set up boilerplate code.
- They hunt down available developers across the company and guess their capacity.
- They manually break down raw product ideas into dozens of Jira/GitLab issues.
- They spend hours doing tedious Code Reviews on Merge Requests, pointing out trivial mistakes like missing types or leftover `console.log`s.
This process drains engineering velocity and burns out senior talent. **We built OmniLead to eliminate this friction.** 
Our vision is to give every software team a tireless, deterministic AI agent that handles the entire project management lifecycle—from "Zero-to-One" idea inception, to smart talent assignment, to continuous code reviews. We want developers to focus purely on coding, while OmniLead handles the management.
## Project Description

**The Solution: What OmniLead Does**
OmniLead acts as an autonomous Staff Engineer and Project Manager integrated directly into your GitLab environment. You just give it a raw idea, and OmniLead builds the foundation, manages the team, and guards the code quality.

**Core Capabilities:**
- 🚀 **Launchpad (Zero-to-One):** Give OmniLead a raw project idea, and it executes a complete bootstrap. It creates the repository, scaffolds the tech stack, designs a 3-layer architectural blueprint (Pages, APIs, DB), and batches it into prioritized GitLab issues.
- 👥 **Smart Talent Acquisition:** OmniLead dynamically analyzes global workloads across all projects and invites the perfect mix of developers (e.g., 1 Junior + 1 Senior per stack), strictly avoiding overloaded engineers.
- 🧠 **AI Tech Lead:** OmniLead acts as an autonomous gatekeeper for your main branch. It reviews Merge Requests for security, performance, and types. It auto-merges pristine code and auto-remediates minor issues (pushing fix commits automatically).
- ⏱️ **Autonomous Sprint Planner:** It organizes issues into active Sprints with strict capacity enforcement (max 25 hours/dev) and prioritizes foundational backend dependencies automatically.
## How it's Made
**Architecture & Flow**
```text
You → [Project Idea] → OmniLead (Launchpad)
                               ↓
                      Creates Repo & Scaffolds Code
                               ↓
            Analyzes Global Workloads & Invites Available Devs
                               ↓
              Generates Blueprint & Dispatches GitLab Issues
                               ↓
Developers → [Push Code & Open MR] → OmniLead (AI Tech Lead)
                               ↓
                Code Review (Security, Types, Performance)
                               ↓
                 [Pass] → Auto-Merge & Close Issue
                 [Minor Fail] → Auto-Remediate (Push Fix Commit)
```
**The Stack**
The system relies on deterministic rules alongside LLM intelligence to prevent hallucinated project management.
- **Agent Engine & Backend:** Python, FastAPI, and Google Agent Development Kit (ADK).
- **Intelligence:** Google Gemini (3.1 Flash-Lite & 2.5 Flash) leveraging the Model Context Protocol (MCP).
- **Frontend Dashboard:** Next.js, React, and Tailwind CSS.
- **Integrations:** GitLab REST API and Webhooks.
