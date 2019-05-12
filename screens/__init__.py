import importlib
import os
import pkgutil

screens_dict = {}

for (module_loader, name, ispkg) in pkgutil.iter_modules(["screens"]):
    try:
        importlib.import_module('.' + name, __package__)
    except ImportError:
        screens_dict[name + " (import failed)"] = None

screens_dict = dict(screens_dict, **{cls.name: cls for cls in screen.Screen.__subclasses__()})
