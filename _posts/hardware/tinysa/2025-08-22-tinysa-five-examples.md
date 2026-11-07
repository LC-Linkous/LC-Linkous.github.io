---
layout: post
title: "Five Things to Do with a tinySA and tsapython"
summary: "Exploring the tinySA and tsapython features: on-screen traces, scans off the screen, scan vs. scanraw, cleaning up a firmware artifact, and a waterfall."
tags: [tinysa, python, hardware, examples, open_source]
---

<div class="justified-content" markdown="1">

The [last post](/posts/tinysa-python-api/) covered what the tinySA is and why there is a Python library for it. This one is the hands-on half: five things you can do with [tsapython](https://github.com/LC-Linkous/tinySA_python) in a few lines each, roughly in the order you would try them with a new device. Each example is condensed from the [README](https://github.com/LC-Linkous/tinySA_python#example-implementations), where the full scripts live and get maintained; the versions here are trimmed to the part that matters.

All of them start the same way, so here is the boilerplate once:

```python
from tsapython import tinySA

tsa = tinySA()
tsa.set_verbose(True)              # print what is sent and received
tsa.set_error_byte_return(True)    # b'ERROR' instead of b'' on a failed command

found, connected = tsa.autoconnect()
if not connected:
    raise SystemExit("could not connect to a tinySA")
```

Everything below goes between that and `tsa.disconnect()`. The examples use numpy and matplotlib, which are not dependencies of the library itself; `pip install tsapython[plotting]` pulls them in.

## 1. Plot what is on the screen

The simplest measurement is the one the device already made. `data()` returns the current trace and `frequencies()` returns the frequency of each point, both as text, one value per line. Because they come from the same sweep they have the same length, so they plot directly against each other.

```python
import matplotlib.pyplot as plt

def to_floats(b):
    return [float(v) for v in b.decode().splitlines()]

trace = to_floats(tsa.data())
freqs = to_floats(tsa.frequencies())

plt.plot(freqs, trace)
plt.xlabel("Frequency (Hz)"); plt.ylabel("dBm")
plt.title("tinySA on-screen trace")
plt.show()
```

<figure>
  <img src="/media/imgs/posts/tinysa-ex1-trace.webp" alt="Line plot of a tinySA on-screen trace from 100 kHz to 800 MHz, amplitude in dBm against frequency">
  <figcaption>The device's own sweep, 100 kHz to 800 MHz, replotted in matplotlib.</figcaption>
</figure>

This is a good first test because if it works, the serial link, the parsing, and the plotting are all fine, and nothing has been changed on the device.

## 2. Scan a range that is not on the screen

`scan(start, stop, points, outmask)` asks the device to sweep a range you specify, whatever the screen is showing. The catch is that `frequencies()` no longer lines up: it reports the frequencies of the *screen* sweep, which depend on the resolution bandwidth, not the number of points you asked for. So the x-axis is calculated instead, with `numpy.linspace` between `start` and `stop`.

```python
import numpy as np

start, stop, pts = 150_000_000, 500_000_000, 450
raw = tsa.scan(start, stop, pts, outmask=2)      # outmask 2 = measured values
tsa.resume()                                      # unfreeze the screen afterwards

freqs = np.linspace(start, stop, pts)
power = [float(line.split()[0]) for line in raw.decode().splitlines() if line.strip()]

plt.plot(freqs / 1e6, power)
plt.xlabel("MHz"); plt.ylabel("dBm")
plt.show()
```

Two habits worth forming here. Call `resume()` after a scan, or the device sits with a frozen display until you do. And if scans feel slow, check the RBW setting on the device; `auto` is usually the right answer.

## 3. `scan` vs. `scanraw`

`scan` returns text, which is easy to read and slow to transfer. `scan_raw()` returns the same measurement as packed binary, roughly three times faster, which matters once you are sweeping repeatedly. The price is that you have to unpack it and convert it to dBm yourself.

```python
import struct

text_raw = tsa.scan(start, stop, pts, 2)
bin_raw  = tsa.scan_raw(start, stop, pts, 2)
tsa.resume()

text_dbm = [float(l.split()[0]) for l in text_raw.decode().splitlines() if l.strip()]

# skip the leading brace; then each point is a marker byte + little-endian uint16
values  = struct.unpack("<" + "xH" * pts, bin_raw[1:1 + 3 * pts])
SCALE   = 174         # tinySA Ultra and newer; the Basic uses 128
bin_dbm = np.array(values) / 32 - SCALE
```

<figure>
  <img src="/media/imgs/posts/tinysa-ex3-scan-vs-scanraw.webp" alt="Two overlaid traces from 150 to 500 MHz, one from scan and one from scanraw, nearly coincident">
  <figcaption>The same sweep via <code>scan</code> and <code>scanraw</code>. Where they disagree by a constant, the scale factor is wrong for your firmware.</figcaption>
</figure>

Plotting the two on top of each other is the diagnostic: if they are offset by a constant number of dB, the scale factor is wrong for your firmware build. That is exactly the check the [tinySA Web](https://lc-linkous.github.io/tinysa-web/) tool later automated.

A note for Linux users, because it cost me a while: reading the serial buffer after `scanraw` is finicky in ways `scan` is not. Asking for data too quickly after the last read, or while the screen is frozen, can come back short or empty. The device needs to resume and re-measure between requests. The 4.0.0 library now treats a short or timed-out `scanraw` frame as a failure and logs it rather than handing you half a sweep.

## 4. Clean up the `:` artifact

On some firmware builds a malformed value like `:.000000e-01` appears in scan output now and then. The `:` is ASCII `0x3A`, one past `9`: the firmware overflowed a single-digit slot where it meant to write `10`. The library's parsing substitutes a value near the noise floor so the data stays numeric, but that leaves a sharp downward spike in the trace.

Two ways to smooth it, with very different results:

```python
def median_filter(x, k=5):          # pure numpy; edge-padded so length is kept
    xp = np.pad(x, k // 2, mode="edge")
    return np.array([np.median(xp[i:i + k]) for i in range(len(x))])

def moving_average(x, k=5):
    xp = np.pad(x, k // 2, mode="edge")
    return np.convolve(xp, np.ones(k) / k, mode="valid")

power = np.array(power)
med = median_filter(power)          # removes isolated spikes, keeps edges
avg = moving_average(power)         # smears the spike into its neighbors

for y, label in [(power, "raw"), (med, "median"), (avg, "moving average")]:
    plt.plot(freqs / 1e6, y, label=label)
plt.legend(); plt.show()
```

<figure>
  <img src="/media/imgs/posts/tinysa-ex4-filters.webp" alt="Three traces of the same sweep: raw with a sharp spike, median-filtered with the spike removed, and moving-average with the spike spread into a dip">
  <figcaption>Raw, median-filtered, and moving-average versions of the same scan. The median filter removes the artifact; the moving average spreads it out.</figcaption>
</figure>

The median filter is the right tool for isolated spikes: it drops the outlier and leaves the real signal alone. The moving average is included as a cautionary example, because it is the first thing most people reach for and it turns one bad sample into five slightly-wrong ones.

## 5. A waterfall

Repeat example 2 on a timer, stack the results, and you have a waterfall: frequency across, time down, color for power. This is the view that makes intermittent signals, drift, and duty cycles obvious in a way a single trace never does.

```python
import time
from datetime import datetime

rows, stamps = [], []
for _ in range(60):
    raw = tsa.scan(start, stop, pts, 2)
    tsa.resume()
    rows.append([float(l.split()[0]) for l in raw.decode().splitlines() if l.strip()])
    stamps.append(datetime.now())
    time.sleep(1.0)

fig, ax = plt.subplots()
im = ax.pcolormesh(freqs / 1e6, range(len(rows)), np.array(rows), shading="auto")
ax.set_xlabel("MHz"); ax.set_ylabel("scan #")
fig.colorbar(im, label="dBm")
plt.show()
```

<figure>
  <img src="/media/imgs/posts/tinysa-ex5-waterfall.webp" alt="Waterfall plot with frequency on the x axis, scan number on the y axis, and power as colour">
  <figcaption>Sixty one-second scans stacked into a waterfall.</figcaption>
</figure>

The README has a second version of this that redraws live as scans arrive, using matplotlib's animation support, and a sixth example that finds peaks in a range. The same loop, with `csv.writer` in place of `rows.append`, is how you log a measurement to a file for later; that example is in the README too.

## Where this goes

These five are the core of what the library does: get a measurement off the device, know what frequencies it belongs to, get it fast when speed matters, clean it, and watch it over time. Everything else in the library is parameter setting (`rbw`, `set_sweep_center`, `set_attenuation`, markers, the signal generator) that wraps around that core. The device-side commands are documented on the [official wiki](https://www.tinysa.org/wiki/); the library's command list is cross-referenced to it so the two can be read together.

---

*Update, October 2026.* The code above is written against tsapython 4.0.0, which is what is on PyPI now; the original 2025 scripts used the same calls with a flat single-class module. Since then the library has grown device profiles (so a command the connected model lacks is refused before it is sent), structured logging, and a hardware-free test suite. If a snippet here disagrees with the README, the README wins.

*This post was written in 2025 and released publicly in August 2025.*

</div>
