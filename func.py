import time
import winsound

def playNotificationSound():
    for x in range(0, 10):
        winsound.Beep(2000, 100)
        time.sleep(0.1)

def playTicketSound():
    playNotificationSound()
    time.sleep(5)
    playNotificationSound()

def countdown(s):
    for x in range(s, 0, -1):
        print(str(x))
        time.sleep(1)