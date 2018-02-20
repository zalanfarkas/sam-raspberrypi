import LCD
import time

LCD.init()

LCD.clear()
#LCD.write("Hello World")
message = "FUCK me asdasd asdas dasdasdasdasd"
LCD.write(message)
for i in range(0, 16):
    time.sleep(0.5)
    LCD.shiftleft()

time.sleep(0.5)
