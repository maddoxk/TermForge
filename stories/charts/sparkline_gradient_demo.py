from termforge.charts import ChartSpec, ChartType, render_chart
from termforge.charts.types import Series
from termforge.core.theme import load_theme_from_dict, NORD
from termforge.core.types import Size

def main():
    theme = load_theme_from_dict(NORD)
    
    spec = ChartSpec(
        chart_type=ChartType.SPARKLINE,
        series=[
            Series(data=[1.0, 3.0, 2.0, 5.0, 7.0, 6.0, 9.0, 11.0, 8.0, 12.0])
        ],
        color_config={
            "gradient": ["success", "error"]  # Green to Red gradient based on values
        }
    )
    
    result = render_chart(spec, theme=theme)
    print("--- Nord Theme Sparkline Gradient Showcase ---")
    print(result[0])

if __name__ == "__main__":
    main()
