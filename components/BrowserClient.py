import keyboard
import time
import win32api, win32con
from PIL import ImageGrab
from func import countdown
import json

class BrowserClient:
    def __init__(self, pos_config, white_color, black_color):
        self.pos_config = pos_config
        self.white_color = white_color
        self.black_color = black_color
        self.buy_timeout_sec = 30

        self.initPositions()

    def initPositions(self):
        print("initialize.")
        createdNewPos = False

        keys = list(self.pos_config.keys())
        keys.remove("open_stadium_button")
        keys.insert(0, "open_stadium_button")
        print(self.pos_config)
        for pos_name in keys:
            if(self.pos_config[pos_name] == ""):
                createdNewPos = True
                print("Where is " + pos_name + "?")
                countdown(5)
                self.pos_config[pos_name] = win32api.GetCursorPos()
                print(str(pos_name) + " -> " + str(self.pos_config[pos_name]))
                if(pos_name == "open_stadium_button"):
                    x, y = self.pos_config["open_stadium_button"]
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
            else:
                print("Position " + pos_name + " is defined.")
                win32api.SetCursorPos(self.pos_config[pos_name])
                time.sleep(1)

        if(createdNewPos):
            with open('latest_pos_config.txt', 'w') as convert_file: 
                convert_file.write(json.dumps(self.pos_config))

        print("Init done.")

    def refreshPage(self):
        print("Refresh")
        keyboard.press_and_release('F5')
        time.sleep(2)
        win32api.SetCursorPos(self.pos_config["open_stadium_button"])
        x, y = self.pos_config["open_stadium_button"]
        time.sleep(0.2)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
        refresh_complete = False
        while not refresh_complete:
            refresh_screenshot = ImageGrab.grab()
            pixel_color = refresh_screenshot.getpixel(self.pos_config["Q"])
            if pixel_color != self.white_color:
                print(pixel_color)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
                time.sleep(0.5)
            else:
                refresh_complete = True

    def select_block(self, block):
        initialTime = int(time.time())
        x, y = self.pos_config[block]
        win32api.SetCursorPos(self.pos_config[block])
        blockSelectScreenshot = ImageGrab.grab()
        buyPixel = blockSelectScreenshot.getpixel(self.pos_config["buy_button"])
        manualBreak = False

        print("Selecting " + block + " | Buy Button: (" + str(buyPixel[0]) + "|" + str(buyPixel[1]) + ")")

        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
        
        #TODO: add black aswell
        while buyPixel == self.white_color and not manualBreak:
            #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
            #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
            time.sleep(0.1)

            buyPixel = blockSelectScreenshot.getpixel(self.pos_config["buy_button"])

             #check for timeou
            currentTime = int(time.time())
            timeDelta = currentTime - initialTime
            if(timeDelta > self.buy_timeout_sec):
                manualBreak = True

        if(manualBreak):
            print("Timeout when selecting.")
            return -1
        else:
            blockSelectScreenshot.save('img/blockSelectScreenshot.png')
            print("Selection success!")
            return 1
        
    def select_block_single(self, block):
        x, y = self.pos_config[block]
        win32api.SetCursorPos(self.pos_config[block])
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
        return 1

    def buy_block_single(self, interval_ms, times):
        x, y = self.pos_config["buy_button"]
        win32api.SetCursorPos(self.pos_config["buy_button"])
        for i in range(0, times):
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
            print("Buy!")
            time.sleep(interval_ms / 1000)
        return -1


    def buy_block(self):
        initialTime = int(time.time())
        manualBreak = False
    
        x, y = self.pos_config["buy_button"]
        win32api.SetCursorPos(self.pos_config["buy_button"])

        # Click until bougt
        bought = False
        while not bought and not manualBreak:
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
            print("Buy!")
            boughtSelectScreenshot = ImageGrab.grab()
            boughtPixel = boughtSelectScreenshot.getpixel(self.pos_config["buy_button"])
            #click until buy button gets black or white
            if(boughtPixel[1] == boughtPixel[2] or boughtPixel[1] < 230):
                bought = True
            else:
                time.sleep(0.1)

            #check for timeout
            currentTime = int(time.time())
            timeDelta = currentTime - initialTime
            if(timeDelta > self.buy_timeout_sec):
                manualBreak = True

        if(manualBreak):
            print("Timeout when buying")
            return -1
        else:
            print("Guess I bought a ticket :)")
            return 1


