# Import cool new rpc module that gives us more control and gets rid of headaches :)
from pypresence import Presence, exceptions
import time
import sys
import os
import psutil
# import info about system
from fetch_cord.args import parse_args
from fetch_cord.config import ConfigError, load_config
from fetch_cord.bash import BashError, exec_bash
from fetch_cord.testing import gpuid, cpuappid, appid, desktopid, termappid, hostappid, shellid, moboid
from fetch_cord.debugger import run_rpc_debug
from fetch_cord.out import sysosline, sysosid, memline, cpuinfo, neofetch, diskline, hostline,\
    gpuinfo, packagesline, kernelline, shell_line, fontline, termline, lapordesk, resline, \
    themeline, batteryline, dewmid, moboline, neofetchwin


uptime = psutil.boot_time()
args = parse_args()


def main():
    if not neofetchwin and not hostline and args.nodistro and args.noshell and args.nohardware:
        print("ERROR: no hostline is available!")
        sys.exit(1)
    # printing info with debug switch
    if args.debug:
        if os.name != "nt":
            run_rpc_debug(uptime=uptime, appid=appid, cpuappid=cpuappid, termappid=termappid,
                          packagesline=packagesline, hostline=hostline, hostappid=hostappid)
        else:
            run_rpc_debug(uptime=uptime, appid=appid, cpuappid=cpuappid)
        config = get_config()
        enter_cycle(config, gpuinfo, memline, cpuinfo,
               diskline, batteryline, packagesline, sysosid,
               neofetchwin, termline, shell_line, hostline, resline,
               kernelline, sysosline, packagesline)


def first_connect():
    try:
        client_id = appid
        RPC = Presence(client_id)
        RPC.connect()
        print("RPC Connection Successful.")
    except ConnectionRefusedError:
        rpc_tryconnect(RPC)


print("Connecting")
try:
    time.sleep(5)
except KeyboardInterrupt:
    print("Stopping connection.")
    sys.exit(0)
# discord uses unix time to interpret time for rich presnse, this is uptime in unix time
start_time = int(uptime)


def rpc_tryconnect(RPC):
    while True:
        try:
            RPC.connect()
            break
        except ConnectionRefusedError:
            print("RPC connection refused (is Discord open?); trying again in 30 seconds")
            time.sleep(30)


def rpc_tryclear(RPC):
    try:
        RPC.clear(pid=os.getpid())
    except exceptions.InvalidID:
        pass


def rpc_tryupdate(RPC, state, details, large_image, large_text, small_image, small_text, start):

    # 128 Char limit
    if state :
        state = state[:128]
    if details:
        details = details[:128]
    if large_text:
        large_text = large_text[:128]
    if small_text:
        small_text = small_text[:128]

    try:
        RPC.update(state=state, details=details, large_image=large_image,
                   large_text=large_text, small_image=small_image, small_text=small_text,
                   start=start)
    # ConnectionResetError is here to avoid crashing if Discord is still just starting
    except (ConnectionResetError, exceptions.InvalidID):
        pass


def get_config():
    try:
        config = load_config()
    except ConfigError as e:
        print("Error loading config file, using default values." % str(e))
    return config


def custom_time():
    ctime = int(args.time)
    time.sleep(ctime)


def cycle(config, gpuinfo, memline, cpuinfo, diskline, batteryline, pacakgesline, sysosid, neofetchwin,
        termline, shell_line, hostline, resline, kernelline, sysosline, packagesline):
    if args.poll_rate:
        rate = int(args.poll_rate)
    else:
        rate = 3
    loop = 0
    while True:
        if sysosid.lower() == "macos":
            from fetch_cord.testing import devicetype, product, bigicon, ver
            client_id = '740822755376758944'  # macos appid for discord rpc
            if args.debug:
                print("runmac")
                print("devicetype: %s" % devicetype)
                print("product %s" % product)
                print("bigicon: %s" % bigicon)
                print("ver: %s" % ver)
                print("uptime: %s" % uptime)
                print("client_id: %s" % client_id)
            RPC = Presence(client_id)
            rpc_tryconnect(RPC)
            rpc_tryupdate(RPC,
                          state=packagesline,  # update state as packages
                          details=kernelline,  # update details as kernel
                          large_image=bigicon,  # set icon
                          large_text=sysosline,  # set large icon text
                          small_image=devicetype,  # set small image icon
                          small_text=product,  # set small image text
                          start=start_time)
            if args.time:
                custom_time()
            elif args.nohost and args.nohardware and args.noshell:
                time.sleep(9999)
            else:
                time.sleep(30)
            rpc_tryclear(RPC)


# cycle 0


        if not args.nodistro and not neofetchwin and sysosid.lower() != "macos":
            top_line = config["cycle_0"]["top_line"]
            if top_line == "kernel":
                top_line = ''.join(kernelline)
            else:
                top_line = packagesline
            bottom_line = config["cycle_0"]["bottom_line"]
            if bottom_line == "kernel":
                bottom_line = ''.join(kernelline)
            else:
                bottom_line = ''.join(packagesline)
            de_wm_icon = config["cycle_0"]["de_wm_icon"]
            if de_wm_icon == "on":
                de_wm_icon = ''.join(desktopid)
            else:
                de_wm_icon = "off"
            if args.debug:
                print("cycle 0")
            client_id = appid
            RPC = Presence(client_id)
            rpc_tryconnect(RPC)
            rpc_tryupdate(RPC,
                          state=bottom_line,
                          details=top_line,
                          large_image="big",
                          large_text=''.join(sysosline),
                          small_image=de_wm_icon,
                          small_text=dewmid,
                          start=start_time)
            if args.debug:
                print("appid: %s" % client_id)
            config_time = config["cycle_0"]["time"]
            if args.time:
                custom_time()
            elif args.nohost and args.nohardware and args.noshell:
                time.sleep(9999)
            elif config_time:
                time.sleep(int(config_time))
            else:
                time.sleep(30)
            rpc_tryclear(RPC)


    # cycle 1


        if not args.nohardware and not neofetchwin:
            top_line = config["cycle_1"]["top_line"]
            if top_line == "gpu":
                top_line = gpuinfo
            elif top_line == "cpu":
                top_line = cpuinfo
            elif top_line == "mem":
                top_line = memline
            elif top_line == "disk":
                top_line = diskline
            bottom_line = config["cycle_1"]["bottom_line"]
            if bottom_line == "gpu":
                bottom_line = gpuinfo
            elif bottom_line == "cpu":
                bottom_line = cpuinfo
            elif bottom_line == "mem":
                bottom_line = memline
            elif bottom_line == "disk":
                bottom_line = diskline
            gpu_icon = config["cycle_1"]["gpu_icon"]
            if gpu_icon == "on":
                gpu_icon = gpuid
            else:
                gpu_icon = "off"
            if args.debug:
                print("cycle 1")
            client_id = cpuappid
            RPC = Presence(client_id)
            rpc_tryconnect(RPC)
            rpc_tryupdate(RPC,
                          state=bottom_line,
                          details=top_line,
                          large_image="big",
                          large_text=cpuinfo,
                          small_image=gpu_icon,
                          small_text=gpuinfo,
                          start=start_time)
            if args.debug:
                print("appid: %s" % client_id)
            config_time = config["cycle_1"]["time"]
            if args.time:
                custom_time()
            elif args.nodistro and args.noshell and args.nohost:
                time.sleep(9999)
            elif config_time:
                time.sleep(int(config_time))
            else:
                time.sleep(30)
            rpc_tryclear(RPC)


    # cycle 2


        if not args.noshell and not neofetchwin:
            top_line = config["cycle_2"]["top_line"]
            if top_line == "font":
                top_line = ''.join(termline)
            elif top_line == "shell":
                top_line = ''.join(shellid)
            elif top_line == "theme":
                top_line = ''.join(themeline)
            bottom_line = config["cycle_2"]["bottom_line"]
            if bottom_line == "font":
                bottom_line = ''.join(termline)
            elif bottom_line == "shell":
                bottom_line = ''.join(shell_line)
            elif bottom_line == "theme":
                bottom_line = ''.join(themeline)
            shell_icon = config["cycle_2"]["shell_icon"]
            if shell_icon == "on":
                shell_icon = shellid
            else:
                shell_icon = "off"
            if args.debug:
                print("cycle 2")
            client_id = termappid
            RPC = Presence(client_id)
            rpc_tryconnect(RPC)
            rpc_tryupdate(RPC,
                          state=bottom_line,
                          details=top_line,
                          large_image="big",
                          large_text=''.join(termline),
                          small_image=shell_icon,
                          small_text=''.join(shell_line),
                          start=start_time)
            if args.debug:
                print("appid: %s" % client_id)
            config_time = config["cycle_2"]["time"]
            if args.time:
                custom_time()
            elif args.nodistro and args.nohardware and args.nohost:
                time.sleep(9999)
            elif config_time:
                time.sleep(int(config_time))
            else:
                time.sleep(30)
            rpc_tryclear(RPC)


    # cycle 3


        if not args.nohost and not neofetchwin and sysosid.lower() != "macos":
            if hostline:
                top_line = config["cycle_3"]["top_line"]
                if top_line == "battery":
                    top_line = ''.join(batteryline)
                elif top_line == "host":
                    top_line = ''.join(hostline)
                elif top_line == "resolution":
                    top_line = ''.join(resline)
                bottom_line = config["cycle_3"]["bottom_line"]
                if bottom_line == "resolution":
                    bottom_line = ''.join(resline)
                elif bottom_line == "host":
                    bottom_line = ''.join(hostline)
                elif bottom_line == "battery":
                    bottom_line = ''.join(batteryline)
                lapordesk_icon = config["cycle_3"]["lapordesk_icon"]
                if lapordesk_icon == "on":
                    lapordesk_icon = lapordesk
                else:
                    lapordesk_icon = "off"
                if args.debug:
                    print("cycle 3")
                client_id = hostappid
                RPC = Presence(client_id)
                rpc_tryconnect(RPC)
                rpc_tryupdate(RPC,
                              state=''.join(resline),
                              details=''.join(batteryline),
                              large_image="big",
                              large_text=''.join(hostline),
                              small_image=lapordesk_icon,
                              small_text=lapordesk,
                              start=start_time)
                if args.debug:
                    print("appid: %s" % client_id)
                config_time = config["cycle_3"]["time"]
                if args.time:
                    custom_time()
                elif args.nodistro and args.nohardware and args.noshell:
                    time.sleep(9999)
                elif config_time:
                    time.sleep(int(config_time))
                else:
                    time.sleep(30)
            rpc_tryclear(RPC)


        if args.pause_cycle:
            if args.debug:
                print("pause_cycle")
            if args.time:
                custom_time()
            else:
                time.sleep(30)

        if loop == rate and not args.nohardware and not args.nodistro and not args.nohost:

            cpuline, gpuline, termline, fontline, wmline, radgpuline, \
                shell_line, kernelline, sysosline, moboline, neofetchwin,\
                deline, batteryline, resline, themeline, hostline, memline, packagesline, diskline, baseinfo = neofetch(
                    loop)

            from fetch_cord.checks import get_cpuinfo, get_gpuinfo
            from fetch_cord.out import primeoffload, sysosid, amdgpurenderlist, laptop, primeoffload

            memline = ''.join(memline)
            packagesline = ''.join(packagesline)
            batteryline = ''.join(batteryline)
            diskline = '\n'.join(diskline)

            cpuinfo = get_cpuinfo(cpuline)
            gpuinfo = "GPU: N/A"
            for line in range(len(gpuline)):
                if sysosid.lower() != "macos" and "NVIDIA" in gpuline[line]:
                    gpuinfo = get_gpuinfo(primeoffload, gpuline,
                                      laptop, sysosid, amdgpurenderlist)


        if neofetchwin:
            if args.debug:
                print("w_cycle 0")
            client_id = appid
            RPC = Presence(client_id)
            rpc_tryconnect(RPC)
            rpc_tryupdate(RPC,
                      state=sysosline,
                      details=memline,
                      large_image="big",
                      large_text=sysosline,
                      small_image=moboid,
                      small_text=moboline,
                      start=start_time)
            if args.debug:
                print("appid: %s" % client_id)
            if args.time:
                custom_time()
            elif args.nohardware:
                time.sleep(9999)
            else:
                time.sleep(30)
            rpc_tryclear(RPC)
        loop += 1
        if loop == rate:
            loop = 0


def enter_cycle(config, gpuinfo, memline, cpuinfo, diskline, batteryline, pacakgesline, sysosid,
        neofetchwin, termline, shell_line, hostline, resline, kernelline, sysosline, packagesline):
    try:
        first_connect()
        cycle(config, gpuinfo, memline, cpuinfo, diskline, batteryline, pacakgesline, sysosid,
                    neofetchwin, termline, shell_line, hostline, resline, kernelline, sysosline, packagesline)
    except (KeyboardInterrupt, ConnectionResetError):
        if KeyboardInterrupt:
            print("Closing connection.")
            sys.exit(0)
        elif ConnectionResetError:
            rpc_tryconnect(RPC)

