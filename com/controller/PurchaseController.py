from _datetime import datetime

from flask import render_template, redirect, url_for, session, request

from project import app
from project.com.controller.LoginController import adminLogoutSession, adminLoginSession
from project.com.dao.PackageDAO import PackageDAO
from project.com.dao.PurchaseDAO import PurchaseDAO
from project.com.vo.PurchaseVO import PurchaseVO
from project.com.vo.LoginVO import LoginVO


@app.route('/user/viewPackage')
def userviewPackage():
    try:
        if adminLoginSession() == 'user':
            packageDAO = PackageDAO()
            packageVOList = packageDAO.viewPackage()
            return render_template('user/viewPackage.html', packageVOList=packageVOList)

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/insertPurchase', methods=['get'])
def userinsertPurchase():
    try:
        if adminLoginSession() == 'user':

            purchaseVO = PurchaseVO()
            purchaseDAO = PurchaseDAO()

            purchase_LoginId = session['session_loginId']
            purchaseDate = datetime.date(datetime.now())
            purchaseTime = datetime.time(datetime.now())
            purchase_PackageId = request.args.get('purchase_PackageId')

            purchaseVO.purchase_LoginId = purchase_LoginId
            purchaseVO.purchaseDate = purchaseDate
            purchaseVO.purchaseTime = purchaseTime
            purchaseVO.purchase_PackageId = purchase_PackageId

            purchaseDAO.insertPurchase(purchaseVO)

            return redirect(url_for('userViewPurchase'))

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/viewPurchase', methods=['get'])
def userViewPurchase():
    try:
        if adminLoginSession() == 'user':
            purchaseDAO = PurchaseDAO()
            purchaseVO = PurchaseVO()

            purchase_PackageId = request.args.get('purchase_PackageId')
            purchaseVO.purchase_PackageId = purchase_PackageId
            purchase_LoginId = session['session_loginId']
            purchaseVO.purchase_LoginId = purchase_LoginId

            purchaseVOList = purchaseDAO.viewPurchase_User()
            return render_template('user/viewPurchase.html', purchaseVOList=purchaseVOList)

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/viewPurchase', methods=['get'])
def adminViewPurchase():
    try:
        if adminLoginSession() == 'admin':
            purchaseDAO = PurchaseDAO()
            purchaseVO = PurchaseVO()
            loginVO = LoginVO()

            purchase_LoginId = session['session_loginId']
            purchaseVO.purchase_LoginId = purchase_LoginId

            purchaseVOList = purchaseDAO.viewPurchase_Admin()
            return render_template('admin/viewPurchase.html', purchaseVOList=purchaseVOList)

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)
