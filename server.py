import datetime
import json

from flask import Flask, redirect, render_template, request

from common import app
from sql import get_blogs, get_users, get_blog_by_id, validate_user, create_blog

uid = None


@app.route("/", methods=["POST", "GET"])
def login():
    global uid
    if request.method == "POST":
        data = request.form
        email = data.get("email")
        password = data.get("password")
        success, uid = validate_user(email, password)
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
    data = get_blogs()
    # print(data)
    return render_template("blogs/blogs_home.html", data=data)


@app.route("/blogs/new/", methods=["GET", "POST"])
def new_blog():
    if request.method == "POST":
        data = request.form
        title = data.get("title")
        desc = data.get("desc")
        create_blog(title, desc, uid)
        return redirect("/blogs/")

    return render_template("blogs/blog_form.html")


@app.route("/blog/<pk>/", methods=["GET"])
def view_blog(pk):
    blog = get_blog_by_id(pk)
    user = blog.user
    return render_template("blogs/blog_view.html", blog=blog, user=user)


app.run(debug=True)
