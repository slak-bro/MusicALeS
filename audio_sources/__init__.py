import importlib
import os
import pkgutil

audio_sources_dict = {}

for (module_loader, name, ispkg) in pkgutil.iter_modules(["audio_sources"]):
    try:
        importlib.import_module('.' + name, __package__)
    except ImportError:
        audio_sources_dict[name + " (import failed)"] = None

audio_sources_dict = dict(audio_sources_dict, **{cls.name: cls for cls in audio_source.AudioSource.__subclasses__()})
