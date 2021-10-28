from project import db
from project.com.vo.FeedbackVO import FeedbackVO
from project.com.vo.LoginVO import LoginVO


class FeedbackDAO:
    def insertFeedback(self, feedbackVO):
        db.session.add(feedbackVO)
        db.session.commit()

    def viewFeedback_Admin(self):
        feedbackList = db.session.query(FeedbackVO, LoginVO) \
            .join(LoginVO, FeedbackVO.feedbackFrom_LoginId == LoginVO.loginId).all()

        return feedbackList

    def reviewFeedback_Admin(self, feedbackVO):
        db.session.merge(feedbackVO)
        db.session.commit()

    def viewFeedback_User(self):
        feedbackList = db.session.query(FeedbackVO, LoginVO) \
            .join(LoginVO, FeedbackVO.feedbackFrom_LoginId == LoginVO.loginId)
        return feedbackList

    def deleteFeedback(self, feedbackVO):
        feedbackList = FeedbackVO.query.get(feedbackVO.feedbackId)

        db.session.delete(feedbackList)
        db.session.commit()

        return feedbackList
