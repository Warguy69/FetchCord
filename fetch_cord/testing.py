# import shit as usual
import os, sys, json
from fetch_cord.args import parse_args
from fetch_cord.bash import exec_bash
from fetch_cord.out import cpumodel, cpuvendor, gpuvendor, sysosid
from fetch_cord.debugger import test_debug
if os.name != "nt":
    from fetch_cord.out import wmid, deid, termid, shellid, sysosid, hostline, termline

elif os.name == "nt":
    from fetch_cord.out import moboline

# macOS hardwawre

def laporp(product):
    if product[0:7] == "MacBook":
        devicetype = "laptop"
    else:
        devicetype = "desktop"
    return devicetype

def get_ver():
    return os.popen("sw_vers -productVersion").read()

def get_product():
    return os.popen("sysctl -n hw.model").read()

def get_icon(ver):
    try:
        bigicon = versions[ver[0:5]]
    except KeyError:
        bigicon = "bigslurp"
        print("Unsupported MacOS version")
    return bigicon
    # this is staying
def iUnity(wmid):
    # this is to check wether the user is actually using unity
    # or using unity as an xdg value to fix issues with electron apps
    if wmid.lower() == "compiz":
        desktopid = "unity"
    else:
        desktopid = wmid
    return desktopid

def get_infos():
    try:
        import importlib.resources as pkg_resources
    except ImportError:
        # Try backported to PY<37 `importlib_resources`.
        import importlib_resources as pkg_resources
    import fetch_cord.ressources as ressources

    with pkg_resources.open_text(ressources, 'infos.json') as f:
        infos = json.load(f)

    return infos

infos = get_infos()

amdcpus = infos["amdcpus"]
intelcpus = infos["intelcpus"]
gpus = infos["gpus"]
distros = infos["distros"]
versions = infos["versions"]
windowmanagers = infos["windowmanagers"]
desktops = infos["desktops"]
terminals = infos["terminals"]
shells = infos["shells"]
hosts= infos["hosts"]
motherboards= infos["motherboards"]
hostlist = infos["hostlist"]
terminallist = infos["terminallist"]

# desktops
if os.name != "nt" and deid == "unity":
    iUnity(wmid)

args = parse_args()


def get_host(hosts):
    hostsplit = hostline[0].split()
    hostid = []
    for line in range(len(hostsplit)):
        if hostsplit[line] in hostlist:
            hostid.append(hostsplit[line].rstrip('\n'))
    try:
        hostid = hostid[0]
    except IndexError:
        hostid = []
        pass
    # try to get MacBook hostid
    if not hostid:
        hostjoin = ' '.join(hostline)
        for numsplit in range(len(hostjoin)):
            if not hostjoin[numsplit].isdigit():
                hostid.append(hostjoin[numsplit])
        hostid = ''.join(hostid)
        hostid = hostid.split()[1]
    return hostid


def get_mobo(moboline):
        mobosplit = moboline[0].split()
        moboid = []
        for line in range(len(mobosplit)):
            if mobosplit[line] in hostlist:
                moboid.append(mobosplit[line].rstrip('\n'))
        try:
            moboid = moboid[0]
        except IndexError:
            moboid = ""
            pass
        return moboid

if args.terminal and args.terminal in terminallist:
    termid = args.terminal
    termline[0] = "Terminal: %s" % args.terminal

elif args.terminal and args.termninal not in terminallist:
    print("\nInvalid terminal, only %s are supported.\n"
            "Please make a github issue if you would like to have your terminal added.\n"
            "https://github.com/MrPotatoBobx/FetchCord" % terminallist)
    sys.exit(1)


def get_termappid(terminals, termid):
    return terminals[termid.lower()]


def get_shell_id(shells, shellid):
    shellid = shellid.lower()
    if shellid in shells:
        shell = shellid
    else:
        print("Unknown shell, contact us on github to resolve this.")
        shell = "unknown"
    return shell


def get_hostappid(hosts):
    return hosts[hostid.lower()]


def get_moboid(motherboards):
    return motherboards[moboid.lower()]


def get_desktopid(deid, wmid):

    deid = deid.lower()
    wmid = wmid.lower()

    if deid != "n/a" and deid in desktops:
        desktopid = deid

    elif deid == "n/a" and wmid in windowmanagers:
        desktopid = wmid
    else:
        print("Unknown DE/WM, contact us on github to resolve this.")
        desktopid = 'unknown'
    return desktopid

def get_appid(distros, sysosid):
    return distros[sysosid.lower()]


def get_cpuappid(cpuvendor, cpumodel, amdcpus, intelcpus):
    if cpuvendor == "AMD":
        cpuappid = amdcpus[cpumodel.lower()]
    elif cpuvendor in ["Intel", "Intel(R)", "Pentium"]:
        cpuappid = intelcpus[cpumodel.lower()]
    else:
        cpuappid = '742887089179197462'
    return cpuappid


def get_gpuid(gpuvendor):
    gpuvendor = gpuvendor.lower()
    if gpuvendor in gpus:
        gpuid = gpuvendor
    else:
        print("Unknown GPU, contact us on github to resolve this.")
        gpuid = 'unknown'
    return gpuid


def get_host_or_mobo(motherboards, hosts):
    if os.name != "nt" and hostline:
        return get_host(hosts)

    elif os.name == "nt" and moboline:
        return get_mobo(moboline)


if sysosid.lower() == "macos":
    devicetype = "N/A"
    bigicon = "unknown"
    ver = get_ver()
    get_icon(ver)
    product = get_product()
    laporp(product)

gpuid = get_gpuid(gpuvendor)
shell = get_shell_id(shells, shellid)

moboid = "Motherboard: N/A"
hostid = "Host: N/A"


if os.name != "nt":
    desktopid = get_desktopid(deid, wmid)
    try:
        hostid = get_host_or_mobo(motherboards, hosts)
        hostappid = get_hostappid(hosts)
    except KeyError:
        print("Unknown Host, contact us on github to resolve this.(Keyerror)")
        hostappid = "742887089179197462"
    try:
        termappid = get_termappid(terminals, termid)
    except KeyError:
        print("Unsupported Terminal. contact us on github to resolve this.(Keyerror)")
        termappid = '745691250186911796'

try:
    moboid = get_host_or_mobo(motherboards, hosts)
except KeyError:
    print("Unknown Motherboard, contact us on github to resolve this.(Keyerror)")
    moboid = "unknown"

#try:
#    hostid = get_host_or_mobo(motherboards, hosts)
#except KeyError:
#    hostid = ""

try:
    appid = get_appid(distros, sysosid)
except KeyError:
    print("Unsupported Distro, contact us on the GitHub page to resolve this.(keyerror)")
    appid = '742993278143692821'

try:
    cpuappid = get_cpuappid(cpuvendor, cpumodel, amdcpus, intelcpus)
except KeyError:
    print("unknown CPU, contact us on github to resolve this.(Keyerror)")
    cpuappid = '742887089179197462'

if args.debug:
    test_debug(deid, wmid, termid, shellid, moboid, gpuvendor, cpumodel, hostid)
