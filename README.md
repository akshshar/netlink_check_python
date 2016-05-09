# netlink_check_python

This is quick and dirty python script that creates a log event when an interface goes up or down.
For this purpose, the script opens a netlink socket and binds to RTMGRP_LINK in the userspace.
This way each link up/down event will create an RTM_NEWLINK event where RTM_NEWLINK=16 (hard coded).

(All the constants are mapped to values defined here http://www.tsri.com/jeneral/init/include/linux/rtnetlink.h/source/SOURCE-rtnetlink.h.html)

It's a blocking script that will output whenever there is a link up/down event and will report the interface associated with the event.
To run it:

```shell
    git clone https://github.com/akshshar/netlink_check_python.git

    cd netlink_check_python/

    python netlink_rtmgrp.py 
```


To test it, try an ifconfig up/down on any linux interface:

```shell
bash:~$ ifconfig br3 up
bash:~$ ifconfig br3 down
bash:~$ 


bash:~/netlink_check_python$ python netlink_rtmgrp.py 
link up/down event!
Interface br3 came up
link up/down event!
Interface br3 went down

```
