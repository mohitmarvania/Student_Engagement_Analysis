import os
from datetime import datetime
from ultralytics import YOLO
import cv2
from pathlib import Path

screenshot_folder_path = "./screenshots"
emotions = ["frustrated", "engaged", "sleepy", "bored", "confused", "yawning"]
engaged = 0
frustrated = 0
sleepy = 0
bored = 0
confused = 0
yawning = 0


def model_predict(output_folder_path, ss_saved_folder_path):
    global predicted_emotion
    model = YOLO("yolov8_best.pt")
    image_folder = Path(ss_saved_folder_path)
    for image_path in image_folder.glob("*.png") or image_folder.glob("*.jpg"):
        image = cv2.imread(str(image_path))
        filename = image_path.stem
        print("filename : ", filename)
        # Use YOLOv8 for face detection
        results = model(source=image)
        names = model.names

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.8
        font_thickness = 2

        # Loop to print the predicted emotion
        for r in results:
            for c in r.boxes.cls:
                predicted_emotion = names[int(c)]

                if predicted_emotion.lower() in emotions:
                    globals()[predicted_emotion.lower()] += 1

        for r in results:
            boxes = r.boxes.cpu().numpy()
            xyxys = boxes.xyxy

            for xyxy in xyxys:
                cv2.rectangle(image, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), (0, 255, 0),
                              font_thickness)
                text = f"{predicted_emotion}"
                cv2.putText(image, text, (int(xyxy[0]), int(xyxy[1]) - 5), font, font_scale, (255, 0, 255),
                            font_thickness)
                output_path = output_folder_path + f"{filename}.jpg"
                cv2.imwrite(output_path, image)

    # Loop to print the value of each emotions
    # for emotion in emotions:
    #     print(f"{emotion}: {globals()[emotion.lower()]}")

    return engaged, frustrated, sleepy, bored, confused, yawning
