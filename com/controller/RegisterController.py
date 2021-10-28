import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import render_template, request

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.LoginDAO import LoginDAO
from project.com.dao.RegisterDAO import RegisterDAO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.RegisterVO import RegisterVO


@app.route('/user/loadRegister', methods=['get'])
def userRegister():
    try:
        return render_template('user/register.html')
    except Exception as ex:
        print(ex)


@app.route('/user/insertRegister', methods=['post'])
def userInsertRegister():
    try:
        loginVO = LoginVO()
        loginDAO = LoginDAO()

        registerVO = RegisterVO()
        registerDAO = RegisterDAO()

        loginUsername = request.form['loginUsername']

        companyName = request.form['companyName']
        registerFirstname = request.form['registerFirstname']
        registerLastname = request.form['registerLastname']
        registerGender = request.form['registerGender']
        registerAddress = request.form['registerAddress']
        registerContact = request.form['registerContact']

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

        loginVO.loginUsername = loginUsername
        loginVO.loginPassword = loginPassword
        loginVO.loginRole = 'user'
        loginVO.loginStatus = 'active'

        loginDAO.insertLogin(loginVO)

        registerVO.companyName = companyName
        registerVO.registerFirstname = registerFirstname
        registerVO.registerLastname = registerLastname
        registerVO.registerAddress = registerAddress
        registerVO.registerGender = registerGender
        registerVO.registerContact = registerContact

        registerVO.register_LoginId = loginVO.loginId

        registerDAO.insertRegister(registerVO)

        server.quit()

        return render_template('admin/login.html')
    except Exception as ex:
        print(ex)


@app.route('/admin/viewUser', methods=['GET'])
def adminViewUser():
    try:
        if adminLoginSession() == 'admin':
            registerDAO = RegisterDAO()
            registerVOList = registerDAO.viewRegister()
            print("______________", registerVOList)

            return render_template('admin/viewUser.html', registerVOList=registerVOList)

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)
