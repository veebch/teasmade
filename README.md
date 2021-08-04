[![YouTube Channel Views](https://img.shields.io/youtube/channel/views/UCz5BOU9J9pB_O0B8-rDjCWQ?label=YouTube&style=social)](https://www.youtube.com/channel/UCz5BOU9J9pB_O0B8-rDjCWQ)

# Teasmade

The script the uses a Google Calendar (via [gcalcli](https://github.com/insanum/gcalcli)) to control a relay placed in a **1974** Goblin 854 [Teasmade](https://www.youtube.com/watch?v=WTlVVQV0Uug) to boil  water for tea/coffee. Shown in this video ***(LINK)***

The motivation for building this, is a simple proof-of-concept for using a ring-fenced online resource to trigger device (not teasmade) - automation.

**Moral**: It's possible to use home-automation controls without signing-up to have a listening device constantly plugged into the cloud. If Edward Snowden had an automated tea/coffee machine, it would be this one, probably. ***(TO DO: Snowden Endorsement Ad)***

# Prerequisites

A Raspberry Pi with a relay switch and an internet connection.

- Relay Switch: Uses a [Grove 2 channel Solid State Relay](https://wiki.seeedstudio.com/Grove-2-Channel_Solid_State_Relay/) (SSR)
- Google Calendar connection: [gcalcli](https://github.com/insanum/gcalcli)

Follow the installation instructions for the above on your Pi.

# Installation

```
git clone https://github.com/llvllch/teasmade.git
cd teasmade
pip3 install -r requirements.txt
```
To install the [mplayer](https://github.com/baudm/mplayer.py) module for the alarm:

```
pip install git+https://github.com/baudm/mplayer.py.git@0.7.2 
```

# Instructions

To run:
```
python3 teasmade.py
```
Put a 5 minute appointement in your google calendar with the title "brew time" (or whatever you chosen trigger word is). 

The script monitors the calendar and when it sees a reminder that it's brew time, it switches the relay to turn the Goblin Teasmade on. It the code scans your chosen gmail calendar once a minute and checks "Is there a matching slot in the next 8 minutes (this is how long the teasmade takes to boil). If it sees a calendar slot with the trigger word(s) (in `config.yaml`) in the title, the relay switch closes (which just mimics the teasmade alarm being activated) and the tea begins to brew. Once the 8 minutes has passed, the alarm plays (we use the British National anthem).

# Add Autostart

```
cat <<EOF | sudo tee /etc/systemd/system/teasmade.service
[Unit]
Description=teasmade
After=network.target

[Service]
ExecStart=/usr/bin/python3 -u /home/pi/bteasmade/teasmade.py
WorkingDirectory=/home/pi/teasmade/
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
EOF
```

# Bonus - Voice control

If you'd like to take all of this off-grid and have a less formal relationship with your Teasmade, then it's relatively simple to control it with an offline voice recognition tool. The file `teasmadevoice.py` contains the code to control the teasmade using Picovoice - an Edge Voice AI Platform. There are fully open-source alternatives to picovoice (eg [Mycroft](https://github.com/MycroftAI)).

Installation instructions for the installation of the required tools can be found on the [Grove Website](https://wiki.seeedstudio.com/ReSpeaker_2_Mics_Pi_HAT_Raspberry/).


