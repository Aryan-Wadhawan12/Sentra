import cv2
import os

# CHANGE THIS to the name of the person you're capturing
person_name = "Aryan Wadhawan"

# Create the directory
save_dir = f"schools/{person_name}"
os.makedirs(save_dir, exist_ok=True)

# Initialize webcam
cap = cv2.VideoCapture(0)
count = 0
max_images = 1  # How many images to save

print("[INFO] Capturing images. Press 'q' to quit early.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Capturing Face", frame)
    

    # Save frame
    img_path = os.path.join(save_dir, f"Aryan Wadhawan.jpg")
    cv2.imwrite(img_path, frame)
    count += 1
    print(f"[INFO] Saved {img_path}")

    if count >= max_images:
        print("[INFO] Done capturing images.")
        break

    # Exit early if needed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
