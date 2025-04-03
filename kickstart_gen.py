import os
import shutil

#Copy of skeleton kickstart file
source_skel = "Skel_Rocky9ks.cfg"

destination_ks = "Rocky9ks.cfg"

with open(source_skel, 'r') as file:
    lines = file.readlines()

# Modify the x-th line (0-based index)
lines[10] = "network  --bootproto=static --device=ens18 --gateway=192.168.1.1 --ip=192.168.1.114 --nameserver=8.8.8.8,8.8.4.4 --netmask=255.255.255.0 --activate" + "\n"

with open(destination_ks, 'w') as file:
    file.writelines(lines)
