from collections import namedtuple
import json
import os


def get_environment():
    Env = namedtuple("Env", "single_run, use_selenoid")
    with open(f"tests{os.sep}test_environment.json") as file:
        env = json.load(file)
        return Env(env["single_run"], env["use_selenoid"])


def get_desired_capabilities():
    with open(f"tests{os.sep}desired_capabilities.json") as file:
        return json.load(file)
