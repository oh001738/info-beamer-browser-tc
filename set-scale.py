import os, ibquery
IS_DRM = os.path.exists('/sys/bus/platform/drivers/vc4-drm')
try:
    if IS_DRM:
        ib = ibquery.InfoBeamerQuery("127.0.0.1")
        display = ib.display

        fd = display[0] # only look at first or only display
        ib_width = fd['x2'] - fd['x1']
        ib_height = fd['y2'] - fd['y1']

        with open("/sys/class/graphics/fb0/virtual_size", "rb") as f:
            fb_width, fb_height = [int(val) for val in f.read().strip().split(',')]

        scale = min(float(fb_width / ib_width), float(fb_height / ib_height))
    else:
        scale = 1.0

    with open('display-scale', 'wb') as f:
        f.write('%f' % scale)
except:
    # If info-beamer is down, don't do anything
    pass
