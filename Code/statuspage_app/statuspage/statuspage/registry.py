import collections

from extras.constants import EXTRAS_FEATURES


class Registry(dict):
    """
    Central registry for registration of functionality. Once a store (key) is defined, it cannot be overwritten or
    deleted (although its value may be manipulated).
    """
    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError:
            raise KeyError(f"Invalid store: {key}")

    def __setitem__(self, key, value):
        if key in self:
            raise KeyError(f"Store already set: {key}")
        super().__setitem__(key, value)

    def __delitem__(self, key):
        raise TypeError("Cannot delete stores from registry")


# Initialize the global registry
registry = Registry()
registry['model_features'] = {
    feature: collections.defaultdict(set) for feature in EXTRAS_FEATURES
}
registry['denormalized_fields'] = collections.defaultdict(list)
registry['views'] = collections.defaultdict(dict)
