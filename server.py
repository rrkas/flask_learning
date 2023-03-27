import os
from pathlib import Path

from flask import Flask, request

app = Flask(__name__)


@app.route("/html")
def home_html():
    return "Hello world"


@app.route("/")
def home_json():
    return {
        "app": "my flask app",
        "version": "1.0.0",
    }


@app.route("/users_list")
# cannot handle /users_list/ requests
@app.route("/users/")
# can handle /users_list/ requests
# trailing / is optional
def users():
    return {
        "app": "my flask app - users",
        "version": "1.0.0",
    }


@app.route("/data_passing/")
def data_passing():
    headers = dict(request.headers)
    form = dict(request.form)

    files = request.files
    file = files.get("profile")

    if file:
        uploads = Path("uploads")
        os.makedirs(uploads, exist_ok=True)
        file.save(uploads / file.filename)
        file = {
            "name": file.name,
            "filename": file.filename,
            "mimetype": file.mimetype,
            "headers": dict(file.headers),
            "size": os.stat(uploads / file.filename).st_size,
            "content_type": file.content_type,
        }

    try:
        json = dict(request.json)
    except BaseException as e:
        json = str(e)

    data = request.get_data(as_text=True)
    args = dict(request.args)
    return {
        "app": "my flask app - users",
        "version": "1.0.0",
        "headers": headers,
        "src-Lang": request.headers.get("src-Lang"),
        "Src-Lang": request.headers.getlist("Src-Lang"),
        "form": form,
        "json": json,
        "data": data,
        "args": args,
        "file": file,
    }


app.run(debug=True)
