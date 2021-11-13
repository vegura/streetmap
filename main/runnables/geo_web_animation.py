from multiprocessing import Value

from casymda.environments.realtime_environment import (
    ChangeableFactorRealtimeEnvironment,
    SyncedFloat,
)
from casymda.visualization.web_server.sim_controller import RunnableSimulation

import main.web.flask_sim_server as fss
import root_dir
from main.geo.geo_info import GeoInfo
from main.model.geo_info_setup import get_geo_info
from main.model.model import Model
from main.visu.geo_visualizer import GeoVisualizer
from main.visu.geo_web_canvas import GeoWebCanvas

WIDTH = 450
HEIGHT = 190

class RunnableTourSimGeoFactory():
    def generate_geo_instance(self, order):
        geo_info: GeoInfo = get_geo_info()
        result = RunnableTourSimGeo(geo_info)


class RunnableTourSimGeo(RunnableSimulation):
    def __init__(self, geo_info: GeoInfo):
        self.width, self.height = WIDTH, HEIGHT
        self.root_file = root_dir.__file__
        self.geo_info = geo_info

    def simulate(
        self, shared_state: dict, should_run: Value, factor: SyncedFloat
    ) -> None:

        # setup environment
        env = ChangeableFactorRealtimeEnvironment(factor=factor, should_run=should_run)
        model = Model(env, self.geo_info)

        canvas = GeoWebCanvas(shared_state)
        geo_visualizer = GeoVisualizer(canvas)

        model.drive_tour.set_geo_visualizer(geo_visualizer)

        env.run()


def run_animation():
    rs = RunnableTourSimGeo()
    fss.run_server(rs)
