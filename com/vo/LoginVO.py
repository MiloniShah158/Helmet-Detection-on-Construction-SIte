from project import db


class LoginVO(db.Model):
    __tablename__ = 'loginmaster'
    loginId = db.Column('loginId', db.Integer, primary_key=True, autoincrement=True)
    loginUsername = db.Column('loginUsername', db.String(100), nullable=False)
    loginPassword = db.Column('loginPassword', db.String(100), nullable=False)
    loginRole = db.Column('loginRole', db.String(100), nullable=False)
    loginStatus = db.Column('loginStatus', db.String(100), nullable=False)

    def as_dict(self):
        return {
            'loginId': self.loginId,
            'loginUsername': self.loginUsername,
            'loginPassword': self.loginPassword,
            'loginRole': self.loginRole,
            'loginStatus': self.loginStatus
        }


db.create_all()
