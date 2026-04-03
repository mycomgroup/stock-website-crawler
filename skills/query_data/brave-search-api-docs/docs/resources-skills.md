---
id: "url-57158399"
type: "api"
title: "Skills"
url: "https://api-dashboard.search.brave.com/documentation/resources/skills"
description: "The Brave Search API now supports Skills—a powerful way to extend\nAI capabilities with modular, reusable workflows. These skills,\na standardized format now open-sourced here,\nenable your AI editor or CLI to dynamically load instructions, scripts, and resources\nfor specialized tasks that the Brave API can help with."
source: ""
tags: []
crawl_time: "2026-03-18T02:32:03.717Z"
metadata:
  endpoint: "https://api.search.brave.com/res/v1/llm/context?q=search+API+for+grounding+LLMs"
  method: "GET"
  sections:
    - {"level":"H2","title":"Overview","content":["The Brave Search API now supports Skills—a powerful way to extend\nAI capabilities with modular, reusable workflows. These skills,\na standardized format now open-sourced here,\nenable your AI editor or CLI to dynamically load instructions, scripts, and resources\nfor specialized tasks that the Brave API can help with.","Skills work with Claude Code, Cursor, GitHub Copilot, Codex, Gemini CLI,\nVS Code, Windsurf, OpenClaw, Cline, Goose, Amp, Roo Code, and many other agents that support the Agent\nSkills standard.","Brave Skills are available as a GitHub repository."],"codeBlocks":[]}
    - {"level":"H2","title":"Quick Setup","content":["Claude Code Install skills to Claude Code CLI  Cursor Install skills to Cursor  OpenAI Codex Install skills to Codex CLI"],"codeBlocks":[]}
    - {"level":"H3","title":"Claude Code","content":["Install skills to Claude Code CLI"],"codeBlocks":[]}
    - {"level":"H3","title":"Cursor","content":["Install skills to Cursor"],"codeBlocks":[]}
    - {"level":"H3","title":"OpenAI Codex","content":["Install skills to Codex CLI"],"codeBlocks":[]}
    - {"level":"H2","title":"Prerequisites","content":["Get a Brave Search API key from your dashboard.","Security tip: Prefer agent-native config over shell profile exports.\nCoding agents can access environment variables — scoped configs limit exposure.\nSee API key setup for all options.","Add to ~/.claude/settings.json (docs):","This makes the key available in all Claude Code sessions. For per-project use,\nadd to .claude/settings.local.json (gitignored) with the same format.","Option 1 — direnv (directory-scoped, auto-loads/unloads):","Option 2 — Shell profile (~/.zshrc or ~/.bashrc):","Then restart Cursor (launch from terminal or fully quit and reopen — reloading\nthe window is not enough). Cursor inherits environment variables from your shell.\nYou can also add skills via Settings > Rules > Add Rule > Remote Rule using\nthe GitHub URL.","Option 1 — config.toml (docs):","Option 2 — Shell profile (~/.zshrc or ~/.bashrc):","Then restart your terminal. Codex reads environment variables from the shell\n(CLI, app, and IDE extension).","Add to ~/.openclaw/.env (docs):","Or add to ~/.openclaw/openclaw.json under the skill’s config:","Option 1 — direnv (directory-scoped, auto-loads/unloads):","Option 2 — Shell profile (~/.zshrc or ~/.bashrc):"],"codeBlocks":["{\n  \"env\": {\n    \"BRAVE_SEARCH_API_KEY\": \"your-key\"\n  }\n}","# Install direnv (https://direnv.net), then in your project directory:\necho 'export BRAVE_SEARCH_API_KEY=\"your-key\"' >> .envrc\ndirenv allow","export BRAVE_SEARCH_API_KEY=\"your-key\"","# ~/.codex/config.toml\n[shell_environment_policy]\nset = { BRAVE_SEARCH_API_KEY = \"your-key\" }","export BRAVE_SEARCH_API_KEY=\"your-key\"","BRAVE_SEARCH_API_KEY=your-key","{\n  \"skills\": {\n    \"entries\": {\n      \"brave-search\": {\n        \"env\": {\n          \"BRAVE_SEARCH_API_KEY\": \"your-key\"\n        }\n      }\n    }\n  }\n}","# Install direnv (https://direnv.net), then in your project directory:\necho 'export BRAVE_SEARCH_API_KEY=\"your-key\"' >> .envrc\ndirenv allow","export BRAVE_SEARCH_API_KEY=\"your-key\""]}
    - {"level":"H3","title":"Claude Code","content":["Add to ~/.claude/settings.json (docs):","This makes the key available in all Claude Code sessions. For per-project use,\nadd to .claude/settings.local.json (gitignored) with the same format."],"codeBlocks":["{\n  \"env\": {\n    \"BRAVE_SEARCH_API_KEY\": \"your-key\"\n  }\n}"]}
    - {"level":"H3","title":"Cursor","content":["Option 1 — direnv (directory-scoped, auto-loads/unloads):","Option 2 — Shell profile (~/.zshrc or ~/.bashrc):","Then restart Cursor (launch from terminal or fully quit and reopen — reloading\nthe window is not enough). Cursor inherits environment variables from your shell.\nYou can also add skills via Settings > Rules > Add Rule > Remote Rule using\nthe GitHub URL."],"codeBlocks":["# Install direnv (https://direnv.net), then in your project directory:\necho 'export BRAVE_SEARCH_API_KEY=\"your-key\"' >> .envrc\ndirenv allow","export BRAVE_SEARCH_API_KEY=\"your-key\""]}
    - {"level":"H3","title":"Codex","content":["Option 1 — config.toml (docs):","Option 2 — Shell profile (~/.zshrc or ~/.bashrc):","Then restart your terminal. Codex reads environment variables from the shell\n(CLI, app, and IDE extension)."],"codeBlocks":["# ~/.codex/config.toml\n[shell_environment_policy]\nset = { BRAVE_SEARCH_API_KEY = \"your-key\" }","export BRAVE_SEARCH_API_KEY=\"your-key\""]}
    - {"level":"H3","title":"OpenClaw","content":["Add to ~/.openclaw/.env (docs):","Or add to ~/.openclaw/openclaw.json under the skill’s config:"],"codeBlocks":["BRAVE_SEARCH_API_KEY=your-key","{\n  \"skills\": {\n    \"entries\": {\n      \"brave-search\": {\n        \"env\": {\n          \"BRAVE_SEARCH_API_KEY\": \"your-key\"\n        }\n      }\n    }\n  }\n}"]}
    - {"level":"H3","title":"Other agents","content":["Option 1 — direnv (directory-scoped, auto-loads/unloads):","Option 2 — Shell profile (~/.zshrc or ~/.bashrc):"],"codeBlocks":["# Install direnv (https://direnv.net), then in your project directory:\necho 'export BRAVE_SEARCH_API_KEY=\"your-key\"' >> .envrc\ndirenv allow","export BRAVE_SEARCH_API_KEY=\"your-key\""]}
    - {"level":"H2","title":"Installation","content":["All agents below support the Agent Skills standard\nand read SKILL.md files from their skills directory.","Skills documentation","Plugin marketplace (auto-updates, no git needed):","curl (no git, no marketplace):","Manual (git clone + cp):","Skills documentation","Remote Rule (no terminal needed):","Settings → Rules → Project Rules → Add Rule → Remote Rule → paste https://github.com/brave/brave-search-skills","Manual (cp — requires git clone above):","Cursor natively reads skills from .cursor/skills/, .claude/skills/, and .codex/skills/ at both project and user level.","Manual (cp — requires git clone above):","Skills documentation","Skill installer (built-in — ask Codex to install skills from https://github.com/brave/brave-search-skills).","Manual (cp — requires git clone above):","Codex reads from .agents/skills/ at repo, parent, root, and user levels. Skills work across the CLI, desktop app, and IDE extension.","Manual (cp — requires git clone above):","Skills documentation","Manual (cp — requires git clone above):","curl (adjust the target directory for your agent):","Or copy skills from a git clone to the agent’s skills directory. All agents following the Agent Skills standard read SKILL.md files from their skills folder.","See openskills on GitHub for details.","Claude Code marketplace: updates automatically, or run /plugin marketplace update brave-search.","curl: re-run the curl command above to overwrite with the latest version.","git clone: pull the latest changes and re-copy:","Or re-run the OpenSkills install command to overwrite with the latest version.","See the full list of compatible agents at agentskills.io."],"codeBlocks":["/plugin marketplace add brave/brave-search-skills\n/plugin install brave-search-skills@brave-search","# User-level (available in all projects)\nmkdir -p ~/.claude/skills && curl -sL https://github.com/brave/brave-search-skills/archive/main.tar.gz | tar xz -C ~/.claude/skills --strip-components=2 brave-search-skills-main/skills\n\n# Project-level\nmkdir -p .claude/skills && curl -sL https://github.com/brave/brave-search-skills/archive/main.tar.gz | tar xz -C .claude/skills --strip-components=2 brave-search-skills-main/skills","git clone https://github.com/brave/brave-search-skills\ncp -r brave-search-skills/skills/* ~/.claude/skills/   # user-level\ncp -r brave-search-skills/skills/* .claude/skills/      # project-level","# Project-level\nmkdir -p .cursor/skills && curl -sL https://github.com/brave/brave-search-skills/archive/main.tar.gz | tar xz -C .cursor/skills --strip-components=2 brave-search-skills-main/skills\n\n# User-level\nmkdir -p ~/.cursor/skills && curl -sL https://github.com/brave/brave-search-skills/archive/main.tar.gz | tar xz -C ~/.cursor/skills --strip-components=2 brave-search-skills-main/skills","cp -r brave-search-skills/skills/* .cursor/skills/      # project-level\ncp -r brave-search-skills/skills/* ~/.cursor/skills/     # user-level","mkdir -p .github/skills && curl -sL https://github.com/brave/brave-search-skills/archive/main.tar.gz | tar xz -C .github/skills --strip-components=2 brave-search-skills-main/skills","cp -r brave-search-skills/skills/* .github/skills/","# User-level\nmkdir -p ~/.agents/skills && curl -sL https://github.com/brave/brave-search-skills/archive/main.tar.gz | tar xz -C ~/.agents/skills --strip-components=2 brave-search-skills-main/skills\n\n# Project-level\nmkdir -p .agents/skills && curl -sL https://github.com/brave/brave-search-skills/archive/main.tar.gz | tar xz -C .agents/skills --strip-components=2 brave-search-skills-main/skills","cp -r brave-search-skills/skills/* ~/.agents/skills/    # user-level\ncp -r brave-search-skills/skills/* .agents/skills/       # project-level","# Project-level\nmkdir -p .windsurf/skills && curl -sL https://github.com/brave/brave-search-skills/archive/main.tar.gz | tar xz -C .windsurf/skills --strip-components=2 brave-search-skills-main/skills\n\n# User-level\nmkdir -p ~/.codeium/windsurf/skills && curl -sL https://github.com/brave/brave-search-skills/archive/main.tar.gz | tar xz -C ~/.codeium/windsurf/skills --strip-components=2 brave-search-skills-main/skills","cp -r brave-search-skills/skills/* .windsurf/skills/             # project-level\ncp -r brave-search-skills/skills/* ~/.codeium/windsurf/skills/   # user-level","mkdir -p ~/.openclaw/skills && curl -sL https://github.com/brave/brave-search-skills/archive/main.tar.gz | tar xz -C ~/.openclaw/skills --strip-components=2 brave-search-skills-main/skills","cp -r brave-search-skills/skills/* ~/.openclaw/skills/","mkdir -p <skills-dir> && curl -sL https://github.com/brave/brave-search-skills/archive/main.tar.gz | tar xz -C <skills-dir> --strip-components=2 brave-search-skills-main/skills","npx openskills install brave/brave-search-skills","cd brave-search-skills && git pull\ncp -r skills/* ~/.claude/skills/    # Claude Code\ncp -r skills/* .cursor/skills/      # Cursor\ncp -r skills/* .agents/skills/      # Codex\ncp -r skills/* ~/.openclaw/skills/  # OpenClaw"]}
    - {"level":"H3","title":"Claude Code","content":["Skills documentation","Plugin marketplace (auto-updates, no git needed):","curl (no git, no marketplace):","Manual (git clone + cp):"],"codeBlocks":["/plugin marketplace add brave/brave-search-skills\n/plugin install brave-search-skills@brave-search","# User-level (available in all projects)\nmkdir -p ~/.claude/skills && curl -sL https://github.com/brave/brave-search-skills/archive/main.tar.gz | tar xz -C ~/.claude/skills --strip-components=2 brave-search-skills-main/skills\n\n# Project-level\nmkdir -p .claude/skills && curl -sL https://github.com/brave/brave-search-skills/archive/main.tar.gz | tar xz -C .claude/skills --strip-components=2 brave-search-skills-main/skills","git clone https://github.com/brave/brave-search-skills\ncp -r brave-search-skills/skills/* ~/.claude/skills/   # user-level\ncp -r brave-search-skills/skills/* .claude/skills/      # project-level"]}
    - {"level":"H3","title":"Cursor","content":["Skills documentation","Remote Rule (no terminal needed):","Settings → Rules → Project Rules → Add Rule → Remote Rule → paste https://github.com/brave/brave-search-skills","Manual (cp — requires git clone above):","Cursor natively reads skills from .cursor/skills/, .claude/skills/, and .codex/skills/ at both project and user level."],"codeBlocks":["# Project-level\nmkdir -p .cursor/skills && curl -sL https://github.com/brave/brave-search-skills/archive/main.tar.gz | tar xz -C .cursor/skills --strip-components=2 brave-search-skills-main/skills\n\n# User-level\nmkdir -p ~/.cursor/skills && curl -sL https://github.com/brave/brave-search-skills/archive/main.tar.gz | tar xz -C ~/.cursor/skills --strip-components=2 brave-search-skills-main/skills","cp -r brave-search-skills/skills/* .cursor/skills/      # project-level\ncp -r brave-search-skills/skills/* ~/.cursor/skills/     # user-level"]}
    - {"level":"H3","title":"GitHub Copilot","content":["Manual (cp — requires git clone above):"],"codeBlocks":["mkdir -p .github/skills && curl -sL https://github.com/brave/brave-search-skills/archive/main.tar.gz | tar xz -C .github/skills --strip-components=2 brave-search-skills-main/skills","cp -r brave-search-skills/skills/* .github/skills/"]}
    - {"level":"H3","title":"Codex","content":["Skills documentation","Skill installer (built-in — ask Codex to install skills from https://github.com/brave/brave-search-skills).","Manual (cp — requires git clone above):","Codex reads from .agents/skills/ at repo, parent, root, and user levels. Skills work across the CLI, desktop app, and IDE extension."],"codeBlocks":["# User-level\nmkdir -p ~/.agents/skills && curl -sL https://github.com/brave/brave-search-skills/archive/main.tar.gz | tar xz -C ~/.agents/skills --strip-components=2 brave-search-skills-main/skills\n\n# Project-level\nmkdir -p .agents/skills && curl -sL https://github.com/brave/brave-search-skills/archive/main.tar.gz | tar xz -C .agents/skills --strip-components=2 brave-search-skills-main/skills","cp -r brave-search-skills/skills/* ~/.agents/skills/    # user-level\ncp -r brave-search-skills/skills/* .agents/skills/       # project-level"]}
    - {"level":"H3","title":"Windsurf","content":["Manual (cp — requires git clone above):"],"codeBlocks":["# Project-level\nmkdir -p .windsurf/skills && curl -sL https://github.com/brave/brave-search-skills/archive/main.tar.gz | tar xz -C .windsurf/skills --strip-components=2 brave-search-skills-main/skills\n\n# User-level\nmkdir -p ~/.codeium/windsurf/skills && curl -sL https://github.com/brave/brave-search-skills/archive/main.tar.gz | tar xz -C ~/.codeium/windsurf/skills --strip-components=2 brave-search-skills-main/skills","cp -r brave-search-skills/skills/* .windsurf/skills/             # project-level\ncp -r brave-search-skills/skills/* ~/.codeium/windsurf/skills/   # user-level"]}
    - {"level":"H3","title":"OpenClaw","content":["Skills documentation","Manual (cp — requires git clone above):"],"codeBlocks":["mkdir -p ~/.openclaw/skills && curl -sL https://github.com/brave/brave-search-skills/archive/main.tar.gz | tar xz -C ~/.openclaw/skills --strip-components=2 brave-search-skills-main/skills","cp -r brave-search-skills/skills/* ~/.openclaw/skills/"]}
    - {"level":"H3","title":"Other Agents (Cline, Gemini CLI, Goose, Amp, Roo Code, etc.)","content":["curl (adjust the target directory for your agent):","Or copy skills from a git clone to the agent’s skills directory. All agents following the Agent Skills standard read SKILL.md files from their skills folder."],"codeBlocks":["mkdir -p <skills-dir> && curl -sL https://github.com/brave/brave-search-skills/archive/main.tar.gz | tar xz -C <skills-dir> --strip-components=2 brave-search-skills-main/skills"]}
    - {"level":"H3","title":"OpenSkills (Third-Party Universal Installer)","content":["See openskills on GitHub for details."],"codeBlocks":["npx openskills install brave/brave-search-skills"]}
    - {"level":"H3","title":"Updating","content":["Claude Code marketplace: updates automatically, or run /plugin marketplace update brave-search.","curl: re-run the curl command above to overwrite with the latest version.","git clone: pull the latest changes and re-copy:","Or re-run the OpenSkills install command to overwrite with the latest version.","See the full list of compatible agents at agentskills.io."],"codeBlocks":["cd brave-search-skills && git pull\ncp -r skills/* ~/.claude/skills/    # Claude Code\ncp -r skills/* .cursor/skills/      # Cursor\ncp -r skills/* .agents/skills/      # Codex\ncp -r skills/* ~/.openclaw/skills/  # OpenClaw"]}
    - {"level":"H2","title":"Quick Start","content":["Returns search results with pre-extracted web content, optimized for LLM grounding:","Standard search with snippets, URLs, and metadata:","OpenAI SDK-compatible endpoint for AI-grounded answers with citations.","Fast single-search (blocking):","Research mode (streaming required):"],"codeBlocks":[]}
    - {"level":"H3","title":"LLM Context (Recommended for AI)","content":["Returns search results with pre-extracted web content, optimized for LLM grounding:"],"codeBlocks":[]}
    - {"level":"H3","title":"Web Search","content":["Standard search with snippets, URLs, and metadata:"],"codeBlocks":[]}
    - {"level":"H3","title":"Answers (AI-Grounded)","content":["OpenAI SDK-compatible endpoint for AI-grounded answers with citations.","Fast single-search (blocking):","Research mode (streaming required):"],"codeBlocks":[]}
    - {"level":"H2","title":"Goggles (Custom Ranking)","content":["Brave’s unique feature lets you filter, boost, or downrank results:","Goggles documentation."],"codeBlocks":[]}
    - {"level":"H2","title":"Documentation","content":["• API Reference: https://api-dashboard.search.brave.com/api-reference/web/search/get\n• Goggles Quickstart: https://github.com/brave/goggles-quickstart\n• Agent Skills Standard: https://agentskills.io/specification\n• Claude Code Skills: https://code.claude.com/docs/en/skills\n• Cursor Skills: https://cursor.com/docs/context/skills\n• Codex Skills: https://developers.openai.com/codex/skills\n• OpenClaw Skills: https://docs.openclaw.ai/tools/skills"],"codeBlocks":[]}
  tables:
    - {"index":0,"headers":["Skill","Description","Endpoint","Best For"],"rows":[["llm-context","Pre-extracted web content for LLM grounding (GET/POST)","/res/v1/llm/context","RAG, AI agents — recommended"],["answers","AI-grounded answers, OpenAI SDK compatible","/res/v1/chat/completions","Chat interfaces, cited answers"],["web-search","Ranked web results with snippets and rich data","/res/v1/web/search","General search queries"],["images-search","Image search with thumbnails (up to 200 results)","/res/v1/images/search","Finding images"],["news-search","News articles with freshness filtering","/res/v1/news/search","Current events, breaking news"],["videos-search","Video search with duration/views/creator","/res/v1/videos/search","Finding video content"],["suggest","Query autocomplete (<100ms response)","/res/v1/suggest/search","Search UX, query expansion"],["spellcheck","Spell correction for query cleanup","/res/v1/spellcheck/search","Query preprocessing"]]}
  examples:
    - {"type":"response","language":"json","code":"{\n  \"env\": {\n    \"BRAVE_SEARCH_API_KEY\": \"your-key\"\n  }\n}"}
    - {"type":"response","language":"json","code":"{\n  \"env\": {\n    \"BRAVE_SEARCH_API_KEY\": \"your-key\"\n  }\n}"}
    - {"type":"response","language":"json","code":"{\n  \"skills\": {\n    \"entries\": {\n      \"brave-search\": {\n        \"env\": {\n          \"BRAVE_SEARCH_API_KEY\": \"your-key\"\n        }\n      }\n    }\n  }\n}"}
    - {"type":"response","language":"json","code":"{\n  \"skills\": {\n    \"entries\": {\n      \"brave-search\": {\n        \"env\": {\n          \"BRAVE_SEARCH_API_KEY\": \"your-key\"\n        }\n      }\n    }\n  }\n}"}
    - {"type":"request","language":"bash","code":"curl -X GET \"https://api.search.brave.com/res/v1/llm/context?q=search+API+for+grounding+LLMs\" \\\n  -H \"X-Subscription-Token: ${BRAVE_SEARCH_API_KEY}\""}
    - {"type":"request","language":"bash","code":"curl -X GET \"https://api.search.brave.com/res/v1/llm/context?q=search+API+for+grounding+LLMs\" \\\n  -H \"X-Subscription-Token: ${BRAVE_SEARCH_API_KEY}\""}
    - {"type":"request","language":"bash","code":"curl -s \"https://api.search.brave.com/res/v1/web/search?q=retrieval+augmented+generation+explained\" \\\n  -H \"Accept: application/json\" \\\n  -H \"X-Subscription-Token: ${BRAVE_SEARCH_API_KEY}\""}
    - {"type":"request","language":"bash","code":"curl -s \"https://api.search.brave.com/res/v1/web/search?q=retrieval+augmented+generation+explained\" \\\n  -H \"Accept: application/json\" \\\n  -H \"X-Subscription-Token: ${BRAVE_SEARCH_API_KEY}\""}
    - {"type":"request","language":"bash","code":"curl -X POST \"https://api.search.brave.com/res/v1/chat/completions\" \\\n  -H \"Content-Type: application/json\" \\\n  -H \"X-Subscription-Token: ${BRAVE_SEARCH_API_KEY}\" \\\n  -d '{\n    \"messages\": [{\"role\": \"user\", \"content\": \"What programming languages are trending in 2026?\"}],\n    \"model\": \"brave\",\n    \"stream\": false\n  }'"}
    - {"type":"request","language":"bash","code":"curl -X POST \"https://api.search.brave.com/res/v1/chat/completions\" \\\n  -H \"Content-Type: application/json\" \\\n  -H \"X-Subscription-Token: ${BRAVE_SEARCH_API_KEY}\" \\\n  -d '{\n    \"messages\": [{\"role\": \"user\", \"content\": \"What programming languages are trending in 2026?\"}],\n    \"model\": \"brave\",\n    \"stream\": false\n  }'"}
    - {"type":"request","language":"bash","code":"curl -X POST \"https://api.search.brave.com/res/v1/chat/completions\" \\\n  -H \"Content-Type: application/json\" \\\n  -H \"X-Subscription-Token: ${BRAVE_SEARCH_API_KEY}\" \\\n  -d '{\n    \"messages\": [{\"role\": \"user\", \"content\": \"How are developers building AI-powered search applications in 2026?\"}],\n    \"model\": \"brave\",\n    \"stream\": true,\n    \"enable_research\": true\n  }'"}
    - {"type":"request","language":"bash","code":"curl -X POST \"https://api.search.brave.com/res/v1/chat/completions\" \\\n  -H \"Content-Type: application/json\" \\\n  -H \"X-Subscription-Token: ${BRAVE_SEARCH_API_KEY}\" \\\n  -d '{\n    \"messages\": [{\"role\": \"user\", \"content\": \"How are developers building AI-powered search applications in 2026?\"}],\n    \"model\": \"brave\",\n    \"stream\": true,\n    \"enable_research\": true\n  }'"}
    - {"type":"request","language":"bash","code":"# Focus on specific domains only\ncurl -X GET \"https://api.search.brave.com/res/v1/llm/context\" \\\n  -H \"X-Subscription-Token: ${BRAVE_SEARCH_API_KEY}\" \\\n  -G \\\n  --data-urlencode \"q=rust programming\" \\\n  --data-urlencode 'goggles=$discard\n$site=docs.rs\n$site=rust-lang.org'"}
    - {"type":"request","language":"bash","code":"# Focus on specific domains only\ncurl -X GET \"https://api.search.brave.com/res/v1/llm/context\" \\\n  -H \"X-Subscription-Token: ${BRAVE_SEARCH_API_KEY}\" \\\n  -G \\\n  --data-urlencode \"q=rust programming\" \\\n  --data-urlencode 'goggles=$discard\n$site=docs.rs\n$site=rust-lang.org'"}
  rawContent: "Quickstart\n\nPricing\n\nAuthentication\n\nVersioning\n\nRate limiting\n\nWeb search\n\nLLM Context New\n\nNews search\n\nVideo search\n\nImage search\n\nSummarizer search\n\nPlace search New\n\nAnswers\n\nAutosuggest\n\nSpellcheck\n\nSkills\n\nHelp & Feedback\n\nGoggles\n\nSearch operators\n\nStatus updates\n\nSecurity\n\nPrivacy notice\n\nTerms of service\n\nResources\n\nOfficial skills for using Brave Search API with AI coding agents.\n\nOverview\n\nThe Brave Search API now supports Skills—a powerful way to extend\nAI capabilities with modular, reusable workflows. These skills,\na standardized format now open-sourced here,\nenable your AI editor or CLI to dynamically load instructions, scripts, and resources\nfor specialized tasks that the Brave API can help with.\n\nSkills work with Claude Code, Cursor, GitHub Copilot, Codex, Gemini CLI,\nVS Code, Windsurf, OpenClaw, Cline, Goose, Amp, Roo Code, and many other agents that support the Agent\nSkills standard.\n\nBrave Skills are available as a GitHub repository.\n\nQuick Setup\n\nClaude Code\n\nInstall skills to Claude Code CLI\n\nCursor\n\nInstall skills to Cursor\n\nOpenAI Codex\n\nInstall skills to Codex CLI\n\nPrerequisites\n\nGet a Brave Search API key from your dashboard.\n\nSecurity tip: Prefer agent-native config over shell profile exports.\nCoding agents can access environment variables — scoped configs limit exposure.\nSee API key setup for all options.\n\nAdd to ~/.claude/settings.json (docs):\n\nThis makes the key available in all Claude Code sessions. For per-project use,\nadd to .claude/settings.local.json (gitignored) with the same format.\n\nOption 1 — direnv (directory-scoped, auto-loads/unloads):\n\nOption 2 — Shell profile (~/.zshrc or ~/.bashrc):\n\nThen restart Cursor (launch from terminal or fully quit and reopen — reloading\nthe window is not enough). Cursor inherits environment variables from your shell.\nYou can also add skills via Settings > Rules > Add Rule > Remote Rule using\nthe GitHub URL.\n\nOption 1 — config.toml (docs):\n\nThen restart your terminal. Codex reads environment variables from the shell\n(CLI, app, and IDE extension).\n\nOpenClaw\n\nAdd to ~/.openclaw/.env (docs):\n\nOr add to ~/.openclaw/openclaw.json under the skill’s config:\n\nOther agents\n\nInstallation\n\nAll agents below support the Agent Skills standard\nand read SKILL.md files from their skills directory.\n\nSkills documentation\n\nPlugin marketplace (auto-updates, no git needed):\n\ncurl (no git, no marketplace):\n\nManual (git clone + cp):\n\nRemote Rule (no terminal needed):\n\nSettings → Rules → Project Rules → Add Rule → Remote Rule → paste https://github.com/brave/brave-search-skills\n\nManual (cp — requires git clone above):\n\nCursor natively reads skills from .cursor/skills/, .claude/skills/, and .codex/skills/ at both project and user level.\n\nGitHub Copilot\n\nSkill installer (built-in — ask Codex to install skills from https://github.com/brave/brave-search-skills).\n\nCodex reads from .agents/skills/ at repo, parent, root, and user levels. Skills work across the CLI, desktop app, and IDE extension.\n\nWindsurf\n\nOther Agents (Cline, Gemini CLI, Goose, Amp, Roo Code, etc.)\n\ncurl (adjust the target directory for your agent):\n\nOr copy skills from a git clone to the agent’s skills directory. All agents following the Agent Skills standard read SKILL.md files from their skills folder.\n\nOpenSkills (Third-Party Universal Installer)\n\nSee openskills on GitHub for details.\n\nUpdating\n\nClaude Code marketplace: updates automatically, or run /plugin marketplace update brave-search.\n\ncurl: re-run the curl command above to overwrite with the latest version.\n\ngit clone: pull the latest changes and re-copy:\n\nOr re-run the OpenSkills install command to overwrite with the latest version.\n\nSee the full list of compatible agents at agentskills.io.\n\nAvailable Skills\n\nQuick Start\n\nLLM Context (Recommended for AI)\n\nReturns search results with pre-extracted web content, optimized for LLM grounding:\n\nWeb Search\n\nStandard search with snippets, URLs, and metadata:\n\nAnswers (AI-Grounded)\n\nOpenAI SDK-compatible endpoint for AI-grounded answers with citations.\n\nFast single-search (blocking):\n\nResearch mode (streaming required):\n\nGoggles (Custom Ranking)\n\nBrave’s unique feature lets you filter, boost, or downrank results:\n\nGoggles documentation.\n\nDocumentation\n\nAPI Reference: https://api-dashboard.search.brave.com/api-reference/web/search/get\n\nGoggles Quickstart: https://github.com/brave/goggles-quickstart\n\nAgent Skills Standard: https://agentskills.io/specification\n\nClaude Code Skills: https://code.claude.com/docs/en/skills\n\nCursor Skills: https://cursor.com/docs/context/skills\n\nCodex Skills: https://developers.openai.com/codex/skills\n\nOpenClaw Skills: https://docs.openclaw.ai/tools/skills\n\nOn this page\n\nClaude Code Install skills to Claude Code CLI  Cursor Install skills to Cursor  OpenAI Codex Install skills to Codex CLI"
  suggestedFilename: "resources-skills"
---

# Skills

## 源URL

https://api-dashboard.search.brave.com/documentation/resources/skills

## 描述

The Brave Search API now supports Skills—a powerful way to extend
AI capabilities with modular, reusable workflows. These skills,
a standardized format now open-sourced here,
enable your AI editor or CLI to dynamically load instructions, scripts, and resources
for specialized tasks that the Brave API can help with.

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.search.brave.com/res/v1/llm/context?q=search+API+for+grounding+LLMs`

## 代码示例

### 示例 1 (json)

```json
{
  "env": {
    "BRAVE_SEARCH_API_KEY": "your-key"
  }
}
```

### 示例 2 (json)

```json
{
  "skills": {
    "entries": {
      "brave-search": {
        "env": {
          "BRAVE_SEARCH_API_KEY": "your-key"
        }
      }
    }
  }
}
```

### 示例 3 (bash)

```bash
curl -X GET "https://api.search.brave.com/res/v1/llm/context?q=search+API+for+grounding+LLMs" \
  -H "X-Subscription-Token: ${BRAVE_SEARCH_API_KEY}"
```

### 示例 4 (bash)

```bash
curl -s "https://api.search.brave.com/res/v1/web/search?q=retrieval+augmented+generation+explained" \
  -H "Accept: application/json" \
  -H "X-Subscription-Token: ${BRAVE_SEARCH_API_KEY}"
```

### 示例 5 (bash)

```bash
curl -X POST "https://api.search.brave.com/res/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "X-Subscription-Token: ${BRAVE_SEARCH_API_KEY}" \
  -d '{
    "messages": [{"role": "user", "content": "What programming languages are trending in 2026?"}],
    "model": "brave",
    "stream": false
  }'
```

### 示例 6 (bash)

```bash
# Focus on specific domains only
curl -X GET "https://api.search.brave.com/res/v1/llm/context" \
  -H "X-Subscription-Token: ${BRAVE_SEARCH_API_KEY}" \
  -G \
  --data-urlencode "q=rust programming" \
  --data-urlencode 'goggles=$discard
$site=docs.rs
$site=rust-lang.org'
```

## 文档正文

The Brave Search API now supports Skills—a powerful way to extend
AI capabilities with modular, reusable workflows. These skills,
a standardized format now open-sourced here,
enable your AI editor or CLI to dynamically load instructions, scripts, and resources
for specialized tasks that the Brave API can help with.

## API 端点

**Method:** `GET`
**Endpoint:** `https://api.search.brave.com/res/v1/llm/context?q=search+API+for+grounding+LLMs`

Quickstart

Pricing

Authentication

Versioning

Rate limiting

Web search

LLM Context New

News search

Video search

Image search

Summarizer search

Place search New

Answers

Autosuggest

Spellcheck

Skills

Help & Feedback

Goggles

Search operators

Status updates

Security

Privacy notice

Terms of service

Resources

Official skills for using Brave Search API with AI coding agents.

Overview

The Brave Search API now supports Skills—a powerful way to extend
AI capabilities with modular, reusable workflows. These skills,
a standardized format now open-sourced here,
enable your AI editor or CLI to dynamically load instructions, scripts, and resources
for specialized tasks that the Brave API can help with.

Skills work with Claude Code, Cursor, GitHub Copilot, Codex, Gemini CLI,
VS Code, Windsurf, OpenClaw, Cline, Goose, Amp, Roo Code, and many other agents that support the Agent
Skills standard.

Brave Skills are available as a GitHub repository.

Quick Setup

Claude Code

Install skills to Claude Code CLI

Cursor

Install skills to Cursor

OpenAI Codex

Install skills to Codex CLI

Prerequisites

Get a Brave Search API key from your dashboard.

Security tip: Prefer agent-native config over shell profile exports.
Coding agents can access environment variables — scoped configs limit exposure.
See API key setup for all options.

Add to ~/.claude/settings.json (docs):

This makes the key available in all Claude Code sessions. For per-project use,
add to .claude/settings.local.json (gitignored) with the same format.

Option 1 — direnv (directory-scoped, auto-loads/unloads):

Option 2 — Shell profile (~/.zshrc or ~/.bashrc):

Then restart Cursor (launch from terminal or fully quit and reopen — reloading
the window is not enough). Cursor inherits environment variables from your shell.
You can also add skills via Settings > Rules > Add Rule > Remote Rule using
the GitHub URL.

Option 1 — config.toml (docs):

Then restart your terminal. Codex reads environment variables from the shell
(CLI, app, and IDE extension).

OpenClaw

Add to ~/.openclaw/.env (docs):

Or add to ~/.openclaw/openclaw.json under the skill’s config:

Other agents

Installation

All agents below support the Agent Skills standard
and read SKILL.md files from their skills directory.

Skills documentation

Plugin marketplace (auto-updates, no git needed):

curl (no git, no marketplace):

Manual (git clone + cp):

Remote Rule (no terminal needed):

Settings → Rules → Project Rules → Add Rule → Remote Rule → paste https://github.com/brave/brave-search-skills

Manual (cp — requires git clone above):

Cursor natively reads skills from .cursor/skills/, .claude/skills/, and .codex/skills/ at both project and user level.

GitHub Copilot

Skill installer (built-in — ask Codex to install skills from https://github.com/brave/brave-search-skills).

Codex reads from .agents/skills/ at repo, parent, root, and user levels. Skills work across the CLI, desktop app, and IDE extension.

Windsurf

Other Agents (Cline, Gemini CLI, Goose, Amp, Roo Code, etc.)

curl (adjust the target directory for your agent):

Or copy skills from a git clone to the agent’s skills directory. All agents following the Agent Skills standard read SKILL.md files from their skills folder.

OpenSkills (Third-Party Universal Installer)

See openskills on GitHub for details.

Updating

Claude Code marketplace: updates automatically, or run /plugin marketplace update brave-search.

curl: re-run the curl command above to overwrite with the latest version.

git clone: pull the latest changes and re-copy:

Or re-run the OpenSkills install command to overwrite with the latest version.

See the full list of compatible agents at agentskills.io.

Available Skills

Quick Start

LLM Context (Recommended for AI)

Returns search results with pre-extracted web content, optimized for LLM grounding:

Web Search

Standard search with snippets, URLs, and metadata:

Answers (AI-Grounded)

OpenAI SDK-compatible endpoint for AI-grounded answers with citations.

Fast single-search (blocking):

Research mode (streaming required):

Goggles (Custom Ranking)

Brave’s unique feature lets you filter, boost, or downrank results:

Goggles documentation.

Documentation

API Reference: https://api-dashboard.search.brave.com/api-reference/web/search/get

Goggles Quickstart: https://github.com/brave/goggles-quickstart

Agent Skills Standard: https://agentskills.io/specification

Claude Code Skills: https://code.claude.com/docs/en/skills

Cursor Skills: https://cursor.com/docs/context/skills

Codex Skills: https://developers.openai.com/codex/skills

OpenClaw Skills: https://docs.openclaw.ai/tools/skills

On this page

Claude Code Install skills to Claude Code CLI  Cursor Install skills to Cursor  OpenAI Codex Install skills to Codex CLI
