
# Example Usage
from render_export.Color import Color
from render_export.StatisticsGraphRenderer import StatisticsGraph


vertices = [6,7,8,9,10,11,12,13,14,15]
oms = [100, 99.5, 97.8, 97.9, 96.2, 95.7, 92.4, 89.8, 91.5, 88.7]
either = [100, 100, 99.9, 100, 99.7,99.7,97.8,98.4,99.6,100]

graph = StatisticsGraph(title='Group 2', xlabel='Number of vertices', ylabel='Percentage (%)')
graph.add_dataset('Improved heuristic', vertices, either, Color.PURPLE, 's')
graph.add_dataset('Simple heuristic', vertices, oms, Color.ORANGE, 'o')
graph.fill_between(vertices, [82.8]*len(vertices), oms, Color.LIGHT_ORANGE)
graph.fill_between(vertices, oms, either, Color.LIGHT_PURPLE)

graph.render('oms_vs_either_group_2', legend_loc='lower left')

#python -m render_export.XImprovedHeuristic2