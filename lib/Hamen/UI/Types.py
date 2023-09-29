import random
import string
from flask import Flask, render_template, request, jsonify
from enum import Enum

def generateID(length: int = 16) -> str:
    assert length > 4
    return random.choice(string.ascii_letters) + "".join(random.choices(string.ascii_letters + string.digits, k = length - 1))

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
            "height": "initial",
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

    def __getattribute__(self, name: str):
        match name:
            case "_styles":
                return super().__getattribute__(name)
            case "__str__":
                styles = dict()
                for k,v in self._styles.items():
                    if v != "initial":
                        styles[k] = v

                return lambda : str(styles)

        assert name in self._styles, f"Property \"{name}\" is invalid!"
        return self._styles[name]

    def __setattr__(self, name: str, value):
        match name:
            case "_styles":
                super().__setattr__(name, value)
                return

        assert name in self._styles, f"Property \"{name}\" is invalid!"
        self._styles[name] = value

class Window:
    pass

class Document:
    def __init__(self, HTTPApplication):
        self.HTTPApplication = HTTPApplication
        self.body = UIContainer()
        self._title = "HamenUI Application"

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        assert type(value) is str, "Title must be string"
        self._title = value
        self.HTTPApplication.executeJavaScript(f"""document.title="{value}\"""", True)

class HTTPApplication:
    def __init__(self):
        self._title = "HamenUI Application"
        self.document = Document(self)
        self.window = Window()
        self.UIElements = UIElementsList(HTTPApplication)

        self.UIElements.registerElement(UIText)
        self.UIElements.registerElement(UIContainer)

        self.app = self._renderFlaskApplication()

        self.draw()

        self.app.run(debug=True)

    def _renderFlaskApplication(self) -> Flask:
        app = Flask(__name__, template_folder=r"templates")

        @app.route('/')
        def index():
            return render_template(r"index.html", bodyContent = self.document.body)

        return app

    def executeJavaScript(self, code: str, useSafety: bool = False) -> property:
        if useSafety:
            code = f"try {{ {code} }} catch {{  }}"
        
        @self.app.route('/execute-js', methods=['POST'])
        def execute_js():
            js_code = request.json.get('code', '')
            return jsonify({'result': js_code})
        
        response = self.app.test_client().post('/execute-js', json={'code': code})

        return response.data

    def draw(self):
        document = self.document
        elements = self.UIElements
        body = document.body

        body.appendChild(elements.UIText(textContent = "Hello World!"))

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
    def __init__(self):
        self.elementType: UIElementType = UIElementType.voidElement
        self._innerText = ""
        self.children = []
        self.ID = generateID()
        self._attributes = AttributeList()
        self.classList = ClassList()
        self.HTTPApplication: HTTPApplication = None
        self.style = StyleSheet()

    def setAttribute(self, key: str, value: str | bool | int | float):
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

        value = str(value)
        self._innerText = value

    def appendChild(self, child):
        self.children.append(child)

    def __str__(self):
        match self.elementType.value:
            case "EMPTY_ELEMENT":
                return f"<{self.tagName()}{self._attributes.__str__(True, True)}{self.classList.__str__(True, True)}/>"
            case "VOID_ELEMENT":
                return f"<{self.tagName()}{self._attributes.__str__(True, True)}{self.classList.__str__(True, True)}>{self.innerText}{''.join([x.__str__() for x in self.children])}</{self.tagName()}>"

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
                    return element(**kwargs)

            raise ValueError(f"Unknown element: \"{attr}\"")

        return default_method

    def registerElement(self, element: UIElement):
        element.HTTPApplication = self.applicationParent
        self._elements.add(element)

    def unregisterElement(self, element: UIElement):
        self._elements.remove(element)

class UIText(UIElement):
    def __init__(self):
        super().__init__()

    @staticmethod
    def tagID():
        return "UIText"

    def tagName(self):
        return "span"

class UIContainer(UIElement):
    def __init__(self):
        super().__init__()
        self.style.display = "flex"

    @staticmethod
    def tagID():
        return "UIContainer"

    def tagName(self):
        return "div"