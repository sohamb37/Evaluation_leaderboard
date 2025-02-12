from website import create_app
from flask import render_template
import webbrowser
app = create_app()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0',port = 8222)
    webbrowser.open('http://10.12.10.60:8222/home')

