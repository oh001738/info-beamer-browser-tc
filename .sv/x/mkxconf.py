#!/usr/bin/python
import json, os

config_json = os.path.join(os.environ['NODE_PATH'], 'config.json')
display_json = os.path.join(os.environ['NODE_PATH'], 'display.json')

IS_DRM = os.path.exists('/sys/bus/platform/drivers/vc4-drm')
USE_DRM = False

with open(config_json, 'rb') as f:
    rotation = json.load(f)['rotation']

with open('xorg.conf', 'wb') as config:
    if IS_DRM:
        def screen_resolution():
            with open("/sys/class/graphics/fb0/virtual_size", "rb") as f:
                return [int(val) for val in f.read().strip().split(',')]
        width, height = screen_resolution()

        # with open(display_json, 'rb') as f:
        #     display = json.load(f)

        # def screen_resolution():
        #     try:
        #         fd = display[0] # only look at first or only display
        #         width = fd['x2'] - fd['x1']
        #         height = fd['y2'] - fd['y1']
        #         return width, height
        #     except:
        #         return 1920, 1080

        # width, height = screen_resolution()

        # os.system("fbset -fb /dev/fb0 -g %(width)d %(height)d %(width)d %(height)d 16" % dict(
        #     width=width, height=height
        # ))
        # with open("/sys/class/graphics/fb0/virtual_size", "wb") as f:
        #     f.write("%d,%d" % (width, height))
        # with open("/sys/class/graphics/fb0/mode", "wb") as f:
        #     f.write("U:%dx%dp-0\n" % (width, height))


        config.write((("""
             Section "Monitor"
                Identifier "Monitor"
                Option "Rotate" "%(rotate)s"
             EndSection

             Section "Device"
                Identifier "Device"
                Driver "fbdev"
                Option "Rotate" "%(rotate_dev)s"
             EndSection

             Section "Screen"
                Identifier "Screen"
                Monitor "Monitor"
                SubSection "Display"
                   Modes "%(width)dx%(height)d"
                   Modes "U:%(width)dx%(height)d-0"
                EndSubSection
            EndSection
        """, """

            # Works, but cannot provide snapshots to the dashboard :(

            Section "Monitor"
               Identifier "HDMI-1"
               Option "Rotate" "%(rotate)s"
            EndSection
            Section "Monitor"
               Identifier "HDMI-2"
               Option "Rotate" "%(rotate)s"
            EndSection

            Section "OutputClass"
              Identifier "vc4"
              MatchDriver "vc4"
              Driver "modesetting"
              Option "PrimaryGPU" "true"
            EndSection

            Section "Device"
               Identifier "Device"
               Driver "modesetting"
               Option "AccelMethod" "none"
               Option "ShadowFB" "on"
               Option "Rotate" "%(rotate_dev)s"
            EndSection

            Section "Screen"
               Monitor "HDMI-1"
               Identifier "HDMI-1"
               SubSection "Display"
                  Modes "%(width)dx%(height)d"
               EndSubSection
            EndSection

            Section "Screen"
               Monitor "HDMI-2"
               Identifier "HDMI-2"
               SubSection "Display"
                  Modes "%(width)dx%(height)d"
               EndSubSection
            EndSection
        """)[USE_DRM]) % dict(
            rotate = {
                0: 'normal',
                90: 'right',
                180: 'inverted',
                270: 'left',
            }[rotation],
            rotate_dev = {
                0: 'off',
                90: 'CW',
                180: 'UD',
                270: 'CCW',
            }[rotation],
            width = width,
            height = height,
        ))
    elif rotation == 0:
        config.write("# empty")
    else:
        config.write("""
            Section "Device"
                Identifier "Device"
                Option "Rotate" "%(rotate)s"
            EndSection

            Section "Screen"
               Identifier "Screen"
               Device "Device"
            EndSection
        """ % dict(
            rotate = {
                90: 'CW',
                180: 'UD',
                270: 'CCW',
            }[rotation]
        ))
