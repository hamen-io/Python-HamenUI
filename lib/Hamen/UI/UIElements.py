from Hamen.UI.Types import (UIElement, UIElementNamespace, HTTPApplication)

class UIBaseElements(UIElementNamespace):
    class UIText(UIElement):
        def __init__(self, applicationParent: HTTPApplication, **kwargs):
            super().__init__(applicationParent, **kwargs)

        @staticmethod
        def tagID():
            return "UIText"

        def tagName(self):
            return "span"

    class UIContainer(UIElement):
        def __init__(self, applicationParent: HTTPApplication, **kwargs):
            super().__init__(applicationParent, **kwargs)
            self.style.display = "flex"

        @staticmethod
        def tagID():
            return "UIContainer"

        def tagName(self):
            return "div"