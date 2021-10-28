from project import db
from project.com.vo.PackageVO import PackageVO
from project.com.vo.PurchaseVO import PurchaseVO
from project.com.vo.LoginVO import LoginVO


class PurchaseDAO:
    def insertPurchase(self, purchaseVO):
        db.session.add(purchaseVO)
        db.session.commit()

    def viewPurchase_User(self):
        purchaseList = db.session.query(PurchaseVO, PackageVO) \
            .join(PackageVO, PurchaseVO.purchase_PackageId == PackageVO.packageId).all()

        return purchaseList

    def viewPurchase_Admin(self):
        packageList = db.session.query(PurchaseVO, PackageVO, LoginVO) \
            .join(PackageVO, PurchaseVO.purchase_PackageId == PackageVO.packageId)\
            .join(LoginVO, PurchaseVO.purchase_LoginId == LoginVO.loginId).all()

        return packageList
