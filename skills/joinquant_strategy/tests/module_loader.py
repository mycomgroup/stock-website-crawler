import importlib.util
import sys
import os


STRATEGIES_DIR = '/Users/yuping/Downloads/git/stock-website-crawler/strategies/joinquant_strategy'
DATA_DIR = '/Users/yuping/Downloads/git/stock-website-crawler/skills/joinquant_strategy/data'


def load_strategy_module(module_name):
    spec = importlib.util.spec_from_file_location(
        module_name,
        os.path.join(STRATEGIES_DIR, f"{module_name}.py")
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def load_data_module(module_name):
    spec = importlib.util.spec_from_file_location(
        module_name,
        os.path.join(DATA_DIR, f"{module_name}.py")
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module