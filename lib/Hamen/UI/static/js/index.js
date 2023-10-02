const initialRender = () => {
    return new Promise((resolve, reject) => {
        const updateEvent = (element, eventType) => {
            fetch('/handle-event', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ elementID: element.getAttribute("id"), eventType: eventType }),
                })
                .then(response => response.json())
                .then(data => {
                    if (data.result === 'success') {
    
                    } else {
                        console.error('Error executing JavaScript on the server:', data.message);
                    }
                })
                .catch(error => {
                    console.error('HTTP request error:', error);
                });
        }
    
        let elements = document.querySelectorAll("*[id]");
        elements.forEach(element => {
            element.addEventListener("click", e => { updateEvent(element, "CLICK"); });
        });

        resolve();
    })
}

window.addEventListener("load", () => {
    initialRender().then(() => {
        const socketURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port;
        const socket = io.connect(socketURL);

        // Set innerText of element:
        socket.on("SET_ELEMENT_INNER_TEXT", function(data = {}) {
            const element = document.getElementById(data["element"]);
            if (element) element.innerText = data["value"];
        });

        // Set document title:
        socket.on("SET_DOCUMENT_TITLE", function(data = {}) {
            document.title = data["value"];
        });
    });
})