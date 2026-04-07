import json
import sys
import os
import random
sys.path.append('../../..')
sys.path.append('D:/BA/BA_code')
from GenerateRandomPointSetTriangulations import get_random_simultaneous_flip_set
from data_structures.Triangulation import Triangulation

with open('14_6_10-45_949804505/rand14_1_1.json', 'r') as f:
    data = json.load(f)

points = [tuple(p) for p in data['vertices']]
base_edges = [tuple(e) for e in data['edges']]
tri = Triangulation()
tri.initialize_from_edges(points, base_edges)

for i in range(100):
    flip_set = get_random_simultaneous_flip_set(tri)
    success = tri.flip_edges_simultaneous(flip_set)
    print(f'Iter {i}: flip_set size {len(flip_set)}, success: {success}')

