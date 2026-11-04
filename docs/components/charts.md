# Charts

All charts use a single `tf.ChartSpec`, selecting a renderer via the `tf.ChartType` enum. Data is passed in `series` (or `ohlc_series` for candlesticks).

## ChartType

| Type | Enum value |
|------|------------|
| Line | `ChartType.LINE` |
| Bar | `ChartType.BAR` |
| Scatter | `ChartType.SCATTER` |
| Sparkline | `ChartType.SPARKLINE` |
| Heatmap | `ChartType.HEATMAP` |
| Candlestick | `ChartType.CANDLESTICK` |

Also available: `HISTOGRAM`, `STACKED_BAR`, `MULTI_BAR`.

## Line

```python
import termforge as tf

print(tf.draw(tf.ChartSpec(
    chart_type=tf.ChartType.LINE,
    series=[[3, 7, 2, 8, 5, 9, 4, 6]],
    width=48,
    height=10,
    title="Requests/sec",
), width=48, height=10))
```

## Bar

```python
import termforge as tf

print(tf.draw(tf.ChartSpec(
    chart_type=tf.ChartType.BAR,
    series=[[12, 30, 18, 25]],
    width=40,
    height=8,
), width=40, height=8))
```

## Scatter

```python
import termforge as tf

print(tf.draw(tf.ChartSpec(
    chart_type=tf.ChartType.SCATTER,
    series=[[1, 4, 2, 8, 5, 3, 7]],
    width=40,
    height=10,
), width=40, height=10))
```

## Sparkline

A compact single-line trend.

```python
import termforge as tf

print(tf.draw(tf.ChartSpec(
    chart_type=tf.ChartType.SPARKLINE,
    series=[[1, 3, 2, 5, 4, 8, 6, 9, 7]],
    width=24,
), width=24))
```

## Heatmap

```python
import termforge as tf

print(tf.draw(tf.ChartSpec(
    chart_type=tf.ChartType.HEATMAP,
    series=[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
    width=30,
    height=8,
), width=30, height=8))
```

## Candlestick

Candlesticks use `ohlc_series`, an `OHLCSeries` whose `data` is a list of
`{"open", "high", "low", "close"}` dicts.

```python
import termforge as tf

ohlc = tf.OHLCSeries(data=[
    {"open": 10, "high": 13, "low": 9, "close": 12},
    {"open": 12, "high": 14, "low": 11, "close": 11},
    {"open": 11, "high": 12, "low": 10, "close": 11},
])
print(tf.draw(tf.ChartSpec(
    chart_type=tf.ChartType.CANDLESTICK,
    ohlc_series=ohlc,
    width=40,
    height=12,
), width=40, height=12))
```

## Previews

### Bar Chart Preview

<div class="terminal-preview">
<pre style="background:#1e1e2e;padding:16px;border-radius:8px;overflow-x:auto;font-family:'Fira Code',monospace;font-size:13px;line-height:1.4;white-space:pre;">--- Bar Chart (Standard Canvas) ---
              Lost Numbers Bar Chart              
  45.0 │                                          
  40.0 │                                   <span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span> 
  35.0 │                                   <span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span> 
  30.0 │                                   <span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span> 
  25.0 │                                   <span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span> 
  20.0 │                            <span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span> <span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span> 
  15.0 │              <span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span> <span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span> <span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span> <span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span> 
  10.0 │              <span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span> <span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span> <span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span> <span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span> 
   5.0 │       <span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span> <span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span> <span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span> <span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span> <span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span> 
   0.0 │<span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span> <span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span> <span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span> <span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span> <span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span> <span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span><span style="color: #000000">█</span> 
       └──────────────────────────────────────────
        .0     1.0     2.0     3.0     4.0      5.
</pre>
</div>

### Line Chart Preview

<div class="terminal-preview">
<pre style="background:#1e1e2e;padding:16px;border-radius:8px;overflow-x:auto;font-family:'Fira Code',monospace;font-size:13px;line-height:1.4;white-space:pre;">--- Sine Wave (Standard Canvas) ---
                    Sine Wave Line Chart                    
  10.0 │                                                    
   8.3 │   <span style="color: #000000">*</span><span style="color: #000000">*</span><span style="color: #000000">*</span><span style="color: #000000">*</span><span style="color: #000000">*</span>                  <span style="color: #000000">*</span><span style="color: #000000">*</span><span style="color: #000000">*</span>                    <span style="color: #000000">*</span><span style="color: #000000">*</span><span style="color: #000000">*</span>
   6.7 │  <span style="color: #000000">*</span>    <span style="color: #000000">*</span>                 <span style="color: #000000">*</span>   <span style="color: #000000">*</span>                 <span style="color: #000000">*</span><span style="color: #000000">*</span>   
   5.0 │  <span style="color: #000000">*</span>     <span style="color: #000000">*</span>               <span style="color: #000000">*</span>     <span style="color: #000000">*</span>               <span style="color: #000000">*</span>     
   3.3 │ <span style="color: #000000">*</span>       <span style="color: #000000">*</span>             <span style="color: #000000">*</span>       <span style="color: #000000">*</span>             <span style="color: #000000">*</span>      
   1.7 │<span style="color: #000000">*</span>        <span style="color: #000000">*</span>            <span style="color: #000000">*</span>         <span style="color: #000000">*</span>           <span style="color: #000000">*</span>       
   0.0 │<span style="color: #000000">*</span>         <span style="color: #000000">*</span>           <span style="color: #000000">*</span>         <span style="color: #000000">*</span>           <span style="color: #000000">*</span>       
  -1.7 │           <span style="color: #000000">*</span>         <span style="color: #000000">*</span>           <span style="color: #000000">*</span>         <span style="color: #000000">*</span>        
  -3.3 │           <span style="color: #000000">*</span>         <span style="color: #000000">*</span>            <span style="color: #000000">*</span>        <span style="color: #000000">*</span>        
  -5.0 │            <span style="color: #000000">*</span>       <span style="color: #000000">*</span>             <span style="color: #000000">*</span>       <span style="color: #000000">*</span>         
  -6.7 │             <span style="color: #000000">*</span>      <span style="color: #000000">*</span>              <span style="color: #000000">*</span>      <span style="color: #000000">*</span>         
  -8.3 │              <span style="color: #000000">*</span>    <span style="color: #000000">*</span>               <span style="color: #000000">*</span>     <span style="color: #000000">*</span>          
 -10.0 │               <span style="color: #000000">*</span><span style="color: #000000">*</span><span style="color: #000000">*</span><span style="color: #000000">*</span>                 <span style="color: #000000">*</span><span style="color: #000000">*</span><span style="color: #000000">*</span><span style="color: #000000">*</span><span style="color: #000000">*</span>           
       └────────────────────────────────────────────────────
        .0         7.2         14.5         21.8         29.
</pre>
</div>

### Sparkline Preview

<div class="terminal-preview">
<pre style="background:#1e1e2e;padding:16px;border-radius:8px;overflow-x:auto;font-family:'Fira Code',monospace;font-size:13px;line-height:1.4;white-space:pre;">Standard Sparkline:
 ▂ ▄▃▆▅▇▄█

Highlighted Peaks &amp; Valleys Sparkline:
<span style="color: #000000"> </span>▂ ▄▃▆▅▇▄<span style="color: #000000">█</span>
</pre>
</div>
