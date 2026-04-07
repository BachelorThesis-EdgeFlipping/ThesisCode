
# Example Usage
from render_export.Color import Color
from render_export.StatisticsGraphRenderer import StatisticsGraph


vertices = [4,5,6,7,8,9,10,11,12,13,14,15]
oms = [100,100,100,97.6,95.3,93.1,90.8,89.9,87.9,89.7,86.3,82.8]
either = [100,100,100,100,99.7,99.5,99,98.6,98.4,98.4,95.6,93.1]

graph = StatisticsGraph(title='Group 1', xlabel='Number of vertices', ylabel='Percentage (%)')
graph.add_dataset('Improved heuristic', vertices, either, Color.PURPLE, 's')
graph.add_dataset('Simple heuristic', vertices, oms, Color.ORANGE, 'o')
graph.fill_between(vertices, [82.8]*len(vertices), oms, Color.LIGHT_ORANGE)
graph.fill_between(vertices, oms, either, Color.LIGHT_PURPLE)

graph.render('oms_vs_either_group_1', legend_loc='lower left')

#python -m render_export.XImprovedHeuristic1