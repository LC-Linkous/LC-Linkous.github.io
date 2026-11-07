---
layout: post
title: "A Python API for the tinySA"
summary: "A quick look at an in-progress Python library for the tinySA line of devices that started as part of a conference project"
tags: [tinysa, python, hardware, open_source]
---

<div class="justified-content" markdown="1">

## What is the tinySA?

The [tinySA](https://tinysa.org/) line of devices are small, portable, and pretty user-friendly instruments that combine a spectrum analyzer with a signal generator. There are four main versions sharing the same core features; the Ultra and Ultra Plus build on the original tinySA Basic with wider frequency range and more capability. They look a lot like the NanoVNA series, but they are **not** the same device, they do different things, and they are made by different people.

The distinction matters if you are new to RF test gear. A vector network analyzer like the NanoVNA measures S-parameters, which is, loosely, how a device or antenna responds to a signal at each frequency: how much is reflected, how much passes through. A spectrum analyzer measures the amplitude of whatever RF energy is present at each frequency, whether that is your transmitter, the FM band, or the noise floor. There is a lot of overlap in how the two get used in antenna work, but the measurements are different things. The signal generator half of the tinySA is exactly what it sounds like: a controllable tone at a chosen frequency and power level, which is handy for checking a receiver or a filter.

The official documentation lives at [tinysa.org](https://tinysa.org/), and the [wiki](https://www.tinysa.org/wiki/) is always going to be more current than anything I write about new firmware and features. It also links to the official GUI software. There is a very active community at [groups.io/g/tinysa](https://groups.io/g/tinysa) with deep Q&A threads on using the device. That community has nothing to do with this library and does not support it; they are a cool group, so please do not bother them with it.

One warning up front, repeated from the project README: improper usage can destroy your device. Read the [First Use page](https://tinysa.org/wiki/pmwiki.php?n=Main.FirstUse) and get familiar with the hardware before you start scripting against it.

## Talking to the tinySA over serial

What makes the tinySA scriptable is that it exposes a plain text console over USB. Plug it in, open the serial port, and you get a `ch>` prompt that accepts one command per line: `version`, `info`, `help`, `sweep`, `scan`, `marker`, `rbw`, and so on. The device answers in text, or in a compact binary form for the raw scan commands, and then prints the prompt again. Frequencies take suffixes (`100k`, `0.1M`, `2.4G`), levels are in dBm, times are in seconds with `m` and `u` for milli and micro.

That is the whole interface. There is no vendor SDK, no driver beyond the generic USB serial class, and nothing stopping you from typing commands into a terminal program by hand. Which is also the problem: for anything repeatable, a batch of sweeps, a logged measurement, a plot that updates, you end up writing the same string-building and response-parsing code over and over. That is what the library is for.

## A non-GUI Python library

[tinySA_python](https://github.com/LC-Linkous/tinySA_python) is an **unofficial** Python API for the tinySA device series. It uses the official documentation and resources but is not endorsed by the tinySA project or anyone who makes the hardware. See the repository's references section for the sources it was built from, and the official wiki for what the device can actually do.

The library wraps most of the documented serial commands as Python methods on a single `tinySA` class, with the documentation organized by the device command each method corresponds to, so the official wiki and the library docs can be read side by side. Error checking exists on both the device and in the library, but neither is exhaustive. The library is deliberately GUI-free: the point is to be the thing you call from a script, a notebook, a test fixture, or a larger program, with `pyserial` as its only dependency. Plotting is left to the examples, which use numpy and matplotlib.

Connecting looks like this:

```python
from tsapython import tinySA

tsa = tinySA()
tsa.set_verbose(True)              # print what is sent and received
tsa.set_error_byte_return(True)    # return b'ERROR' on a failed command

found, connected = tsa.autoconnect()
if connected:
    print(tsa.command("version"))
    tsa.disconnect()
```

Autodetection is rudimentary: it looks for the device's USB vendor ID and takes the first match, so if you have more than one serial device of the same family plugged in you can pass the port explicitly instead. From there the examples in the README cover sweeping a range with `scan` and `scanraw`, calculating the frequency axis from the sweep settings, saving results to CSV, filtering out the occasional bad return, and drawing a live waterfall.

**Where it stands.** The library commands for the common arguments are in, with documentation and basic examples, and it has been tested mainly on Debian-flavored Linux. What is still being worked on: filling in the less common arguments and anything new in recent firmware; `scan` and `scanraw` occasionally return bad data, which one of the examples works around but which deserves a real fix; the `scanraw` path has a device-side buffer issue under investigation (see the plotting examples); `trigger` needs more alias functions to cover everything it can do; and I want to add an argparse front end, some example scripts, and a set of beginner notes and vocabulary for people coming to this from the antenna side rather than the software side.

The code is at [github.com/LC-Linkous/tinySA_python](https://github.com/LC-Linkous/tinySA_python). Issues and pull requests are welcome, especially device reports from hardware I do not own.

---

*Update, October 2026.* A lot has happened since this was written. The library is on PyPI as [`tsapython`](https://pypi.org/project/tsapython/) (3.0.0 restructured it into an installable package with an automated test suite that replays captured device responses, so most tests run without hardware). [4.0.0](https://github.com/LC-Linkous/tinySA_python/blob/main/CHANGELOG.md) added a typed API, per-model device profiles that stop the library from sending commands a given tinySA does not have, structured logging, and CI across Windows, Linux, and macOS. Short or timed-out `scanraw` frames are now treated as failures and logged rather than returned as data. It is archived on Zenodo with a DOI ([10.5281/zenodo.20546764](https://doi.org/10.5281/zenodo.20546764)), and there is now a browser front end built on the same protocol, [tinySA Web](https://lc-linkous.github.io/tinysa-web/), with a simulated device for trying it without hardware.

*This post was written in 2025 and released publicly in August 2025.*

</div>