import json
import random
import smtplib
import warnings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model

from object_tracking.application_util import generate_detections as gdet
from object_tracking.deep_sort import nn_matching
from object_tracking.deep_sort.detection import Detection
from object_tracking.deep_sort.tracker import Tracker
from utils.bbox import draw_box_with_id
from utils.utils import get_yolo_boxes

warnings.filterwarnings("ignore")

config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True

tf.compat.v1.keras.backend.set_session(tf.compat.v1.Session(config=config))


def main():
    try:
        mailCounter = 0

        receiverEmail = "dhairyapatel335@gmail.com"
        print("---------------------------------", receiverEmail)

        videoInputFileName = "7_new.avi"
        print(videoInputFileName)

        videoInputFilePath = "inputVideo/"
        print(videoInputFilePath)

        random_number = random.randint(0, 1000)

        if videoInputFileName.split(".")[1] == "avi":
            videoOutputFileName = videoInputFileName.replace(".avi", "") + str(random_number) + ".avi"

        videoOutputFilePath = r"outputVideo/"

        config_path = "modelDump/config.json"
        W = None
        H = None
        writer = None

        with open(config_path) as config_buffer:
            config = json.load(config_buffer)
            print(config)

        net_h, net_w = 416, 416
        obj_thresh, nms_thresh = 0.5, 0.45

        # os.environ['CUDA_VISIBLE_DEVICES'] = config['train']['gpus']
        infer_model = load_model(config['train']['saved_weights_name'])
        print(infer_model)
        max_cosine_distance = 0.3
        nn_budget = None

        model_filename = 'modelDump/mars-small128.pb'
        print(model_filename)
        encoder = gdet.create_box_encoder(model_filename, batch_size=1)

        trackers = []
        metric = nn_matching.NearestNeighborDistanceMetric("cosine", max_cosine_distance, nn_budget)
        tracker = Tracker(metric)
        trackers.append(tracker)

        inputVideo = videoInputFilePath + videoInputFileName
        video_reader = cv2.VideoCapture(inputVideo)

        images = []
        while True:
            ret_val, image = video_reader.read()
            length = int(video_reader.get(cv2.CAP_PROP_FRAME_COUNT))
            print("length of frames>>>>>>>>>", length)
            if ret_val:
                print("in if ret_val>>>>", ret_val)

                images += [image]
                if W is None or H is None:
                    (H, W) = image.shape[:2]

                batch_boxes = get_yolo_boxes(infer_model, images, net_h, net_w, config['model']['anchors'], obj_thresh,
                                             nms_thresh)

                for i in range(len(images)):
                    boxs = [[box1.xmin, box1.ymin, box1.xmax - box1.xmin, box1.ymax - box1.ymin] for box1 in
                            batch_boxes[i]]
                    features = encoder(images[i], boxs)

                    detections = []
                    for j in range(len(boxs)):
                        label = batch_boxes[i][j].label
                        detections.append(Detection(boxs[j], batch_boxes[i][j].c, features[j], label))

                    trackers[i].predict()
                    trackers[i].update(detections)

                    n_without_helmet = 0
                    n_with_helmet = 0

                    for track in trackers[i].tracks:
                        if not track.is_confirmed() or track.time_since_update > 1:
                            continue
                        if track.label == 2:
                            n_without_helmet += 1
                            if mailCounter < 3:
                                print("----------------------------------------")

                                sender = "helmetconst@gmail.com"

                                receiver = receiverEmail

                                msg = MIMEMultipart()

                                msg['From'] = sender

                                msg['To'] = receiver

                                msg['subject'] = "Worker Helmet Detection"

                                msg.attach(
                                    MIMEText(
                                        'AI Based Safety Norms System has detected ' + str(
                                            n_without_helmet) + " None Helmet Workers !"))

                                server = smtplib.SMTP('smtp.gmail.com', 587)

                                server.starttls()

                                server.login(sender, "dkppwd1998@")

                                text = msg.as_string()
                                print("---------------------------------------------", receiver)
                                server.sendmail(sender, receiver, text)

                                server.quit()

                                mailCounter = mailCounter + 1

                        if track.label == 1:
                            n_with_helmet += 1

                        bbox = track.to_tlbr()
                        print(track.track_id, "+", track.label)
                        draw_box_with_id(images[i], bbox, track.track_id, track.label, config['model']['labels'])

                    print("CAM " + str(i))
                    print("Persons without helmet = " + str(n_without_helmet))
                    print("Persons with helmet = " + str(n_with_helmet))

                    if writer is None:
                        fourcc = cv2.VideoWriter_fourcc(*"VP80")
                        writer = cv2.VideoWriter(videoOutputFilePath + videoOutputFileName, fourcc, 30, (W, H), True)

                    writer.write(images[i])

                images = []
                if cv2.waitKey(0) & 0xFF == ord('q'):
                    break
            else:
                print("in else")
                writer.release()
                video_reader.release()
                cv2.destroyAllWindows()
                break

    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    main()
