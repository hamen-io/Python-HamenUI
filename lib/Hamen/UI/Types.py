import random
import string
from flask import Flask, render_template, request, jsonify
from enum import Enum
import typing
from flask_socketio import SocketIO

def generateID(length: int = 16) -> str:
    assert length > 4
    return random.choice(string.ascii_letters) + "".join(random.choices(string.ascii_letters + string.digits, k = length - 1))

class Event:
    click = "CLICK"

class StyleSheet:
    def __init__(self, **styles):
        self._styles = {
            "background": "initial",
            "backgroundColor": "initial",
            "margin": "initial",
            "marginLeft": "initial",
            "marginTop": "initial",
            "marginRight": "initial",
            "marginBottom": "initial",
            "padding": "initial",
            "paddingLeft": "initial",
            "paddingTop": "initial",
            "paddingRight": "initial",
            "paddingBottom": "initial",
            "border": "initial",
            "borderLeft": "initial",
            "borderTop": "initial",
            "borderRight": "initial",
            "borderBottom": "initial",
            "outline": "initial",
            "outlineLeft": "initial",
            "outlineTop": "initial",
            "outlineRight": "initial",
            "outlineBottom": "initial",
            "color": "initial",
            "fontSize": "initial",
            "fontWeight": "initial",
            "textAlign": "initial",
            "textDecoration": "initial",
            "textTransform": "initial",
            "lineHeight": "initial",
            "letterSpacing": "initial",
            "display": "initial",
            "width": "initial",
            "minWidth": "initial",
            "maxWidth": "initial",
            "height": "initial",
            "minHeight": "initial",
            "maxHeight": "initial",
            "float": "initial",
            "clear": "initial",
            "position": "initial",
            "top": "initial",
            "left": "initial",
            "right": "initial",
            "bottom": "initial",
            "zIndex": "initial",
            "opacity": "initial",
            "boxShadow": "initial",
            "textShadow": "initial",
            "cursor": "initial",
            "transition": "initial",
            "transform": "initial",
            "flex": "initial",
            "flexGrow": "initial",
            "flexShrink": "initial",
            "justifyContent": "initial",
            "alignItems": "initial",
            "alignSelf": "initial",
            "flexDirection": "initial",
            "flexWrap": "initial",
            "gridTemplateColumns": "initial",
            "gridTemplateRows": "initial",
            "gridGap": "initial",
            "backgroundImage": "initial",
            "backgroundPosition": "initial",
            "backgroundRepeat": "initial",
            "boxSizing": "initial",
            "overflow": "initial",
            "textAlign": "initial",
            "verticalAlign": "initial",
            "whiteSpace": "initial"
        }

        self.background = None;self.backgroundColor = None;self.margin = None;self.marginLeft = None;self.marginTop = None;self.marginRight = None;self.marginBottom = None;self.padding = None;self.paddingLeft = None;self.paddingTop = None;self.paddingRight = None;self.paddingBottom = None;self.border = None;self.borderLeft = None;self.borderTop = None;self.borderRight = None;self.borderBottom = None;self.outline = None;self.outlineLeft = None;self.outlineTop = None;self.outlineRight = None;self.outlineBottom = None;self.color = None;self.fontSize = None;self.fontWeight = None;self.textAlign = None;self.textDecoration = None;self.textTransform = None;self.lineHeight = None;self.letterSpacing = None;self.display = None;self.width = None;self.height = None;self.minWidth = None;self.minHeight = None;self.maxWidth = None;self.maxHeight = None;self.float = None;self.clear = None;self.position = None;self.top = None;self.left = None;self.right = None;self.bottom = None;self.zIndex = None;self.opacity = None;self.boxShadow = None;self.textShadow = None;self.cursor = None;self.transition = None;self.transform = None;self.flex = None;self.justifyContent = None;self.alignItems = None;self.alignSelf = None;self.flexDirection = None;self.flexWrap = None;self.gridTemplateColumns = None;self.gridTemplateRows = None;self.gridGap = None;self.backgroundImage = None;self.backgroundPosition = None;self.backgroundRepeat = None;self.boxSizing = None;self.overflow = None;self.textAlign = None;self.verticalAlign = None;self.whiteSpace = None;self.flexGrow = None;self.flexShrink = None;

    def __getattribute__(self, name: str):
        match name:
            case "_styles":
                return super().__getattribute__(name)
            case "__str__":
                styles = dict()
                for k,v in self._styles.items():
                    if v != "initial":
                        styles[k] = v

                return lambda inline=False : ";".join([f"{camelToKebab(k)}: {v}" for k,v in self._styles.items() if v]) if inline else str(styles)

        if name.startswith("__") and name.endswith("__"): return

        assert name in self._styles, f"Property \"{name}\" is invalid!"
        return self._styles[name]

    def __setattr__(self, name: str, value):
        match name:
            case "_styles":
                super().__setattr__(name, value)
                return

        assert name in self._styles, f"Property \"{name}\" is invalid!"
        self._styles[name] = value

def camelToKebab(camel: str) -> str:
    return "".join(["-" + char.lower() if char.isupper() else char for char in camel])

class Window:
    pass

class SubscriptionList:
    def __init__(self):
        self._list = []
        self._keys = set()

    def subscribe(self, key: str, fn: typing.Callable):
        assert key not in self._keys, f"Key: \"{key}\" already exists."
        self._keys.add(key)
        self._list.append({"key": key, "event": fn})

    def trigger(self, key: str, *args, **kwargs):
        for ev in self._list:
            if ev["key"] == key:
                return ev["event"](*args, **kwargs)

    def unsubscribe(self, key: str):
        if key not in self._keys:
            return

        for ev in self._list:
            if ev["key"] == key:
                self._list.remove(ev)
                self._keys.remove(key)
                return

class HTTPCommand:
    setDocumentTitle = "SET_DOCUMENT_TITLE"
    setElementInnerText = "SET_ELEMENT_INNER_TEXT"

    class IO:
        ALERT = "IO:ALERT"

    __all__ = ("SET_DOCUMENT_TITLE", "SET_ELEMENT_INNER_TEXT", "IO:ALERT")

class HTTPApplication:
    def __init__(self):
        self._title = "HamenUI Application"
        self.document = Document(self)
        self.window = Window()
        self._events = SubscriptionList()

        self._renderFlaskApplication()
        self.app: Flask
        self.socketio: SocketIO

        self.draw()

        self.socketio.run(self.app, debug=True)

    def _identifyEvent(self, elementID, event: Event):
        return f"{{{event}|{elementID}}}"

    def addEventListener(self, element, event: Event, fn: typing.Callable = lambda : None):
        self._events.subscribe(self._identifyEvent(element.ID, event), fn)

    def removeEventListener(self, element, event: Event, fn: typing.Callable = lambda : None):
        self._events.unsubscribe(self._identifyEvent(element.ID, event), fn)

    def _renderFlaskApplication(self) -> Flask:
        app = Flask(__name__, template_folder=r"templates")

        @app.route('/')
        def index():
            return render_template(r"index.html", bodyContent = self.document.body)

        @app.route('/handle-event', methods=["POST"])
        def handleEvents():
            response = request.json
            get = lambda string : response.get(string)
            self._events.trigger(self._identifyEvent(get("elementID"), get("eventType")))

            return jsonify({'result': 'success'})

        self.socketio = SocketIO(app)
        self.app = app

    def sendCommand(self, commandName: HTTPCommand, data: dict = dict()) -> property:
        assert commandName in HTTPCommand.__all__, f"Invalid command: \"{commandName}\"; commands are monitored to prevent any malicious injections or attacks"

        self.socketio.emit(commandName, data = data)

    def draw(self):
        document = self.document
        elements = self.UIElements
        body = document.body

        body.appendChild(elements.UIText(textContent = "Hello World!"))

class Document:
    def __init__(self, HTTPApplication: HTTPApplication):
        self.HTTPApplication: HTTPApplication = HTTPApplication
        self.body: UIBody = UIBody(self.HTTPApplication, IDOverride = "Application")
        self._title = "HamenUI Application"

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        assert type(value) is str, "Title must be string"
        self._title = value
        self.HTTPApplication: HTTPApplication
        self.HTTPApplication.sendCommand(HTTPCommand.setDocumentTitle, { "value": value })

class UIElementType(Enum):
    emptyElement = "EMPTY_ELEMENT"
    voidElement = "VOID_ELEMENT"

class AttributeList:
    def __init__(self, **attributes):
        self._attributeList = dict()

    def removeAttribute(self, name: str):
        del self._attributeList[name]

    def setAttribute(self, name: str, value: str | bool | float | int):
        assert type(value) in [str, bool, float, int], f"Invalid attribute value type: \"{type(value)}\""

        self._attributeList[name] = value

    def getAttribute(self, name: str):
        return self._attributeList.get(name)

    def __str__(self, inlineAttributes = False, offsetAttributes: bool = False) -> str:
        if inlineAttributes:
            attributeString = " ".join([f"{k}=\"{str(v)}\"" for k,v in self._attributeList.items()])
            if len(attributeString) > 0:
                return " " + attributeString
            return attributeString

        return str(self._attributeList)

class ClassList:
    def __init__(self, *classes):
        self._classes = set()

    def add(self, className: str):
        self._classes.add(className)

    def remove(self, className: str):
        self._classes.remove(className)

    def contains(self, className: str) -> bool:
        return className in self._classes

    def toggle(self, className: str):
        if self.contains(className):
            self.remove(className)
        else:
            self.add(className)

    def __str__(self, inlineClassNames: bool = False, offsetClasses: bool = False):
        if inlineClassNames:
            classString = f"class=\"{' '.join([x for x in self._classes])}\""
            if len(self._classes) > 0:
                if offsetClasses:
                    return " " + classString
                return classString
            return ""

        return str(list(self._classes))

class UIElement:
    def __init__(self, applicationParent, IDOverride: str = None, **kwargs):
        self.elementType: UIElementType = UIElementType.voidElement
        self._innerText = ""
        self.children = []
        self._ID = IDOverride or generateID()
        self._attributes = AttributeList()
        self.classList = ClassList()
        self.HTTPApplication: HTTPApplication = applicationParent
        self.style = StyleSheet()
        self._reservedAttributes = ("ev-rendered")

    @property
    def reservedAttributes(self) -> tuple:
        return self._reservedAttributes

    @property
    def ID(self) -> str:
        return self._ID

    @ID.setter
    def ID(self, value: str) -> str:
        raise ValueError("ID is read only")

    def setAttribute(self, key: str, value: str | bool | int | float):
        if key in self._reservedAttributes:
            raise ValueError(f"Attribute: \"{key}\" is reserved; cannot set it.")

        self._attributes.setAttribute(key, value)

    def removeAttribute(self, key: str):
        self._attributes.removeAttribute(key)

    def getAttribute(self, key: str) -> str:
        self._attributes.getAttribute(key)

    @staticmethod
    def tagID() -> str:
        return "UIElement"

    def tagName(self) -> str:
        return "UIElement"

    @property
    def innerText(self) -> str:
        return self._innerText

    @innerText.setter
    def innerText(self, value: str):
        assert type(value) in [str, int, float], f"`UIElement.innerText` must be type: `str`, not \"{type(value)}\"; if parameter is `int` or `float`, the value will be casted"

        value = str(value).strip()
        self._innerText = value

        # If HTTPApplication is not instantiated, it is likely due to changing the `innerText` inside the `draw` so the element has not been registered since the server has not been started/run:
        if self.HTTPApplication:
            self.HTTPApplication.sendCommand(HTTPCommand.setElementInnerText, { "element": self.ID, "value": self._innerText })

    def appendChild(self, child):
        self.children.append(child)

    def appendChildren(self, children: tuple):
        assert type(children) is tuple, f"Cannot append children of array-type not <class 'tuple'>"

        for child in children:
            self.children.append(child)

    def __str__(self):
        match self.elementType.value:
            case "EMPTY_ELEMENT":
                return f"<{self.tagName()}{self._attributes.__str__(True, True)} style=\"{self.style.__str__(True)}\" id=\"{self.ID}\"{self.classList.__str__(True, True)}/>"
            case "VOID_ELEMENT":
                return f"<{self.tagName()}{self._attributes.__str__(True, True)} style=\"{self.style.__str__(True)}\" id=\"{self.ID}\"{self.classList.__str__(True, True)}>{self.innerText}{''.join([x.__str__() for x in self.children])}</{self.tagName()}>"

        raise TypeError("Elements must be either empty, or void")

class UIElementsList:
    def __init__(self, applicationParent: HTTPApplication):
        self.applicationParent = applicationParent
        self._elements = set()

    def __getattr__(self, attr: str):
        def default_method(**kwargs):
            for element in self._elements:
                element: UIElement
                if element.tagID().upper() == attr.upper():
                    return element(self.applicationParent, **kwargs)

            raise ValueError(f"Unknown element: \"{attr}\"")

        return default_method

    def registerElement(self, element: UIElement):
        element.HTTPApplication = self.applicationParent
        self._elements.add(element)

    def unregisterElement(self, element: UIElement):
        self._elements.remove(element)

class UIElementNamespace:
    pass

class UIBody(UIElement):
    def __init__(self, applicationParent, **kwargs):
        super().__init__(applicationParent, **kwargs)
        self.style.display = "flex"

    @staticmethod
    def tagID():
        return "UIBody"

    def tagName(self):
        return "div"