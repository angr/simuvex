import importlib
import pkgutil
import simuvex

def import_submodules(package):
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name
        print full_name
        if 'procedures' in full_name and '_' in full_name:
            continue
        results[full_name] = importlib.import_module(full_name)
        if is_pkg:
            results.update(import_submodules(full_name))
    return results

if __name__ == '__main__':
    import_submodules(simuvex)
