import os
import logging
from termforge.core.types import BoxConstraints, RenderableSpec
from termforge.core.layout import LayoutNode, BoxModel, compute_layout

def test_layout_collapse_logging(tmp_path):
    log_file = tmp_path / "test_termforge.log"
    
    os.environ["TERMFORGE_LOG_FILE"] = str(log_file)
    os.environ["TERMFORGE_LOG_LEVEL"] = "WARNING"
    
    logger = logging.getLogger("termforge.core.layout")
    logger.handlers.clear()
    
    spec = RenderableSpec(spec_type="collapsed_component")
    node = LayoutNode(spec=spec, box=BoxModel(width=0, height=0))
    constraints = BoxConstraints(min_width=0, max_width=0, min_height=0, max_height=0)
    
    compute_layout(node, constraints)
    
    assert log_file.exists()
    content = log_file.read_text(encoding="utf-8")
    assert "collapsed_component" in content
    assert "collapsed to size 0x0" in content
    
    logger.handlers.clear()
