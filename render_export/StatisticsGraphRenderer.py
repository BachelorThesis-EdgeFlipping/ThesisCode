import matplotlib.pyplot as plt

from render_export.Color import Color
from render_export.Globals import DEFAULT_EXPORT_PATH
from dataclasses import dataclass
from typing import List, Optional

#####################
#  Default Config   #
#####################
LINE_WIDTH = 2
MARKER_SIZE = 6
GRID_ALPHA = 0.4
FILL_ALPHA = 0.4

@dataclass
class DataSet:
    label: str
    x_values: List[float]
    y_values: List[float]
    color: Color
    marker: str = 'o'

@dataclass
class LinearFunction:
    label: str
    m: float
    c: float
    color: Color
    x_bounds: Optional[tuple[float, float]] = None
    y_bounds: Optional[tuple[float, float]] = None
    linestyle: str = 'dashed'

class StatisticsGraph:
    def __init__(self, title: str, xlabel: str, ylabel: str):
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.datasets: List[DataSet] = []
        self.fills: List[tuple[List[float], List[float], List[float], Color, float]] = []
        self.linear_functions: List[LinearFunction] = []
        
    def add_dataset(self, label: str, x_values: List[float], y_values: List[float], color: Color, marker: str = 'o'):
        self.datasets.append(DataSet(label, x_values, y_values, color, marker))
        
    def fill_between(self, x_values: List[float], y_values1: List[float], y_values2: List[float], color: Color = Color.LIGHT_GRAY, alpha: float = FILL_ALPHA):
        self.fills.append((x_values, y_values1, y_values2, color, alpha))
        
    def add_linear_function(self, label: str, m: float, c: float, color: Color, x_bounds: Optional[tuple[float, float]] = None, y_bounds: Optional[tuple[float, float]] = None, linestyle: str = 'dashed'):
        self.linear_functions.append(LinearFunction(label, m, c, color, x_bounds, y_bounds, linestyle))
        
    def render(self, filename: str, legend_loc: str = 'best'):
        plt.figure()
        
        # Plot each dataset
        for ds in self.datasets:
            color_normalized = ds.color.value_normalized()
            plt.plot(ds.x_values, ds.y_values, color=color_normalized, marker=ds.marker, linewidth=LINE_WIDTH, markersize=MARKER_SIZE, label=ds.label)
            
        # Draw linear functions
        for lf in self.linear_functions:
            if lf.x_bounds is not None:
                x_min, x_max = lf.x_bounds
            else:
                if not self.datasets:
                    continue  # Can't infer x_bounds
                all_xs = [x for ds in self.datasets for x in ds.x_values]
                x_min, x_max = min(all_xs), max(all_xs)
                
            # Generate fine-grained points to handle y_bounds clipping smoothly
            steps = 200
            x_vals = [x_min + (x_max - x_min) * i / steps for i in range(steps + 1)]
            y_vals = [lf.m * x + lf.c for x in x_vals]
            
            if lf.y_bounds is not None:
                y_min, y_max = lf.y_bounds
                y_vals = [max(y_min, min(y_max, y)) for y in y_vals]
                
            plt.plot(x_vals, y_vals, color=lf.color.value_normalized(), linestyle=lf.linestyle, linewidth=LINE_WIDTH, label=lf.label)

        # Draw fills
        for (x, y1, y2, color, alpha) in self.fills:
            plt.fill_between(x, y1, y2, color=color.value_normalized(), alpha=alpha)
            
        # Labels and styling
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.title(self.title)
        
        if self.datasets or self.linear_functions:
            plt.legend(loc=legend_loc)
            
        plt.grid(True, alpha=GRID_ALPHA)
        
        # Export as SVG
        export_path = f"{DEFAULT_EXPORT_PATH}/{filename}.svg"
        plt.savefig(export_path, format="svg")
        print(f"Exported figure to {export_path}.")
        plt.close()
