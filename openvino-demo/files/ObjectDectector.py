from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2

class ObjectDectector:
	def __init__(self):
		# 初始化标签列表 MobileNet SSD was trained to
		# detect, then generate a set of bounding box colors for each class
		CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
			"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
			"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
			"sofa", "train", "tvmonitor"]
		COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

		# 从磁盘上加载模型
		print("[INFO] loading model...")
		net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt", "MobileNetSSD_deploy.caffemodel")

		# 指定棒子 Myriad NCS 作为处理设备
		net.setPreferableTarget(cv2.dnn.DNN_TARGET_MYRIAD)

		# 初始化摄像头，并等待设备启动
		print("[INFO] starting video stream...")
		vs = VideoStream(usePiCamera=True).start()
		time.sleep(2.0)

    def detect(self):
       
		# 从视频流中抓帧, 最大设置为400像素
		frame = vs.read()
		frame = imutils.resize(frame, width=400)

		# 打包为blob数据格式
		(h, w) = frame.shape[:2]
		blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)

		# 通过网络发送到棒子进行识别
		net.setInput(blob)
		detections = net.forward()

		# 识别结果处理
		for i in np.arange(0, detections.shape[2]):
			# 可信度
			confidence = detections[0, 0, i, 2]

 			# 检测框
			idx = int(detections[0, 0, i, 1])
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			# 绘制检测框
			label = "{}: {:.2f}%".format(CLASSES[idx],
				confidence * 100)
			cv2.rectangle(frame, (startX, startY), (endX, endY),
				COLORS[idx], 2)
			y = startY - 15 if startY - 15 > 15 else startY + 15
			cv2.putText(frame, label, (startX, y),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

		# 输出全屏视频
		out_win = "FullScreen"
		cv2.namedWindow(out_win, cv2.WINDOW_NORMAL)
		cv2.setWindowProperty(out_win, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
		cv2.imshow(out_win, frame)

		key = cv2.waitKey(1) & 0xFF

		return detections

	def clean(self):
		# 关闭设备
		cv2.destroyAllWindows()
		vs.stop()
