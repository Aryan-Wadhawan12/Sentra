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
csv_file = 'attendence_log.csv'
write_header = os.path.exists(csv_file)
marked_today = set()
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
                    db_path='schools',
                    enforce_detection=True,
                    model_name='ArcFace',  # Or any other model
                    detector_backend='retinaface'
                )
        

        if len(results) > 0 and not results[0].empty:
                    for _, row in results[0].iterrows():
                        if row['distance'] < 0.3:
                            best_match = results[0].iloc[0]
                            identity = os.path.basename(os.path.dirname(row['identity']))  # Extract file name
                           
                            try:
                                    result = DeepFace.analyze(frame, detector_backend='retinaface', enforce_detection=True)
                                    if result and result[0]['dominant_emotion']:  # Example check
                                        print("Real face likely detected")
                                        if identity not in marked_today:
                                            marked_today.add(identity)
                                            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                            writer.writerow([identity, timestamp])
                                            print(f"{identity} is present")
                                    else: 
                                         print('Stranger Alert!')
                                         with open('stranger_log.csv', 'a') as stranger_file:
                                              writer = csv.writer(stranger_file)
                                              writer.writerow(f'Stranger entered at {timestamp}')
        
                            except ValueError:
                                    print("No face detected")
                                    

        if cv2.waitKey(1000) & 0xFF == ord('q'):
            break

webcam.release()
cv2.destroyAllWindows()

cv2.destroyAllWindows()
