import cv2
import serial

# Serial connection
arduino = serial.Serial('COM3', 9600)

# Camera
cap = cv2.VideoCapture(0)

# ArUco setup
aruco = cv2.aruco
dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
detector = aruco.ArucoDetector(dictionary)

def scan_tool(slot):
    ret, frame = cap.read()
    if not ret:
        return "ERROR"

    corners, ids, _ = detector.detectMarkers(frame)

    if ids is not None:
        tool_id = int(ids[0][0])
        print(f"Slot {slot}: Tool ID {tool_id}")
        return f"TOOL_{tool_id}"
    else:
        print(f"Slot {slot}: Unknown tool")
        return "UNKNOWN"

while True:
    if arduino.in_waiting > 0:
        data = arduino.readline().decode().strip()

        if "SCAN_SLOT_" in data:
            slot = data.split("_")[-1]

            result = scan_tool(slot)

            # Send result back
            message = f"{slot}:{result}\n"
            arduino.write(message.encode())
