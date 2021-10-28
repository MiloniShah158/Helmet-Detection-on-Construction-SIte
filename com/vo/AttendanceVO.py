from project import db
from project.com.vo.RegisterVO import RegisterVO


class AttendanceVO(db.Model):
    __tablename__ = 'attendancemaster'
    attendanceId = db.Column('attendanceId', db.Integer, primary_key=True, autoincrement=True)
    attendanceFileName = db.Column('attendanceFileName', db.String(100), nullable=False)
    attendanceFilePath = db.Column('attendanceFilePath', db.String(100), nullable=False)
    attendanceDate = db.Column('attendanceDate', db.String(100), nullable=False)
    attendanceTime = db.Column('attendanceTime', db.String(100), nullable=False)
    attendance_RegisterId = db.Column('attendance_RegisterId', db.ForeignKey(RegisterVO.registerId))

    def as_dict(self):
        return {
            'attendanceId': self.attendanceId,
            'attendanceFileName': self.attendanceFileName,
            'attendanceFilePath': self.attendanceFilePath,
            'attendanceDate': self.attendanceDate,
            'attendanceTime': self.attendanceTime,
            'attendance_RegisterId': self.attendance_RegisterId,
        }


db.create_all()
