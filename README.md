# r410-fan-controller
Python script to automate control the fan speeds of the Dell r410 11th generation server.

I use this on my FreeNAS/TrueNAS box. I placed the script on my windows share and used the FreeNAS UI to run the script on boot.

1) Tasks
2) Init/Shutdown Scripts
3) Add
4) Command
5) `nohup python /mnt/Test\ Storage/windowset/scripts/fan_controller.py > /var/log/fan-controller.log 2>&1 &`

Ensure you know what you are doing. Use at own risk. Manually controlling your fans could damage hardware or worse!
