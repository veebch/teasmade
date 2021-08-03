[![YouTube Channel Views](https://img.shields.io/youtube/channel/views/UCz5BOU9J9pB_O0B8-rDjCWQ?label=YouTube&style=social)](https://www.youtube.com/channel/UCz5BOU9J9pB_O0B8-rDjCWQ)

# Teasmade

The script the uses a Google Calendar (via [gcalcli](https://github.com/insanum/gcalcli)) to control a relay placed in an old Goblin Teasmade that boils water for a steep-release ([Clever Dripper](https://library.sweetmarias.com/clever-coffee-dripper-a-full-immersion-brewing-method/)) coffee. Shown in this video ***(LINK)***

The motivation for building this, is a simple proof-of-concept for using a ring-fenced online resource to trigger device-automation, without sacrificing vast amounts of privacy. 

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

# Instructions

To run:
```
python3 teasmade.py
```
The script monitors the calendar and when it sees a reminder that it's coffee time, it switches the relay to turn the Goblin Teasmade on.

# Coffee - Will it Brew?

The lack of ability to pre-heat the Clever Dripper means that the plastic body absorbs some of the heat from the brew water which reads at 95C immediately after  the Clever Dripper is filled. One minute after pouring, the water temperature is around 85C.

Water volume is determined by the teasmade's rocker-switch cut-off, ~430ml

Freshly ground Coffee, 26g (ie 60g of coffee per kg of water)
