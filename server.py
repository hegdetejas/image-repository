from flask import Flask, request, render_template, jsonify
import boto3
import botocore.exceptions
import uuid
import random
import json

app = Flask(__name__)


def verify_input_file(filepath):
    if filepath[-4:] == "jpg":
        return True
    else:
        return False


@app.route("/index.html", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def index():
    s3_client = boto3.client("s3")
    generated_uuid = str(uuid.uuid1())
    unique_filename = generated_uuid + "~" + "${filename}"
    try:
        print(f"images/{unique_filename}")
        response = s3_client.generate_presigned_post(Bucket="shopify-repository", Key=f"images/{unique_filename}", Fields=None, ExpiresIn=300, \
        Conditions=[["starts-with", "$success_action_redirect", ""]])
    except botocore.exceptions.ClientError as e:
        logging.error(e)
        return None

    response["fields"]["success_action_redirect"] = "http://0.0.0.0:5000/success"
    response["fields"]["bucket_name"] = "shopify-repository"

    return render_template("index.html", data=response["fields"])


@app.route("/success", methods=["GET"])
def add_success():
    return render_template("add-success.html")

@app.route("/about", methods=["GET"])
@app.route("/about.html", methods=["GET"])
def about():
    return render_template("about.html")


@app.route("/uploaded", methods=["GET", "POST"])
@app.route("/uploaded.html", methods=["GET", "POST"])
def uploaded_images():
    if request.method == "GET":
        s3_client = boto3.client("s3")
        curr_bucket = s3_client.list_objects_v2(Bucket="shopify-repository", Prefix="images")
        http_dict = {}
        http_dict["paths"] = []
        temp = []
        try:
            for stored_obj in curr_bucket["Contents"]:
                temp.append(f"https://shopify-repository.s3.amazonaws.com/{stored_obj['Key']}")
        except KeyError:
            http_dict = {}
            temp = []
    
        for path in temp:
            if not path.endswith("~"):
                http_dict["paths"].append(path)
    
        return render_template("uploaded.html", data=http_dict)
    else:
        data = request.get_json()
        s3_client = boto3.resource("s3")
        try:
            filename = data["image_src"].split("/")[-1]
            s3 = boto3.resource("s3")
            obj = s3.Object("shopify-repository", f"images/{filename}")
            obj.delete()
            return jsonify(status="success")
        except:
            return jsonify(status="failure")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')