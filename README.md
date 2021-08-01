[![YouTube Channel Views](https://img.shields.io/youtube/channel/views/UCz5BOU9J9pB_O0B8-rDjCWQ?label=YouTube&style=social)](https://www.youtube.com/channel/UCz5BOU9J9pB_O0B8-rDjCWQ)

# Teasmade

The script the uses picovoice to voice-control a relay placed in an old Goblin Teasmade that boils water for a steep-release coffee. Shown in this video (LINK)

The motivation for doing this is a simple proof-of-concept for using an offline speech processing engine to control devices. Moral: It's possible to use voice controls without signing-up to have a listening device plugged into the cloud. If Edward Snowden had a voice activated coffee machine, it would be this one.

# Prerequisites

Uses a two channel Grove Solid State Relay (SSR) and a Grove Repeaker 2 mics HAT

Follow the istallation instructions for the two devices above on a Pi Zero WH

# Instructions

Install the Python SDK:

```
pip3 install pvporcupine
```
