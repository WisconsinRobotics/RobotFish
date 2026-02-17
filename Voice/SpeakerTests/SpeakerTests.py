# Source - https://stackoverflow.com/a/43947830
# Posted by Logic1
# Retrieved 2026-02-16, License - CC BY-SA 3.0

import pyaudio

p = pyaudio.PyAudio()
for i in range(p.get_device_count()):#list all available audio devices
  dev = p.get_device_info_by_index(i)
  print((i,dev['name'],dev['maxInputChannels']))
