# Tejas Hegde - Shopify Image Repository

Hello! Welcome to my GitHub repository that contains the code for the public image repository. server.py contains the web server 
that was built using Python. The backend was developed with the Flask framework and connects and stores all images in an Amazon
Web Services S3 Storage Bucket. I hope you enjoy it :)


**********************************************************************************************************************************


## Usage

To run this application, first clone the repository and ensure that boto3 and flask are installed by your package manager (I use
pip). Then, cd into the folder that was created by the clone and type `python server.py`. This should start the local web server
and provide you with an IP address to copy and paste into the browser (should be http://0.0.0.0:5000/). The homepage allows you
to choose a file to upload. The files must be of type .jpg or .png. If an invalid file format is inputted, the user is informed
by the alert function from JavaScript. The Uploaded Images tab retrieves all the files from the AWS S3 Bucket and displays them
to the user. An image can be deleted by clicking on it and confirming. Finally, there's an About Me page that has a little bit
of information and a link to my LinkedIn page.


**********************************************************************************************************************************


## Further Steps

My aim for this project was to create a simple functioning public image repository that allows for the Add and Delete commands.
An interesting addition to this would be to limit role access through including login forms where access tokens can determine the
user and the displayed images. This would be added using the python-oauth2 framework within Python and allows for easy credential
verification using OAuth2.0
