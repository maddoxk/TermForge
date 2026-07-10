import pytest
from termforge.core.types import StyleSpec, ColorValue
from termforge.text.types import TextSpan, TextRun, TextSpec, TextAlign, TextOverflow
from termforge.text.markup import parse_markup, strip_markup
from termforge.text.wrap import char_width, get_string_width, measure_text, wrap_text, truncate_text, wrap_run

def test_text_types_serialization():
    style = StyleSpec(fg=ColorValue(255, 0, 0, "red"), bold=True)
    span = TextSpan("hello", style)
    span_dict = span.to_dict()
    assert span_dict["text"] == "hello"
    assert span_dict["style"]["fg"]["r"] == 255
    
    span_back = TextSpan.from_dict(span_dict)
    assert span_back.text == "hello"
    assert span_back.style.bold is True
    assert span_back.style.fg.name == "red"

    run = TextRun([span, TextSpan(" world")])
    run_dict = run.to_dict()
    assert len(run_dict["spans"]) == 2
    
    run_back = TextRun.from_dict(run_dict)
    assert len(run_back.spans) == 2
    assert run_back.spans[0].text == "hello"

    spec = TextSpec(content=run, align=TextAlign.CENTER, overflow=TextOverflow.ELLIPSIS, max_width=40)
    spec_dict = spec.to_dict()
    assert spec_dict["align"] == "center"
    assert spec_dict["overflow"] == "ellipsis"
    assert spec_dict["max_width"] == 40
    
    spec_back = TextSpec.from_dict(spec_dict)
    assert isinstance(spec_back.content, TextRun)
    assert spec_back.align == TextAlign.CENTER
    assert spec_back.overflow == TextOverflow.ELLIPSIS
    assert spec_back.max_width == 40

def test_parse_markup():
    text = "Normal [bold]Bold[/bold] [fg=red]Red[/fg]"
    run = parse_markup(text)
    assert len(run.spans) == 4
    
    # Filter out empty spans
    non_empty_spans = [s for s in run.spans if s.text]
    assert len(non_empty_spans) == 4
    assert non_empty_spans[0].text == "Normal "
    assert non_empty_spans[0].style.bold is False
    assert non_empty_spans[1].text == "Bold"
    assert non_empty_spans[1].style.bold is True
    assert non_empty_spans[2].text == " "
    assert non_empty_spans[2].style.bold is False
    assert non_empty_spans[3].text == "Red"
    assert non_empty_spans[3].style.fg.name == "red"

def test_strip_markup():
    text = "Normal [bold]Bold[/bold] [fg=red]Red[/fg]"
    assert strip_markup(text) == "Normal Bold Red"

def test_char_width():
    assert char_width("a") == 1
    assert char_width(" ") == 1
    assert char_width("中") == 2
    assert char_width("😀") == 1 or char_width("😀") == 2 # depends on terminal/unicode block, but let's test CJK
    assert char_width("国") == 2

def test_measure_text():
    run = TextRun([TextSpan("hello"), TextSpan("中国")])
    assert measure_text(run) == 5 + 4 == 9

def test_wrap_text():
    text = "hello world this is a test of word wrapping"
    wrapped = wrap_text(text, 12)
    assert len(wrapped) > 1
    for line in wrapped:
        assert len(line) <= 12
    assert "".join(wrapped).replace(" ", "") == text.replace(" ", "")

def test_truncate_text():
    text = "hello world"
    assert truncate_text(text, 8) == "hello w…"
    assert truncate_text("中国文字非常好看", 8) == "中国文…"

def test_wrap_run():
    run = TextRun([
        TextSpan("hello world ", StyleSpec(bold=True)),
        TextSpan("this is a test", StyleSpec(fg=ColorValue(0, 0, 255, "blue")))
    ])
    wrapped = wrap_run(run, 10)
    assert len(wrapped) > 1
    for w_run in wrapped:
        assert measure_text(w_run) <= 10

def test_render_text():
    import re
    from termforge.text.render import render_text
    from termforge.core.types import ColorDepth
    
    spec = TextSpec(content="[bold]Hello[/bold] [fg=red]World[/fg]", align=TextAlign.CENTER, max_width=20)
    lines = render_text(spec, depth=ColorDepth.TRUECOLOR)
    assert len(lines) == 1
    assert "Hello" in lines[0]
    assert "World" in lines[0]
    # Check that it is padded to 20 chars (including ANSI sequences, but display width should be 20)
    # Since it has ANSI sequences, strip them to measure display width
    from termforge.text.markup import strip_markup
    # Simple regex to strip ANSI codes
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    plain_line = ansi_escape.sub('', lines[0])
    assert len(plain_line) == 20

