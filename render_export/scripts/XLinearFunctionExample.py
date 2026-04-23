# Example Usage for Linear Functions
from render_export.Color import Color
from render_export.StatisticsGraphRenderer import StatisticsGraph

# Sample data
vertices = [4,5,6,7,8,9,10,11,12,13,14,15]
oms = [100,100,100,97.6,95.3,93.1,90.8,89.9,87.9,89.7,86.3,82.8]
either = [100,100,100,100,99.7,99.5,99,98.6,98.4,98.4,95.6,93.1]
s_h_trend_m = -1.59833
s_h_trend_c = 107.95944
i_h_trend_m = -0.805952
i_h_trend_c = 107.05595
x_bounds = (4, 45)
y_bounds = (0, 100)

# Initialize the graph
graph = StatisticsGraph(title='Extrapolation of Group 1', xlabel='Number of vertices', ylabel='Percentage (%)', markersize=4)

# Example: Fill area between the two linear trends
graph.fill_between_linear_functions(
    m1=i_h_trend_m, c1=i_h_trend_c, y_bounds1=(0, 100),
    m2=s_h_trend_m, c2=s_h_trend_c, y_bounds2=(0, 100),
    color=Color.LIGHT_PURPLE,
    x_bounds=x_bounds
)
graph.fill_between_linear_functions(
    m1=s_h_trend_m, c1=s_h_trend_c, y_bounds1=(0, 100),
    m2=0.0, c2=0.0, y_bounds2=(0, 0),
    color=Color.LIGHT_ORANGE,
    x_bounds=x_bounds
)

#data points
graph.add_dataset('Data I.H.', vertices, either, Color.PURPLE, 's', connected=False)
graph.add_linear_function(
    label='Expected trend I.H.',
    m=i_h_trend_m,
    c=i_h_trend_c,
    color=Color.PURPLE,
    x_bounds=x_bounds,
    y_bounds=y_bounds,
    linestyle='solid'
)
graph.add_dataset('Data S.H.', vertices, oms, Color.ORANGE, 'o', connected=False)
graph.add_linear_function(
    label='Expected trend S.H.',
    m=s_h_trend_m,
    c=s_h_trend_c,
    color=Color.ORANGE,
    x_bounds=x_bounds,
    y_bounds=y_bounds,
    linestyle='solid'
)

# Render and export to SVG
graph.render('linear_function_example', legend_loc='lower left')

# Run this example using:
# python -m render_export.scripts.XLinearFunctionExample
