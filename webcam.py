import cv2
from deepface import DeepFace
import csv
from datetime import datetime
import os

# Open the default webcam
webcam = cv2.VideoCapture(0)

# Define the desired frame size
width = 640
height = 480

# Setup CSV file
csv_file = 'recognition_log.csv'
write_header = not os.path.exists(csv_file)

with open(csv_file, 'w', newline='') as f:
    writer = csv.writer(f)
    if write_header:
        writer.writerow(['Name', 'Time'])

    while webcam.isOpened():
        ret, frame = webcam.read()

        if not ret:
            print("Failed to grab frame")
            break

        resized_frame = cv2.resize(frame, (width, height))
        cv2.imshow("Resized Webcam", resized_frame)

        
        results = DeepFace.find(
                    img_path=resized_frame,
                    db_path='faces',
                    enforce_detection=False,
                    model_name='Facenet',  # Or any other model
                    detector_backend='opencv'
                )

        if len(results) > 0 and not results[0].empty:
                    for _, row in results[0].iterrows():
                        identity = os.path.basename(row['identity'])  # Extract file name
                        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        writer.writerow([identity, timestamp])
                        print(f"Logged: {identity} at {timestamp}")
        

        if cv2.waitKey(1000) & 0xFF == ord('q'):
            break

webcam.release()
cv2.destroyAllWindows()

cv2.destroyAllWindows()
