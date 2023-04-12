from flask import Flask, request, send_file, render_template_string, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template_string(
        """
        <html>
            <body>
                Hello There!
                <p>
                    <a href="https://www.google.com">Click here</a>
                </p>
            </body>
        </html>
        """
    )


@app.route("/home/")
def home_2():
    return render_template("core/index.html")


@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        print(request.form)
        return render_template("core/index.html")

    return render_template("auth/login.html")


app.run(debug=True)
