# Layout Components

Components for structuring the screen — windows, split panes, dialogs, and collapsible sections.

## Windows

A bordered, titled region with scrollable content.

```python
import termforge as tf

print(tf.draw(tf.WindowSpec(
    title="Logs",
    content="[12:00] boot complete\n[12:01] listening on :8080",
    width=48,
    height=6,
), width=48, height=6))
```

## Panes

Split layouts that compose child windows horizontally or vertically.

```python
import termforge as tf

left = tf.WindowSpec(title="Nav", content="Home\nDocs\nAbout")
right = tf.WindowSpec(title="Content", content="Welcome to TermForge")

pane = tf.PaneSpec(direction="horizontal", children=[left, right], ratios=[1, 2])
print(tf.draw(pane, width=60, height=8))
```

## Dialog

A modal prompt with a title, body, and focusable buttons.

```python
import termforge as tf

print(tf.draw(tf.DialogSpec(
    title="Confirm",
    body="Delete this file? This cannot be undone.",
    buttons=["Cancel", "Delete"],
    focused_button_index=1,
), width=48, height=8))
```

## Accordion

A vertical list of collapsible sections.

```python
import termforge as tf

print(tf.draw(tf.AccordionSpec(
    items=[
        tf.AccordionItemSpec(title="General", details="Theme, language", is_expanded=True),
        tf.AccordionItemSpec(title="Advanced", details="Flags, env vars"),
    ],
    selected_idx=0,
)))
```

## Tabs

A horizontal tab strip with one active tab.

```python
import termforge as tf

print(tf.draw(tf.TabSpec(titles=["Overview", "Metrics", "Logs"], active_index=1), width=48))
```

## Previews

### Windows Preview

<div class="terminal-preview">
<pre style="background:#1e1e2e;padding:16px;border-radius:8px;overflow-x:auto;font-family:'Fira Code',monospace;font-size:13px;line-height:1.4;white-space:pre;">--- Window Layout Composited Screen ---
<span style="color: #000000">┌──── Sidebar ─────┐</span><span style="color: #000000">┌──────────── Content Pane ────────────┐</span>
<span style="color: #000000">│</span>* Home            <span style="color: #000000">│</span><span style="color: #000000">│</span>Welcome to TermForge!                 <span style="color: #000000">│</span>
<span style="color: #000000">│</span><span style="color: #000000">┌───── Modal Alert ─────┐</span>   a split screen layout demo.   <span style="color: #000000">│</span>
<span style="color: #000000">│</span><span style="color: #000000">│</span> Are you sure you      <span style="color: #000000">│</span><span style="color: #505050"></span><span style="font-weight: lighter; color: #505050">██</span>ht window has focus.           <span style="color: #000000">│</span>
<span style="color: #000000">│</span><span style="color: #000000">│</span> want to proceed?      <span style="color: #000000">│</span><span style="color: #505050"></span><span style="font-weight: lighter; color: #505050">██</span>math distributed sizes auto:   <span style="color: #000000">│</span>
<span style="color: #000000">│</span><span style="color: #000000">│</span>  [ OK ]  [ Cancel ]   <span style="color: #000000">│</span><span style="color: #505050"></span><span style="font-weight: lighter; color: #505050">██</span>                               <span style="color: #000000">│</span>
<span style="color: #000000">│</span><span style="color: #000000">└───────────────────────┘</span><span style="color: #505050"></span><span style="font-weight: lighter; color: #505050">██</span>                               <span style="color: #000000">│</span>
<span style="color: #000000">│</span>  <span style="color: #505050"></span><span style="font-weight: lighter; color: #505050">█████████████████████████</span>                               <span style="color: #000000">│</span>
<span style="color: #000000">│</span>                  <span style="color: #000000">│</span><span style="color: #000000">│</span>                                      <span style="color: #000000">│</span>
<span style="color: #000000">└──────────────────┘</span><span style="color: #000000">└──────────────────────────────────────┘</span>
</pre>
</div>

### Dialog Preview

<div class="terminal-preview">
<pre style="background:#1e1e2e;padding:16px;border-radius:8px;overflow-x:auto;font-family:'Fira Code',monospace;font-size:13px;line-height:1.4;white-space:pre;">┌─ Exit Confirmation ──────────────────────────┐
│Are you sure you want to exit the application?│
│                                              │
│[Yes]  &lt;No&gt;                                   │
└──────────────────────────────────────────────┘
                                                
</pre>
</div>

### Accordion Preview

<div class="terminal-preview">
<pre style="background:#1e1e2e;padding:16px;border-radius:8px;overflow-x:auto;font-family:'Fira Code',monospace;font-size:13px;line-height:1.4;white-space:pre;">=== TermForge Accordion Component Demo ===

--- 1. Expanded Item 0 &amp; Focused Cursor (Width = 50, Height = 7) ---
<span style="color: #E0AF68">v </span><span style="color: #E0AF68">General Configurations</span>                          
<span style="color: #BB9AF7">    Contains theme selections, font configurations,</span>
<span style="color: #BB9AF7">    and system locale mappings.</span>                   
&gt; Advanced System Settings                        
&gt; Diagnostic Logging API                          
                                                  
                                                  

--- 2. Expanded Item 0 &amp; Focused Cursor on Collapsed Item 1 ---
<span style="color: #7AA2F7">v </span><span style="color: #7AA2F7">General Configurations</span>                          
<span style="color: #BB9AF7">    Contains theme selections, font configurations,</span>
<span style="color: #BB9AF7">    and system locale mappings.</span>                   
<span style="color: #E0AF68">&gt; </span><span style="color: #E0AF68">Advanced System Settings</span>                        
&gt; Diagnostic Logging API                          
                                                  </pre>
</div>

### Tabs Preview

<div class="terminal-preview">
<pre style="background:#1e1e2e;padding:16px;border-radius:8px;overflow-x:auto;font-family:'Fira Code',monospace;font-size:13px;line-height:1.4;white-space:pre;">┌──────────┐ ┌──────┐ ┌──────────┐      
│*Overview*│ │ Logs │ │ Settings │      
└──────────┘ └──────┘ └──────────┘      
                                        
                                        
</pre>
</div>
