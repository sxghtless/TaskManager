import logging
import os
import sys

from fastapi import FastAPI

from src.config import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()

def load_module(module):
    module_path = module

    if module_path in sys.modules:
        return sys.modules[module_path]

    return __import__(module_path, fromlist=["object"])


def include_routers(app: FastAPI, app_path: str, **kwargs) -> None:
    path = os.path.join(os.path.dirname(os.path.abspath(app_path)), "routers")
    for file in os.listdir(path):
        if (
            os.path.isfile(os.path.join(path, file))
            and file.endswith(".py")
            and not file.startswith("__")
        ):
            module = load_module(f"routers.{file[:-3]}")
            try:
                router = getattr(module, "router")
                app.include_router(router, **kwargs)
                logger.info(f"add router {module}")
            except AttributeError:
                continue


