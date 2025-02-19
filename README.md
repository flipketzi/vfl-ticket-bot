
<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/flipketzi/vfl-ticket-bot">
    <img src="./rsc/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">VfL Ticketing</h3>

  <p align="center">
    Enhance your Zweitmarkt experience!
  </p>
</div>




<!-- ABOUT THE PROJECT -->
## About The Project

Everyone who ever tried to get tickets for the great VfL Bochum from Bochum knows the pain of scouting for Zweitmarkt tickets. As a proud season ticket owner, I want to have the option to visit the games with my friends. However, in the past it was an absolute pain to hunt for tickets. The shop is flaky and there has been a good chance that you are leaving empty handed. That's when I had the idea of a ticketing bot.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

To get the bot running, follow these few steps.

### Prerequisites

You might want to look at _Anaconda_ for managing your python packages. A basic instruction can be easily found online.

### Installation


1. Clone the repo
   ```sh
   git clone https://https://github.com/flipketzi/vfl-ticket-bot.git
   ```
2. Create a config.py
   ```python
   application_config = {
    "sound": False,
    "interval_ms": 0, #click interval in miliseconds
    "refresh_interval": 15, #in seconds
    "white_color": (245, 245, 245), #reference color for white
    "black_color": (31, 31, 31), #reference color for black
    "pos_config": {
        "O": (739, 576), #pos for block O (example)
        "N2": "",  #leave positions blank for init at startup
        "P": "", 
        "buy_button": "", #pos of buy button
        "Q": "", 
        "refresh_check": "", #pos for refresh check (white space)
        "open_stadium_button": "" #pos for opening the ticket selection
        },
    "block_list": ["N2", "O", "P", "Q"], #this shouldn't be edited
    #the following section is the configuration for whatsapp notifications
    "wa_client_config": {
        "active": True, #enable whatsapp notifications
        "account_ssid": "YOUR_TWILIO_ACCOUNT_SSID",
        "auth_token": "YOUR_TWILIO_AUTH_TOKEN",
        "sender": 'YOUR_TWILIO_SENDER_NUMBER',
        "receiver": 'YOUR_WHATSAPP_NUMBER'
    },
    #the following section is the configuartion for cloudinary
    #to send images via twilio
    "cloud_config": {
        "api_key": "YOUR_CLOUDINARY_API_KEY",
        "api_secret": "YOUR_CLOUDINARY_API_SECRET",
        "cloud_name": "YOUR_CLOUDINARY_NAME"
    }
    }

3. Run main.py


<p align="right">(<a href="#readme-top">back to top</a>)</p>
