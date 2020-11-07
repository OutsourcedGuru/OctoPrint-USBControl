# USBControl

An OctoPrint plugin to allow USB ports to be programmatically turned OFF and ON from within the web interface.

## Overview
> **Raspberry Pi**: A single-board computer made by the Raspberry Pi Foundation
> 
> **USB**: (abbreviation of Universal Serial Bus) is an industry standard that establishes specifications for cables, connectors and protocols for connection, communication and power supply between personal computers and their peripheral devices.
>
> **uhubctl**: The underlying program to turn USB power off and on. In addition to Raspberry Pi 2B, 3B and 3B+ it supports other USB hubs - refer to the list of supported devices on [uhubctl home page](https://github.com/mvp/uhubctl).

* The USB specification was created originally when the Type-A side of a USB cable was the PC and the Type-B side was the device. It was assumed that the PC could always provide power to the device.
* For OctoPi, the Type-A side is the Raspberry Pi 3B with a 5V 2.5A power adapter. It can't be sinking power over to the printer controller board since that's now considered to be the one with beefier power needs. This is often the case when the printer board is powered off and the Raspberry is still powered on. This could lead to the printer's LCD remaining on under these circumstances.
* It is suggested that this sinking of power is causing undervoltage conditions in some cases.
* The typical USB connection has four pins: 5V, ground, transmit and receive. OctoPrint appears to be happy with just the last three of these (as suggested by some users). As they say, though, "*your mileage may vary*".
* Many people are applying a small strip of tape to the inside of their Type-A connectors to prevent 5V from being felt on the controller (Arduino) board.
* There are other configurations in which the user feels like they want to have programmatic control over providing power to downstream devices.

### The rationale for this plugin

Rather than rigging up inline switches, applying tape inside the tongue of a USB connector or purchasing specialized male/female adapters which omit the 5V line...

    ...I thought that I would provide this plugin as a simpler alternative.

## Compatibility
This plugin was created to support only the following platforms:

* Raspberry Pi 4B
* Raspberry Pi 3B
* Raspberry Pi 3B+
* Raspberry Pi 2B

It is NOT intended to support the following:

* Raspberry Pi 3A+
* Raspberry Pi Compute Modules
* Raspberry Pi 1B+
* Raspberry Pi 1A+
* Raspberry Pi Zero W
* Raspberry Pi Zero
* PCs, Macs, generic Linux workstations *or anything else*

Also, this plugin is NOT intended to support those of you who wish to plug more than one printer into your Raspberry Pi.

## Primary use case
I expect that this plugin would be useful for anyone who needs to remove power which is being sinked over to their printer's LCD panel when their printer board is powered OFF.

## Complications

### Raspberry Pis can't individually control ports
The `uhubctl` program that this project uses at its core is unable to toggle individual USB ports on Raspberry Pi devices.  This is a limitation of the hardware, not the software.  When using this plugin, you can only control *all four* USB ports at the same time.

### This won't necessarily work while printing
I note that on my own test rig, the Robo 3D printer board includes a jumper to determine how the board is powered. If the jumper is set to "USB", this plugin works as expected to completely power ON/OFF all functions on the board over the USB port although this wouldn't technically work in a real printer given the power limitation. **If instead the jumper is set to "5V" then toggling the associated USB port to OFF from this plugin will result in a communication error after the timeout has been reached.** Therefore this is not compatible with the normal functioning of this board for the purpose of printing.


### Persistence
At the moment, this plugin does not save the power state for each USB port. Each restart of OctoPrint will basically forget how you last left these and assume that they're all ON.

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/OutsourcedGuru/OctoPrint-USBControl/archive/master.zip

## Configuration

When initially installed, the plugin still needs a script to be run once. The instructions for doing this may be found in the associated **Settings** page but is also included below.

1. Install the plugin (see **Setup** in the section above)
2. Visit the **Settings** page
3. Follow the instructions under the **Setup required** section there
   * For this, you are required to remote into the Raspberry Pi 3B using `ssh` or `PuTTY`
   * Copy/paste the install script into this remote session
   * Return back to the OctoPrint **Settings** page
   * Indicate that you have run the script
   * Select the **Save** button at the bottom of the **Settings** page
4. Restart OctoPrint
5. Return to the **Settings** page (you should see the control sliders now for each USB port)

> For an OctoPi installation, the command you are asked to run in Step 3 above would be `sudo ~/oprint/lib/python2.7/site-packages/usbcontrol/bin/install`.

## REST API
The plugin includes an API for programmatically toggling the ports ON/OFF in a way which is similar to OctoPrint's. You can find/copy your API key under **Settings** -> **API**.

### Controlling power remotely (All except Raspberry Pi 4B)
```
POST /api/plugin/usbcontrol HTTP/1.1
Host: example.com
Content-Type: application/json
X-Api-Key: abcdef...

{
  "command": "all",
  "argAll": "on"
}
```
Values for argAll are "on" and "off"

#### Controlling power remotely (Raspberry Pi 4B)
```
POST /api/plugin/usbcontrol HTTP/1.1
Host: example.com
Content-Type: application/json
X-Api-Key: abcdef...

{
  "command": "usb4",
  "arg4": "on"
}
```
Values for arg4 are "on" and "off"

## Update 1.0.8
Update to support RPi4

## Update 1.0.7
Installation process of the plugin will automatically add a symlink to `/usr/local/bin` for the `uhubctl` program so that you can simply run it from the command line if you're into that.

## Reporting bugs/issues
Please do not report a bug if you *can't* print with the USB power turned OFF. It is assumed that this is the case for most printer controllers. If this does work for you, feel lucky.

By the way, this means the same as "I've just gotten a **Communications Error** popup with the USB port toggled OFF". This is not meant to be a solution to this problem.

Please do not report a bug if you are plugging more than one printer into your Raspberry Pi at the same time.

Please do not report a bug if you are using a platform that isn't listed in the **Compatibility** section above.
