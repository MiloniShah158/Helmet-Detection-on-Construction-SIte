import os

from flask import render_template, request, url_for, redirect, session
from werkzeug.utils import secure_filename

from project import app
from project.com.controller.LoginController import adminLogoutSession, adminLoginSession
from project.com.dao.StaffDAO import StaffDAO
from project.com.vo.StaffVO import StaffVO

UPLOAD_FOLDER_PHOTO = 'project/static/userResources/staffPhotos/'

app.config['UPLOAD_FOLDER_PHOTO'] = UPLOAD_FOLDER_PHOTO


@app.route('/user/loadStaff')
def userloadStaff():
    try:
        if adminLoginSession() == 'user':
            return render_template('user/addStaff.html')

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/insertStaff', methods=['post'])
def userinsertStaff():
    try:
        if adminLoginSession() == 'user':

            staffVO = StaffVO()
            staffDAO = StaffDAO()

            staffFirstname = request.form['staffFirstname']
            staffLastname = request.form['staffLastname']
            staffGender = request.form['staffGender']
            staffContact = request.form['staffContact']
            staffDOB = request.form['staffDOB']
            staffJD = request.form['staffJD']
            staff_LoginId = session['session_loginId']

            file = request.files['file']
            print(file)

            staffPhoto = secure_filename(file.filename)
            print(staffPhoto)

            staffPhotoPath = os.path.join(app.config['UPLOAD_FOLDER_PHOTO'])
            print(staffPhotoPath)

            file.save(os.path.join(staffPhotoPath, staffPhoto))

            staffVO.staffFirstname = staffFirstname
            staffVO.staffLastname = staffLastname
            staffVO.staffGender = staffGender
            staffVO.staffContact = staffContact
            staffVO.staffDOB = staffDOB
            staffVO.staffJD = staffJD
            staffVO.staffPhoto = staffPhoto
            staffVO.staffPhotoPath = staffPhotoPath.replace("project", "..")
            staffVO.staff_LoginId = staff_LoginId

            staffDAO.insertStaff(staffVO)

            return redirect(url_for('userviewStaff'))

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/viewStaff', methods=['get'])
def userviewStaff():
    try:
        if adminLoginSession() == 'user':
            staffDAO = StaffDAO()
            staffVO = StaffVO()

            staff_LoginId = session['session_loginId']
            staffVO.staff_LoginId = staff_LoginId

            staffVOList = staffDAO.viewStaff(staffVO)
            print("___________", staffVOList)

            return render_template('user/viewStaff.html', staffVOList=staffVOList)

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/deleteStaff', methods=['get'])
def userdeleteStaff():
    try:
        if adminLoginSession() == 'user':

            staffVO = StaffVO()
            staffDAO = StaffDAO()

            staffId = request.args.get('staffId')
            staffVO.staffId = staffId

            print("staffId::", staffId)

            staffDAO.deleteStaff(staffVO)

            return redirect(url_for('userviewStaff'))

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)
