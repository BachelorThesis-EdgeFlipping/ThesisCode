# Example Usage for Linear Functions
from render_export.Color import Color
from render_export.StatisticsGraphRenderer import StatisticsGraph

# Sample data
vertices_simple = [4, 5, 6, 7, 8, 9, 10, 11, 12]
data_points_simple = [80, 82, 85, 87, 90, 88, 85, 83, 80]

# Initialize the graph
graph = StatisticsGraph(title='Linear Function Example', xlabel='Number of vertices (x)', ylabel='Value (y)')

# Add a regular dataset
graph.add_dataset('Sample Data', vertices, data_points, Color.BLUE, 'o')

# Example 1: Linear function with automatic bounds (inferred from the dataset vertices)
# Equation: y = -4.0x + 115, capped at y=80 (so it doesn't go below 80%)
graph.add_linear_function(
    label='Expected Trend (Capped at 80%)',
    m=-4.0,
    c=115,
    color=Color.RED,
    y_bounds=(80, 100),
    linestyle='dashed'
)

# Example 2: Linear function with explicit x_bounds AND y_bounds
# Equation: y = 5.0x + 60 (plotted strictly from x=2 to x=14, capped to max strictly 100%)
graph.add_linear_function(
    label='Theoretical Limit (Max 100%)',
    m=5.0,
    c=60,
    color=Color.GREEN,
    x_bounds=(2, 14),
    y_bounds=(0, 100),
    linestyle='dotted'
)

# Render and export to SVG
graph.render('linear_function_example', legend_loc='lower center')

# Run this example using:
# python -m render_export.XLinearFun