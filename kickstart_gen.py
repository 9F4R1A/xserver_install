#!/usr/bin/env python
import ipaddress
import os
import shutil

virtual = None

ans_virt = input("The installation is virtual or physical?:(v/p) ")
ans_part = input("Full partition config?:(y/n) ")
if ans_virt.lower() == "v":
    virtual = True
elif ans_virt.lower() == "p":
    virtual = False
else:
    print("ERROR: invalid input")
    raise SystemExit(1)

if ans_part.lower() == "y":
    part = True
elif ans_part.lower() == "n":
    part = False
else:
    print("ERROR: invalid input")
    raise SystemExit(1)

#Copy of skeleton kickstart file
source_skel = "Skel_Rocky9ks.cfg"
keyfile = "key.pub"
destination_ks = "Rocky9ks.cfg"

if virtual == True and part == False:
    ans_ipaddr = input("what is the ip address for installation?:(x.x.x.x) ")
    try:
        ipaddr = ipaddress.ip_address(ans_ipaddr)
    except ValueError:
        print("ERROR: invalid input")
        raise SystemExit(1)
    ans_netmask = input("what is the netmask?:(x.x.x.x) ")
    try:
        ipnmask = ipaddress.ip_address(ans_netmask)
    except ValueError:
        print("ERROR: invalid input")
        raise SystemExit(1)
    ans_gw = input("what is the gateway?:(x.x.x.x) ")
    try:
        ipgw = ipaddress.ip_address(ans_gw)
    except ValueError:
        print("ERROR: invalid input")
        raise SystemExit(1)
    try:
        with open(source_skel, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("File Skel_Rocky9ks.cfg not found!")
    
    try:
        with open(keyfile, 'r') as file:
            keylines = file.readlines()
    except FileNotFoundError:
        print("File key.pub not found!")

    # Modify the x-th line (0-based index)
    lines[10] = "network  --bootproto=static --device=ens18 --gateway=" + ans_gw + " --ip=" + ans_ipaddr + " --nameserver=8.8.8.8,8.8.4.4 --netmask=" + ans_netmask + " --activate" + "\n"
    
    lines[26] = "ignoredisk --only-use=sda" + "\n"
    lines[28] = "bootloader --append=\" crashkernel=auto\" --location=mbr --boot-drive=sda" + "\n"
    lines[30] = "clearpart --all --initlabel --drives=sda" + "\n"
    lines[32] = "part /boot --fstype=\"xfs\" --ondisk=sda --size=1024" + "\n"
    lines[33] = "part pv.01 --fstype=\"lvmpv\" --ondisk=sda --size=1 --grow" + "\n"
    lines[34] = "volgroup rl --pesize=4096 pv.01" + "\n"
    lines[35] = "logvol swap --fstype=\"swap\" --size=2098 --name=swap --vgname=rl" + "\n"
    lines[36] = "logvol / --fstype=\"xfs\" --grow --size=1024 --name=root --vgname=rl" + "\n"
    lines[73] = "echo \"" + keylines[0] + "\" >> /root/.ssh/authorized_keys" + "\n"
    with open(destination_ks, 'w') as file:
        file.writelines(lines)

elif virtual == True and part == True:
    ans_ipaddr = input("what is the ip address for installation?:(x.x.x.x) ")
    try:
        ipaddr = ipaddress.ip_address(ans_ipaddr)
    except ValueError:
        print("ERROR: invalid input")
        raise SystemExit(1)
    ans_netmask = input("what is the netmask?:(x.x.x.x) ")
    try:
        ipnmask = ipaddress.ip_address(ans_netmask)
    except ValueError:
        print("ERROR: invalid input")
        raise SystemExit(1)
    ans_gw = input("what is the gateway?:(x.x.x.x) ")
    try:
        ipgw = ipaddress.ip_address(ans_gw)
    except ValueError:
        print("ERROR: invalid input")
        raise SystemExit(1)
    try:
        with open(source_skel, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("File Skel_Rocky9ks.cfg not found!")
    
    try:
        with open(keyfile, 'r') as file:
            keylines = file.readlines()
    except FileNotFoundError:
        print("File key.pub not found!")

    # Modify the x-th line (0-based index)
    lines[10] = "network  --bootproto=static --device=ens18 --gateway=" + ans_gw + " --ip=" + ans_ipaddr + " --nameserver=8.8.8.8,8.8.4.4 --netmask=" + ans_netmask + " --activate" + "\n"

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
    lines[73] = "echo \"" + keylines[0] + "\" >> /root/.ssh/authorized_keys" + "\n"
    with open(destination_ks, 'w') as file:
        file.writelines(lines)

elif virtual == False:
    ans_ipaddr = input("what is the ip address for installation?:(x.x.x.x) ")
    try:
        ipaddr = ipaddress.ip_address(ans_ipaddr)
        ipaddress.ip_network
    except ValueError:
        print("ERROR: invalid input")
        raise SystemExit(1)
    ans_netmask = input("what is the netmask?:(x.x.x.x) ")
    try:
        ipnmask = ipaddress.ip_address(ans_netmask)
    except ValueError:
        print("ERROR: invalid input")
        raise SystemExit(1)
    ans_gw = input("what is the gateway?:(x.x.x.x) ")
    try:
        ipgw = ipaddress.ip_address(ans_gw)
    except ValueError:
        print("ERROR: invalid input")
        raise SystemExit(1)
    ans_card = input("what is the card interface?:(ex.ens18) ")
    
    try:
        with open(source_skel, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("File Skel_Rocky9ks.cfg not found!")
    
    try:
        with open(keyfile, 'r') as file:
            keylines = file.readlines()
    except FileNotFoundError:
        print("File key.pub not found!")

    # Modify the x-th line (0-based index)
    lines[10] = "network  --bootproto=static --device=" + ans_card + " --gateway=" + ans_gw + " --ip=" + ans_ipaddr + " --nameserver=8.8.8.8,8.8.4.4 --netmask=" + ans_netmask + " --activate" + "\n"

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
    lines[73] = "echo \"" + keylines[0] + "\" >> /root/.ssh/authorized_keys" + "\n"
    with open(destination_ks, 'w') as file:
        file.writelines(lines)
