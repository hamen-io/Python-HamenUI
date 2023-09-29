from Hamen import UI as HamenUI

class HomePage(HamenUI.Types.HTTPApplication):
    def __init__(self):
        super().__init__()

    def draw(self):
        document = self.document
        elements = self.UIElements
        body = document.body

        body.appendChild(elements.UIText())
        body.style.backgroundColor = "red"
        body.classList.add("test")
        body.innerText = "Hello World!"
        body.setAttribute("test", "false")

        document.title = "Bye"

if __name__ == "__main__":
    app = HomePage()