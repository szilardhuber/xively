xively
======

This repository contains my playing with Xively.com and my home devices.  

Current features
----------------

- Loads up the 1 minute load average of my Raspberry Pi.
- Checks which devices are online (who is at home) and feeds this to Xively.

Further plans
-------------

- Modify the locator script to be more friendly with Xively and send information only when needed. (Don't sync up when online status don't change.)
- Find if there is a more suitable method for detecting mobile devices. The current n-tries method seems to be far from being optimal.
- Add a webserver to the source code that can be a target for Xively triggers and do some fancy stuff when someone comes home or leaves home.
- Add the source code of my Arduino here. Sample usage idea: turn on the yellow LED when wife is at home and the red one when she isn't.
