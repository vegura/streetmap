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
import time

WIDTH = 450
HEIGHT = 190

class RunnableTourSimGeoFactory:
    def generate_geo_instance(self, order):
        start_time = time.time()
        geo_info: GeoInfo = order.convert_from_geo_info()
        print("Geo info get instance time: ", time.time() - start_time)
        start_time = time.time()
        result = RunnableTourSimGeo(geo_info)
        print("Runnable tour sim geo time: ", time.time() - start_time)
        return result


class RunnableTourSimGeo(RunnableSimulation):
    def __init__(self, geo_info: GeoInfo):
        self.width, self.height = WIDTH, HEIGHT
        self.root_file = root_dir.__file__
        self.geo_info = geo_info

    def simulate(
        self, shared_state: dict, should_run: Value, factor: SyncedFloat
    ) -> None:

        # setup environment

        start_time = time.time()
        env = ChangeableFactorRealtimeEnvironment(factor=factor, should_run=should_run)
        print("Env loading time: ", time.time() - start_time)
        start_time = time.time()
        model = Model(env, self.geo_info)
        print("Model init time: ", time.time() - start_time)
        canvas = GeoWebCanvas(shared_state)
        geo_visualizer = GeoVisualizer(canvas)

        model.drive_tour.set_geo_visualizer(geo_visualizer)

        env.run()


def run_animation():
    rs_factory = RunnableTourSimGeoFactory()
    fss.run_server(rs_factory)
