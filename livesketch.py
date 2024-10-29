import cv2
import numpy as np

# Variables to track recording status
recording = False
out = None

def sketch(image):
    # Sharpen the image
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharp = cv2.filter2D(image, -1, kernel)
    
    # Convert to grayscale and invert
    gray = cv2.cvtColor(sharp, cv2.COLOR_BGR2GRAY)
    inv = 255 - gray
    
    # Apply Gaussian blur
    blur = cv2.GaussianBlur(src=inv, ksize=(13, 13), sigmaX=0, sigmaY=0)
    
    # Generate sketch
    s = cv2.divide(gray, 255 - blur, scale=256)
    return s

# Mouse callback function to handle button clicks
def mouse_event(event, x, y, flags, param):
    global recording, out
    
    # Define button positions
    record_button_pos = (10, 40, 100, 80)  # x1, y1, x2, y2
    capture_button_pos = (10, 100, 100, 140)
    
    # If left mouse button is clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        if record_button_pos[0] <= x <= record_button_pos[2] and record_button_pos[1] <= y <= record_button_pos[3]:
            # Toggle recording
            if not recording:
                # Start recording
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter('sketch_video.avi', fourcc, 20.0, (frame.shape[1], frame.shape[0]))
                recording = True
            else:
                # Stop recording
                recording = False
                out.release()
        
        elif capture_button_pos[0] <= x <= capture_button_pos[2] and capture_button_pos[1] <= y <= capture_button_pos[3]:
            # Capture image without buttons
            clean_sketch_frame = sketch(frame)
            cv2.imwrite('sketch_image.png', clean_sketch_frame)
            print("Image saved as sketch_image.png")

cap = cv2.VideoCapture(0)
cv2.namedWindow('Sketch Camera')
cv2.setMouseCallback('Sketch Camera', mouse_event)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Apply sketch effect
    sketch_frame = sketch(frame)
    
    # Draw buttons on a copy of the sketch frame for display only
    display_frame = sketch_frame.copy()
    cv2.rectangle(display_frame, (10, 40), (100, 80), (50, 50, 200), -1)  # Record button
    cv2.putText(display_frame, 'Record', (15, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    cv2.rectangle(display_frame, (10, 100), (100, 140), (50, 200, 50), -1)  # Capture button
    cv2.putText(display_frame, 'Capture', (15, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    
    # Display the normal and sketch frames
    cv2.imshow('Normal Camera', frame)
    cv2.imshow('Sketch Camera', display_frame)
    
    # Save video frame if recording
    if recording and out is not None:
        out.write(sketch_frame)
    
    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release everything
cap.release()
if out is not None:
    out.release()
cv2.destroyAllWindows()
