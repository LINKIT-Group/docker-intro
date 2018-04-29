from flask import Flask, render_template
import random

app = Flask(__name__)

# list of LINKIT images
images = [
    "https://www.linkit.nl/themes/default/assets/img/uploaded/Remco%20Dekkinga%201511883240.jpg",
    "https://www.linkit.nl/themes/default/assets/img/uploaded/Marco%20Arede%201518081723.jpg",
    "https://www.linkit.nl/themes/default/assets/img/uploaded/Kees%20Kleybeuker%201512053230.jpg",
    "https://www.linkit.nl/themes/default/assets/img/uploaded/Yuri%20Dolzhenko%201512054809.jpg",
    "https://www.linkit.nl/themes/default/assets/img/uploaded/Joao%20Duro%201512053051.jpg",
    "https://www.linkit.nl/themes/default/assets/img/uploaded/Dragos%20Panaite%201512052476.jpg",
    "https://www.linkit.nl/themes/default/assets/img/uploaded/Souri%20Roy%201518082233.jpg",
    "https://www.linkit.nl/themes/default/assets/img/uploaded/Mikhail%20Kaduchka%201518081814.jpg",
    "https://www.linkit.nl/themes/default/assets/img/uploaded/Tiago%20Berardo%201512054591.jpg",
    "https://www.linkit.nl/themes/default/assets/img/uploaded/Parma%20Bhagwandin%201518082027.jpg",
    "https://www.linkit.nl/themes/default/assets/img/uploaded/Frank%20Boldingh%201518081400.jpg",
    "https://www.linkit.nl/themes/default/assets/img/uploaded/%C3%96nder%20Ceylan%201512054277.jpg"
]

@app.route('/')
def index():
    url = random.choice(images)
    return render_template('index.html', url=url)

if __name__ == "__main__":
    app.run(host="0.0.0.0")