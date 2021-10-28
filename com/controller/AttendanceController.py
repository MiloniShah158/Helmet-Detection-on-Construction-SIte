import os
from datetime import datetime
from project import app
from flask import render_template, request, url_for, redirect, session
from werkzeug.utils import secure_filename
from project.com.controller.LoginController import adminLogoutSession, adminLoginSession
from project.com.dao.AttendanceDAO import AttendanceDAO
from project.com.dao.RegisterDAO import RegisterDAO
from project.com.vo.AttendanceVO import AttendanceVO

UPLOAD_FOLDER = 'project/static/userResources/face/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/admin/loadAttendance')
def adminloadAttendance():
    try:
        if adminLoginSession() == 'admin':
            registerDAO = RegisterDAO()
            registerVOList = registerDAO.viewRegister_User()

            return render_template('admin/addAttendance.html', registerVOList=registerVOList)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/insertAttendance', methods=['post'])
def admininsertAttendance():
    try:
        if adminLoginSession() == 'admin':
            attendanceVO = AttendanceVO()
            attendanceDAO = AttendanceDAO()

            attendance_RegisterId = session['session_registerId']

            file = request.files['file']
            print(file)

            attendanceFileName = secure_filename(file.filename)
            print(attendanceFileName)

            attendanceFilePath = os.path.join(app.config['UPLOAD_FOLDER'])
            print(attendanceFilePath)

            file.save(os.path.join(attendanceFilePath, attendanceFileName))

            videoUploadDate = datetime.date(datetime.now())
            videoUploadTime = datetime.time(datetime.now())

            attendanceVO.attendanceFileName = attendanceFileName
            attendanceVO.attendanceFilePath = attendanceFilePath.replace("project", "..")

            attendanceVO.videoUploadDate = videoUploadDate
            attendanceVO.videoUploadTime = videoUploadTime

            attendanceVO.video_RegisterId = attendance_RegisterId

            attendanceDAO.adminInsertAttendance(attendanceVO)

            return redirect(url_for('adminviewAttendance'))

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/viewAttendance')
def adminviewAttendance():
    try:
        if adminLoginSession() == 'admin':
            attendanceDAO = AttendanceDAO()
            attendanceVO = AttendanceVO()

            attendance_RegisterId = session['attendance_RegisterId']
            attendanceVO.attendance_RegisterId = attendance_RegisterId

            attendanceVOList = attendanceDAO.adminViewAttendance(attendanceVO)
            print("___________", attendanceVOList)

            return render_template('admin/viewAttendance.html', attendanceVOList=attendanceVOList)

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/deleteAttendance', methods=['get'])
def userdeleteAttendance():
    try:
        if adminLoginSession() == 'user':
            attendanceVO = AttendanceVO()
            attendanceDAO = AttendanceDAO()

            attendanceId = request.args.get('attendanceId')
            print('AttendanceId::', attendanceId)
            attendanceVO.attendanceId = attendanceId

            attendanceList = attendanceDAO.deleteAttendance(attendanceVO)
            attendanceFileName = attendanceList.attendanceFileName
            attendanceFilePath = attendanceList.attendanceFilePath

            if attendanceList.attendanceFileName is not None:
                attendanceFilePath = attendanceFilePath.replace('..', 'project') + attendanceFileName
                os.remove(attendanceFilePath)

            return redirect(url_for('userviewAttendance'))


        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)







