# YOLOv8s Object Detection with TensorFlow Lite and GStreamer

This repository contains a GStreamer pipeline implementation for performing object detection using the YOLOv8s (float32) model with TensorFlow Lite. The pipeline utilizes the nnstreamer plugin for seamless integration and efficient inference.

## Requirements

- GStreamer (>= 1.18)
- nnstreamer (>= 1.1.0)

## Installation

1. **GStreamer**: Follow the installation instructions provided by the GStreamer website: [GStreamer Installation Guide](https://gstreamer.freedesktop.org/documentation/installing/index.html)

2. **Install YoloV8**:
   
   **Install YoloV8**:

    ```bash
    $ pip install ultralytics
    ```

    **Export to tflite model**

   '''bash
   from ultralytics import YOLO

   # Load a model
   model = YOLO("yolov8s.pt") # load a pretrained model

   # Export the model
   model.export(format="tflite", imgsz=320) # export the model to tflite format
   '''

5. **nnstreamer**: Follow the installation instructions provided by the nnstreamer GitHub repository: [nnstreamer Installation Guide](https://github.com/nnstreamer/nnstreamer)

## Usage

1. Clone this repository:

    ```bash
    git clone https://github.com/your_username/your_repo.git
    ```

2. Run the GStreamer pipeline:

    ```bash
    ./nnstreamer_yolov8_pipeline.py
    ```

## Acknowledgements

This project is based on the following libraries and frameworks:

- GStreamer: [https://gstreamer.freedesktop.org/](https://gstreamer.freedesktop.org/)
- nnstreamer: [https://github.com/nnstreamer/nnstreamer](https://github.com/nnstreamer/nnstreamer)
