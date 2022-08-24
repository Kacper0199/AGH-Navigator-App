"""
Dijkstra's Algorithm
This script allows to implement the shortest path algorithm for finding 
the minimum distances between nodes in a graph. It uses a data structure 
for storing and querying partial solutions sorted by distance from the start. 
The worst case performance of this algorithm is O((V+E)logV) time complexity, 
where V is the number of nodes and E is the number of edges. 
This script requires that `heapq` be installed within the Python environment 
you are running this script in.
This file can also be imported as a module and contains the following classes:
    * Edge
    * Vertex
    * DijkstraAlgorithm
"""

import heapq


class Edge:
    """
    A class used to represent an edge of the weighted graph. The aim of 
    this class is to model a sidewalk and road network between the buildings 
    on the map.

    Attributes
    ----------
    weight : int
        A weight (distance) of the edge connecting two vertices.
    start_vertex : type[Vertex]
        A starting vertex (node) in the particular edge of the graph.
    end_vertex : type[Vertex]
        An ending vertex (node) in the particular edge of the graph.
    """

    def __init__(self, weight, start_vertex, end_vertex) -> None:
        self.weight = weight
        self.start_vertex = start_vertex
        self.end_vertex = end_vertex


class Vertex:
    """
    A class used to represent a vertex or node in the weighted graph. This 
    class models points and intersections of the road network on the map. 

    Attributes
    ----------
    name : str
        Name of the vertex.
    visited : bool
        Marks if the algorithm visits the vertex to determine a distance from 
        the starting point.
    predecessor : type[Vertex]
        A predecessor of the vertex in the shortest path (minimum distance from 
        the starting point).
    adjacency_list: list[type[Vertex]]
        A list containing all adjacent edges that are connected to the particular 
        vertex.
    min_distance: float
        Minimum distance to the vertex from the starting point.
    coordinates: list[float, float]
        A list containing two float variables (latitude and longitude of the vertex 
        or point on the map).
    """

    def __init__(self, name) -> None:
        self.name = name
        self.visited = False
        self.predecessor = None
        self.adjacency_list = []
        self.min_distance = float("inf")
        self.coordinates = None

    def __lt__(self, other_vertex):
        return self.min_distance < other_vertex.min_distance


class DijkstraAlgorithm:
    """
    The main purpose of this class is to apply a Dijkstra's algorithm to find the shortest 
    path between nodes in the graph. This class is used to determine the minimum distance 
    to a given object on the interactive map of this application.

    Attributes
    ----------
    heap : list[type[Vertex]]
        A list representing minimum heap data structure containing vertices that are prioritized 
        by minimum distance value.

    Methods
    -------
    calculate(start_vertex)
        Calculates distances from starting vertex to all the vertices in the graph.
    get_shortest_path(vertex)
        Collects coordinates of all the vertices creating the shortest path and returns it with 
        minimal distance to a given point.
    """

    def __init__(self) -> None:
        self.heap = []

    def calculate(self, start_vertex):
        """
        Designates distances to the vertices in the graph.
        Uses min-heap data structure to implement a double-ended priority queue on vertices 
        containing minimum distances from the starting point.

        Parameters
        ----------
        start_vertex : type[Vertex]
            Starting point used as a reference to calculate distances to other vertices.
        """

        start_vertex.min_distance = 0
        heapq.heappush(self.heap, start_vertex)

        while self.heap:
            actual_vertex = heapq.heappop(self.heap)

            if actual_vertex.visited:
                continue

            for edge in actual_vertex.adjacency_list:
                start = edge.start_vertex
                end = edge.end_vertex
                new_distance = start.min_distance + edge.weight

                if new_distance < end.min_distance:
                    end.predecessor = start
                    end.min_distance = new_distance
                    heapq.heappush(self.heap, end)

            actual_vertex.visited = True

    @staticmethod
    def get_shortest_path(vertex):
        """
        Collects coordinates of all the vertices creating the shortest path and returns it. 
        It also returns a minimum distance value to the passed vertex. 

        Parameters
        ----------
        vertex : type[Vertex]
            Vertex for which the minimum path is determined.

        Returns
        -------
        coordinates_list : list[[float, float]]
            A list of coordinates for a points in the shortest path. For example: 
            [[50.0691, 19.9048], [50.0687, 19.9042], [50.0693, 19.9054]].

        distance_meters : int
            A distance of the shortest path expressed in meters.
        """

        coordinates_list = []
        actual_vertex = vertex
        distance_meters = int(actual_vertex.min_distance)

        while actual_vertex:
            coordinates_list.append(actual_vertex.coordinates)
            actual_vertex = actual_vertex.predecessor

        return coordinates_list, distance_meters
