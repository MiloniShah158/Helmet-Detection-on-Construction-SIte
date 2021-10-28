from project import db
from project.com.vo.StaffVO import StaffVO


class StaffDAO:
    def insertStaff(self, staffVO):
        db.session.add(staffVO)
        db.session.commit()

    def viewStaff(self, staffVO):
        staffList = StaffVO.query.filter_by(staff_LoginId=staffVO.staff_LoginId)

        return staffList

    def deleteStaff(self, staffVO):
        staffList = StaffVO.query.get(staffVO.staffId)

        db.session.delete(staffList)
        db.session.commit()
        return staffList
