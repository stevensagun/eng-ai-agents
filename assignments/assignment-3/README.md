# Detections

The detection sample frames can be found here: https://huggingface.co/datasets/Sutiibun/DS681-Assignment3-Detections

# Dataset

The dataset used is the [Seraphom Drone Detection Dataset](https://huggingface.co/datasets/lgrzybowski/seraphim-drone-detection-dataset). This dataset consists of 83,483 images with a train-test split of 75,134 and 8,349, respectively, and is sourced from 23 different datasets. These images contain only one class (drone) and in various sizes, environments, and viewing angles.

# Detector

The detector used is [Ultralytics YOLOv8](https://docs.ultralytics.com/models/yolov8/). The default parameters were used with Ultralytics Trainer for 5 epochs. The detector ran at 5 fps, providing the "true" center x and y measurements. Between those measurements, the Kalman filter predicted the x and y positions. The filter also predicted the position of the drone when the detector failed to detect it.

# Kalman Filter

The input is assumed to be 30 fps. The size of the state vector (dim_x) of the Kalman filter is set to 6. Each dimension represents the x and y positions, the x and y velocities, and x and y accelerations, respectively. Dim_z is size 2 since the x and y coordinates are all that we would be able to provide via the detector. The model assumes constant acceleration to handle the fast speed-ups and slow-downs of the drone better. The transition matrix describes the kinematic equations for motion with constant acceleration for the x and y dimensions. The variance for the measurement noise is set to 5 so some measurement noise is allowed. For the process noise, the variance is set to 250 as drones are known to rapidly change acceleration.

# Failure cases

Setting the confidence threshold was tricky. Too low of a threshold and it would detect the birds and bugs flying across the screen. If it was too high, it would not detect the drone enough to update the Kalman filter. In both cases, it would cause the tracking to veer way off course.

# Output Tracking Videos

Click on the thumbnails below to open a new tab to the video. The red box indicate the detector detecting the drone at the frame. The green polyline is the predicted trajectory of the drone.

## Test Video 1

[![Watch the video](https://img.youtube.com/vi/UvT-JMjIfAE/0.jpg)](https://www.youtube.com/watch?v=UvT-JMjIfAE)

## Test Video 2

[![Watch the video](https://img.youtube.com/vi/abYBFoeQmb0/0.jpg)](https://www.youtube.com/watch?v=abYBFoeQmb0)
