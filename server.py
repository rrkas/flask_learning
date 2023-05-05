import json
import datetime
from flask import Flask, redirect, render_template, request

from models.blog import Blog

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
    with open("./demo/blogs.json") as f:
        data = json.load(f)

    data = [Blog(**e) for e in data]
    print(data)
    return render_template("blogs/blogs_home.html", data=data)


@app.route("/blogs/new/", methods=["GET", "POST"])
def create_blog():
    if request.method == "POST":
        data = request.form
        title = data.get("title")
        desc = data.get("desc")
        blog = Blog(title, desc, datetime.datetime.now(), "demo_user")

        with open("./demo/blogs.json") as f:
            data: list = json.load(f)

        data.append(blog.to_dict())

        with open("./demo/blogs.json", "w") as f:
            json.dump(data, f, indent=4, default=str)

        return redirect("/blogs/")

    return render_template("blogs/blog_form.html")


@app.route("/blog/<pk>/", methods=["GET"])
def view_blog(pk):
    data = json.load(open("./demo/blogs.json"))
    blog = None
    for e in data:
        if e["id"] == pk:
            blog = e
            break
    
    user = None
    if blog:
        blog = Blog(**blog)
        users = json.load(open("./demo/users.json"))
        for e in users:
            if e["uid"] == blog.uid:
                user = e
    
    return render_template("blogs/blog_view.html", blog=blog, user=user)

app.run(debug=True)
