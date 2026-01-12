def dict_contains_subset(superset, subset) -> bool:
    for key, value in subset.items():
        if key not in superset:
            return False
        if superset[key] != value:
            return False
    return True
