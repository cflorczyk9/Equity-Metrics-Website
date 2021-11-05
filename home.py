from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)


@app.route("/")
@app.route("/home", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("user", usr=user))
    else:
        return render_template('home.html')


@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"


@app.route("/about_me")
def about():
    return render_template('about_me.html', title='About')


if __name__ == '__main__':
    app.run(debug=True)