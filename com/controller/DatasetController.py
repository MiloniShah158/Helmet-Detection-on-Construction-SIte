import os
from datetime import datetime

from flask import render_template, request, url_for, redirect
from werkzeug.utils import secure_filename

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.DatasetDAO import DatasetDAO
from project.com.vo.DatasetVO import DatasetVO

UPLOAD_FOLDER = 'project/static/adminResources/dataset/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/admin/loadDataset')
def adminLoadDataset():
    try:
        if adminLoginSession() == 'admin':
            return render_template('admin/addDataset.html')

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/insertDataset', methods=['post'])
def adminInsertDataset():
    try:
        if adminLoginSession() == 'admin':
            datasetVO = DatasetVO()
            datasetDAO = DatasetDAO()

            file = request.files['file']
            print(file)

            datasetFileName = secure_filename(file.filename)
            print(datasetFileName)

            datasetFilePath = os.path.join(app.config['UPLOAD_FOLDER'])
            print(datasetFilePath)

            file.save(os.path.join(datasetFilePath, datasetFileName))

            datasetUploadDate = datetime.date(datetime.now())
            datasetUploadTime = datetime.time(datetime.now())

            datasetVO.datasetFileName = datasetFileName
            datasetVO.datasetFilePath = datasetFilePath.replace("project", "..")

            datasetVO.datasetUploadDate = datasetUploadDate
            datasetVO.datasetUploadTime = datasetUploadTime

            datasetDAO.insertDataset(datasetVO)

            return redirect(url_for('adminViewDataset'))

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/viewDataset', methods=['GET'])
def adminViewDataset():
    try:
        if adminLoginSession() == 'admin':
            datasetDAO = DatasetDAO()
            datasetVOList = datasetDAO.viewDataset()
            print("______________", datasetVOList)

            return render_template('admin/viewDataset.html', datasetVOList=datasetVOList)

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/deleteDataset', methods=['GET'])
def adminDeleteDataset():
    try:
        if adminLoginSession() == 'admin':
            datasetVO = DatasetVO()

            datasetDAO = DatasetDAO()

            datasetId = request.args.get('datasetId')

            print('datasetId::', datasetId)

            datasetVO.datasetId = datasetId

            datasetDAO.deleteDataset(datasetVO)

            return redirect(url_for('adminViewDataset'))

        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
