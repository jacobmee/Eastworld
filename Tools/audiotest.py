import pyaudio

p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    print((i,dev['name'],dev['maxInputChannels']))

    try:
        if p.is_format_supported(rate=44100,  # Sample rate
                               input_device=dev['index'],
                               input_channels=dev['maxInputChannels'],
                               input_format=pyaudio.paInt16):
            print '44100 - Yay!'
    except ValueError as err:
        print("OS error: {0}".format(err))

    try:
        if p.is_format_supported(rate=16000,  # Sample rate
                               input_device=dev['index'],
                               input_channels=dev['maxInputChannels'],
                               input_format=pyaudio.paInt16):
            print '16000 - Yay!'
    except ValueError as err:
        print("OS error: {0}".format(err))

    try:
        if p.is_format_supported(rate=8000,  # Sample rate
                               input_device=dev['index'],
                               input_channels=dev['maxInputChannels'],
                               input_format=pyaudio.paInt16):
            print '8000 - Yay!'
    except ValueError as err:
        print("OS error: {0}".format(err))


dev = p.get_device_info_by_index(0)
print(dev['name'],dev['maxInputChannels'])

if p.is_format_supported(16000,  # Sample rate
                         input_device=dev['index'],
                         input_channels=dev['maxInputChannels'],
                         input_format=pyaudio.paInt16):
    print 'Yay!'