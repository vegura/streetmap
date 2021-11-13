"""provides control endpoints and serves visual state of a simulation model"""

import logging
import os

from casymda.visualization.web_server.sim_controller import (
    RunnableSimulation,
    SimController,
)
from flask import Flask, request, send_file, send_from_directory
from flask_cors import CORS

from main.model.model import Order
from main.runnables.geo_web_animation import RunnableTourSimGeoFactory

logging.getLogger("werkzeug").setLevel(logging.ERROR)

sim_instances = {}

class FlaskSimServer:

    # def __init__(self, sim_controller: SimController) -> None:
    #     self.sim_controller: SimController = sim_controller
    #     self.root_file = sim_controller.simulation.root_file

    def __init__(self, sim_factory):
        self.sim_factory = sim_factory

    def run_sim_server(self):
        app = Flask(__name__)
        CORS(app)
        app_dir = os.path.dirname(os.path.abspath(self.root_file))
        flask_dir = os.path.dirname(os.path.abspath(__file__))
        print(
            "starting flask server, app_dir: %s, flask_dir: %s" % (app_dir, flask_dir)
        )

        @app.route("/")
        def root():
            # assumed to be next to this file
            HTML_FILE = "geo_animation.html"
            return send_from_directory(flask_dir, HTML_FILE)

        @app.route("/lib-files/<filename>")
        def lib_files(filename):
            # assumed to be next to this file
            return send_from_directory(flask_dir, filename)

        @app.route("/files")
        def provide_file():
            filepath = request.args.get("filepath")
            if filepath.startswith("/") or filepath.startswith("C:"):
                # absolute path
                return send_file(filepath)
            else:
                # relative path
                return send_from_directory(app_dir, filepath)

        @app.route("/order/<order_id>")
        def get_order(order_id):
            # order: json = get_order_from_mongo_by(order_id)
            #
            order_json = {
                  "id": 12343,
                  "route_points":[
                    {
                      "id": 1,
                      "postal_code": "SW1X 8BY",
                      "x": 51.49701939844378,
                      "y": -0.15334817975876766
                    },
                    {
                      "id": 2,
                      "postal_code": "SW1X 9BC",
                      "x": 51.4952531089578,
                      "y": -0.14379338326757904
                    },
                    {
                      "id": 3,
                      "postal_code": "SW1X 4EZ",
                      "x": 51.49404056290103,
                      "y": -0.15337663339296168
                    }
                  ],
                  "feedback": "Was a nice ride"
            }
            order = Order(order_json["id"], order_json["route_points"], order_json["feedback"])
            if sim_instances[]
            runnable_sim = self.sim_factory.generate_geo_instance(order)
            sim_conrtoller = SimController(runnable_sim)
            HTML_FILE = "geo_animation.html"
            return send_from_directory(flask_dir, HTML_FILE, sim_conrtoller=sim_conrtoller)
            # return str(sim_conrtoller.get)




        @app.route("/width/<order>")
        def get_width(order):

            # sim_instances[order]
            return str(self.sim_controller.get_sim_width())

        @app.route("/height")
        def get_height():
            return str(self.sim_controller.get_sim_height())

        @app.route("/state")
        def get_state():
            return self.sim_controller.get_state_dumps()

        @app.route("/start", methods=["POST"])
        def start():
            return self.sim_controller.start_simulation_process()

        @app.route("/stop", methods=["POST"])
        def stop():
            return self.sim_controller.reset_sim()

        @app.route("/pause", methods=["POST"])
        def pause():
            return self.sim_controller.pause_sim()

        @app.route("/resume", methods=["POST"])
        def resume():
            return self.sim_controller.resume_sim()

        @app.route("/rt_factor", methods=["POST"])
        def post_rt_factor():
            value = float(request.args.get("value"))
            return self.sim_controller.set_rt_factor(value)

        app.run(debug=True, threaded=False, port=5000, host="0.0.0.0")


# def run_server(runnable_sim: RunnableSimulation):
#     sim_controller = SimController(runnable_sim)
#     flask_sim_server = FlaskSimServer(sim_controller)
#     flask_sim_server.run_sim_server()
#
# def run_server(runnable_sim_factory: RunnableTourSimGeoFactory):
#     sim_controller = SimController(runnable_sim)
#     flask_sim_server = FlaskSimServer(sim_controller)
#     flask_sim_server.run_sim_server()

def run_server():
    sim_factory = RunnableTourSimGeoFactory()
    flask_sim_server = FlaskSimServer(sim_factory)
    flask_sim_server.run_sim_server()
