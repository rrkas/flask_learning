from flask import Flask, redirect, render_template, request

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        data = request.form
        email = data.get("email")
        password = data.get("password")
        success = email == "admin@admin.com" and password == "admin"
        if success:
            return redirect("/blogs/")    
        
        message = "invalid credentials"
        return render_template(
            "auth/login.html",
            message=message,
            success=success,
        )

    return render_template("auth/login.html")


@app.route("/blogs/", methods=["GET"])
def blogs_home():
    return render_template("blogs/blogs_home.html")

app.run(debug=True)
