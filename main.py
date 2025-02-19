from PIL import ImageGrab
import time
from datetime import datetime

from components.WhatsAppClient import WhatsAppClient
from components.BrowserClient import BrowserClient
from components.CloudClient import CloudClient
from func import countdown, playTicketSound
from config import application_config


# Set the interval in milliseconds
interval_ms = application_config["interval_ms"]  # Change this to your desired interval in milliseconds
refresh_interval_sec = application_config["refresh_interval"]

noTicket = True

#Set up Cloudinary
cloudClient = CloudClient(application_config["cloud_config"])

#Set up WhatsAppClient 
waClient = WhatsAppClient(wa_client_config=application_config["wa_client_config"])
    
#Set up BrowserClient with optional initialization
browserClient = BrowserClient(pos_config=application_config["pos_config"], white_color=application_config["white_color"], black_color=application_config["black_color"])


print("Live in: ")
countdown(3)

browserClient.refreshPage()

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
waClient.sendMessage("Ticketing live {}".format(timestamp))

timeLastRefresh = int(time.time())
while noTicket:
    # Capture the screen
    screenshot = ImageGrab.grab()

    out = ""

    for block in application_config["block_list"]:
        pixel_color = screenshot.getpixel(browserClient.pos_config[block])
        out = out + "{}: {} | ".format(block, pixel_color)

        if pixel_color != application_config["white_color"]:
            print(out)
            screenshot.save('img/ticket_trigger.png')
            waClient.sendMessage("Triggered: Block " + block + ".")
            #selectionValue = browserClient.select_block(block)
            selectionValue = browserClient.select_block_single(block)
            if(selectionValue == 1):
                #ticketValue = browserClient.buy_block()
                ticketValue = browserClient.buy_block_single(100, 30)
                if(ticketValue == 1):
                    #waClient.sendMessage("Erfolgreich.")
                    time.sleep(2) #2 sek delay for browser to set itself
                    ticket_screenshot = ImageGrab.grab()
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    waClient.sendImage(cloudClient.uploadImage(ticket_screenshot), "Ticket {}".format(timestamp))
                    noTicket = False
                    if(application_config["sound"]):
                        playTicketSound()
                    break
                else:
                    ticket_screenshot = ImageGrab.grab()
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    waClient.sendImage(cloudClient.uploadImage(ticket_screenshot), "Timeout Purchase {}".format(timestamp))
                    timeLastRefresh = 0
                    break
            else:
                ticket_screenshot = ImageGrab.grab()
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                waClient.sendImage(cloudClient.uploadImage(ticket_screenshot), "Timeout Selection {}".format(timestamp))
                waClient.sendMessage("Fehler: Timeout selection")
                time.sleep(5)
                timeLastRefresh = 0
                break
    
    if not noTicket:
        break
    
    currentTime = int(time.time())

    timeDelta = currentTime - timeLastRefresh
    if(timeDelta > refresh_interval_sec):
        browserClient.refreshPage()
        timeLastRefresh = int(time.time())
    
    print("[" + str((currentTime - timeLastRefresh)) + "/" + str(refresh_interval_sec) + "]\t" + out)

    # Wait for the specified interval
    if(interval_ms > 0):
        time.sleep(interval_ms / 1000)  # Convert milliseconds to seconds

print("Done")
