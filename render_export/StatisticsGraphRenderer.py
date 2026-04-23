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
    connected: bool = True

@dataclass
class LinearFunction:
    label: str
    m: float
    c: float
    color: Color
    x_bounds: Optional[tuple[float, float]] = None
    y_bounds: Optional[tuple[float, float]] = None
    linestyle: str = 'dashed'

@dataclass
class FunctionFill:
    m1: float
    c1: float
    m2: float
    c2: float
    color: Color
    x_bounds: Optional[tuple[float, float]] = None
    y_bounds1: Optional[tuple[float, float]] = None
    y_bounds2: Optional[tuple[float, float]] = None
    alpha: float = FILL_ALPHA

class StatisticsGraph:
    def __init__(self, title: str, xlabel: str, ylabel: str, markersize: int = MARKER_SIZE):
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.markersize = markersize
        self.datasets: List[DataSet] = []
        self.fills: List[tuple[List[float], List[float], List[float], Color, float]] = []
        self.linear_functions: List[LinearFunction] = []
        self.function_fills: List[FunctionFill] = []
        self.render_queue = []
        
    def add_dataset(self, label: str, x_values: List[float], y_values: List[float], color: Color, marker: str = 'o', connected: bool = True):
        ds = DataSet(label, x_values, y_values, color, marker, connected)
        self.datasets.append(ds)
        self.render_queue.append(('dataset', ds))
        
    def fill_between(self, x_values: List[float], y_values1: List[float], y_values2: List[float], color: Color = Color.LIGHT_GRAY, alpha: float = FILL_ALPHA):
        fill_data = (x_values, y_values1, y_values2, color, alpha)
        self.fills.append(fill_data)
        self.render_queue.append(('fill', fill_data))
        
    def fill_between_linear_functions(self, m1: float, c1: float, m2: float, c2: float, color: Color = Color.LIGHT_GRAY, x_bounds: Optional[tuple[float, float]] = None, y_bounds1: Optional[tuple[float, float]] = None, y_bounds2: Optional[tuple[float, float]] = None, alpha: float = FILL_ALPHA):
        ff = FunctionFill(m1, c1, m2, c2, color, x_bounds, y_bounds1, y_bounds2, alpha)
        self.function_fills.append(ff)
        self.render_queue.append(('function_fill', ff))
        
    def add_linear_function(self, label: str, m: float, c: float, color: Color, x_bounds: Optional[tuple[float, float]] = None, y_bounds: Optional[tuple[float, float]] = None, linestyle: str = 'dashed'):
        lf = LinearFunction(label, m, c, color, x_bounds, y_bounds, linestyle)
        self.linear_functions.append(lf)
        self.render_queue.append(('linear_function', lf))
        
    def render(self, filename: str, legend_loc: str = 'best'):
        plt.figure()
        
        # Render elements sequentially in the exact order they were added
        for element_type, el in self.render_queue:
            if element_type == 'dataset':
                ds = el
                color_normalized = ds.color.value_normalized()
                ls = 'solid' if ds.connected else 'none'
                plt.plot(ds.x_values, ds.y_values, color=color_normalized, marker=ds.marker, linestyle=ls, linewidth=LINE_WIDTH, markersize=self.markersize, label=ds.label)
                
            elif element_type == 'linear_function':
                lf = el
                if lf.x_bounds is not None:
                    x_min, x_max = lf.x_bounds
                else:
                    if not self.datasets: continue
                    all_xs = [x for ds in self.datasets for x in ds.x_values]
                    x_min, x_max = min(all_xs), max(all_xs)
                    
                steps = 200
                x_vals = [x_min + (x_max - x_min) * i / steps for i in range(steps + 1)]
                y_vals = [lf.m * x + lf.c for x in x_vals]
                
                if lf.y_bounds is not None:
                    y_min, y_max = lf.y_bounds
                    y_vals = [max(y_min, min(y_max, y)) for y in y_vals]
                    
                plt.plot(x_vals, y_vals, color=lf.color.value_normalized(), linestyle=lf.linestyle, linewidth=LINE_WIDTH, label=lf.label)

            elif element_type == 'fill':
                x, y1, y2, color, alpha = el
                plt.fill_between(x, y1, y2, color=color.value_normalized(), alpha=alpha)
                
            elif element_type == 'function_fill':
                ff = el
                if ff.x_bounds is not None:
                    x_min, x_max = ff.x_bounds
                else:
                    if not self.datasets: continue
                    all_xs = [x for ds in self.datasets for x in ds.x_values]
                    x_min, x_max = min(all_xs), max(all_xs)
                    
                steps = 200
                x_vals = [x_min + (x_max - x_min) * i / steps for i in range(steps + 1)]
                y_vals1 = [ff.m1 * x + ff.c1 for x in x_vals]
                y_vals2 = [ff.m2 * x + ff.c2 for x in x_vals]
                
                if ff.y_bounds1 is not None:
                    y1_min, y1_max = ff.y_bounds1
                    y_vals1 = [max(y1_min, min(y1_max, y)) for y in y_vals1]
                    
                if ff.y_bounds2 is not None:
                    y2_min, y2_max = ff.y_bounds2
                    y_vals2 = [max(y2_min, min(y2_max, y)) for y in y_vals2]
                    
                plt.fill_between(x_vals, y_vals1, y_vals2, color=ff.color.value_normalized(), alpha=ff.alpha)

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
