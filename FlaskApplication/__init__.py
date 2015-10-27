from flask import Flask, redirect, render_template
from azure.servicemanagement import ServiceManagementService
from datetime import date
subscription_id = ''
cert_file = ''
sms = ServiceManagementService(subscription_id, cert_file)
service_name = ''
deployment_name = ''
role_name = ''
post_shutdown_action = 'StoppedDeallocated'
app = Flask(__name__)

@app.route('/')
def home():
    deployments = sms.get_deployment_by_name(service_name, deployment_name)
    out0 = deployments.status
    if out0 == 'Running':
        return render_template("home.html",
        title = 'VM | Running',
        year = date.today().year)
    else:
        return render_template("home2.html",
        title = 'VM | Suspended',
        year = date.today().year)

@app.route('/runit')
def runit():
    deployments = sms.get_deployment_by_name(service_name, deployment_name)
    out0 = deployments.status
    if out0 == 'Running':
        return redirect("/", code=302)
    elif out0 == 'Suspended':
        sms.start_role(service_name, deployment_name, role_name)
        return render_template("runit.html",
             StateToCheck = 'Running',
             title = 'VM | Launching...',
             year = date.today().year)
    else:
        return redirect("/", code=302)

@app.route('/shutit')
def shutit():
    deployments = sms.get_deployment_by_name(service_name, deployment_name)
    out0 = deployments.status
    if out0 == 'Suspended':
        return redirect("/", code=302)
    elif out0 == 'Running':
        sms.shutdown_role(service_name, deployment_name, role_name, post_shutdown_action)
        return render_template("shutit.html",
            StateToCheck = 'Suspended',
            title = 'VM | Shutting...',
            year = date.today().year)
    else:
        return redirect("/", code=302)

@app.route('/contact')
def kontakt():
    return render_template("contact.html",
            title = 'Contact',
            year = date.today().year)

@app.route('/checkstate')
def checkstate():
    deployments = sms.get_deployment_by_name(service_name, deployment_name)
    out0 = deployments.status
    if out0 == "Running":
        return out0
    elif out0 == "Suspended":
        return out0
    else:
        return redirect("/", code=302)

app.debug = True
if __name__ == "__main__":
    app.run()
