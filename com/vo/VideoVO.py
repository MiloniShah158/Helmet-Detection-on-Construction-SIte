from project import db
from project.com.vo.RegisterVO import RegisterVO


class VideoVO(db.Model):
    __tablename__ = 'videomaster'
    videoId = db.Column('videoId', db.Integer, primary_key=True, autoincrement=True)
    videoInputFileName = db.Column('videoInputFileName', db.String(100), nullable=False)
    videoInputFilePath = db.Column('videoInputFilePath', db.String(100), nullable=False)
    videoOutputFileName = db.Column('videoOutputFileName', db.String(100), nullable=False)
    videoOutputFilePath = db.Column('videoOutputFilePath', db.String(100), nullable=False)
    videoUploadDate = db.Column('videoUploadDate', db.String(100), nullable=False)
    videoUploadTime = db.Column('videoUploadTime', db.String(100), nullable=False)
    video_RegisterId = db.Column('video_RegisterId', db.ForeignKey(RegisterVO.registerId))

    def as_dict(self):
        return {
            'videoId': self.videoId,
            'videoInputFileName': self.videoInputFileName,
            'videoInputFilePath': self.videoInputFilePath,
            'videoOutputFileName': self.videoOutputFileName,
            'videoOutputFilePath': self.videoOutputFilePath,
            'videoUploadDate': self.videoUploadDate,
            'videoUploadTime': self.videoUploadTime,
            'video_RegisterId': self.video_RegisterId
        }


db.create_all()
