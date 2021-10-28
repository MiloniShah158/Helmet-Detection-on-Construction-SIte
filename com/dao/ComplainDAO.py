from project import db
from project.com.vo.ComplainVO import ComplainVO
from project.com.vo.LoginVO import LoginVO


class ComplainDAO:
    def insertComplain(self, complainVO):
        db.session.add(complainVO)
        db.session.commit()

    def insertComplainReply_Admin(self, complainVO):
        db.session.merge(complainVO)
        db.session.commit()

    def viewComplain_Admin(self, complainVO):
        complainList = db.session.query(ComplainVO, LoginVO) \
            .join(LoginVO, ComplainVO.complainFrom_LoginId == LoginVO.loginId) \
            .filter(ComplainVO.complainStatus == complainVO.complainStatus).all()

        return complainList

    def viewComplain_User(self, complainVO):
        complainList = ComplainVO.query.filter_by(complainFrom_LoginId=complainVO.complainFrom_LoginId).all()

        return complainList

    def viewComplainReply_User(self, complainVO):
        complainList = ComplainVO.query.filter_by(complainId=complainVO.complainId).all()

        return complainList

    def deleteComplain(self, complainVO):
        complainList = ComplainVO.query.get(complainVO.complainId)

        db.session.delete(complainList)
        db.session.commit()

        return complainList
