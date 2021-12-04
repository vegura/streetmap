from typing import Any, Dict, List
from main.geo.geo_info import init
from casymda.blocks import Sink, Source

from main.geo.geo_info import GeoInfo
from main.model.blocks.drive_tour import DriveTour
from main.model.blocks.truck import Truck
from main.model.geo_info_setup import get_geo_info

#geo_info: GeoInfo = get_geo_info()

class Order:
    def __init__(self, id, route_points, feedback):
        self.id = id
        self.route_points = route_points
        self.feedback = feedback

    def convert_from_geo_info(self) -> GeoInfo:
        ## define center
        ## define distance
        ## CENTER - get centroid between route points
        ## DISTANCE - get max distance from centroid to route points + delta
        x0, y0 = self.route_points[0]['x'], self.route_points[0]['y']
        CENTER = (x0, y0)
        distances = []
        for point in self.route_points:
            x_i = point['x']
            y_i = point['y']
            distances.append(((x_i - x0)**2 + (y_i - y0)**2)**0.5)
        print("Distances: ", distances)
        DISTANCE = max(distances)*111139*1.25

        #CENTER = (51.4978, -0.1533)
        #DISTANCE = 10_000

        NETWORK_TYPE="drive"
        return init(
            route_points = self.route_points,
            #nodes_csv_path=NODES_CSV_PATH,
            center=CENTER,
            distance=DISTANCE,
            network_type=NETWORK_TYPE,
        )

class Model:
    def __init__(self, env, geo_info: GeoInfo):

        self.env = env
        self.model_components: Any
        self.model_graph_names: Dict[str, List[str]]

        #!resources+components (generated)

        self.source = Source(
            self.env,
            "source",
            xy=(79, 59),
            entity_type=Truck,
            max_entities=10,
            inter_arrival_time=250,
            ways={"drive_tour": [(97, 59), (180, 59)]},
        )

        self.sink = Sink(self.env, "sink", xy=(368, 59), ways={})
        print(geo_info.get_nodes())
        self.drive_tour = DriveTour(
            self.env,
            "drive_tour",
            xy=(230, 59),
            geo_info=geo_info,
            start=geo_info.get_nodes()[0],
            stops=geo_info.get_nodes()[1:],
            #start="PAT",
            #stops=["ZFB", "MMC", "CAV"],
            ways={"sink": [(280, 59), (350, 59)]},
        )

        #!model (generated)

        self.model_components = {
            "source": self.source,
            "sink": self.sink,
            "drive_tour": self.drive_tour,
        }

        self.model_graph_names = {
            "source": ["drive_tour"],
            "sink": [],
            "drive_tour": ["sink"],
        }
        # translate model_graph_names into corresponding objects
        self.model_graph = {
            self.model_components[name]: [
                self.model_components[nameSucc]
                for nameSucc in self.model_graph_names[name]
            ]
            for name in self.model_graph_names
        }

        for component in self.model_graph:
            component.successors = self.model_graph[component]
