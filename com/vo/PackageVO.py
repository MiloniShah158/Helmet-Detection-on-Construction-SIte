from project import db


class PackageVO(db.Model):
    __tablename__ = 'packagemaster'
    packageId = db.Column('packageId', db.Integer, primary_key=True, autoincrement=True)
    packageName = db.Column('packageName', db.String(100))
    packageDuration = db.Column('packageDuration', db.String(100))
    packagePrice = db.Column('packagePrice', db.String(100))

    def as_dict(self):
        return {
            'packageId': self.packageId,
            'packageName': self.packageName,
            'packageDuration': self.packageDuration,
            'packagePrice': self.packagePrice

        }


db.create_all()
