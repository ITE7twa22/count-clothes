import cv2

# Replace with your RTSP URL
rtsp_url = "rtsp://admin:L29D36B9@192.168.8.158:554/stream"

# Open the RTSP stream
cap = cv2.VideoCapture(rtsp_url)

if not cap.isOpened():
    print("Error: Could not open RTSP stream.")
else:
    print("RTSP stream is working!")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to read frame.")
            break

        # Display the frame
        cv2.imshow("RTSP Stream", frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the stream and close the window
    cap.release()
    cv2.destroyAllWindows()