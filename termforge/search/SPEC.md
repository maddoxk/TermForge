# SearchBar Component Specification

Provides input query lines with case-insensitive filtered lists, highlighting the matching characters.

## 1. Data Models

### `SearchBarSpec`
- `query`: string (the search query)
- `candidates`: list of strings (raw strings to filter)
- `placeholder`: string (default `"Search..."`)
- `match_style`: string | null (theme token for matching text runs)
- `input_style`: string | null (theme token for input text)
- `placeholder_style`: string | null (theme token for placeholder text)
- `width`: integer | null
- `height`: integer | null
- `spec_type`: `"search_bar"`

---

## 2. Filtering & Case-Insensitive Highlight Math

Filters list options matching the query. Split occurrences of the query case-insensitively while preserving the original character case inside the styled blocks.

#### Pseudocode:
```
function highlight_matches(text: str, query: str, match_style: str) -> str:
    if query is empty:
        return text
        
    q_len = length(query)
    q_lower = lowercase(query)
    text_lower = lowercase(text)
    
    parts = []
    start = 0
    idx = find_substring(text_lower, q_lower, start)
    
    while idx != -1:
        parts.push(substring(text, start, idx))
        match_str = substring(text, idx, idx + q_len)
        parts.push(style_string(match_str, match_style))
        start = idx + q_len
        idx = find_substring(text_lower, q_lower, start)
        
    parts.push(substring(text, start))
    return join(parts)

function render_search_bar(spec: SearchBarSpec, max_width: int, max_height: int) -> list[str]:
    # Line 0: Input line
    prefix = "🔍 Search: "
    if spec.query is empty:
        styled_input = style_string(spec.placeholder, spec.placeholder_style)
        raw_len = length(prefix) + length(spec.placeholder)
    else:
        styled_input = style_string(spec.query, spec.input_style)
        raw_len = length(prefix) + length(spec.query)
        
    lines = [prefix + styled_input + spaces(max_width - raw_len)]
    
    # Lines 1..H: Candidates
    q_lower = lowercase(spec.query)
    for cand in spec.candidates:
        if q_lower in lowercase(cand):
            styled_cand = highlight_matches(cand, spec.query, spec.match_style)
            lines.push(styled_cand + spaces(max_width - length(cand)))
            
    # Pad vertical height
    while length(lines) < max_height:
        lines.push(spaces(max_width))
        
    return lines[0:max_height]
```
