import os
import socket
import struct

# These constants map to constants in the Linux kernel. This is a crappy
# way to get at them, but it'll do for now.
RTMGRP_LINK = 1

RTM_NEWLINK = 16
RTM_DELLINK = 17

IFLA_IFNAME = 3
IFF_RUNNING = 0x40
IFF_LOWER_UP = 0x10000
# Create the netlink socket and bind to RTMGRP_LINK,
s = socket.socket(socket.AF_NETLINK, socket.SOCK_RAW, socket.NETLINK_ROUTE)
s.bind((os.getpid(), RTMGRP_LINK))

while True:
    data = s.recv(65535)
    msg_len, msg_type, flags, seq, pid = struct.unpack("=LHHLL", data[:16])
    if msg_type != RTM_NEWLINK:
        print  "New link!"

    data = data[16:]

    family, _, if_type, index, flags, change = struct.unpack("=BBHiII", data[:16])

    print "family = " +str(family)
    print "if_type = " + str(if_type)
    print "index = " + str(index)
    print "flags = " +str(flags)
    print  "change = "+ str(change)

    # Crude check but will do for now
    if_running_flag = flags&IFF_RUNNING
    if_lower_up_flag = flags&IFF_LOWER_UP

    print if_running_flag
    print if_lower_up_flag
    if not if_running_flag|if_lower_up_flag:
      print "Interface went down"
    else:
      print "Interface came up" 
    continue 
