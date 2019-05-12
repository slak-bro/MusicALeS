import importlib
import os
import pkgutil

animators_dict = {}

for (module_loader, name, ispkg) in pkgutil.iter_modules(["animators"]):
    try:
        importlib.import_module('.' + name, __package__)
    except ImportError:
        animators_dict[name + " (import failed)"] = None

animators_dict = dict(animators_dict, **{cls.name: cls for cls in animator.Animator.__subclasses__()})
