from flask import render_template

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession


@app.route('/admin/viewDetection')
def adminviewDetection():
    try:
        if adminLoginSession() == 'admin':
            return render_template('admin/viewDetection.html')
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/viewAttendance')
def userviewAttendance():
    try:
        if adminLoginSession() == 'user':
            return render_template('user/viewAttendance.html')
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/viewDetection')
def userviewDetection():
    try:
        if adminLoginSession() == 'user':
            return render_template('user/viewDetection.html')
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)
