#!/bin/bash
# run vncserver @ :64
# FreshBooks/QuickBooks script will use this in order to download files successfully
IS_VNC_RUNNING=$(ps aux | grep "Xtightvnc" | grep -v "grep")
if [ "$IS_VNC_RUNNING" != "" ]; then
  echo "VNC Server is running."
else
  echo "VNC Server is not running. Starting VNC Server..."
  vncserver :64
fi

exit 0
