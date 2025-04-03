import os
import shutil

virtual = True

#Copy of skeleton kickstart file
source_skel = "Skel_Rocky9ks.cfg"

destination_ks = "Rocky9ks.cfg"

if virtual == True:
    with open(source_skel, 'r') as file:
        lines = file.readlines()

    # Modify the x-th line (0-based index)
    lines[10] = "network  --bootproto=static --device=ens18 --gateway=192.168.1.1 --ip=192.168.1.114 --nameserver=8.8.8.8,8.8.4.4 --netmask=255.255.255.0 --activate" + "\n"
    
    lines[26] = "ignoredisk --only-use=sda" + "\n"
    lines[28] = "bootloader --append=\" crashkernel=auto\" --location=mbr --boot-drive=sda" + "\n"
    lines[30] = "clearpart --all --initlabel --drives=sda" + "\n"
    lines[32] = "part /boot --fstype=\"xfs\" --ondisk=sda --size=1024" + "\n"
    lines[33] = "part pv.01 --fstype=\"lvmpv\" --ondisk=sda --size=1 --grow" + "\n"
    lines[34] = "volgroup rl --pesize=4096 pv.01" + "\n"
    lines[35] = "logvol swap --fstype=\"swap\" --size=2098 --name=swap --vgname=rl" + "\n"
    lines[36] = "logvol / --fstype=\"xfs\" --grow --size=1024 --name=root --vgname=rl" + "\n"
    with open(destination_ks, 'w') as file:
        file.writelines(lines)
elif virtual == False:
    with open(source_skel, 'r') as file:
        lines = file.readlines()

    # Modify the x-th line (0-based index)
    lines[10] = "network  --bootproto=static --device=ens18 --gateway=192.168.1.1 --ip=192.168.1.114 --nameserver=8.8.8.8,8.8.4.4 --netmask=255.255.255.0 --activate" + "\n"

    lines[41] = "ignoredisk --only-use=nvme0n1" + "\n"
    lines[43] = "clearpart --none --initlabel" + "\n"
    lines[45] = "part /boot/efi --fstype=\"efi\" --ondisk=nvme0n1 --size=5124 --fsoptions=\"umask=0077,shortname=winnt\"" + "\n"
    lines[46] = "part /boot --fstype=\"xfs\" --ondisk=nvme0n1 --size=512" + "\n"
    lines[47] = "part pv.560 --fstype=\"lvmpv\" --ondisk=nvme0n1 --size=799752" + "\n"
    lines[48] = "volgroup rl --pesize=4096 pv.560" + "\n"
    lines[49] = "logvol /opt --fstype=\"xfs\" --size=225280 --name=opt --vgname=rl" + "\n"
    lines[50] = "logvol /app --fstype=\"xfs\" --size=358400 --name=app --vgname=rl" + "\n"
    lines[51] = "logvol swap --fstype=\"swap\" --size=6144 --name=swap --vgname=rl" + "\n"
    lines[52] = "logvol / --fstype=\"xfs\" --size=153600 --name=root --vgname=rl" + "\n"
    lines[53] = "logvol /tmp --fstype=\"xfs\" --size=5120 --name=tmp --vgname=rl" + "\n"
    lines[54] = "logvol /home --fstype=\"xfs\" --size=51200 --name=home --vgname=rl" + "\n"
    with open(destination_ks, 'w') as file:
        file.writelines(lines)
