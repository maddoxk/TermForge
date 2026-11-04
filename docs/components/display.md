# Display Components

Components for presenting information. Each example builds a spec and renders it with `tf.draw()`.

## Card

A bordered panel with an optional title, subtitle, and body content.

```python
import termforge as tf

print(tf.draw(tf.CardSpec(
    title="Server Node-01",
    subtitle="us-east-1",
    content="CPU: 42%\nRAM: 8.2 GB\nStatus: healthy",
    width=36,
)))
```

## Badge

A compact status label with a severity color.

```python
import termforge as tf

print(tf.draw(tf.BadgeSpec(text="ACTIVE", severity="success")))
print(tf.draw(tf.BadgeSpec(text="DEGRADED", severity="warning")))
print(tf.draw(tf.BadgeSpec(text="OFFLINE", severity="error")))
```

## Text

Aligned, wrapped text with overflow control.

```python
import termforge as tf

print(tf.draw(tf.TextSpec(
    content="TermForge renders rich text with alignment and wrapping.",
    align="center",
    max_width=40,
), width=40))
```

## Toast

A transient notification bubble.

```python
import termforge as tf

print(tf.draw(tf.ToastSpec(text="File saved successfully", toast_type="success")))
```

## Tooltip

A pointer bubble anchored to a coordinate.

```python
import termforge as tf

print(tf.draw(tf.TooltipSpec(text="Press Enter to confirm", anchor_x=4, anchor_y=0)))
```

## Divider

A horizontal rule with an optional centered label.

```python
import termforge as tf

print(tf.draw(tf.DividerSpec(label="SETTINGS", alignment="center", width=40), width=40))
```

## Previews

### Card Preview

<div class="terminal-preview">
<pre style="background:#1e1e2e;padding:16px;border-radius:8px;overflow-x:auto;font-family:'Fira Code',monospace;font-size:13px;line-height:1.4;white-space:pre;">=== TermForge Card Component Demo ===

--- 1. Card with Header &amp; Single Borders (Width = 40, Height = 7) ---
<span style="color: #3D3F55">┌</span><span style="color: #3D3F55">─</span><span style="color: #7AA2F7"> Host Statistics </span><span style="color: #BB9AF7">(Node-01) </span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">┐</span>
<span style="color: #3D3F55">│</span><span style="color: #9ECE6A">CPU Load: 45.8%                       </span><span style="color: #3D3F55">│</span>
<span style="color: #3D3F55">│</span><span style="color: #9ECE6A">RAM Usage: 8.2 GB / 16.0 GB           </span><span style="color: #3D3F55">│</span>
<span style="color: #3D3F55">│</span><span style="color: #9ECE6A">IO operations: Normal                 </span><span style="color: #3D3F55">│</span>
<span style="color: #3D3F55">│</span><span style="color: #9ECE6A">Temperature: 42 C                     </span><span style="color: #3D3F55">│</span>
<span style="color: #3D3F55">│</span><span style="color: #9ECE6A">                                      </span><span style="color: #3D3F55">│</span>
<span style="color: #3D3F55">└</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">┘</span>

--- 2. Card with Rounded Borders &amp; No Header (Width = 40, Height = 7) ---
<span style="color: #3D3F55">╭</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">╮</span>
<span style="color: #3D3F55">│</span><span style="color: #E0AF68">CPU Load: 45.8%                       </span><span style="color: #3D3F55">│</span>
<span style="color: #3D3F55">│</span><span style="color: #E0AF68">RAM Usage: 8.2 GB / 16.0 GB           </span><span style="color: #3D3F55">│</span>
<span style="color: #3D3F55">│</span><span style="color: #E0AF68">IO operations: Normal                 </span><span style="color: #3D3F55">│</span>
<span style="color: #3D3F55">│</span><span style="color: #E0AF68">Temperature: 42 C                     </span><span style="color: #3D3F55">│</span>
<span style="color: #3D3F55">│</span><span style="color: #E0AF68">                                      </span><span style="color: #3D3F55">│</span></pre>
</div>

### Toast Preview

<div class="terminal-preview">
<pre style="background:#1e1e2e;padding:16px;border-radius:8px;overflow-x:auto;font-family:'Fira Code',monospace;font-size:13px;line-height:1.4;white-space:pre;">=== TermForge Toast Component Demo ===

--- 1. Success Toast (Top-Right, Rounded) ---
     <span style="color: #3D3F55">╭</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">╮</span>
     <span style="color: #3D3F55">│</span><span style="color: #9ECE6A">[SUCCESS]</span> <span style="color: #BB9AF7">Build compiled in 1.45s</span><span style="color: #3D3F55">│</span>
     <span style="color: #3D3F55">╰</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">╯</span>
                                        
                                        

--- 2. Error Toast (Bottom-Left, Double) ---
                                        
                                        
<span style="color: #3D3F55">╔</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">╗</span>  
<span style="color: #3D3F55">║</span>[ERROR] <span style="color: #BB9AF7">Disk write permission denied</span><span style="color: #3D3F55">║</span>  
<span style="color: #3D3F55">╚</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">═</span><span style="color: #3D3F55">╝</span>  

--- 3. Warning Toast (Top-Left, Single) ---
<span style="color: #3D3F55">┌</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">┐</span>   </pre>
</div>

### Text Preview

<div class="terminal-preview">
<pre style="background:#1e1e2e;padding:16px;border-radius:8px;overflow-x:auto;font-family:'Fira Code',monospace;font-size:13px;line-height:1.4;white-space:pre;">--- TermForge Text Markup Gallery ---
Plain text example.
<span style="font-weight: bold">Bold text example.</span>
<span style="font-weight: lighter">Dim text example.</span>
<span style="font-style: italic">Italic text example.</span>
<span style="text-decoration: underline">Underline text example.</span>
<span style="text-decoration: line-through">Strikethrough text example.</span>
<span style="font-weight: bold"></span><span style="font-weight: bold; font-style: italic"></span><span style="font-weight: bold; font-style: italic; text-decoration: underline">Bold, italic, and underline combined.</span>
<span style="color: #CD0000">Red foreground text.</span>
<span style="background-color: #0000EE">Blue background text.</span>
<span style="color: #00CD00"></span><span style="color: #00CD00; background-color: #CDCD00">Green on yellow text.</span>
<span style="color: #FF00FF">Custom Magenta via hex #ff00ff</span>

--- Alignment Examples (width=40) ---
|<span style="font-weight: bold">Aligned LEFT</span>|
|             <span style="font-weight: bold">Aligned CENTER</span>             |
|                           <span style="font-weight: bold">Aligned RIGHT</span>|
</pre>
</div>
