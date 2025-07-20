import cv2
from deepface import DeepFace
import csv
from datetime import datetime
import os

# Webcam setup
webcam = cv2.VideoCapture(0)
webcam.set(3, 640)
webcam.set(4, 480)

# Track known faces and strangers
marked_today = set()         # known people
logged_strangers = set()     # timestamps of strangers

frame_count = 0
process_every = 10

# DeepFace setup
detector_backend = 'opencv'
model_name = 'SFace'

# Prepare CSV file if not exists
csv_file = 'stranger1_log.csv'
if not os.path.exists(csv_file):
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Label', 'Timestamp'])

# Main loop
while webcam.isOpened():
    ret, frame = webcam.read()
    if not ret:
        break

    cv2.imshow("Sentra", frame)
    frame_count += 1

    # Skip some frames for performance
    if frame_count % process_every != 0:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue

    try:
        # Step 1: Try to match known faces
        results = DeepFace.find(
            img_path=frame,
            db_path='faces',
            model_name=model_name,
            detector_backend=detector_backend,
            enforce_detection=True
        )

        if len(results) > 0 and not results[0].empty:
            for _, row in results[0].iterrows():
                if row['distance'] < 0.3:
                    identity = os.path.basename(os.path.dirname(row['identity']))
                    if identity not in marked_today:
                        marked_today.add(identity)
                        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        print(f"✅ {identity} is present")
                        with open('recognition_log.csv', 'a', newline='') as f:
                            csv.writer(f).writerow([identity, timestamp])
                    break

    except ValueError:
        try:
            # Step 2: Stranger detection
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            result = DeepFace.analyze(frame, detector_backend='retinaface', enforce_detection=True)

            if result and isinstance(result, list) and 'dominant_emotion' in result[0]:
                if timestamp not in logged_strangers:
                    logged_strangers.add(timestamp)
                    print("⚠️ Stranger Alert!")

                    # ✅ Write to CSV in append mode
                    with open(csv_file, 'a', newline='') as stranger_file:
                        writer = csv.writer(stranger_file)
                        writer.writerow(['Stranger', timestamp])
                    print(f"✅ Stranger logged at {timestamp}")

        except ValueError:
            print("🕵️ No face in frame")

    # Exit condition
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
webcam.release()
cv2.destroyAllWindows()

