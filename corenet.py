#!/usr/bin/python
# -*- coding: UTF-8 -*-
#/**
# * Software Name : corenet 
# * Version : 0.1.0
# *
# * Copyright © 2015. Benoit Michau. ANSSI.
# *
# * This program is free software: you can redistribute it and/or modify
# * it under the terms of the GNU General Public License version 2 as published
# * by the Free Software Foundation. 
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# * GNU General Public License for more details. 
# *
# * You will find a copy of the terms and conditions of the GNU General Public
# * License version 2 in the "license.txt" file or
# * see http://www.gnu.org/licenses/ or write to the Free Software Foundation,
# * Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA
# *
# *--------------------------------------------------------
# * File Name : corenet.py
# * Created : 2015-09-05
# * Authors : Benoit Michau 
# *--------------------------------------------------------
#*/

# IPython interactive shell
import sys
from time import sleep
from IPython.terminal.embed import InteractiveShellEmbed
#
from libmich.utils.repr import *
from libmich.formats.L3Mobile import parse_L3
from libmich.mobnet2.MME import *
from libmich.mobnet2.AuC import AuC
from libmich.mobnet2.GTPmgr import ARPd, GTPUd, TCPSYNACK
from libmich.mobnet2.utils import mac_aton

# list of UE IMSI and associated IP address
# those IMSI needs to be configured in libmich/mobnet/AuC.db too
UE = {'001010000000001': {'IP': '192.168.1.201'},
      '001010000000002': {'IP': '192.168.1.202'},
      }

def main():
    
    # debugging / tracing level
    AuC.DEBUG = ('ERR', 'WNG', 'INF')
    ARPd.DEBUG = ('ERR', 'WNG', 'INF')
    GTPUd.DEBUG = ('ERR', 'WNG', 'INF')
    MMEd.DEBUG = ('ERR', 'WNG', 'INF', 'DBG')
    MMEd.TRACE_SK = True
    MMEd.TRACE_ASN1 = True
    MMEd.TRACE_SEC = True
    MMEd.TRACE_NAS = True
    
    ### AuC config ###
    # authentication center
    AuC.OP = 'ffffffffffffffff'
    
    ### ARPd config ###
    # ARP resolver for the P-GW
    ARPd.GGSN_ETH_IF = 'eth0'
    ARPd.GGSN_MAC_ADDR = '08:00:00:01:02:03'
    ARPd.GGSN_IP_ADDR = '192.168.1.100'
    # IP given to UE
    ARPd.SUBNET_PREFIX = '192.168.1'
    ARPd.IP_POOL = []
    for ue_config in UE.values():
        ARPd.IP_POOL.append(ue_config['IP'])
    # IPv4 1st hop after GGSN
    ARPd.ROUTER_MAC_ADDR = 'f4:00:00:01:02:03'
    ARPd.ROUTER_IP_ADDR = '192.168.1.1'
    
    ### GTPUd config ###
    # GTP user-plane packets forwarder
    # internal interface (SGW S1U user-plane)
    GTPUd.INT_IP = '10.1.1.1'
    GTPUd.INT_PORT = 2152
    # GTP User-Plane handler external interface (PGW SGi)
    GTPUd.EXT_IF = ARPd.GGSN_ETH_IF
    GTPUd.GGSN_MAC_ADDR = ARPd.GGSN_MAC_ADDR
    # mobile traffic filtering
    GTPUd.BLACKHOLING = 'ext' # only traffic to local LAN will be handled
    GTPUd.WL_ACTIVE = True # excepted DNS and NTP request to the Internet which will be handled too
    GTPUd.WL_PORTS = [('UDP', 53), ('UDP', 123)]
    
    ### MME config ###
    # hardcode DNS servers to be signalled to UE
    for apn in UEd.ESM_PDN:
        UEd.ESM_PDN[apn]['DNS'][0] = '192.168.1.1'
        UEd.ESM_PDN[apn]['DNS'][1] = '8.8.8.8'
    
    # start AuC, ARPd and GTPUd, MMEd
    log('\n\n\n', withdate=False)
    log('--------########<<<<<<<<////////:::::::: CORENET ::::::::\\\\\\\\\\\\\\\\>>>>>>>>########--------')
    log('...')
    AUCd = AuC()
    GTPd = GTPUd() # this starts ARPd automatically
    MME = MMEd(config={'server':('127.0.1.100', 36412),
                       'ue': UE,
                       'enb': {},
                       })
    
    # add the TCPSYNACK module in GTPd (TCP SYN-ACK auto-answer to UE)
    TCPSYNACK.GTPUd = GTPd
    GTPd.MOD = [TCPSYNACK]
    #GTPd.MOD = []
    
    # configure MMEd IO to AuC and GTPUd
    MME.AUCd = AUCd
    MME.GTPd = GTPd
    
    def stop():
        AUCd.stop()
        GTPd.stop()
        MME.stop()
    
    # configure IPython corenet banner
    _ipy_banner = \
        'EPC 0.1.0 loaded -- interactive Evolved Packet Core\n' \
        'ASN.1 classes: ASN1Obj, PER, GLOBAL\n' \
        'Protocol stack classes: ENBd, UEd\n' \
        'instances:\n' \
        '\tMME: MME server, handling .UE and .ENB\n' \
        '\tAUCd: AuC Authentication center\n' \
        '\tGTPd: GTPU tunnel manager\n' \
        'functions:\n' \
        '\tstop: stops all 3 running instances\n' \
        '\tshow: nicely prints signalling packets\n' \
        '\tparse_L3: parses NAS-PDU\n' \
        'MME-initiated procedures:\n' \
        '\tIdentification, GUTIReallocation, Authentication, ' \
        'SecurityModeControl, EMMInformation, MMEDetach'
    
    # configure IPython kernel namespace
    _ipy_ns = {}
    _ipy_ns['GLOBAL'] = GLOBAL
    _ipy_ns['ASN1Obj'] = ASN1Obj
    _ipy_ns['PER'] = PER
    _ipy_ns['UEd'] = UEd
    _ipy_ns['ENBd'] = ENBd
    _ipy_ns['MME'] = MME
    _ipy_ns['AUCd'] = AUCd
    _ipy_ns['GTPd'] = GTPd
    _ipy_ns['show'] = show
    _ipy_ns['stop'] = stop
    _ipy_ns['parse_L3'] = parse_L3
    _ipy_ns['Identification'] = Identification
    _ipy_ns['GUTIReallocation'] = GUTIReallocation
    _ipy_ns['Authentication'] = Authentication
    _ipy_ns['SecurityModeControl'] = SecurityModeControl
    _ipy_ns['EMMInformation'] = EMMInformation
    _ipy_ns['MMEDetach'] = MMEDetach
    
    # interactive epc session
    ipshell = InteractiveShellEmbed(user_ns=_ipy_ns, \
                                    banner1=_ipy_banner, \
                                    exit_msg='leaving corenet now...')
    ipshell()
    #
    # before exiting, we need to close everything properly
    # MMEd, GTPUd, AuC ...
    AUCd.stop()
    GTPd.stop()
    MME.stop()
    #
    # exit the application
    sys.exit()

if __name__ == '__main__':
    main()
