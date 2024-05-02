#!/usr/bin/env python3

import os
import sys
import gi
import logging

gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

DEBUG = False

class NNStreamerExample:
    """NNStreamer example for Object Detection."""

    def __init__(self, argv=None):
        self.loop = None
        self.pipeline = None

        self.tflite_model = ''
        self.tflite_label = ''

        if not self.tflite_init():
            raise Exception

        GObject.threads_init()
        Gst.init(argv)

    def run_example(self):
        """Init pipeline and run example.
        :return: None
        """

        print("Run: NNStreamer example for object detection.")

        # main loop
        self.loop = GObject.MainLoop()

        # init pipeline
        self.pipeline = Gst.parse_launch(
            'v4l2src device=/dev/video1 ! videoconvert ! videoscale ! '
            'video/x-raw,width=640,height=480,format=RGB,pixel-aspect-ration=1/1,framerate=30/1 ! '
            'tee name=t_raw t_raw. ! queue leaky=2 max-size-buffers=2 ! videoscale ! '
                'video/x-raw,width=320,height=320,format=RGB ! '
                'tensor_converter ! '
                'tensor_transform mode=arithmetic option=typecast:float32,div:255.0 ! '
                'tensor_filter framework=tensorflow2-lite model=' + self.tflite_model + ' ! '
                'tensor_transform mode=transpose option=1:0:2:3 ! '
                'tensor_decoder mode=bounding_boxes option1=yolov8 option2=' + self.tflite_label + ' option3=0 option4=640:480 option5=320:320 ! '
                'video/x-raw,widht=640,height=480,format=RGBA ! mix.sink_0 '
            't_raw. ! queue leaky=2 max-size-buffers=10 ! mix.sink_1 '
            'compositor name=mix sink_0::zorder=2 sink_1::zorder=1 ! '
            'videoconvert ! autovideosink sync=false '
        )

        # bus and message callback
        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect('message', self.on_bus_message)

        # start pipeline
        self.pipeline.set_state(Gst.State.PLAYING)

        # run main loop
        self.loop.run()

        # quit when received eos or error message
        self.pipeline.set_state(Gst.State.NULL)

        bus.remove_signal_watch()

    def tflite_init(self):
        """
        :return: True if successfully initialized
        """
        tflite_model = 'yolov8s_float32.tflite'
        tflite_label = 'coco_labels_list.txt'

        current_folder = os.path.dirname(os.path.abspath(__file__))
        model_folder = os.path.join(current_folder, 'yolov8')

        self.tflite_model = os.path.join(model_folder, tflite_model)
        if not os.path.exists(self.tflite_model):
            logging.error('cannot find tflite model [%s]', self.tflite_model)
            return False

        self.tflite_label = os.path.join(model_folder, tflite_label)
        if not os.path.exists(self.tflite_label):
            logging.error('cannot find tflite label [%s]', self.tflite_label)
            return False

        return True

    def on_bus_message(self, bus, message):
        """
        :param bus: pipeline bus
        :param message: message from pipeline
        :return: None
        """
        if message.type == Gst.MessageType.EOS:
            logging.info('received eos message')
            self.loop.quit()
        elif message.type == Gst.MessageType.ERROR:
            error, debug = message.parse_error()
            logging.warning('[error] %s : %s', error.message, debug)
            self.loop.quit()
        elif message.type == Gst.MessageType.WARNING:
            error, debug = message.parse_warning()
            logging.warning('[warning] %s : %s', error.message, debug)
        elif message.type == Gst.MessageType.STREAM_START:
            logging.info('received start message')
        elif message.type == Gst.MessageType.QOS:
            data_format, processed, dropped = message.parse_qos_stats()
            format_str = Gst.Format.get_name(data_format)
            logging.debug('[qos] format[%s] processed[%d] dropped[%d]', format_str, processed, dropped)


if __name__ == '__main__':
    example = NNStreamerExample(sys.argv[1:])
    example.run_example()

