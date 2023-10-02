from Hamen import UI as HamenUI
UIElements = HamenUI.UIElements.UIBaseElements
from Hamen.Console import Console

class HomePage(HamenUI.Types.HTTPApplication):
    def __init__(self):
        super().__init__()

    def draw(self):
        document = self.document
        body = document.body

        header = UIElements.UIContainer(self)
        header.classList.add("header")
        header.style.minHeight = '16px'

        main = UIElements.UIContainer(self)
        main.classList.add("main")
        main.style.flexGrow = '1'

        body.appendChildren((header, main))

if __name__ == "__main__":
    app = HomePage()