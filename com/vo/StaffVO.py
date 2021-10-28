from project import db
from project.com.vo.LoginVO import LoginVO


class StaffVO(db.Model):
    __tablename__ = 'staffmaster'
    staffId = db.Column('staffId', db.Integer, primary_key=True, autoincrement=True)
    staffFirstname = db.Column('staffFirstname', db.String(100), nullable=False)
    staffLastname = db.Column('staffLastname', db.String(100), nullable=False)
    staffGender = db.Column('staffGender', db.String(100), nullable=False)
    staffContact = db.Column('staffContact', db.String(100), nullable=False)
    staffDOB = db.Column('staffDOB', db.String(100), nullable=False)
    staffJD = db.Column('staffJD', db.String(100), nullable=False)
    staffPhoto = db.Column('staffPhotos', db.String(100), nullable=False)
    staffPhotoPath = db.Column('staffPhotoPath', db.String(100), nullable=False)
    staff_LoginId = db.Column('staff_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))

    def as_dict(self):
        return {
            'staffId': self.staffId,
            'staffFirstname': self.staffFirstname,
            'staffLastname': self.staffLastname,
            'staffGender': self.staffGender,
            'staffContact': self.staffContact,
            'staffDOB': self.staffDOB,
            'staffJD': self.staffJD,
            'staffPhotos': self.staffPhoto,
            'staffPhotoPath': self.staffPhotoPath,
            'staff_LoginId': self.staff_LoginId

        }


db.create_all()
