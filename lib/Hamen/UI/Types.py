from enum import Enum

class Window:
    pass

class Document:
    pass

class UIElementType(Enum):
    emptyElement = "EMPTY_ELEMENT"
    voidElement = "VOID_ELEMENT"

class UIElement:
    def __init__(self):
        self.tagName = None
        self.elementType: UIElementType = UIElementType.voidElement
        self._innerText = ""

    @property
    def innerText(self) -> str:
        return self._innerText

    @innerText.setter
    def innerText(self, value: str):
        assert type(value) in [str, int, float], f"`UIElement.innerText` must be type: `str`, not \"{type(value)}\"; if parameter is `int` or `float`, the value will be casted"

        value = str(value)
        self._innerText = value

    def __str__(self):
        match self.elementType.value:
            case "EMPTY_ELEMENT":
                return
            case "VOID_ELEMENT":
                return

        raise TypeError("Elements must be either empty, or void")