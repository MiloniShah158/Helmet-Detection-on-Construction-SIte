from project import db
from project.com.vo.LoginVO import LoginVO


class RegisterVO(db.Model):
    __tablename__ = 'registermaster'
    registerId = db.Column('registerId', db.Integer, primary_key=True, autoincrement=True)
    companyName = db.Column('companyName', db.String(100), nullable=False)
    registerFirstname = db.Column('registerFirstname', db.String(100), nullable=False)
    registerLastname = db.Column('registerLastname', db.String(100), nullable=False)
    registerGender = db.Column('registerGender', db.CHAR(100), nullable=False)
    registerContact = db.Column('registerContact', db.CHAR(100), nullable=False)
    registerAddress = db.Column('registerAddress', db.String(100), nullable=False)
    register_LoginId = db.Column('register_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId), nullable=False)

    def as_dict(self):
        return {
            'registerId': self.registerId,
            'companyName': self.companyName,
            'registerFirstname': self.registerFirstname,
            'registerLastname': self.registerLastname,
            'registerGender': self.registerGender,
            'registerAddress': self.registerAddress,
            'registerContact': self.registerContact,
            'register_LoginId': self.register_LoginId
        }


db.create_all()
