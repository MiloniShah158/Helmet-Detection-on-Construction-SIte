import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import render_template, request, session, url_for, redirect

from project import app
from project.com.dao.LoginDAO import LoginDAO
from project.com.dao.RegisterDAO import RegisterDAO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.RegisterVO import RegisterVO


@app.route('/', methods=['get'])
def adminLoadLogin():
    try:
        session.clear()
        return render_template('admin/login.html')
    except Exception as ex:
        print(ex)


@app.route('/admin/validateLogin', methods=['post'])
def adminValidateLogin():
    try:
        loginUsername = request.form['loginUsername']
        loginPassword = request.form['loginPassword']

        loginVO = LoginVO()
        loginDAO = LoginDAO()

        loginVO.loginUsername = loginUsername
        loginVO.loginPassword = loginPassword
        # loginVO.loginStatus = 'active'

        loginVOList = loginDAO.validateLogin(loginVO)

        loginDictList = [i.as_dict() for i in loginVOList]

        print(loginDictList)

        lenLoginDictList = len(loginDictList)

        if lenLoginDictList == 0:

            msg = "Username Or Password Incorrect!!!"
            print(msg)
            return render_template('admin/login.html', error=msg)

        elif loginDictList[0]['loginStatus'] == 'inactive':
            msg = "You are Temporarily blocked by Admin!!!"
            return render_template('admin/login.html', error=msg)

        else:
            for row1 in loginDictList:

                loginId = row1['loginId']
                loginUsername = row1['loginUsername']
                loginRole = row1['loginRole']

                session['session_loginId'] = loginId
                session['session_loginUsername'] = loginUsername
                session['session_loginRole'] = loginRole

                session.permanent = True

                if loginRole == 'admin':
                    return redirect(url_for('adminLoadDashboard'))

                elif loginRole == 'user':
                    return redirect(url_for('userLoadDashboard'))
    except Exception as ex:
        print(ex)


@app.route('/admin/unblockUser', methods=['get'])
def adminunblockUser():
    try:

        loginVO = LoginVO()
        loginDAO = LoginDAO()

        loginId = request.args.get('loginId')

        print('loginId::', loginId)

        loginVO.loginId = loginId

        registerDAO = RegisterDAO()

        loginVO.loginRole = 'user'
        loginVO.loginStatus = 'active'

        loginDAO.validateLogin(loginVO)
        registerDAO.viewRegister()
        loginDAO.unblockUser(loginVO)

        return redirect(url_for('adminViewUser'))


    except Exception as ex:
        print(ex)


@app.route('/admin/blockUser', methods=['get'])
def adminblockUser():
    try:

        loginVO = LoginVO()
        loginDAO = LoginDAO()

        loginId = request.args.get('loginId')

        print('loginId::', loginId)

        loginVO.loginId = loginId

        registerDAO = RegisterDAO()

        loginVO.loginRole = 'user'
        loginVO.loginStatus = 'inactive'

        loginDAO.validateLogin(loginVO)
        registerDAO.viewRegister()
        loginDAO.blockUser(loginVO)

        return redirect(url_for('adminViewUser'))


    except Exception as ex:
        print(ex)


@app.route('/admin/LoadDashboard', methods=['get'])
def adminLoadDashboard():
    try:
        if adminLoginSession() == 'admin':
            return render_template('admin/index.html')
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/LoadDashboard', methods=['get'])
def userLoadDashboard():
    try:
        if adminLoginSession() == 'user':
            return render_template('user/index.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/forgotPassword')
def userforgotPassword():
    try:
        return render_template('user/forgotPassword.html')
    except Exception as ex:
        print(ex)


@app.route('/user/validateUsername', methods=['post'])
def uservalidateUsername():
    try:
        loginUsername = request.form['loginUsername']
        loginVO = LoginVO()
        loginDAO = LoginDAO()

        loginVO.loginUsername = loginUsername

        loginVOList = loginDAO.loginUsername(loginVO)

        loginDictList = [i.as_dict() for i in loginVOList]

        print(loginDictList)

        lenLoginDictList = len(loginDictList)

        if lenLoginDictList == 0:

            msg = "Username is Incorrect!!!"
            print(msg)
            return render_template('user/forgotPassword.html', error=msg)

        else:
            loginOTP = ''.join((random.choice(string.digits)) for x in range(4))

            session['session_OTP'] = loginOTP
            session['session_loginUsername'] = loginUsername
            session['session_loginId'] = loginDictList[0]['loginId']

            print("loginOTP= " + loginOTP)

            sender = 'helmetconst@gmail.com'

            receiver = loginUsername

            msg = MIMEMultipart()

            msg['FROM'] = sender

            msg['TO'] = receiver

            msg['SUBJECT'] = 'OTP from helmetconst'

            msg.attach(MIMEText(loginOTP, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)

            server.starttls()

            server.login(sender, "dkppwd1998@")

            text = msg.as_string()

            server.sendmail(sender, receiver, text)

        return render_template('user/generateOTP.html')
    except Exception as ex:
        print(ex)


@app.route('/user/newPassword', methods=['POST'])
def usernewPassword():
    try:
        userOTP = request.form['userOtp']
        if userOTP == session['session_OTP']:
            loginVO = LoginVO()
            loginDAO = LoginDAO()

            loginPassword = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))

            print("loginPassword= " + loginPassword)

            sender = 'helmetconst@gmail.com'

            receiver = session['session_loginUsername']

            msg = MIMEMultipart()

            msg['FROM'] = sender

            msg['TO'] = receiver

            msg['SUBJECT'] = 'PYTHON PASSWORD'

            msg.attach(MIMEText(loginPassword, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)

            server.starttls()

            server.login(sender, "dkppwd1998@")

            text = msg.as_string()

            server.sendmail(sender, receiver, text)

            loginVO.loginUsername = receiver
            loginVO.loginId = session['session_loginId']
            loginVO.loginPassword = loginPassword

            loginDAO.updatePassword(loginVO)

            return render_template("admin/login.html", error="Your new password is sent to your email address!")
        else:
            return render_template('admin/login.html', error="Invalid OTP,Please ty again!")
    except Exception as ex:
        print(ex)


@app.route('/user/editProfile', methods=['get'])
def usereditProfile():
    try:
        if adminLoginSession() == 'user':

            loginId = session['session_loginId']

            registerVO = RegisterVO()
            registerVO.register_LoginId = loginId

            registerDAO = RegisterDAO()
            registerDAO.editProfile(registerVO)
            registerVOList = registerDAO.editProfile(registerVO)

            print("=========registerVOList==========", registerVOList)

            print("=======type of registerVOList=======", type(registerVOList))

            return render_template('user/editProfile.html', registerVOList=registerVOList)

        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/userUpdateProfile', methods=['POST'])
def userupdateProfile():
    try:
        if adminLoginSession() == 'user':
            registerId = request.form['registerId']
            companyName = request.form['companyName']
            registerFirstname = request.form['registerFirstname']
            registerLastname = request.form['registerLastname']
            registerGender = request.form['registerGender']
            registerAddress = request.form['registerAddress']
            registerContact = request.form['registerContact']

            loginId = request.form['loginId']
            loginUsername = request.form['loginUsername']

            registerVO = RegisterVO()
            registerDAO = RegisterDAO()
            loginVO = LoginVO()
            loginDAO = LoginDAO()

            loginVO.loginId = loginId
            loginList = loginDAO.getLoginDetails(loginVO)

            if loginUsername != loginList[0].loginUsername:
                loginPassword = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))

                print("loginPassword= " + loginPassword)

                sender = 'helmetconst@gmail.com'

                receiver = loginUsername

                msg = MIMEMultipart()

                msg['FROM'] = sender

                msg['TO'] = receiver

                msg['SUBJECT'] = 'PYTHON PASSWORD'

                msg.attach(MIMEText(loginPassword, 'plain'))

                server = smtplib.SMTP('smtp.gmail.com', 587)

                server.starttls()

                server.login(sender, "dkppwd1998@")

                text = msg.as_string()

                server.sendmail(sender, receiver, text)

                server.quit()

                loginVO.loginUsername = loginUsername
                loginVO.loginPassword = loginPassword

                loginDAO.updatePassword(loginVO)

            registerVO.registerId = registerId
            registerVO.companyName = companyName
            registerVO.registerFirstname = registerFirstname
            registerVO.registerLastname = registerLastname
            registerVO.registerAddress = registerAddress
            registerVO.registerGender = registerGender
            registerVO.registerContact = registerContact

            registerDAO.updateProfile(registerVO)

            return redirect(url_for('userLoadDashboard'))

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/changePassword')
def userchangePassword():
    try:
        if adminLoginSession() == 'user':
            return render_template('user/changePassword.html')
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/updatePassword', methods=['post'])
def userupdatePassword():
    try:
        if adminLoginSession() == 'user':

            oldPassword = request.form['oldPassword']
            newPassword = request.form['newPassword']
            confirmPassword = request.form['confirmPassword']

            loginId = session['session_loginId']
            loginUsername = session['session_loginUsername']

            loginVO = LoginVO()
            loginDAO = LoginDAO()

            loginVO.loginUsername = loginUsername

            loginVOList = loginDAO.loginUsername(loginVO)

            loginDictList = [i.as_dict() for i in loginVOList]

            print(loginDictList)

            for row in loginDictList:
                loginPassword = row['loginPassword']

                session['session_loginPassword'] = loginPassword

                session.permanent = True

                if session['session_loginPassword'] == oldPassword:
                    if newPassword == confirmPassword:

                        loginVO.loginId = loginId
                        loginVO.loginPassword = confirmPassword
                        loginDAO.updatePassword(loginVO)

                        return redirect(url_for('userLoadDashboard'))

                    else:
                        msg = "Your New and Confirm Password does not match!!!"
                        return render_template('user/changePassword.html', error=msg)
                else:
                    msg = "Your Old password is Incorrect!!!"
                    return render_template('user/changePassword.html', error=msg)

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)

@app.route('/admin/loginSession')
def adminLoginSession():
    try:
        if 'session_loginId' and 'session_loginRole' in session:

            if session['session_loginRole'] == 'admin':
                print("!!!!!!!!!!!!!TRUE!!!!!!!!!!!!!!")
                return 'admin'

            elif session['session_loginRole'] == 'user':
                print("!!!!!!!!!!!!!TRUE!!!!!!!!!!!!!!")
                return 'user'

        else:
            print("!!!!!!!!!!!!!FALSE!!!!!!!!!!!!!!")
            return False
    except Exception as ex:
        print(ex)


@app.route('/admin/logoutSession', methods=['get'])
def adminLogoutSession():
    try:
        session.clear()
        return redirect(url_for('adminLoadLogin'))
    except Exception as ex:
        print(ex)
