from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/choose_block')
def code_block():
    return render_template('choose_block.html')

@app.route('/edit_block')
def edit_code():
    return render_template('edit_block.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
