import os
from datetime import datetime

from flask import render_template, request, url_for, redirect, session
from werkzeug.utils import secure_filename

from project import app
from project.com.controller.LoginController import adminLogoutSession, adminLoginSession
from project.com.dao.VideoDAO import VideoDAO
from project.com.vo.VideoVO import VideoVO
from project.com.dao.RegisterDAO import RegisterDAO

UPLOAD_FOLDER = 'project/static/userResources/video/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/admin/loadVideo')
def adminloadVideo():
    try:
        if adminLoginSession() == 'admin':
            registerDAO = RegisterDAO()
            registerVOList = registerDAO.viewRegister_User()

            return render_template('admin/addVideo.html', registerVOList=registerVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/insertVideo', methods=['post'])
def adminInsertVideo():
    try:
        if adminLoginSession() == 'admin':
            videoVO = VideoVO()
            videoDAO = VideoDAO()

            video_RegisterId = session['session_registerId']

            file = request.files['file']
            print(file)

            videoInputFileName = secure_filename(file.filename)
            print(videoInputFileName)

            videoInputFilePath = os.path.join(app.config['UPLOAD_FOLDER'])
            print(videoInputFilePath)

            file.save(os.path.join(videoInputFilePath, videoInputFileName))

            videoUploadDate = datetime.date(datetime.now())
            videoUploadTime = datetime.time(datetime.now())

            videoVO.videoInputFileName = videoInputFileName
            videoVO.videoInputFilePath = videoInputFilePath.replace("project", "..")

            videoVO.videoUploadDate = videoUploadDate
            videoVO.videoUploadTime = videoUploadTime

            videoVO.video_RegisterId = video_RegisterId

            videoDAO.adminInsertVideo(videoVO)

            return redirect(url_for('adminviewVideo'))

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/viewVideo', methods=['get'])
def adminviewVideo():
    try:
        if adminLoginSession() == 'admin':
            videoDAO = VideoDAO()
            videoVO = VideoDAO()

            video_RegisterId = session['session_registerId']
            videoVO.video_RegisterId = video_RegisterId

            videoVOList = videoDAO.adminViewRegister()
            print("____________", videoVOList)
            return render_template('admin/viewVideo.html', videoVOList=videoVOList)

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/loadVideo')
def userloadVideo():
    try:
        if adminLoginSession() == 'user':
            return render_template('user/addVideo.html')
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/insertVideo', methods=['post'])
def userinsertVideo():
    try:
        if adminLoginSession() == 'user':

            videoVO = VideoVO()
            videoDAO = VideoDAO()

            videoType = request.form['videoType']
            video_LoginId = session['session_loginId']

            file = request.files['file']
            print(file)

            videoFileName = secure_filename(file.filename)
            print(videoFileName)

            videoFilePath = os.path.join(app.config['UPLOAD_FOLDER'])
            print(videoFilePath)

            file.save(os.path.join(videoFilePath, videoFileName))

            videoUploadDate = datetime.date(datetime.now())
            videoUploadTime = datetime.time(datetime.now())

            videoVO.videoType = videoType
            videoVO.videoFileName = videoFileName
            videoVO.videoFilePath = videoFilePath.replace("project", "..")

            videoVO.videoUploadDate = videoUploadDate
            videoVO.videoUploadTime = videoUploadTime
            videoVO.video_LoginId = video_LoginId

            videoDAO.userInsertVideo(videoVO)

            return redirect(url_for('userviewVideo'))

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/viewVideo', methods=['get'])
def userviewVideo():
    try:
        if adminLoginSession() == 'user':
            videoDAO = VideoDAO()
            videoVO = VideoDAO()

            video_LoginId = session['session_loginId']
            videoVO.video_LoginId = video_LoginId

            videoVOList = videoDAO.userViewVideo(videoVO)
            print("____________", videoVOList)
            return render_template('user/viewVideo.html', videoVOList=videoVOList)

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route("/user/deleteVideo", methods=['get'])
def userdeleteVideo():
    try:
        if adminLoginSession() == 'user':
            videoVO = VideoVO()
            videoDAO = VideoDAO()

            videoId = request.args.get('videoId')
            print('videoID::', videoId)
            videoVO.videoId = videoId

            videoList = videoDAO.deleteVideo(videoVO)
            videoInputFileName = videoList.videoInputFileName
            videoInputFilePath = videoList.videoInputFilePath
            videoOutputFileName = videoList.videoOutputFileName
            videoOutputFilePath = videoList.videoOutputFilePath

            if videoList.videoInputFileName is not None:
                videoInputFilePath = videoInputFilePath.replace('..', 'project') + videoInputFileName
                os.remove(videoInputFilePath)

            elif videoList.videoOutputFileName is not None:

                videoOutputFilePath = videoOutputFilePath.replace('..', 'project') + videoOutputFileName
                os.remove(videoOutputFilePath)

            return redirect(url_for('userviewVideo'))


        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)
