import cv2
import pandas as pd

class Video:
    def __init__(self, path, model):
        self.path = path
        self.model = model
        self.cap = cv2.VideoCapture(path)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.duration = self.frame_count / self.fps
        self.data = []

    def index_frames(self):
        second = 0
        while second < self.duration:
            self.cap.set(cv2.CAP_PROP_POS_MSEC, second * 1000)
            ret, frame = self.cap.read()
            if not ret:
                break
            cv2.imwrite("frame.jpg", frame)
            
            result = self.model.predict("frame.jpg")
            cls = result.boxes.cls.tolist()
            for indx, c in enumerate(cls):
                self.data.append({
                    "video_id": self.path,
                    "timestamp": second,
                    "class_label": c,
                    "bounding_box": result.boxes.xyxy[indx].tolist(),
                    "confidence": result.boxes.conf[indx].item()
                })
            second += 1

        self.cap.release()

        df = pd.DataFrame(self.data)
        df.to_parquet("detection-results.parquet", engine="pyarrow", index=False)
       