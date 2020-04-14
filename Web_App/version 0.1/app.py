import os
from flask import Flask, request, render_template, url_for, redirect
import flask
import paramiko
#Initialize the app by adding:

app = Flask(__name__)

#Add the below line to create the home page route:

@app.route("/")
def fileFrontPage():
    return render_template('index.html')


@app.route("/handleUpload", methods=['POST'])
def handleFileUpload():
    files = flask.request.files.getlist("photo")
    protocol = 'pscp -i'
    key_loc = ' C:/Users/iGuest/Downloads/bittu.ppk'
    upload_dir = ' C:/Users/iGuest/Desktop/Photo/'
    ec2_instance = ' ubuntu@ec2-18-237-110-201.us-west-2.compute.amazonaws.com'
    remote_dir = ':/home/RAW_Images'
    for file in files:
        #file.save(os.path.join('C:/Users/iGuest/Desktop/', file.filename))
        arg = protocol+key_loc+upload_dir+file.filename+ec2_instance+remote_dir
        os.system(arg)

    k = paramiko.RSAKey.from_private_key_file("C:/Users/iGuest/Downloads/bittu.pem")
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("connecting")
    c.connect(hostname="ec2-18-237-110-201.us-west-2.compute.amazonaws.com", username="ubuntu", pkey=k)
    print("connected")
    commands = ["bash /home/execute.sh", "zip -r /home/Optimized_Image.zip /home/Optimized_Image"]
    for command in commands:
        print("Executing {0}".format(command))
        stdin , stdout, stderr = c.exec_command(command)
        print(stdout.read())
        print("Errors")
        print(stderr.read())
    c.close()

    os.system('pscp -i C:/Users/iGuest/Downloads/bittu.ppk ubuntu@ec2-18-237-110-201.us-west-2.compute.amazonaws.com:/home/Optimized_Image.zip C:/Users/iGuest/Downloads')
    return redirect(url_for('fileFrontPage'))

if __name__ == '__main__':
    app.run()
