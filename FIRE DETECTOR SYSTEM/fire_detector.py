import cv2
import numpy as np
import playsound
import smtplib
import time
import threading
from plyer import notification
import requests


notification.notify(
    title='WARNING',
    message='A fire accident has been reported',
    app_icon=None,
    timeout=10,
)

Fire_Repoted = 0
Alarm_Status = False

def play_audio():
    playsound.playsound("alarm.wav",True)


# email funtion;
def send_email():

    recipientEmail = "firedetectionaiproject@gmail.com"
    recipientEmail = recipientEmail.lower()

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("tbodastuff@gmail.com", 'ffgzfzdyahuiaiby')
        server.sendmail('tbodastuff@gmail.com', recipientEmail, "WARNING!! Fire Detected!!!!!","Fire has been detected in your area. Please evacuate the area immediately.\nFrom Sydney Nzunguli Kathina")
        print("sent to {}".format(recipientEmail))
        server.close()
    except Exception as e:
    	print(e)


#load vision
video = cv2.VideoCapture("fire.mov")

# //// FIRE DETECTION ////
while True:
# read vision
    ret, frame = video.read()
   # resize frame 
    frame = cv2.resize(frame, (1000,600))

    # blur vision to reduce noise
    blur = cv2.GaussianBlur(frame, (15,15),0)

    # add a specific hsv color to the vision
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # define specific variable for hsv color of the fire
    lower = [18, 50, 50]
    upper = [35, 255, 255]

    # convert color as numpy array
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")

    # create a mask to look for specific two types of color in hsv color
    mask = cv2.inRange(hsv, lower, upper)
    
    # display hsv colors
    output = cv2.bitwise_and(frame, hsv, mask=mask)

    #measure size of the fire by adjusting the threshhold
    size = cv2.countNonZero(mask)


    # time.sleep(5)
    cv2.imshow("Recording", output)

    if int(size) > 15000:
        print("WARNING: FIRE DETECTED!!")
        #play alarm
        Fire_Repoted = Fire_Repoted + 1

        if Fire_Repoted >= 1:
            if Alarm_Status == False:
                # send_email()
                t = threading.Thread(target=play_audio, args=()) 
                t.start()
                url = 'https://us-central1-darboda-flutter.cloudfunctions.net/sendAlarm'
                data = {
            "id": "bbDaWFsg33ZIgB4u7SpyrtJXony2"
                    }

                res=requests.post(url, json=data)

                # play_audio()
            Alarm_Status = True

    if ret == False:
        break


    if cv2.waitKey(1) & 0xFF == ord ("q"):
        break

cv2.destroyAllWindows()
video.release()