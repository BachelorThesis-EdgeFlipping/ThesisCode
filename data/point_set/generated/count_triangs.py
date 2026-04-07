import json
import sys
import os
sys.path.append('../../..')
sys.path.append('D:/BA/BA_code')
from GenerateRandomPointSetTriangulations import discover_all_triangulations

def count_triangulations(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    print(f'Checking {filepath}')
    points = [tuple(p) for p in data['vertices']]
    base_edges = [tuple(e) for e in data['edges']]
    tris = discover_all_triangulations(points, base_edges)
    return len(tris)

print('Triangulations for N=13')
print('13_1_1:', count_triangulations('13_6_10-40_113806977/rand13_1_1.json'))
print('Triangulations for N=14')
print('14_1_1:', count_triangulations('14_6_10-45_949804505/rand14_1_1.json'))
