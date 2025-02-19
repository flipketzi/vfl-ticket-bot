from twilio.rest import Client

class WhatsAppClient:
  def __init__(self, wa_client_config):
    self.account_ssid = wa_client_config["account_ssid"]
    self.auth_token = wa_client_config["auth_token"]
    self.client = Client(self.account_ssid, self.auth_token)

    self.sender = wa_client_config["sender"]
    self.receiver = wa_client_config["receiver"]

    self.active = wa_client_config["active"]

  def sendMessage(self, message):
    try:
      if(self.active):
        self.client.messages.create(body=message, from_=self.sender, to=self.receiver)
    except:
      print("An exception occurred sending the message")
      
  def sendImage(self, imageUrl, caption):
    try:
      if(self.active):
        self.client.messages.create(body=caption, media_url=imageUrl, from_=self.sender, to=self.receiver)
    except:
      print("An exception occured sending the image")        