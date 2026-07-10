# Changelog

## v1.6.0
- **Feature**: Added declarative JSON Schema exporter CLI subcommand (`termforge-schema`).
- **Feature**: Added declarative layout config auto-formatter CLI subcommand (`termforge-format`).
- **Feature**: Added declarative layout format translator/converter CLI subcommand (`termforge-convert`).
- **Feature**: Added CLI layout tree hierarchy and computed coordinates inspector (`termforge-inspect`).

## v1.5.0
- **Feature**: Added declarative input keybinding parser and matching router (`InputRouter`, `InputBindingSpec`).
- **Feature**: Added declarative configuration validation/linter CLI subcommand (`termforge-validate`).
- **Feature**: Added core layout constraint checking and exception resolver diagnostics (`LayoutConstraintError`).
- **Feature**: Added diagnostic logging framework and collapse audits (`TERMFORGE_LOG_FILE`).

## v1.4.0
- **Feature**: Added status tags rendering in window borders.
- **Feature**: Added peak high/low highlighting options to sparkline charts.
- **Feature**: Added declarative layout config serialization exporter to JSON, TOML, and YAML.
- **Feature**: Added layout validator and visualizer CLI subcommand (`termforge-layout`).
- **Feature**: Added hot-reloading file watcher subcommand (`--watch`) for the layout previewer.

## v1.3.0
- **Feature**: Added Retro `Gruvbox` and `Nord` color palettes.
- **Feature**: Added local `color_config` overrides for individual components.
- **Feature**: Added `Marquee/Ticker` text animation for overflow window content.
- **Feature**: Added drop shadows for floating windows and modals.
- **Feature**: Added bespoke large ASCII art text `BannerSpec` and figlet fonts.
- **Feature**: Added animated logo reveal intros.
- **Refactor**: Resolved all 37 mypy warnings, achieving 100% strict type safety.

## v1.2.0
- **Feature**: Added `TreeView` component.
- **Feature**: Added `Checkbox/SelectionList` component.
- **Feature**: Added `Modal Dialog` component.
- **Feature**: Added `Tabbed Container` component.
- **Refactor**: Resolved multiple `mypy` strict typing errors in wrap, borders, and windows compositor.
- **Fix**: Shortened sentence in split-screen demo to prevent off-by-one border alignment failure.

## v1.1.0
- **Feature**: Added `DataTable` component.
- **Feature**: Added `ProgressBar` component.
- **Fix**: FlexDirection import in CLI demo.
