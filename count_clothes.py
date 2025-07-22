import cv2
from ultralytics import YOLO  # Assuming you're using Ultralytics YOLOv8
import time
import pandas as pd
from datetime import datetime
import schedule
import os

# Load your trained YOLO model
model = YOLO("./best.pt")  # Replace with your model path

# Initialize video capture from live camera (0 is usually the default camera)
# Initialize video capture from the IMOU camera using its RTSP URL
rtsp_url = "rtsp://admin:L29D36B9@192.168.8.158:554/stream"
cap = cv2.VideoCapture(rtsp_url)
# Set the interval (in frames) to process images
frame_interval = 140  # Process every 140th frame (adjust as needed)

# Initialize counters
frame_count = 0
total_clothes_count = 0

# Function to get the current count of clothes
def get_camera_counts():
    return total_clothes_count

# Function to log counts to an Excel file
def log_counts_to_excel():
    global total_clothes_count

    # Get the current counts from the camera
    camera_1_count = get_camera_counts()

    # Calculate the total count (sum of two cameras)
    total_count = camera_1_count

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create a new row of data
    row = {
        "Timestamp": current_time,
        "Camera 1 Count": camera_1_count,
        "Total Count": total_count
    }

    # Initialize the Excel file
    file_name = "product_counts.xlsx"
    if not os.path.exists(file_name):
        data = pd.DataFrame(columns=["Timestamp", "Camera 1 Count", "Total Count"])
        # Save the new file
        data.to_excel(file_name, index=False)
        print(f"Created new file: {file_name}")
    else:
        data = pd.read_excel(file_name)

    # Append the new row to the DataFrame
    data = pd.concat([data, pd.DataFrame([row])], ignore_index=True)

    # Save the updated DataFrame back to the Excel file
    data.to_excel(file_name, index=False)
    print(f"Logged counts at: {current_time} | Total Count: {total_count}")

    # Reset the total clothes count after logging
    total_clothes_count = 0

# Schedule the logging function to run every 1 minute
schedule.every(1).minutes.do(log_counts_to_excel)

# Run the scheduler and video capture in parallel
print("Starting the product count logger...")
while True:
    # Read a frame from the live camera
    ret, frame = cap.read()
    if not ret:
        break  # Exit the loop if the camera fails

    # Increment frame count
    frame_count += 1

    # Process the frame at the specified interval
    if frame_count % frame_interval == 0:
        # Run YOLO model on the frame
        results = model(frame)

        # Count the number of detected clothes
        clothes_count = len(results[0].boxes)
        total_clothes_count += clothes_count

        # Print the count for the current frame
        print(f"Frame {frame_count}: Detected {clothes_count} clothes")

        # Optionally, visualize the results
        annotated_frame = results[0].plot()  # Get annotated frame
        cv2.imshow("YOLO Detection", annotated_frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Run pending scheduled tasks
    schedule.run_pending()

# Release the video capture and close windows
cap.release()
cv2.destroyAllWindows()

# Print the total count of clothes detected
print(f"Total clothes detected: {total_clothes_count}")