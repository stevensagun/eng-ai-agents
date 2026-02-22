from ultralytics import YOLO

class Model():
    def __init__(self, weights_path="yolo12m.pt"):
        self.model = YOLO(weights_path)
    
    def train(self, epochs=100):
        self.epochs = epochs
        self.model.train(data="carparts-seg.yaml", epochs=epochs, imgsz=640, cache=True, dropout=0.1, fliplr=0.0)
        self.model.save(f"model_weights_{epochs}.pt")

    def evaluate(self):
        results = self.model.val(data="carparts-seg.yaml")
        return results

    def predict(self, image):
        results = self.model([image])
        return results[0]