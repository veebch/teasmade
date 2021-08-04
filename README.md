[![YouTube Channel Views](https://img.shields.io/youtube/channel/views/UCz5BOU9J9pB_O0B8-rDjCWQ?label=YouTube&style=social)](https://www.youtube.com/channel/UCz5BOU9J9pB_O0B8-rDjCWQ)

# Teasmade

The script the uses a Google Calendar (via [gcalcli](https://github.com/insanum/gcalcli)) to control a relay placed in an old Goblin Teasmade that boils water for a steep-release ([Clever Dripper](https://library.sweetmarias.com/clever-coffee-dripper-a-full-immersion-brewing-method/)) coffee. Shown in this video ***(LINK)***

The motivation for building this, is a simple proof-of-concept for using a ring-fenced online resource to trigger device (not teasmade) - automation.

**Moral**: It's possible to use home-automation controls without signing-up to have a listening device constantly plugged into the cloud. If Edward Snowden had an automated coffee machine, it would be this one, probably. ***(TO DO: Snowden Endorsement Ad)***

# Prerequisites

Uses a [Grove 2 channel Solid State Relay](https://wiki.seeedstudio.com/Grove-2-Channel_Solid_State_Relay/) (SSR) and [gcalcli](https://github.com/insanum/gcalcli)

Follow the istallation instructions for the above on a Pi Zero WH

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
Put a 5 minute appointement in your google calendar with the title "teasmade" (or whatever you chosen trigger word is). 

The script monitors the calendar and when it sees a reminder that it's coffee time, it switches the relay to turn the Goblin Teasmade on. It the code scans your chosen gmail calendar once a minute and checks "Is there a coffee break in the next 8 minutes (this is how long the teasmade takes to boil). If it sees a calendar slot with the trigger word (in `config.yaml`) in the title, the relay switch closes (which just mimics the alarm being activated) and the tea begins to brew. 

# Coffee - Will it Brew?

The lack of ability to pre-heat the Clever Dripper means that the plastic body absorbs some of the heat from the brew water which reads at 95C immediately after  the Clever Dripper is filled. One minute after pouring, the water temperature is around 85C.

Water volume is determined by the teasmade's rocker-switch cut-off, ~430ml

Freshly ground Coffee, 26g (ie 60g of coffee per kg of water)

# Bonus - Voice control

If you'd like to take all of this off-grid and have a less formal relationship with your Teasmade, then it's relatively simple to control it with an offline voice recognition tool. The file `teasmadevoice.py` contains the code to control the teasmade isng picovoice - an Edge Voice AI Platform. There are fully open-source alternatives to this (eg Mycroft). 


