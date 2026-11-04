# Traditional Chinese browser variant

Based on the supplied Fullscreen Browser 104.4 package. Adds unmodified Noto Sans CJK TC Regular under OFL 1.1 (see OFL-Noto.txt), and installs the font into the browser profile before Chromium starts. No changes to overlay.squashfs or user browser settings.

To retain login and display pairing across restarts, enable Persistent Profile in the package setup and restart the setup/device. Default setup still does not persist profiles.

Use a distinct imported package/setup for initial testing. This variant has not been verified on a physical info-beamer device. Test font appearance, selected language, navigation and pairing on the target device.
