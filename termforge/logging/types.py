"""TermForge log streamer component specifications."""
from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from typing import Any
from termforge.core.types import RenderableSpec


@dataclass
class LogStreamerSpec(RenderableSpec):
    """Specification for a scrollable logging component with level highlights.

    Attributes:
        max_lines: Rolling buffer limit size (number of logs to retain).
        auto_scroll: If True, viewport displays the most recent logs at bottom.
        timestamp_format: Datetime format string for log timestamps (e.g. "%H:%M:%S").
        level_colors: Mapping of log levels (e.g. INFO, ERROR) to color tokens.
        buffer: List of log entry dictionaries, retaining log state.
        width: Optional fixed canvas width.
        height: Optional fixed canvas height.
    """
    max_lines: int = 500
    auto_scroll: bool = True
    timestamp_format: str = "%H:%M:%S"
    level_colors: dict[str, str] = field(default_factory=dict)
    buffer: list[dict[str, Any]] = field(default_factory=list)
    width: int | None = None
    height: int | None = None
    spec_type: str = "log_streamer"

    def log(self, level: str, message: str, timestamp: str | None = None) -> None:
        """Append a new log message to the rolling buffer.

        Args:
            level: The log level identifier (e.g. "INFO", "WARNING").
            message: The core text message to log.
            timestamp: Optional timestamp string. If None, uses current system time.
        """
        ts = timestamp
        if ts is None:
            if self.timestamp_format:
                ts = datetime.datetime.now().strftime(self.timestamp_format)
            else:
                ts = ""
        
        self.buffer.append({
            "timestamp": ts,
            "level": level,
            "message": message,
        })
        
        if len(self.buffer) > self.max_lines:
            self.buffer = self.buffer[-self.max_lines:]

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dict.

        Returns:
            A plain dict containing log streamer properties.
        """
        return {
            "spec_type": self.spec_type,
            "max_lines": self.max_lines,
            "auto_scroll": self.auto_scroll,
            "timestamp_format": self.timestamp_format,
            "level_colors": dict(self.level_colors),
            "buffer": [dict(entry) for entry in self.buffer],
            "width": self.width,
            "height": self.height,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> LogStreamerSpec:
        """Deserialise from a dict produced by :meth:`to_dict`.

        Args:
            d: Dict containing log streamer properties.

        Returns:
            A new :class:`LogStreamerSpec` instance.
        """
        return cls(
            max_lines=d.get("max_lines", 500),
            auto_scroll=d.get("auto_scroll", True),
            timestamp_format=d.get("timestamp_format", "%H:%M:%S"),
            level_colors=dict(d.get("level_colors", {})),
            buffer=[dict(entry) for entry in d.get("buffer", [])],
            width=d.get("width"),
            height=d.get("height"),
        )
