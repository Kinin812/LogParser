import importlib
import inspect
import os
import re
import sys

from core.base import BaseReport

PLUGIN_DIR = os.path.dirname(__file__)
ALL_REPORTS = {}


def load_plugin_reports():
    """
    Загружает все классы-отчёты и связанные с ними парсеры из модулей в директории `plugins`.
    """
    if not os.path.exists(PLUGIN_DIR):
        print(f"Plugin directory {PLUGIN_DIR} does not exist.", file=sys.stderr)
        return

    for filename in os.listdir(PLUGIN_DIR):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f"reports.plugins.{filename[:-3]}"

            try:
                module = importlib.import_module(module_name)

                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, BaseReport) and obj is not BaseReport:
                        report_name = re.sub(
                            r"([a-z0-9])([A-Z])", r"\1_\2", name
                        ).lower()
                        ALL_REPORTS[report_name] = obj

            except ModuleNotFoundError as e:
                print(f"Module {module_name} not found: {e}", file=sys.stderr)
            except Exception as e:
                print(f"Error loading plugin {filename}: {e}", file=sys.stderr)
