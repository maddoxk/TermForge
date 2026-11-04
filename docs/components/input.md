# Input Components

Components that represent interactive controls. Specs are stateless — you hold selection state (e.g. `selected_idx`) in your own application and re-render on change.

## ButtonGroup

A horizontal row of buttons with one selected.

```python
import termforge as tf

print(tf.draw(tf.ButtonGroupSpec(
    buttons=["Save", "Cancel", "Reset"],
    selected_idx=0,
)))
```

## Checklist

A multi-item list with checked/unchecked state and a cursor.

```python
import termforge as tf

print(tf.draw(tf.ChecklistSpec(
    items=[
        tf.ChecklistItemSpec(label="Enable logging", checked=True),
        tf.ChecklistItemSpec(label="Verbose output", checked=False),
    ],
    selected_idx=0,
)))
```

## Combobox

A single-select dropdown.

```python
import termforge as tf

print(tf.draw(tf.ComboboxSpec(
    options=["Python", "Rust", "Go"],
    selected_idx=0,
    is_open=True,
)))
```

## Radio

A single-select group of options.

```python
import termforge as tf

print(tf.draw(tf.RadioButtonSpec(
    items=[
        tf.RadioButtonItemSpec(label="Light"),
        tf.RadioButtonItemSpec(label="Dark"),
    ],
    selected_idx=1,
)))
```

## Slider

A value slider between a min and max.

```python
import termforge as tf

print(tf.draw(tf.SliderSpec(value=65, min_val=0, max_val=100, label="Volume", width=40), width=40))
```

## Toggle

An on/off switch.

```python
import termforge as tf

print(tf.draw(tf.ToggleSwitchSpec(label="Dark mode", state=True)))
```

## SearchBar

A query field with filtered candidates.

```python
import termforge as tf

print(tf.draw(tf.SearchBarSpec(
    query="dra",
    candidates=["dracula", "gruvbox", "nord"],
    placeholder="Search themes...",
)))
```

## Previews

### Checklist Preview

<div class="terminal-preview">
<pre style="background:#1e1e2e;padding:16px;border-radius:8px;overflow-x:auto;font-family:'Fira Code',monospace;font-size:13px;line-height:1.4;white-space:pre;">=== TermForge Checklist Component Demo ===

--- 1. Custom Checkbox Indicators &amp; Selection focused on Item 1 ---
<span style="color: #9ECE6A">☑ </span><span style="color: #9ECE6A">Install Core Dependencies</span>             
<span style="color: #7AA2F7">☐ </span><span style="color: #7AA2F7">Download Asset Resource Bundles</span>       
<span style="color: #9ECE6A">☑ </span><span style="color: #9ECE6A">Compile Binary Releases</span>               
<span style="color: #BB9AF7">☐ </span><span style="color: #BB9AF7">Run Local Verification Tests</span>          
                                        

--- 2. Standard Indicator Brackets &amp; Selection focused on Item 2 ---
<span style="color: #9ECE6A">[x] </span><span style="color: #9ECE6A">Install Core Dependencies</span>           
[ ] Download Asset Resource Bundles     
<span style="color: #E0AF68">[x] </span><span style="color: #E0AF68">Compile Binary Releases</span>             
[ ] Run Local Verification Tests        
                                        

JSON serialization length: 500 bytes
Portability check: OK</pre>
</div>

### Combobox Preview

<div class="terminal-preview">
<pre style="background:#1e1e2e;padding:16px;border-radius:8px;overflow-x:auto;font-family:'Fira Code',monospace;font-size:13px;line-height:1.4;white-space:pre;">=== TermForge Combobox Component Demo ===

--- 1. Combobox Closed (Width = 30, Height = 2) ---
<span style="color: #7AA2F7">[ 1440p (QHD)    ] ▼</span>          
                              

--- 2. Combobox Open (Width = 30, Height = 8) ---
<span style="color: #BB9AF7">[ 1440p (QHD)    ] ▼</span>          
<span style="color: #3D3F55">┌</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">┐</span>            
<span style="color: #3D3F55">│</span><span style="color: #BB9AF7"> 1080p (FHD)    </span><span style="color: #3D3F55">│</span>            
<span style="color: #3D3F55">│</span><span style="color: #BB9AF7"> 1440p (QHD)    </span><span style="color: #3D3F55">│</span>            
<span style="color: #3D3F55">│</span><span style="color: #E0AF68"> 2160p (4K UHD) </span><span style="color: #3D3F55">│</span>            
<span style="color: #3D3F55">│</span><span style="color: #BB9AF7"> 720p (HD)      </span><span style="color: #3D3F55">│</span>            
<span style="color: #3D3F55">└</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">─</span><span style="color: #3D3F55">┘</span>            
                              

JSON serialization length: 314 bytes
Portability check: OK</pre>
</div>

### Slider Preview

<div class="terminal-preview">
<pre style="background:#1e1e2e;padding:16px;border-radius:8px;overflow-x:auto;font-family:'Fira Code',monospace;font-size:13px;line-height:1.4;white-space:pre;">=== TermForge Slider Component Demo ===

--- 1. Slider at Minimum (0%) (Width = 40, Height = 2) ---
Volume Level  <span style="color: #3D3F55">[</span><span style="color: #9ECE6A"></span><span style="color: #7AA2F7">●</span><span style="color: #BB9AF7">--------------------</span><span style="color: #3D3F55">]</span> 0%
                                        

--- 2. Slider at Middle (50%) (Width = 40, Height = 2) ---
Volume Level  <span style="color: #3D3F55">[</span><span style="color: #9ECE6A">=========</span><span style="color: #7AA2F7">●</span><span style="color: #BB9AF7">----------</span><span style="color: #3D3F55">]</span> 50%
                                        

--- 3. Slider at Maximum (100%) (Width = 40, Height = 2) ---
Volume Level  <span style="color: #3D3F55">[</span><span style="color: #9ECE6A">==================</span><span style="color: #7AA2F7">●</span><span style="color: #BB9AF7"></span><span style="color: #3D3F55">]</span> 100%
                                        

JSON serialization length: 383 bytes
Portability check: OK
</pre>
</div>

### Search Bar Preview

<div class="terminal-preview">
<pre style="background:#1e1e2e;padding:16px;border-radius:8px;overflow-x:auto;font-family:'Fira Code',monospace;font-size:13px;line-height:1.4;white-space:pre;">=== TermForge SearchBar Component Demo ===

--- 1. Search Bar Empty Input (Width = 40, Height = 6) ---
🔍 Search: <span style="color: #BB9AF7">Type search terms here...</span>     
github                                  
gitlab                                  
git commit                              
subversion                              
mercurial                               

--- 2. Search Bar Filtered matches for 'git' (Width = 40, Height = 6) ---
🔍 Search: <span style="color: #7AA2F7">git</span>                           
<span style="color: #E0AF68">git</span>hub                                  
<span style="color: #E0AF68">git</span>lab                                  
<span style="color: #E0AF68">git</span> commit                              
di<span style="color: #E0AF68">git</span>al ocean                           
<span style="color: #E0AF68">Git</span> LFS                                 
</pre>
</div>
