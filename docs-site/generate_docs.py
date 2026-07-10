#!/usr/bin/env python3
import os
import re
import json

def main() -> None:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    stories_dir = os.path.join(base_dir, "stories")
    docs_dir = os.path.join(base_dir, "docs-site")
    os.makedirs(docs_dir, exist_ok=True)
    
    # 1. Gather all golden files and code files
    goldens = {}
    for root, _, files in os.walk(stories_dir):
        for file in files:
            if file.endswith(".golden.txt"):
                path = os.path.join(root, file)
                rel_path = os.path.relpath(path, stories_dir)
                parts = rel_path.split(os.sep)
                if len(parts) >= 2:
                    module = parts[0]
                    name = os.path.splitext(parts[1])[0].replace(".golden", "")
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    py_path = os.path.join(root, name + ".py")
                    py_code = ""
                    if os.path.exists(py_path):
                        with open(py_path, "r", encoding="utf-8") as f:
                            py_code = f.read()
                            
                    if module not in goldens:
                        goldens[module] = {}
                    goldens[module][name] = {
                        "raw_ansi": content,
                        "code": py_code
                    }
                    
    # 2. Write HTML template
    html_template = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TermForge Interactive Showcase Documentation</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Outfit:wght@400;600;800&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/xterm@5.3.0/css/xterm.css" />
    <script src="https://cdn.jsdelivr.net/npm/xterm@5.3.0/lib/xterm.js"></script>
    <style>
        :root {
            /* Catppuccin Mocha Theme (Default) */
            --bg-color: #1e1e2e;
            --text-color: #cdd6f4;
            --sidebar-bg: rgba(30, 30, 46, 0.75);
            --card-bg: rgba(49, 50, 68, 0.45);
            --border-glow: #b4befe;
            --accent-glow: #89b4fa;
        }
        
        .theme-dracula {
            --bg-color: #282a36;
            --text-color: #f8f8f2;
            --sidebar-bg: rgba(40, 42, 54, 0.8);
            --card-bg: rgba(68, 71, 90, 0.5);
            --border-glow: #bd93f9;
            --accent-glow: #8be9fd;
        }

        .theme-tokyo {
            --bg-color: #1a1b26;
            --text-color: #a9b1d6;
            --sidebar-bg: rgba(26, 27, 38, 0.8);
            --card-bg: rgba(36, 40, 59, 0.5);
            --border-glow: #bb9af7;
            --accent-glow: #7aa2f7;
        }

        .theme-contrast {
            --bg-color: #000000;
            --text-color: #ffffff;
            --sidebar-bg: #111111;
            --card-bg: #222222;
            --border-glow: #ffffff;
            --accent-glow: #00ffff;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            min-height: 100vh;
            display: flex;
            overflow-x: hidden;
            transition: all 0.3s ease;
        }
        
        .glow-sphere {
            position: absolute;
            border-radius: 50%;
            filter: blur(120px);
            z-index: -1;
            opacity: 0.25;
        }
        .sphere-1 {
            width: 400px;
            height: 400px;
            background: var(--border-glow);
            top: -100px;
            right: -100px;
        }
        .sphere-2 {
            width: 350px;
            height: 350px;
            background: var(--accent-glow);
            bottom: -50px;
            left: -50px;
        }
        
        .sidebar {
            width: 300px;
            background: var(--sidebar-bg);
            backdrop-filter: blur(20px);
            border-right: 1px solid rgba(255, 255, 255, 0.08);
            padding: 30px 20px;
            display: flex;
            flex-direction: column;
            gap: 25px;
            height: 100vh;
            position: sticky;
            top: 0;
        }
        
        .logo-container h1 {
            font-family: 'Outfit', sans-serif;
            font-weight: 800;
            font-size: 24px;
            letter-spacing: -0.5px;
            background: linear-gradient(135deg, var(--border-glow), var(--accent-glow));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .menu-title {
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            opacity: 0.4;
            margin-bottom: 15px;
        }
        
        .sidebar-scroller {
            overflow-y: auto;
            max-height: calc(100vh - 140px);
            display: flex;
            flex-direction: column;
            gap: 12px;
            padding-right: 5px;
        }

        .sidebar-scroller::-webkit-scrollbar {
            width: 6px;
        }
        .sidebar-scroller::-webkit-scrollbar-track {
            background: transparent;
        }
        .sidebar-scroller::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 3px;
        }
        .sidebar-scroller::-webkit-scrollbar-thumb:hover {
            background: var(--border-glow);
        }

        .module-group {
            display: flex;
            flex-direction: column;
        }
        
        .module-header {
            width: 100%;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.05);
            color: var(--text-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 16px;
            font-size: 13px;
            font-weight: 600;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s ease;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .module-header:hover {
            background: rgba(255, 255, 255, 0.06);
            border-color: rgba(255, 255, 255, 0.1);
        }
        
        .module-header.expanded .chevron {
            transform: rotate(180deg);
        }
        
        .chevron {
            font-size: 10px;
            transition: transform 0.2s ease;
            opacity: 0.5;
        }

        .menu-list {
            list-style: none;
            display: none;
            flex-direction: column;
            gap: 5px;
            padding-left: 10px;
            margin-top: 5px;
        }
        
        .menu-item button {
            width: 100%;
            background: transparent;
            border: none;
            color: var(--text-color);
            text-align: left;
            padding: 8px 12px;
            font-size: 13px;
            font-weight: 500;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s ease;
            opacity: 0.7;
        }
        
        .menu-item button:hover, .menu-item.active button {
            background: rgba(255, 255, 255, 0.05);
            box-shadow: inset 0 0 10px rgba(255, 255, 255, 0.02);
            color: #ffffff;
            opacity: 1;
        }
        
        .menu-item.active button {
            border-left: 2px solid var(--border-glow);
            border-radius: 0 6px 6px 0;
            padding-left: 10px;
        }
        
        .main-content {
            flex-grow: 1;
            padding: 50px 60px;
            max-width: 1200px;
            display: flex;
            flex-direction: column;
            gap: 40px;
        }
        
        .controls-card {
            background: var(--card-bg);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 20px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .controls-title h2 {
            font-family: 'Outfit', sans-serif;
            font-size: 20px;
            font-weight: 600;
        }
        
        .theme-selector {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .theme-selector select {
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: var(--text-color);
            padding: 8px 16px;
            border-radius: 8px;
            outline: none;
            cursor: pointer;
        }
        
        .terminal-container {
            background: rgba(10, 11, 16, 0.95);
            border: 1.5px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6), 0 0 20px rgba(127, 0, 255, 0.15);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            width: 100%;
        }
        
        .terminal-header {
            background: rgba(255, 255, 255, 0.03);
            border-bottom: 1.5px solid rgba(255, 255, 255, 0.08);
            padding: 12px 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .terminal-dots {
            display: flex;
            gap: 8px;
        }
        
        .dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
        }
        .dot-red { background: #ff5f56; }
        .dot-yellow { background: #ffbd2e; }
        .dot-green { background: #27c93f; }
        
        .terminal-title {
            font-size: 13px;
            font-family: 'Fira Code', monospace;
            opacity: 0.5;
        }
        
        .tab-bar {
            display: flex;
            background: rgba(0, 0, 0, 0.4);
            border-bottom: 1.5px solid rgba(255, 255, 255, 0.08);
        }
        
        .tab-button {
            flex: 1;
            background: transparent;
            border: none;
            color: rgba(255, 255, 255, 0.5);
            padding: 14px;
            font-family: 'Inter', sans-serif;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            border-bottom: 2px solid transparent;
            transition: all 0.2s ease;
        }
        
        .tab-button.active {
            color: #ffffff;
            border-bottom: 2px solid var(--border-glow);
            background: rgba(255, 255, 255, 0.02);
        }
        
        .terminal-body {
            padding: 16px;
            min-height: 420px;
            overflow: hidden;
            position: relative;
        }

        #terminal-screen-code {
            padding: 24px;
            font-family: 'Fira Code', monospace;
            font-size: 15px;
            line-height: 1.45;
            white-space: pre;
            overflow-x: auto;
            color: #a9b1d6;
            background: #111217;
            min-height: 420px;
        }

        /* Customize xterm scrollbar */
        .xterm-viewport::-webkit-scrollbar {
            width: 8px;
        }
        .xterm-viewport::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.15);
            border-radius: 4px;
        }
        
        @keyframes pulse-glow {
            0% { box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6), 0 0 20px rgba(127, 0, 255, 0.15); }
            50% { box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6), 0 0 35px rgba(0, 240, 255, 0.25); }
            100% { box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6), 0 0 20px rgba(127, 0, 255, 0.15); }
        }
        
        .terminal-container {
            animation: pulse-glow 8s infinite alternate;
        }
    </style>
</head>
<body class="theme-catppuccin">
    <div class="glow-sphere sphere-1"></div>
    <div class="glow-sphere sphere-2"></div>
    
    <div class="sidebar">
        <div class="logo-container">
            <h1>TermForge</h1>
            <p style="font-size: 12px; opacity: 0.5; margin-top: 5px;">Universal CLI Showcase</p>
        </div>
        
        <div style="display: flex; flex-direction: column; height: 100%;">
            <div class="menu-title">Stories</div>
            <div class="sidebar-scroller" id="sidebar-scroller">
                <!-- Javascript populated grouped modules -->
            </div>
        </div>
    </div>
    
    <div class="main-content">
        <div class="controls-card">
            <div class="controls-title">
                <h2 id="active-title">Story Showcase</h2>
                <p style="font-size: 13px; opacity: 0.6; margin-top: 5px;">Interactive TermForge rendering gallery</p>
            </div>
            <div class="theme-selector">
                <label for="theme-skin" style="font-size: 14px; font-weight: 600;">Theme skin:</label>
                <select id="theme-skin" onchange="changeThemeSkin(this.value)">
                    <option value="catppuccin">Catppuccin Mocha</option>
                    <option value="dracula">Dracula</option>
                    <option value="tokyo">Tokyo Night</option>
                    <option value="contrast">High Contrast</option>
                </select>
            </div>
        </div>
        
        <div class="terminal-container">
            <div class="terminal-header">
                <div class="terminal-dots">
                    <div class="dot dot-red"></div>
                    <div class="dot dot-yellow"></div>
                    <div class="dot dot-green"></div>
                </div>
                <div class="terminal-title" id="term-filename">story.py</div>
                <div></div>
            </div>
            
            <div class="tab-bar">
                <button id="tab-preview" class="tab-button active" onclick="showTab('preview')">Terminal Preview</button>
                <button id="tab-code" class="tab-button" onclick="showTab('code')">Python Source Code</button>
            </div>
            
            <div class="terminal-body" id="terminal-screen-preview" style="display: block;">
                <!-- xterm.js mounts here -->
            </div>
            <div class="terminal-body" id="terminal-screen-code" style="display: none; background: #111217; color: #a9b1d6;">
                <!-- code text loaded here -->
            </div>
        </div>
    </div>
    
    <script>
        const storiesData = %STORIES_DATA%;
        let currentMod = "";
        let currentComp = "";
        let currentTab = "preview";
        
        let term;
        let currentLine = "";
        let inRepl = false;
        
        const xtermThemes = {
            catppuccin: {
                background: '#1e1e2e',
                foreground: '#cdd6f4',
                cursor: '#b4befe',
                black: '#11111b',
                red: '#f38ba8',
                green: '#a6e3a1',
                yellow: '#f9e2af',
                blue: '#89b4fa',
                magenta: '#f5c2e7',
                cyan: '#94e2d5',
                white: '#cdd6f4',
                brightBlack: '#585b70',
                brightRed: '#f38ba8',
                brightGreen: '#a6e3a1',
                brightYellow: '#f9e2af',
                brightBlue: '#89b4fa',
                brightMagenta: '#f5c2e7',
                brightCyan: '#94e2d5',
                brightWhite: '#a6adc8'
            },
            dracula: {
                background: '#282a36',
                foreground: '#f8f8f2',
                cursor: '#bd93f9',
                black: '#21222c',
                red: '#ff5555',
                green: '#50fa7b',
                yellow: '#f1fa8c',
                blue: '#bd93f9',
                magenta: '#ff79c6',
                cyan: '#8be9fd',
                white: '#f8f8f2',
                brightBlack: '#6272a4',
                brightRed: '#ff6e6e',
                brightGreen: '#69ff94',
                brightYellow: '#ffffa5',
                brightBlue: '#d6acff',
                brightMagenta: '#ff92df',
                brightCyan: '#a4ffff',
                brightWhite: '#ffffff'
            },
            tokyo: {
                background: '#1a1b26',
                foreground: '#a9b1d6',
                cursor: '#bb9af7',
                black: '#15161e',
                red: '#f7768e',
                green: '#9ece6a',
                yellow: '#e0af68',
                blue: '#7aa2f7',
                magenta: '#bb9af7',
                cyan: '#7dcfff',
                white: '#a9b1d6',
                brightBlack: '#414868',
                brightRed: '#ff7a93',
                brightGreen: '#b9f27c',
                brightYellow: '#ff9e64',
                brightBlue: '#7da6ff',
                brightMagenta: '#bb9af7',
                brightCyan: '#0db9d7',
                brightWhite: '#c0caf5'
            },
            contrast: {
                background: '#000000',
                foreground: '#ffffff',
                cursor: '#ffffff',
                black: '#000000',
                red: '#ffffff',
                green: '#ffffff',
                yellow: '#ffffff',
                blue: '#ffffff',
                magenta: '#ffffff',
                cyan: '#ffffff',
                white: '#ffffff',
                brightBlack: '#555555',
                brightRed: '#ffffff',
                brightGreen: '#ffffff',
                brightYellow: '#ffffff',
                brightBlue: '#ffffff',
                brightMagenta: '#ffffff',
                brightCyan: '#ffffff',
                brightWhite: '#ffffff'
            }
        };

        function initTerminal() {
            term = new Terminal({
                fontFamily: '"Fira Code", monospace',
                fontSize: 14,
                lineHeight: 1.25,
                cols: 80,
                rows: 24,
                theme: xtermThemes.catppuccin,
                cursorBlink: true,
                cursorStyle: 'block'
            });
            
            term.open(document.getElementById('terminal-screen-preview'));
            
            term.writeln("\x1b[1;36mWelcome to TermForge Interactive Documentation Shell!\x1b[0m");
            term.writeln("Type \x1b[33mhelp\x1b[0m to list available commands.");
            term.writeln("");
            prompt();
            
            term.onData(data => {
                const code = data.charCodeAt(0);
                if (code === 13) { // Enter
                    term.write("\r\n");
                    handleCommand(currentLine);
                    currentLine = "";
                } else if (code === 127) { // Backspace
                    if (currentLine.length > 0) {
                        currentLine = currentLine.slice(0, -1);
                        term.write("\b \b");
                    }
                } else if (code < 32) {
                    // Ignore other control codes
                } else {
                    currentLine += data;
                    term.write(data);
                }
            });
        }

        function prompt() {
            if (inRepl) {
                term.write("\x1b[32m>>> \x1b[0m");
            } else {
                term.write("\x1b[1;34mdox@termforge\x1b[0m:\x1b[1;32m~\x1b[0m$ ");
            }
        }

        function handleCommand(line) {
            const cmd = line.trim();
            if (!cmd) {
                prompt();
                return;
            }
            
            if (inRepl) {
                if (cmd === "exit()" || cmd === "quit" || cmd === "exit") {
                    inRepl = false;
                    term.writeln("Exiting TermForge interactive REPL.");
                    prompt();
                    return;
                }
                
                if (cmd.startsWith("from termforge")) {
                    term.writeln("");
                } else if (cmd.includes(".render()")) {
                    term.writeln("\x1b[33m[Simulated Rendering Output]\x1b[0m");
                    term.writeln("┌──────────────────────────┐");
                    term.writeln("│   Hello from TermForge   │");
                    term.writeln("└──────────────────────────┘");
                } else {
                    term.writeln("Python 3.12 (mock): executed successfully.");
                }
                prompt();
                return;
            }
            
            const parts = cmd.split(" ");
            const mainCmd = parts[0];
            
            if (mainCmd === "help") {
                term.writeln("Available commands:");
                term.writeln("  \x1b[33mlist\x1b[0m                    List all available stories");
                term.writeln("  \x1b[33mrun <story>\x1b[0m             Run a story (e.g. run text/markup_demo)");
                term.writeln("  \x1b[33mtermforge-play\x1b[0m          Boot interactive python REPL");
                term.writeln("  \x1b[33mtermforge-layout\x1b[0m        Run layout visualizer simulation");
                term.writeln("  \x1b[33mclear\x1b[0m                   Clear terminal screen");
            } else if (mainCmd === "clear") {
                term.clear();
                term.write("\x1b[H"); // Reset cursor home
            } else if (mainCmd === "list") {
                term.writeln("Stories:");
                for (const mod in storiesData) {
                    for (const comp in storiesData[mod]) {
                        term.writeln(`  - ${mod}/${comp}`);
                    }
                }
            } else if (mainCmd === "run") {
                const target = parts[1];
                if (!target) {
                    term.writeln("Usage: run <module/component>");
                } else {
                    const [mod, comp] = target.split("/");
                    if (storiesData[mod] && storiesData[mod][comp]) {
                        selectStory(mod, comp);
                    } else {
                        term.writeln(`Error: Story not found: ${target}`);
                    }
                }
            } else if (mainCmd === "termforge-play") {
                inRepl = true;
                term.writeln("TermForge Interactive Playground REPL (mock)");
                term.writeln("Type exit() to return to shell.");
            } else if (mainCmd === "termforge-layout") {
                term.writeln("TermForge Layout Visualizer simulation:");
                term.writeln("┌───────────────────────────────────┐");
                term.writeln("│  [Window] width=60 height=10      │");
                term.writeln("│  - Box constraints: FIXED         │");
                term.writeln("└───────────────────────────────────┘");
            } else {
                term.writeln(`bash: ${mainCmd}: command not found`);
            }
            
            prompt();
        }

        function populateMenu() {
            const scroller = document.getElementById("sidebar-scroller");
            scroller.innerHTML = "";
            
            let firstKey = null;
            
            for (const mod in storiesData) {
                const groupDiv = document.createElement("div");
                groupDiv.className = "module-group";
                
                const header = document.createElement("button");
                header.className = "module-header";
                header.id = "header-" + mod;
                header.onclick = () => toggleModule(mod);
                
                const titleSpan = document.createElement("span");
                titleSpan.textContent = mod;
                
                const chevronSpan = document.createElement("span");
                chevronSpan.className = "chevron";
                chevronSpan.textContent = "▼";
                
                header.appendChild(titleSpan);
                header.appendChild(chevronSpan);
                
                const list = document.createElement("ul");
                list.className = "menu-list";
                list.id = "group-" + mod;
                
                for (const comp in storiesData[mod]) {
                    const key = mod + "/" + comp;
                    if (!firstKey) firstKey = key;
                    
                    const li = document.createElement("li");
                    li.className = "menu-item";
                    li.id = "item-" + mod + "-" + comp;
                    
                    const btn = document.createElement("button");
                    btn.textContent = comp;
                    btn.onclick = () => selectStory(mod, comp);
                    
                    li.appendChild(btn);
                    list.appendChild(li);
                }
                
                groupDiv.appendChild(header);
                groupDiv.appendChild(list);
                scroller.appendChild(groupDiv);
            }
            
            if (firstKey) {
                const [mod, comp] = firstKey.split("/");
                // Open first module group automatically
                toggleModule(mod);
                selectStory(mod, comp);
            }
        }
        
        function toggleModule(mod) {
            const header = document.getElementById("header-" + mod);
            const list = document.getElementById("group-" + mod);
            
            if (list.style.display === "flex") {
                list.style.display = "none";
                header.classList.remove("expanded");
            } else {
                list.style.display = "flex";
                header.classList.add("expanded");
            }
        }

        function selectStory(mod, comp) {
            currentMod = mod;
            currentComp = comp;
            
            // Remove active state
            document.querySelectorAll(".menu-item").forEach(el => el.classList.remove("active"));
            
            const item = document.getElementById("item-" + mod + "-" + comp);
            if (item) {
                item.classList.add("active");
                // Ensure parent list is displayed
                const list = document.getElementById("group-" + mod);
                if (list && list.style.display !== "flex") {
                    toggleModule(mod);
                }
            }
            
            document.getElementById("active-title").textContent = mod.toUpperCase() + " : " + comp.toUpperCase();
            document.getElementById("term-filename").textContent = comp + ".py";
            
            const data = storiesData[mod][comp];
            
            // Clear and render raw ANSI in terminal emulator
            term.clear();
            term.write("\x1b[H"); // Reset cursor home
            term.writeln(`\x1b[1;34mdox@termforge\x1b[0m:\x1b[1;32m~\x1b[0m$ run ${mod}/${comp}`);
            term.write(data.raw_ansi.replace(/\n/g, "\r\n"));
            term.writeln("");
            prompt();
            
            // Code view
            const codeEscaped = data.code
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;");
            document.getElementById("terminal-screen-code").innerHTML = codeEscaped;
        }
        
        function showTab(tab) {
            currentTab = tab;
            document.getElementById("tab-preview").classList.remove("active");
            document.getElementById("tab-code").classList.remove("active");
            
            if (tab === 'preview') {
                document.getElementById("tab-preview").classList.add("active");
                document.getElementById("terminal-screen-preview").style.display = "block";
                document.getElementById("terminal-screen-code").style.display = "none";
            } else {
                document.getElementById("tab-code").classList.add("active");
                document.getElementById("terminal-screen-preview").style.display = "none";
                document.getElementById("terminal-screen-code").style.display = "block";
            }
        }
        
        function changeThemeSkin(theme) {
            document.body.className = "theme-" + theme;
            if (term && xtermThemes[theme]) {
                term.options.theme = xtermThemes[theme];
            }
        }
        
        window.onload = () => {
            initTerminal();
            populateMenu();
        };
    </script>
</body>
</html>
"""
    
    # 3. Inject goldens JSON data
    injected_html = html_template.replace("%STORIES_DATA%", json.dumps(goldens, indent=2))
    
    output_path = os.path.join(docs_dir, "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(injected_html)
        
    print(f"✅ Static docs site successfully compiled to {output_path}")

if __name__ == "__main__":
    main()
