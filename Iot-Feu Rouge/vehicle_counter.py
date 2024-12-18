import cv2
import numpy as np
import time
import requests

# Paths to your pre-downloaded videos
video_path_way1 = 'C:\\Users\\HP\\Desktop\\Volvo\\cars.mp4'
video_path_way2 = 'C:\\Users\\HP\\Desktop\\Volvo\\cars.mp4'

# Pre-trained COCO model for object detection (you may need to install necessary libraries)
model_config = 'yolov3.cfg'
model_weights = 'yolov3.weights'
# Replace with the actual IP of your ESP8266
esp8266_ip = "http://128.10.1.133/"
# confidence threshold
CONF_THRESHOLD = 0.4
# number of frames before re-evaluation
FRAMES_BEFORE_EVALUATION = 30
  

# Load YOLO model
net = cv2.dnn.readNetFromDarknet(model_config, model_weights)
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
classes = []
with open('coco.names', 'r') as f:
    classes = [line.strip() for line in f.readlines()]

# Function to detect objects
def detect_objects(frame):
    height, width, channels = frame.shape
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > CONF_THRESHOLD:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, CONF_THRESHOLD, 0.4)
    detected_objects = []
    for i in range(len(boxes)):
        if i in indexes:
            detected_objects.append((boxes[i], class_ids[i]))
    return detected_objects

# Function to count vehicles
def count_vehicles(frame, way_region):
    detected_objects = detect_objects(frame)
    way_count = 0
    for box , class_id in detected_objects:
        x, y, w, h = box
        center_x = x + w // 2
        center_y = y + h // 2

        if class_id == 2 or class_id == 7 or class_id == 1 or class_id == 3 :
            if cv2.pointPolygonTest(way_region, (center_x, center_y), False) >= 0:
                way_count += 1

    return way_count

# Function to send data to ESP8266
def send_traffic_info(direction, duration, total_vehicles, way1_vehicles, way2_vehicles):
    try:
        url = f"{esp8266_ip}/setTraffic"
        params = {'direction': direction, 'duration': duration, 'total_vehicles': total_vehicles, 'way1_vehicles': way1_vehicles, 'way2_vehicles': way2_vehicles}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            print("Traffic info sent successfully.")
        else:
            print(f"Failed to send traffic info. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def main():
    cap_way1 = cv2.VideoCapture(video_path_way1)
    cap_way2 = cv2.VideoCapture(video_path_way2)

    if not cap_way1.isOpened():
        print("Error: Could not open video for way 1.")
        return
    if not cap_way2.isOpened():
        print("Error: Could not open video for way 2.")
        return

    # Define region of interest (ROI) polygons for each traffic direction
    # These coordinates need to be determined based on your video
    way_1_region = np.array([
      [400, 200], [900, 200], [900, 650], [400, 650] # Example
    ], np.int32)
    way_2_region = np.array([
         [400, 200], [900, 200], [900, 650], [400, 650] # Example
    ], np.int32)

    frame_count = 0
    while True:
        ret1, frame1 = cap_way1.read()
        ret2, frame2 = cap_way2.read()

        if not ret1 or not ret2:
            break

        if frame_count % FRAMES_BEFORE_EVALUATION == 0:
            way1_count = count_vehicles(frame1, way_1_region)
            way2_count = count_vehicles(frame2, way_2_region)
            total_vehicles = way1_count + way2_count
            if way1_count > way2_count:
                print("Way 1 has more traffic")
                send_traffic_info('way1', 10, total_vehicles, way1_count, way2_count) #duration in seconds
            elif way2_count > way1_count :
                print("Way 2 has more traffic")
                send_traffic_info('way2', 10, total_vehicles, way1_count, way2_count) #duration in seconds
            else :
                 send_traffic_info('default', 6, total_vehicles, way1_count, way2_count) #duration in seconds
            frame_count = 1
        frame_count +=1

        # Display the frames (optional)
        cv2.polylines(frame1, [way_1_region], isClosed=True, color=(0, 255, 0), thickness=2)
        cv2.polylines(frame2, [way_2_region], isClosed=True, color=(0, 0, 255), thickness=2)
        cv2.imshow("Traffic Analysis way 1", frame1)
        cv2.imshow("Traffic Analysis way 2", frame2)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap_way1.release()
    cap_way2.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()