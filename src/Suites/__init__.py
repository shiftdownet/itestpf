import importlib
import os
for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    module_name = module[:-3]
    module = importlib.import_module("Suites." + module_name)
    exec(module_name + " = getattr(module, module_name)")
    #__import__("Suites." + module[:-3], locals(), globals())
del module
