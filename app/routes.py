from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/choose-block")
def choose_block():
    return render_template("choose_block.html")

@main.route("/edit-block/<int:id>")
def edit_block(id):
    # Your logic to fetch code block by id and render it on page
    return render_template("edit_block.html", block_id=id)
