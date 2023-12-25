class A:
    TEST = "hello"

    def __init__(self) -> None:
        self.attrs = type(self)._get_attributes()

    @staticmethod
    def _get_class_attributes(cls):
        attrs = {}
        for key in cls.__dict__.keys():
            if key.startswith("__") or key.startswith("_"):
                continue
            attrs[key] = getattr(cls, key)
        return attrs

    @classmethod
    def _get_attributes(cls):
        attrs = {}
        for base in cls.__bases__:
            attrs.update(cls._get_class_attributes(base))
        attrs.update(cls._get_class_attributes(cls))
        return attrs


class B(A):
    BEST = "hehe"
    TEST = "hoho"


b = B()
a = A()
print(b.attrs)
print(a.attrs)
