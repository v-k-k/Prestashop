from collections import namedtuple
import json
import os


def get_environment():
    Env = namedtuple("Env", "single_run, use_selenoid, sauce_labs, browser_stack")
    with open(f"tests{os.sep}test_environment.json") as file:
        env = json.load(file)
        return Env(env["single_run"], env["use_selenoid"], env["sauce_labs"], env["browser_stack"])


def get_desired_capabilities():
    with open(f"tests{os.sep}desired_capabilities.json") as file:
        return json.load(file)


def get_sauce_labs_capabilities():
    with open(f"tests{os.sep}sauce_labs.json") as file:
        return json.load(file)


def get_browser_stack_capabilities():
    with open(f"tests{os.sep}browser_stack.json") as file:
        return json.load(file)
