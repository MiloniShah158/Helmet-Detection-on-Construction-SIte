import os
from datetime import datetime

from flask import render_template, request, url_for, redirect, session
from werkzeug.utils import secure_filename

from project import app
from project.com.controller.LoginController import adminLogoutSession, adminLoginSession
from project.com.dao.ComplainDAO import ComplainDAO
from project.com.vo.ComplainVO import ComplainVO

UPLOAD_FOLDER_COMPLAIN = 'project/static/userResources/complain/'

app.config['UPLOAD_FOLDER_COMPLAIN'] = UPLOAD_FOLDER_COMPLAIN

UPLOAD_FOLDER_REPLY = 'project/static/adminResources/reply/'

app.config['UPLOAD_FOLDER_REPLY'] = UPLOAD_FOLDER_REPLY


@app.route('/user/loadComplain')
def userloadComplain():
    try:
        if adminLoginSession() == 'user':
            return render_template('user/addComplain.html')
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/insertComplain', methods=['post'])
def userinsertComplain():
    try:
        if adminLoginSession() == 'user':

            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainSubject = request.form['complainSubject']
            complainDescription = request.form['complainDescription']
            complainFrom_LoginId = session['session_loginId']

            file = request.files['file']
            print(file)

            complainFileName = secure_filename(file.filename)
            print(complainFileName)

            complainFilePath = os.path.join(app.config['UPLOAD_FOLDER_COMPLAIN'])
            print(complainFilePath)

            file.save(os.path.join(complainFilePath, complainFileName))

            complainDate = datetime.date(datetime.now())
            complainTime = datetime.time(datetime.now())
            complainStatus = 'PENDING'

            complainVO.complainSubject = complainSubject
            complainVO.complainDescription = complainDescription
            complainVO.complainDate = complainDate
            complainVO.complainTime = complainTime
            complainVO.complainStatus = complainStatus
            complainVO.complainFileName = complainFileName
            complainVO.complainFilePath = complainFilePath.replace("project", "..")

            complainVO.complainFrom_LoginId = complainFrom_LoginId

            complainDAO.insertComplain(complainVO)

            return redirect(url_for('userviewComplain'))

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/viewComplain', methods=['get'])
def userviewComplain():
    try:
        if adminLoginSession() == 'user':
            complainDAO = ComplainDAO()
            complainVO = ComplainVO()
            complainFrom_LoginId = session['session_loginId']
            complainVO.complainFrom_LoginId = complainFrom_LoginId
            complainVOList = complainDAO.viewComplain_User(complainVO)

            print("____________", complainVOList)
            return render_template('user/viewComplain.html', complainVOList=complainVOList)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/viewComplain', methods=['get'])
def adminviewComplain():
    try:
        if adminLoginSession() == 'admin':
            complainDAO = ComplainDAO()
            complainVO = ComplainVO()
            complainVO.complainStatus = "pending"
            complainVOList = complainDAO.viewComplain_Admin(complainVO)
            print("____________", complainVOList)
            return render_template('admin/viewComplain.html', complainVOList=complainVOList)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/loadComplainReply')
def adminloadComplainReply():
    try:
        if adminLoginSession() == 'admin':
            complainId = request.args.get('complainId')

            return render_template('admin/addComplainReply.html', complainId=complainId)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/insertComplainReply', methods=['post'])
def admininsertComplainReply():
    try:
        if adminLoginSession() == 'admin':

            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainId = request.form['complainId']
            replySubject = request.form['replySubject']
            replyMessage = request.form['replyMessage']
            complainStatus = 'REPLIED'
            complainTo_LoginId = session['session_loginId']

            file = request.files['reply']
            print(file)

            replyFileName = secure_filename(file.filename)
            print(replyFileName)

            replyFilePath = os.path.join(app.config['UPLOAD_FOLDER_REPLY'])
            print(replyFilePath)

            file.save(os.path.join(replyFilePath, replyFileName))

            replyDate = datetime.date(datetime.now())
            replyTime = datetime.time(datetime.now())

            complainVO.complainId = complainId
            complainVO.replySubject = replySubject
            complainVO.replyMessage = replyMessage
            complainVO.replyFileName = replyFileName
            complainVO.replyFilePath = replyFilePath.replace("project", "..")
            complainVO.complainStatus = complainStatus
            complainVO.replyDate = replyDate
            complainVO.replyTime = replyTime

            complainVO.complainTo_LoginId = complainTo_LoginId

            complainDAO.insertComplainReply_Admin(complainVO)

            return redirect(url_for('adminviewComplain'))

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/viewComplainReply', methods=['get'])
def userviewComplainReply():
    try:
        if adminLoginSession() == 'user':
            complainDAO = ComplainDAO()
            complainVO = ComplainVO()

            complainId = request.args.get('complainId')
            complainVO.complainId = complainId

            complainVOList = complainDAO.viewComplainReply_User(complainVO)

            print("____________", complainVOList)
            return render_template('user/viewComplainReply.html', complainVOList=complainVOList)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/deleteComplain', methods=['get'])
def userdeleteComplain():
    try:
        if adminLoginSession() == 'user':

            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainId = request.args.get('complainId')
            complainVO.complainId = complainId

            complainList = complainDAO.deleteComplain(complainVO)
            complainFileName = complainList.complainFileName
            complainFilePath = complainList.complainFilePath

            complainFilePath = complainFilePath.replace('..', 'project') + complainFileName
            os.remove(complainFilePath)

            if complainList.replyFileName is not None:
                replyFilePath = complainList.replyFilePath.replace('..', 'project') + complainList.replyFileName
                os.remove(replyFilePath)

            return redirect(url_for('userviewComplain'))

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)
