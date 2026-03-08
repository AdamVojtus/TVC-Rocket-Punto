import serial
import time

ser = None

def connect_system(port='COM3', baud=9600):
    global ser
    try:
        ser = serial.Serial(port, baud, timeout=0.1)
        time.sleep(2)
        ser.reset_input_buffer()
        return True
    except:
        return False

def get_latest_data():
    global ser
    if ser and ser.in_waiting > 0:
        try:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            return line
        except:
            return None
    return None