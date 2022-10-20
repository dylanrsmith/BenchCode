Raspberry Pi Next Generation Combine Bench Code - Fargo Engineering Inc.
=========================================================================

The code largely consists of a tkinter-generated user interface, where a user can toggle various relay states and I/O values.

HwConnect
-----------
These Modules handle communication over i2c, SPI, and CAN.

PlantModels
------------
4 Possible UCM's to test.

UserInterface
--------------
Tkinter based notebook-style interface.



v10.2:
    Adding ping functionality and disabling of widgets that are offline.


v7.08:
    Added Backwards Compatibility: 
        Open and Actuator Tabs will only show if ConfigSheet is properly configured.

    Added Simulator Mode: 
        Turn Off to disable Relay controls and Enable Bypass Relay Boards. 
        Turn on to control relays manually. Button located under settings.
        Value is written to SimMode.txt file for storage between power cycles.
