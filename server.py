# Import required modules
from flask import Flask, request, render_template, jsonify
import boto3
import botocore.exceptions
import uuid
import random
import json



# Run a flask app
app = Flask(__name__)



@app.route("/index.html", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def index():
    """
        Called when user visits the homepage.
    """

    # Initialise s3 client
    s3_client = boto3.client("s3")
    generated_uuid = str(uuid.uuid1())
    # Create unique filename to store on S3
    unique_filename = generated_uuid + "~" + "${filename}"
    try:
        # Create a presigned post to upload images
        response = s3_client.generate_presigned_post(Bucket="shopify-repository", Key=f"images/{unique_filename}", Fields=None, ExpiresIn=300, \
        Conditions=[["starts-with", "$success_action_redirect", ""]])
    except botocore.exceptions.ClientError as e:
        logging.error(e)
        return None

    # Create key value pairs for URL redirect upon adding an image
    response["fields"]["success_action_redirect"] = "http://0.0.0.0:5000/success"
    response["fields"]["bucket_name"] = "shopify-repository"

    return render_template("index.html", data=response["fields"])


@app.route("/success", methods=["GET"])
def add_success():
    """
        Called when a user uploads an image successfully.
    """

    return render_template("add-success.html")


@app.route("/about", methods=["GET"])
@app.route("/about.html", methods=["GET"])
def about():
    """
        Called when a user vists the About Me page.
    """

    return render_template("about.html")


@app.route("/uploaded", methods=["GET", "POST"])
@app.route("/uploaded.html", methods=["GET", "POST"])
def uploaded_images():
    """
        Called when a user visits the Uploaded Images page.
    """

    # When user just wants to view the existing images
    if request.method == "GET":
        # Initialise S3 client
        s3_client = boto3.client("s3")
        # Retrieve all objects from the S3 bucket
        curr_bucket = s3_client.list_objects_v2(Bucket="shopify-repository", Prefix="images")
        # Initialise variables to send as data to HTML
        http_dict = {}
        http_dict["paths"] = []
        temp = []

        try:
            # Go through the bucket and add to temp list
            for stored_obj in curr_bucket["Contents"]:
                temp.append(f"https://shopify-repository.s3.amazonaws.com/{stored_obj['Key']}")
        except KeyError:
            http_dict = {}
            temp = []

        # Check for any objects that should not be displayed
        for path in temp:
            if not path.endswith("~"):
                http_dict["paths"].append(path)
    
        return render_template("uploaded.html", data=http_dict)
    # When the user clicks on an image to delete
    else:
        # Retrieve URL of the file that was deleted
        data = request.get_json()
        try:
            # Get filename from entire URL of file
            filename = data["image_src"].split("/")[-1]
            # Initialise s3 client
            s3_client = boto3.resource("_client")
            # Get specific object from s3 bucket
            obj = s3_client.Object("shopify-repository", f"images/{filename}")
            # Delete object
            obj.delete()

            return jsonify(status="success")
        except:
            return jsonify(status="failure")





##################################################### DRIVER CODE #####################################################
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')