import io
import os
from pathlib import Path

import requests
from flask import Flask, request, send_file

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


def _pow(power):
    num = request.json["num"]
    return {"num": num, "result": num**power}


@app.route("/sq")
def sq():
    return _pow(2)


@app.route("/cube")
def cube():
    return _pow(3)


@app.route("/get_bill_amount")
def get_bill_amount():
    data = request.json

    # method 1
    # total_amount = 0
    # for item in data:
    #     total_amount += item["rate"] * item["qty"]

    # method 2
    total_amount = sum([item["rate"] * item["qty"] for item in data])

    return {"data": data, "amount": total_amount}


@app.route("/set_colors")
def set_colors():
    colors = request.form.getlist("colors[]")
    return colors


@app.route("/tts")
def get_tts_result():
    data = requests.get(
        "https://unsplash.com/photos/0boeA7NBluU/download?ixid=MnwxMjA3fDF8MXxhbGx8MXx8fHx8fDJ8fDE2ODAxMDU2NTM&force=true"
    )
    return send_file(
        io.BytesIO(data.content),
        mimetype="image/jpeg",
        as_attachment=True,
        download_name="result.jpg",
    )


@app.route("/file_binary")
def file_binary_input():
    file = request.stream
    with open("uploads/temp.wav", "wb") as f:
        f.write(file.read())

    return str(os.stat("uploads/temp.wav").st_size) + "b"


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    args = request.args

    return {
        "data": data,
        "args": args,
    }


@app.route("/set_password", methods=["PATCH", "PUT", "POST"])
def set_password():
    data = request.json
    args = request.args

    return {
        "data": data,
        "args": args,
    }


"""
GET = receive resource / data
    HEAD = only headers and metadata about response
    OPTIONS = available methods and things related to a endpoint

POST = send resource / data
    PUT = set resource / data
    PATCH = modify resource / data
    DELETE = delete resource / data

"""

app.run(debug=True)
