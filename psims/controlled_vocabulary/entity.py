try:
    from collections import Mapping
except ImportError:
    from collections.abc import Mapping


class Entity(Mapping):
    def __init__(self, vocabulary=None, **attributes):
        self.data = dict(attributes)
        self.children = []
        self.vocabulary = vocabulary

    def get(self, key, default=None):
        return self.data.get(key, default)

    def __contains__(self, key):
        return key in self.data

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        if key in ("vocabulary", "children", "data"):
            object.__setattr__(self, key, value)
        else:
            self[key] = value

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.keys())

    def keys(self):
        return self.data.keys()

    def values(self):
        return self.data.values()

    def items(self):
        return self.data.items()

    @property
    def definition(self):
        return self.data.get("def", '')

    def parent(self):
        try:
            reference = self.is_a
        except KeyError:
            return None
        try:
            return self.vocabulary[reference]
        except TypeError:
            return [self.vocabulary[r] for r in reference]

    def __repr__(self):
        template = 'Entity({self.id!r}, {self.name!r}, {self.definition!r})'
        return template.format(self=self)
