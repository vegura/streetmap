"""provides control endpoints and serves visual state of a simulation model"""

import logging
import os

from casymda.visualization.web_server.sim_controller import (
    RunnableSimulation,
    SimController,
)
from flask import Flask, request, send_file, send_from_directory, render_template
from flask_cors import CORS

from main.model.model import Order
#from main.runnables.geo_web_animation import RunnableTourSimGeoFactory

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
        # app_dir = os.path.dirname(os.path.abspath(self.root_file))
        app_dir = os.path.dirname(os.path.abspath('root_dir.py'))
        flask_dir = os.path.dirname(os.path.abspath(__file__))
        print(
            "starting flask server  flask_dir: %s" % (flask_dir)
            #"starting flask server, app_dir: %s, flask_dir: %s" % (app_dir, flask_dir)
        )

        @app.route("/")
        def root(order_id):
            # assumed to be next to this file
            HTML_FILE = "geo_animation.html"
            return send_from_directory(flask_dir, HTML_FILE)

        @app.route("/order/<order_id>/lib-files/<filename>")
        def lib_files(order_id, filename):
            # assumed to be next to this file
            return send_from_directory(flask_dir, filename)

        @app.route("/order/files")
        def provide_file():
            print("HELLO")
            filepath = request.args.get("filepath")
            print(f"================================FILEPATH is {filepath}")
            if filepath.startswith("/") or filepath.startswith("C:"):
                # absolute path
                print("I'm here")
                return send_file(filepath)
            else:
                #sim_controller = sim_instances[order_id]
                # relative path
                directory = "/usr/src/"
                return send_from_directory(directory, filepath)

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
                      "y": -0.15334817975876766,
                      "description": "aaaaa"
                    },
                    {
                      "id": 2,
                      "postal_code": "SW1X 9BC",
                      "x": 51.4952531089578,
                      "y": -0.14379338326757904,
                      "description": "aaaaa"
                    },
                    {
                      "id": 3,
                      "postal_code": "SW1X 4EZ",
                      "x": 51.49404056290103,
                      "y": -0.15337663339296168,
                      "description": "aaaaa"
                    }
                  ],
                  "feedback": "Was a nice ride"
            }
            order = Order(order_json["id"], order_json["route_points"], order_json["feedback"])
            if not str(order_id) in sim_instances.keys():
                runnable_sim = self.sim_factory.generate_geo_instance(order)
                sim_conrtoller = SimController(runnable_sim)
                sim_instances[str(order_id)] = sim_conrtoller
            HTML_FILE = "geo_animation.html"
            #return send_from_directory(flask_dir, HTML_FILE, sim_instances[str(order_id)])
            return send_from_directory(flask_dir, HTML_FILE)
            #return render_template(HTML_FILE)
            # return str(sim_conrtoller.get)




        @app.route("/order/<order_id>/width/")
        def get_width(order_id):
            return sim_instances[order_id].get_sim_width()

        @app.route("/order/<order_id>/height")
        def get_height(order_id):
            return sim_instances[order_id].get_sim_height()

        @app.route("/order/<order_id>/state")
        def get_state(order_id):
            return sim_instances[order_id].get_state_dumps()
            #return self.sim_controller.get_state_dumps()

        @app.route("/order/<order_id>/start", methods=["POST"])
        def start(order_id):
            return sim_instances[order_id].start_simulation_process()
            #return self.sim_controller.start_simulation_process()

        @app.route("/order/<order_id>/stop", methods=["POST"])
        def stop(order_id):
            return sim_instances[order_id].reset_sim()
            #return self.sim_controller.reset_sim()

        @app.route("/order/<order_id>/pause", methods=["POST"])
        def pause(order_id):
            return sim_instances[order_id].pause_sim()
            #return self.sim_controller.pause_sim()

        @app.route("/order/<order_id>/resume", methods=["POST"])
        def resume(order_id):
            return sim_instances[order_id].resume_sim()
            #return self.sim_controller.resume_sim()

        @app.route("/order/<order_id>/rt_factor", methods=["POST"])
        def post_rt_factor(order_id):
            value = float(request.args.get("value"))
            return sim_instances[order_id].set_rt_factor(value)
            #return self.sim_controller.set_rt_factor(value)

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

def run_server(sim_factory):
    #sim_factory = RunnableTourSimGeoFactory()
    flask_sim_server = FlaskSimServer(sim_factory)
    flask_sim_server.run_sim_server()
