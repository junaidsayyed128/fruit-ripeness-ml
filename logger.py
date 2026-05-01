import serial
import csv
import time

# Change COM port if needed
ser = serial.Serial('COM3', 115200)

time.sleep(2)

# Clear buffer (important)
ser.flushInput()

with open('fruit_data.csv', 'a', newline='') as file:
    writer = csv.writer(file)

    # Header
    writer.writerow(["temperature", "pressure", "gas", "delta"])

    print("Collecting data... Press Ctrl+C to stop")

    try:
        while True:
            line = ser.readline().decode(errors='ignore').strip()

            if line:
                print(line)

                values = line.split(',')

                if len(values) == 4:
                    writer.writerow(values)

    except KeyboardInterrupt:
        print("Stopped.")
        ser.close()