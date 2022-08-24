"""
Navigator App
This script allows to create navigator web app for a particular area (AGH University 
of Science and Technology). The application is built with `folium` and `streamlit` framework
to handle user inputs and display current routes between the characteristic points listed
on the apps sidebar.
This script requires to install the following modules:
    * `streamlit`
    * `folium`
    * `streamlit_folium`
    * `geopy`
The file contains the following classes:
    * Map
    * App
"""


import json
import folium
import streamlit as st
from geopy import distance
from algorithm import DijkstraAlgorithm, Edge, Vertex
from streamlit_folium import folium_static
from math import ceil


class Map:
    """
    A class used to generate map of selected area with markers and routes. The purpose is to
    visualize navigation algorithm in this application using `folium` module.

    Attributes
    ----------
    chart : type[folium.Map]
        A `folium` Map object created with selected built in attributes.
    route_coords : list[[float, float]]
        A list of coordinates for a given route.
    vertices : dict[str, type[algorithm.Vertex]]
        A dict used to store all the map points (buildings and roads intersections) 
        represented as the graph vertices.
    min_distance : int
        Variable used to store value of the minimum distance to a given point.
    """

    def __init__(self):
        self.chart = folium.Map(location=[50.067535331738206, 19.91289138793945],
                                min_lat=50.06110619395334,
                                max_lat=50.07427346546824,
                                min_lon=19.89147663116455,
                                max_lon=19.93014335632324,
                                max_bounds=True,
                                min_zoom=15,
                                zoom_start=16,
                                control_scale=True)

        self.route_coords = []
        self.vertices = {}
        self.min_distance = 0

    def load_points(self):
        """
        Creates vertices according to parameters contained in the `points.json` file 
        and appends them to the `vertices` list class attribute.
        """

        with open("points.json", encoding="UTF-8") as file:
            data = json.load(file)

        for key, val in data.items():
            if key not in self.vertices:
                self.vertices[key] = Vertex(key)
                self.vertices[key].coordinates = val["coordinates"]
            for adj_pt in val["adjacents"]:
                if adj_pt not in self.vertices:
                    self.vertices[adj_pt] = Vertex(adj_pt)
                    self.vertices[adj_pt].coordinates = data[adj_pt]["coordinates"]
                dist = distance.distance(
                    self.vertices[key].coordinates, self.vertices[adj_pt].coordinates).m
                self.vertices[key].adjacency_list.append(
                    Edge(dist, self.vertices[key], self.vertices[adj_pt]))

    def map_markers(self, current_position, target_position):
        """
        Adds current and target position markers on the map.

        Parameters
        ----------
        current_position : list[float, float]
            Coordinates of actual position on the map.
        target_position : list[float, float]
            Coordinates of destination position on the map.
        """

        folium.CircleMarker(location=current_position, radius=10,
                            color="black", fill_color="blue",
                            fill_opacity=1, popup="Current position").add_to(self.chart)
        folium.Marker(location=target_position,
                      icon=folium.Icon(icon="glyphicon-flag", color="red")).add_to(self.chart)

    def generate_map(self, start, destination):
        """
        Loads points, uses Dijkstra's algorithm, draws a path on the map and adds markers
        for start and destination points.

        Parameters
        ----------
        start : str
            Starting point keyword.
        destination : str
            Destination point keyword.
        """

        self.load_points()

        algorithm = DijkstraAlgorithm()
        algorithm.calculate(self.vertices[start])
        self.route_coords, self.min_distance = algorithm.get_shortest_path(
            self.vertices[destination])

        folium.plugins.AntPath(
            self.route_coords, delay=2000, reverse=True).add_to(self.chart)

        self.map_markers(self.vertices[start].coordinates,
                         self.vertices[destination].coordinates)


class App:
    """
    A class used to create the web app using `streamlit` framework.

    Attributes
    ----------
    APP_NAME : str
        Name of the web app.
    GITHUB_LINK : str
        Link to the project github repository.
    DESCRIPTION : str
        Short description of the web app.
    MAP_WINDOW_HEIGHT : int
        The height of the map window.
    MAP_WINDOW_WIDTH : int
        The width of the map window.
    speed : dict[str, float]
        Dictionary representing available walking speeds in the app.
    buildings : list[str]
        List of available buildings as starting and destination points.
    """

    APP_NAME = "AGH Navigator"
    GITHUB_LINK = "https://github.com/Kacper0199"
    DESCRIPTION = "# This app was created using *Dijkstra's* algorithm to find the shortest \
                    path between buildings of AGH University of Science and Technology"
    MAP_WINDOW_HEIGHT = 550
    MAP_WINDOW_WIDTH = 1100

    def __init__(self) -> None:
        self.speed = {"slow": 1.5, "walk": 2, "fast": 3}
        self.buildings = []
        self.init_building_list()

    def init_building_list(self):
        """
        Initializes list of available buildings in the app.
        """

        with open("points.json", encoding="UTF-8") as file:
            data = json.load(file)

        self.buildings = sorted(
            [key for key in data if key[0] != "p"], key=lambda x: (x[1], x[0], "{0:0>4}".format(x)))

    def show(self):
        """
        Generates a map, configures app, handles user input and displays entire web app.
        """

        map_window = Map()
        st.set_page_config(self.APP_NAME, layout="wide",
                           menu_items={
                               "Get Help": self.GITHUB_LINK,
                               "Report a bug": self.GITHUB_LINK,
                               "About": self.DESCRIPTION
                           })
        col1, col2 = st.columns(2)

        start = st.sidebar.selectbox(
            "Select start point", self.buildings, 0)
        destination = st.sidebar.radio(
            "Select destination", self.buildings, 0)

        map_window.generate_map(start, destination)

        speed_key = col2.select_slider(
            "", options=[opt for opt in self.speed], value="walk")
        col1.subheader(f"Distance: {map_window.min_distance} meters")
        col1.subheader(
            f"Time: {ceil(map_window.min_distance/(60*self.speed[speed_key]))} min")

        folium_static(map_window.chart,
                      height=self.MAP_WINDOW_HEIGHT, width=self.MAP_WINDOW_WIDTH)


def main():
    app = App()
    app.show()


if __name__ == "__main__":
    main()
