import os
import socket
import struct

# Hard coded values to map to the linux kernel constants 
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
    if msg_type == RTM_NEWLINK:
        print  "link up/down event!"

    data = data[16:]

    family, _, if_type, index, flags, change = struct.unpack("=BBHiII", data[:16])

    # Crude check but will do for now
    if_running_flag = flags&IFF_RUNNING
    if_lower_up_flag = flags&IFF_LOWER_UP

    remaining = msg_len - 32
    data = data[16:]

    while remaining:
        rta_len, rta_type = struct.unpack("=HH", data[:4])

        if rta_len < 4:
            break

        rta_data = data[4:rta_len]

        increment = (rta_len + 3) & ~(3)
        data = data[increment:]
        remaining -= increment

        if rta_type == IFLA_IFNAME:
          if not if_running_flag|if_lower_up_flag:
            print "Interface %s went down" % rta_data
          else:
            print "Interface %s came up" % rta_data

    continue
