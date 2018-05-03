import os
import json
import importlib.util
import logging

from yumi.modulecontext import ModuleContext


BASE_ABS_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)),
        "base"))

BASE_CONF = "conf.json"

DATA_DIR = ".yumi"
DATA_CACHE_DIR = "cache"
DATA_TEMP_DIR = "temp"
DATA_CONF = "conf.json"

LOCAL_CONF = "yumi.json"


def init_global(dir_path):
    dir_path = os.path.abspath(dir_path)

    data_path = os.path.join(dir_path, DATA_DIR)
    data_cache_path = os.path.join(dir_path, DATA_DIR, DATA_CACHE_DIR)
    data_temp_path = os.path.join(dir_path, DATA_DIR, DATA_TEMP_DIR)
    data_conf_path = os.path.join(dir_path, DATA_DIR, DATA_CONF)

    result = False
    dirs = [data_path, data_cache_path, data_temp_path]
    for d in dirs:
        if not os.path.exists(d):
            os.mkdir(d)
            result = True
    if not os.path.exists(data_conf_path):
        with open(os.path.join(os.path.dirname(__file__), "yumi.default.json"), "rb") as fr:
            with open(data_conf_path, "wb") as fw:
                fw.write(fr.read())
                result = True
    return result


def get_yumi_root(dir_path: str):
    dir_path = os.path.abspath(dir_path)
    while True:
        if os.path.exists(os.path.join(dir_path, DATA_DIR)):
            return dir_path
        next_dir = os.path.dirname(dir_path)
        if next_dir == dir_path:
            return None
        dir_path = next_dir


def get_local_conf(dir_path: str):
    path = os.path.join(dir_path, LOCAL_CONF)
    if os.path.exists(path):
        with open(path, "rb") as f:
            return json.load(f)
    return None


def set_local_conf(dir_path: str, conf: dict):
    path = os.path.join(dir_path, LOCAL_CONF)
    if conf is None:
        if os.path.exists(path):
            os.remove(path)
    else:
        with open(path, "w") as f:
            json.dump(conf, f)


def load_python_modules(path: str):
    path = os.path.abspath(path)
    name = path.replace("/", ".")

    spec = importlib.util.spec_from_file_location(name, path)
    pymodule = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pymodule)
    result = pymodule.Modules
    return result


def load_conf_modules(path: str):
    path = os.path.abspath(path)
    dir_path = os.path.dirname(path)
    with open(path, "rb") as f:
        data = json.load(f)
    result = {}
    include_list = data.get("include", [])
    modules_list = data.get("modules", {})
    for x in include_list:
        result.update(load_modules(dir_path, x))

    for key in modules_list:
        value = modules_list[key]
        value_res = load_modules(dir_path, value)
        if len(value_res) != 1:
            logging.error("{} module conflict: {} targets".format(key, len(value_res)))
        else:
            for x in value_res:
                result[key] = value_res[x]

    return result


def load_modules(dir_path: str, path: str):
    path, _, target = path.partition("@")

    if path == "#base":
        path = os.path.join(BASE_ABS_DIR, BASE_CONF)
    else:
        path = os.path.join(dir_path, path)
    path = os.path.abspath(path)

    if not os.path.exists(path):
        logging.error("{} not found".format(path))
        return None
    extension = os.path.splitext(path)[1]
    if extension == ".py":
        result = load_python_modules(path)
    else:
        result = load_conf_modules(path)

    if target:
        if isinstance(target, str):
            target = [target]
        if not isinstance(target, list):
            return None

        filtered_result = {}
        for x in target:
            if x in result: filtered_result[x] = result[x]
        result = filtered_result
    return result


def load_root_modules(root_path):
    modules = None
    if root_path is not None:
        conf_path = os.path.join(root_path, DATA_DIR, DATA_CONF)
        if os.path.exists(conf_path):
            modules = load_modules(root_path, conf_path)
    if modules is None:
        modules = load_modules(os.path.dirname(__file__), "yumi.default.json")
    return modules


def run(dir_path: str, module: str, module_args: list):
    local_conf = get_local_conf(dir_path)
    yumi_root = get_yumi_root(dir_path)
    modules = load_root_modules(yumi_root)

    if not module:
        logging.info("Available modules:")
        for x in modules:
            logging.info("  {}".format(x))
    if module not in modules:
        logging.error("{} not found".format(module))
        return

    context = ModuleContext()
    context.working_dir = dir_path
    context.root_dir = yumi_root
    context.local_conf = local_conf

    target_module = modules[module]
    result = target_module.do(module_args, context)
    set_local_conf(dir_path, context.local_conf)
    return result
