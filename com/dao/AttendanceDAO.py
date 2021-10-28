from project import db
from project.com.vo.AttendanceVO import AttendanceVO

class AttendanceDAO:
    def adminInsertAttendance(self, attendanceVO):
        db.session.add(attendanceVO)
        db.session.commit()

    def adminViewAttendance(self, attendanceVO):
        attendanceList = AttendanceVO.query.filter_by(attendance_RegisterId = attendanceVO.attendance_RegisterId)

        return attendanceList

    def deleteAttendance(self, attendanceVO):
        attendanceList = attendanceVO.query.get(attendanceVO.attendanceId)

        db.session.delete(attendanceList)
        db.session.commit()
        return attendanceList


