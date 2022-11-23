"""A dummy class to enumerate numerous columns names in string values."""
import re


class DummyStrEnum:
    # TODO -- написать кастомный getattr (зачем, лол?)
    # TODO -- typehints
    def __init__(self, type_name: str, **elements: str):
        self._type = type_name
        self._elements = elements
        for name, value in elements.items():
            self.__setattr__(name, value)

    @property
    def elements(self) -> dict[str, str]:
        return self._elements

    def for_pattern(self, *, new_type: str = None,
                    key_pattern: str = ".*", value_pattern: str = ".*"):
        """Construct new enum from elements that match given regex.

        :param new_type: new type name
        :param key_pattern: regex to match keys
        :param value_pattern: regex to match values
        """
        new_type = new_type or self._type
        new_elements = {
            k: v for k, v in self._elements.items()
            if re.match(key_pattern, k) and re.match(value_pattern, v)
        }
        return DummyStrEnum(new_type, **new_elements)

    def __iter__(self):
        return self._elements.items()

    def __getitem__(self, item):
        return self._elements[item]

    def __add__(self, other):
        return DummyStrEnum(self._type + "+" + other._type,
                            **self._elements, **other.elements)

    def __str__(self):
        elements_str = ", ".join(f"{k}={v}" for k, v in self._elements.items())
        return f"{self.__class__.__name__}({self._type})[{elements_str}]"

    @staticmethod
    def from_list(type_name: str, *elements: str):
        pairs = dict(zip(elements, elements))
        return DummyStrEnum(type_name, **pairs)
