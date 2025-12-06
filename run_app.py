import cv2
import numpy as np
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet50 import preprocess_input

MODEL_PATH = 'models/resnet_rgb_model.h5' 
CLASS_PATH = 'models/classes_rgb.pkl'
THRESHOLD_SCORE = 0.85
BOX_SIZE = 224
STABILITY_FRAMES = 15

current_word = ""
last_pred_char = ""
stable_count = 0

print("Loading RGB model...")
try:
    model = load_model(MODEL_PATH)
    with open(CLASS_PATH, 'rb') as f:
        classes = pickle.load(f)
    print(f"-> Loaded {len(classes)} classes.")
except Exception as e:
    print(f"LOAD ERROR: {e}")
    exit()

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

print("\n--- INSTRUCTIONS ---")
print("- Place hand in the green box.")
print("- Hold hand still for 0.5s to enter character.")
print("- Press 'R': Clear all text.")
print("- Press 'Q': Quit.\n")

while True:
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    
    roi_right = w - 50
    roi_left = roi_right - BOX_SIZE
    roi_top = 50
    roi_bottom = roi_top + BOX_SIZE
    
    roi = frame[roi_top:roi_bottom, roi_left:roi_right]
    if roi.size == 0: continue

    img = cv2.resize(roi, (224, 224))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = np.expand_dims(img, axis=0).astype('float32')
    img = preprocess_input(img)

    preds = model.predict(img, verbose=0)
    idx = np.argmax(preds)
    score = np.max(preds)
    char = classes[idx]

    cv2.rectangle(frame, (roi_left, roi_top), (roi_right, roi_bottom), (0, 255, 0), 2)

    if score > THRESHOLD_SCORE:
        cv2.putText(frame, f"{char} {score*100:.0f}%", (roi_left, roi_top - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        if char == last_pred_char:
            stable_count += 1
        else:
            stable_count = 0
            last_pred_char = char
        
        progress_width = int((stable_count / STABILITY_FRAMES) * BOX_SIZE)
        cv2.rectangle(frame, (roi_left, roi_bottom + 5), (roi_left + progress_width, roi_bottom + 15), (0, 255, 255), -1)

        if stable_count == STABILITY_FRAMES:
            if char == 'space':
                current_word += " "
            elif char == 'del':
                current_word = current_word[:-1]
            elif char == 'nothing':
                pass
            else:
                current_word += char
            
            stable_count = 0
    else:
        stable_count = 0

    cv2.rectangle(frame, (0, h-80), (w, h), (0, 0, 0), -1)
    
    cv2.putText(frame, f"Text: {current_word}", (20, h-30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
    
    cv2.imshow("Sign Language Translator", frame)
    
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('r'):
        current_word = ""

cap.release()
cv2.destroyAllWindows()