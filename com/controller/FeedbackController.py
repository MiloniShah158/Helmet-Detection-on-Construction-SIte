from datetime import datetime

from flask import render_template, request, url_for, redirect, session

from project import app
from project.com.controller.LoginController import adminLogoutSession, adminLoginSession
from project.com.dao.FeedbackDAO import FeedbackDAO
from project.com.vo.FeedbackVO import FeedbackVO


@app.route('/user/loadFeedback')
def userloadFeedback():
    try:
        if adminLoginSession() == 'user':
            return render_template('user/addFeedback.html')
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/insertFeedback', methods=['post'])
def userinsertFeedback():
    try:
        if adminLoginSession() == 'user':

            feedbackVO = FeedbackVO()
            feedbackDAO = FeedbackDAO()

            feedbackSubject = request.form['feedbackSubject']
            feedbackDescription = request.form['feedbackDescription']
            feedbackRating = request.form['feedbackRating']
            feedbackFrom_LoginId = session['session_loginId']

            feedbackDate = datetime.date(datetime.now())
            feedbackTime = datetime.now().strftime("%H:%M:%S")

            feedbackVO.feedbackSubject = feedbackSubject
            feedbackVO.feedbackDescription = feedbackDescription
            feedbackVO.feedbackRating = feedbackRating
            feedbackVO.feedbackDate = feedbackDate
            feedbackVO.feedbackTime = feedbackTime

            feedbackVO.feedbackFrom_LoginId = feedbackFrom_LoginId

            feedbackDAO.insertFeedback(feedbackVO)

            return redirect(url_for('userviewFeedback'))

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/viewFeedback', methods=['get'])
def userviewFeedback():
    try:
        if adminLoginSession() == 'user':
            feedbackDAO = FeedbackDAO()
            feedbackVO = FeedbackVO()

            feedbackFrom_LoginId = session['session_loginId']
            feedbackVO.feedbackFrom_LoginId = feedbackFrom_LoginId

            feedbackVOList = feedbackDAO.viewFeedback_User()

            print("___________", feedbackVOList)
            return render_template('user/viewFeedback.html', feedbackVOList=feedbackVOList)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/reviewFeedback', methods=['get'])
def adminreviewFeedback():
    try:
        if adminLoginSession() == 'admin':
            feedbackDAO = FeedbackDAO()
            feedbackVO = FeedbackVO()

            feedbackId = request.args.get('feedbackId')
            feedbackTo_LoginId = session['session_loginId']

            feedbackVO.feedbackId = feedbackId
            feedbackVO.feedbackTo_LoginId = feedbackTo_LoginId

            feedbackDAO.reviewFeedback_Admin(feedbackVO)

            return redirect(url_for('adminviewFeedback'))

        else:
            return adminLogoutSession()



    except Exception as ex:
        print(ex)


@app.route('/admin/viewFeedback', methods=['get'])
def adminviewFeedback():
    try:
        if adminLoginSession() == 'admin':
            feedbackDAO = FeedbackDAO()
            feedbackVOList = feedbackDAO.viewFeedback_Admin()
            print("___________", feedbackVOList)
            return render_template('admin/viewFeedback.html', feedbackVOList=feedbackVOList)

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/deleteFeedback', methods=['get'])
def userdeleteFeedback():
    try:
        if adminLoginSession() == 'user':

            feedbackVO = FeedbackVO()
            feeedbackDAO = FeedbackDAO()

            feedbackId = request.args.get('feedbackId')
            feedbackVO.feedbackId = feedbackId

            print("feedbackId::", feedbackId)
            feeedbackDAO.deleteFeedback(feedbackVO)

            return redirect(url_for('userviewFeedback'))

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)
