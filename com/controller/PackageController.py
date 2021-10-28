from flask import render_template, request, url_for, redirect

from project import app
from project.com.controller.LoginController import adminLogoutSession, adminLoginSession
from project.com.dao.PackageDAO import PackageDAO
from project.com.vo.PackageVO import PackageVO


@app.route('/admin/loadPackage')
def adminloadPackage():
    if adminLoginSession() == 'admin':
        return render_template('admin/addPackage.html')

    else:
        return adminLogoutSession()


@app.route('/admin/insertPackage', methods=['post'])
def admininsertPackage():
    try:
        if adminLoginSession() == 'admin':
            packageName = request.form['packageName']
            packageDuration = request.form['packageDuration']
            packagePrice = request.form['packagePrice']

            packageVO = PackageVO()
            packageDAO = PackageDAO()

            packageVO.packageName = packageName
            packageVO.packageDuration = packageDuration
            packageVO.packagePrice = packagePrice

            packageDAO.insertPackage(packageVO)

            return redirect(url_for('adminViewPackage'))

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/viewPackage', methods=['GET'])
def adminViewPackage():
    try:
        if adminLoginSession() == 'admin':
            packageDAO = PackageDAO()
            packageVOList = packageDAO.viewPackage()
            print("______________", packageVOList)

            return render_template('admin/viewPackage.html', packageVOList=packageVOList)

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/deletePackage', methods=['GET'])
def adminDeletePackage():
    try:
        if adminLoginSession() == 'admin':
            packageVO = PackageVO()
            packageDAO = PackageDAO()

            packageId = request.args.get('packageId')

            print('packageId::', packageId)

            packageVO.packageId = packageId

            packageDAO.deletePackage(packageVO)

            return redirect(url_for('adminViewPackage'))

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/editPackage', methods=['GET'])
def adminEditPackage():
    try:
        if adminLoginSession() == 'admin':
            packageVO = PackageVO()

            packageDAO = PackageDAO()

            packageId = request.args.get('packageId')

            print('packageId::', packageId)

            packageVO.packageId = packageId

            packageVOList = packageDAO.editPackage(packageVO)

            print("=======packageVOList=======", packageVOList)

            print("=======type of packageVOList=======", type(packageVOList))

            return render_template('admin/editPackage.html', packageVOList=packageVOList)

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/updatePackage', methods=['POST'])
def adminUpdatePackage():
    try:
        if adminLoginSession() == 'admin':
            packageId = request.form['packageId']
            packageName = request.form['packageName']
            packageDuration = request.form['packageDuration']
            packagePrice = request.form['packagePrice']

            packageVO = PackageVO()
            packageDAO = PackageDAO()

            packageVO.packageId = packageId
            packageVO.packageName = packageName
            packageVO.packageDuration = packageDuration
            packageVO.packagePrice = packagePrice

            packageDAO.updatePackage(packageVO)

            return redirect(url_for('adminViewPackage'))

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)
