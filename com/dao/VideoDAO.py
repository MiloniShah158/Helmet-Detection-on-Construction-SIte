from project import db
from project.com.vo.RegisterVO import RegisterVO
from project.com.vo.VideoVO import VideoVO


class VideoDAO:
    def adminInsertVideo(self, videoVO):
        db.session.add(videoVO)
        db.session.commit()

    def userInsertVideo(self, videoVO):
        db.session.add(videoVO)
        db.session.commit()

    def adminViewRegister(self):
        videoList = db.session.query(VideoVO, RegisterVO) \
        .join(RegisterVO, VideoVO.video_RegisterId == RegisterVO.registerId).all()

        return videoList

    def userViewVideo(self, videoVO):
        videoList = VideoVO.query.filter_by(video_LoginId=videoVO.video_LoginId)

        return videoList

    def deleteVideo(self, videoVO):
        videoList = VideoVO.query.get(videoVO.videoId)

        db.session.delete(videoList)
        db.session.commit()
        return videoList
