[![YouTube Channel Views](https://img.shields.io/youtube/channel/views/UCz5BOU9J9pB_O0B8-rDjCWQ?label=YouTube&style=social)](https://www.youtube.com/channel/UCz5BOU9J9pB_O0B8-rDjCWQ)

# Teasmade

The script the uses a Google Calendar (via [gcalcli](https://github.com/insanum/gcalcli)) to control a relay placed in an old Goblin Teasmade that boils water for a steep-release coffee. Shown in this video ***(LINK)***

The motivation for doing this is a simple proof-of-concept for using a ring-fenced resource to trigger home-automation without sacrificing vast amounts of privacy. 

**Moral**: It's possible to use home-automation controls without signing-up to have a listening device constantly plugged into the cloud. If Edward Snowden had an automated coffee machine, it would be this one, probably. ***(TODO: Snowden Endorsement Ad)***

# Prerequisites

Uses a two channel Grove Solid State Relay (SSR) and [gcalcli](https://github.com/insanum/gcalcli)

Follow the istallation instructions for the above on a Pi Zero WH

# Installation

```
git clone https://github.com/llvllch/teasmade.git
cd teasmade
pip3 install -r requirements.txt
```
Next, use alsameter to adjust the capture volume, leaving it at 100% default makes for a pretty ugly recording, set to mid-range.
# Instructions

To run:
```
python3 teasmade.py
```
The script monitors the calendar and when it sees a reminder that it's coffee time, it switches the relay to turn the Goblin Teasmade on.

# Coffee - Will it Brew?

The lack of ability to pre-heat the Clever Dripper means that the plastic body absorbs some of the heat from the brew water which reads at 95C immediately after  the Clever Dripper is filled. One minute after pouring, the water temperature is around 85C. 
