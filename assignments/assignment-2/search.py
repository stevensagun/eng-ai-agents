import pandas as pd
from classes import CLASSES
import pyarrow as pa

class Search():
    def __init__(self, model):
        self.df = pd.read_parquet("hf://datasets/Sutiibun/DS681-Assignment2-Detections/detection-results.parquet")
        self.model = model
        self.youtube_template = 'https://www.youtube.com/embed/YcvECxtXoxQ?start={}&end={}'
        self.player_template = 'https://stevensagun.github.io/yt-embed/?videoId=YcvECxtXoxQ&start={}&end={}'

        classes = range(23)
        timestamp_dict = { i: [] for i in classes }
        self.clip_dict = { i: [] for i in classes }  

        for c in classes:
            timestamp_dict[c] = sorted(self.df[self.df['class_label'] == c]['timestamp'])

        for c, timestamps in timestamp_dict.items():
            grouped_timestamps = self._group_consecutive_timestamps(timestamps)
            for group in grouped_timestamps:
                start = group[0]
                end = group[-1] + 1
                self.clip_dict[c].append({
                    "player_embed": self.player_template.format(start, end),
                    "youtube_embed": self.youtube_template.format(start, end)
                })

    def search(self, image):
        result = self.model.predict(image)
        cls = set(result.boxes.cls.tolist())
        df = []
        for c in cls:
            for clip in self.clip_dict[c]:
                df.append({
                    "class_label": c,
                    'class_name': CLASSES[c],
                    "yt_embed": clip['youtube_embed'],
                    "player_embed": clip['player_embed']
                })
        df = pd.DataFrame(df)
        return (result, df)
        
    def _group_consecutive_timestamps(self, timestamps):
        if not timestamps:
            return []
        
        grouped = []
        current_group = [timestamps[0]]
        
        for i in range(1, len(timestamps)):
            if timestamps[i] - timestamps[i-1] <= 1:
                current_group.append(timestamps[i])
            else:
                grouped.append(current_group)
                current_group = [timestamps[i]]
        
        grouped.append(current_group)
        return grouped