#!/usr/bin/env python3
import os
import re
import json

def ansi_to_html(ansi_str: str) -> str:
    pattern = re.compile(r'\033\[([0-9;]*)m')
    parts = pattern.split(ansi_str)
    
    html = []
    active_span = False
    
    fg = None
    bg = None
    bold = False
    dim = False
    italic = False
    underline = False
    strikethrough = False
    
    def get_style_str() -> str:
        styles = []
        if fg:
            styles.append(f"color: {fg}")
        if bg:
            styles.append(f"background-color: {bg}")
        if bold:
            styles.append("font-weight: bold")
        if dim:
            styles.append("opacity: 0.6")
        if italic:
            styles.append("font-style: italic")
        if underline or strikethrough:
            dec = []
            if underline: dec.append("underline")
            if strikethrough: dec.append("line-through")
            styles.append(f"text-decoration: {' '.join(dec)}")
        return "; ".join(styles)

    for i, part in enumerate(parts):
        if i % 2 == 0:
            if part:
                escaped = part.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                if active_span:
                    html.append(f"</span>")
                style_str = get_style_str()
                if style_str:
                    html.append(f'<span style="{style_str}">{escaped}')
                    active_span = True
                else:
                    html.append(escaped)
                    active_span = False
        else:
            codes = []
            if part:
                try:
                    codes = [int(c) for c in part.split(";") if c]
                except ValueError:
                    pass
            if not codes:
                fg, bg = None, None
                bold, dim, italic, underline, strikethrough = False, False, False, False, False
                continue
                
            idx = 0
            while idx < len(codes):
                code = codes[idx]
                if code == 0:
                    fg, bg = None, None
                    bold, dim, italic, underline, strikethrough = False, False, False, False, False
                elif code == 1:
                    bold = True
                elif code == 2:
                    dim = True
                elif code == 3:
                    italic = True
                elif code == 4:
                    underline = True
                elif code == 9:
                    strikethrough = True
                elif code == 22:
                    bold, dim = False, False
                elif code == 23:
                    italic = False
                elif code == 24:
                    underline = False
                elif code == 29:
                    strikethrough = False
                elif 30 <= code <= 37:
                    colors = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
                    fg = f"var(--ansi-{colors[code - 30]})"
                elif 90 <= code <= 97:
                    colors = ["bright_black", "bright_red", "bright_green", "bright_yellow", "bright_blue", "bright_magenta", "bright_cyan", "bright_white"]
                    fg = f"var(--ansi-{colors[code - 90]})"
                elif code == 38:
                    if idx + 1 < len(codes):
                        mode = codes[idx+1]
                        if mode == 5:
                            idx += 2
                        elif mode == 2:
                            if idx + 4 < len(codes):
                                r, g, b = codes[idx+2], codes[idx+3], codes[idx+4]
                                fg = f"rgb({r},{g},{b})"
                                idx += 4
                elif 40 <= code <= 47:
                    colors = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
                    bg = f"var(--ansi-{colors[code - 40]})"
                elif 100 <= code <= 107:
                    colors = ["bright_black", "bright_red", "bright_green", "bright_yellow", "bright_blue", "bright_magenta", "bright_cyan", "bright_white"]
                    bg = f"var(--ansi-{colors[code - 100]})"
                elif code == 48:
                    if idx + 1 < len(codes):
                        mode = codes[idx+1]
                        if mode == 5:
                            idx += 2
                        elif mode == 2:
                            if idx + 4 < len(codes):
                                r, g, b = codes[idx+2], codes[idx+3], codes[idx+4]
                                bg = f"rgb({r},{g},{b})"
                                idx += 4
                idx += 1
                
    if active_span:
        html.append("</span>")
    return "".join(html)

def main() -> None:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    stories_dir = os.path.join(base_dir, "stories")
    docs_dir = os.path.join(base_dir, "docs-site")
    os.makedirs(docs_dir, exist_ok=True)
    
    # 1. Gather all golden files
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
                    
                    if module not in goldens:
                        goldens[module] = {}
                    goldens[module][name] = ansi_to_html(content)
                    
    # 2. Write HTML template
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TermForge Documentation Site</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Outfit:wght@400;600;800&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            /* Theme variables mapping */
            --bg-color: #0f111a;
            --text-color: #e6edf3;
            --sidebar-bg: rgba(20, 24, 38, 0.6);
            --card-bg: rgba(30, 35, 54, 0.4);
            --border-glow: #7f00ff;
            --accent-glow: #00f0ff;
            
            /* ANSI Palette fallback mapping */
            --ansi-black: #151820;
            --ansi-red: #ff5555;
            --ansi-green: #50fa7b;
            --ansi-yellow: #f1fa8c;
            --ansi-blue: #bd93f9;
            --ansi-magenta: #ff79c6;
            --ansi-cyan: #8be9fd;
            --ansi-white: #f8f8f2;
            
            --ansi-bright_black: #6272a4;
            --ansi-bright_red: #ff6e6e;
            --ansi-bright_green: #69ff94;
            --ansi-bright_yellow: #ffffa5;
            --ansi-bright_blue: #d6acff;
            --ansi-bright_magenta: #ff92df;
            --ansi-bright_cyan: #a4ffff;
            --ansi-bright_white: #ffffff;
        }
        
        /* Dracula theme skin override */
        .theme-dracula {
            --bg-color: #282a36;
            --text-color: #f8f8f2;
            --sidebar-bg: rgba(40, 42, 54, 0.7);
            --card-bg: rgba(68, 71, 90, 0.4);
            --border-glow: #bd93f9;
            --accent-glow: #8be9fd;
        }

        /* Tokyo Night theme skin override */
        .theme-tokyo {
            --bg-color: #1a1b26;
            --text-color: #a9b1d6;
            --sidebar-bg: rgba(26, 27, 38, 0.7);
            --card-bg: rgba(36, 40, 59, 0.4);
            --border-glow: #bb9af7;
            --accent-glow: #7aa2f7;
        }

        /* Catppuccin Mocha theme skin override */
        .theme-catppuccin {
            --bg-color: #1e1e2e;
            --text-color: #cdd6f4;
            --sidebar-bg: rgba(30, 30, 46, 0.7);
            --card-bg: rgba(49, 50, 68, 0.4);
            --border-glow: #b4befe;
            --accent-glow: #89b4fa;
        }

        /* High Contrast theme skin override */
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
        
        /* Neon Blur Background Highlights */
        .glow-sphere {
            position: absolute;
            border-radius: 50%;
            filter: blur(120px);
            z-index: -1;
            opacity: 0.35;
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
        
        /* Layout */
        .sidebar {
            width: 280px;
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
            margin-bottom: 10px;
        }
        
        .menu-list {
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        
        .menu-item button {
            width: 100%;
            background: transparent;
            border: none;
            color: var(--text-color);
            text-align: left;
            padding: 10px 15px;
            font-size: 14px;
            font-weight: 500;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .menu-item button:hover, .menu-item.active button {
            background: rgba(255, 255, 255, 0.05);
            box-shadow: inset 0 0 10px rgba(255, 255, 255, 0.02);
            color: #ffffff;
        }
        
        .menu-item.active button {
            border-left: 3px solid var(--border-glow);
            border-radius: 0 8px 8px 0;
            padding-left: 12px;
        }
        
        /* Main Panel */
        .main-content {
            flex-grow: 1;
            padding: 50px 60px;
            max-width: 1200px;
            display: flex;
            flex-direction: column;
            gap: 40px;
        }
        
        /* Header switcher card */
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
        
        /* Terminal Showcase Emulator */
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
        
        .terminal-body {
            padding: 24px;
            font-family: 'Fira Code', monospace;
            font-size: 15px;
            line-height: 1.45;
            white-space: pre;
            overflow-x: auto;
            color: var(--ansi-white);
        }
        
        /* Floating animations */
        @keyframes pulse-glow {
            0% { box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6), 0 0 20px rgba(127, 0, 255, 0.1); }
            50% { box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6), 0 0 35px rgba(0, 240, 255, 0.2); }
            100% { box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6), 0 0 20px rgba(127, 0, 255, 0.1); }
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
            <h1>TermForge v1.0</h1>
            <p style="font-size: 12px; opacity: 0.5; margin-top: 5px;">TUI Design System</p>
        </div>
        
        <div>
            <div class="menu-title">Modules</div>
            <ul class="menu-list" id="component-menu">
                <!-- Javascript populated -->
            </ul>
        </div>
    </div>
    
    <div class="main-content">
        <div class="controls-card">
            <div class="controls-title">
                <h2 id="active-title">Component Showcase</h2>
                <p style="font-size: 13px; opacity: 0.6; margin-top: 5px;">Interactive golden file visualization</p>
            </div>
            <div class="theme-selector">
                <label for="theme-skin" style="font-size: 14px; font-weight: 600;">Theme Skin:</label>
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
                <div class="terminal-title" id="term-filename">component.py</div>
                <div></div>
            </div>
            <div class="terminal-body" id="terminal-screen">
                <!-- Javascript populated -->
            </div>
        </div>
    </div>
    
    <script>
        const storiesData = %STORIES_DATA%;
        
        function populateMenu() {
            const menu = document.getElementById("component-menu");
            menu.innerHTML = "";
            
            let firstKey = null;
            
            for (const mod in storiesData) {
                for (const comp in storiesData[mod]) {
                    const key = mod + "/" + comp;
                    if (!firstKey) firstKey = key;
                    
                    const li = document.createElement("li");
                    li.className = "menu-item";
                    li.id = "item-" + mod + "-" + comp;
                    
                    const btn = document.createElement("button");
                    btn.textContent = mod + " : " + comp;
                    btn.onclick = () => selectStory(mod, comp);
                    
                    li.appendChild(btn);
                    menu.appendChild(li);
                }
            }
            
            if (firstKey) {
                const [mod, comp] = firstKey.split("/");
                selectStory(mod, comp);
            }
        }
        
        function selectStory(mod, comp) {
            // Remove active classes
            document.querySelectorAll(".menu-item").forEach(el => el.classList.remove("active"));
            
            // Set active class
            const item = document.getElementById("item-" + mod + "-" + comp);
            if (item) item.classList.add("active");
            
            // Update title & screen
            document.getElementById("active-title").textContent = mod.toUpperCase() + " : " + comp.toUpperCase();
            document.getElementById("term-filename").textContent = comp + ".py";
            
            const screen = document.getElementById("terminal-screen");
            screen.innerHTML = storiesData[mod][comp];
        }
        
        function changeThemeSkin(theme) {
            document.body.className = "theme-" + theme;
        }
        
        window.onload = populateMenu;
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
