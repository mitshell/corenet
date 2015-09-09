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
from libmich.mobnet.MME import *
from libmich.mobnet.AuC import AuC
from libmich.mobnet.GTPmgr import ARPd, GTPUd, TCPSYNACK
from libmich.mobnet.utils import mac_aton

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
    # ARP resolver for the PGW on SGi
    ARPd.GGSN_ETH_IF = 'eth0'
    ARPd.GGSN_MAC_ADDR = '08:00:00:01:02:03'
    ARPd.GGSN_IP_ADDR = '192.168.1.100'
    # IP given to UE on SGi
    ARPd.SUBNET_PREFIX = '192.168.1'
    ARPd.IP_POOL = []
    for ue_config in UE.values():
        ARPd.IP_POOL.append(ue_config['IP'])
    # IPv4 1st hop after PGW on SGi
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
    GTPUd.BLACKHOLING = 'ext' # only traffic to local LAN will be forwarded
    GTPUd.WL_ACTIVE = True # excepted DNS and NTP request to the Internet which will be handled too
    GTPUd.WL_PORTS = [('UDP', 53), ('UDP', 123)]
    
    ### MME config ###
    MMEd.ConfigS1 = {
    'MMEname': 'MichTelecomMME', # optional
    'ServedGUMMEIs': [
        {'servedPLMNs': [bytes(PLMN('00101'))],
         'servedGroupIDs': ['\x00\x01'],
         'servedMMECs': ['\x01']}
        ], # mandatory, at least 1
    'RelativeMMECapacity': 20, # mandatory, 0 < X < 255
    'MMERelaySupportIndicator': None, # optional
    'CriticalDiagnostics': None, # optional, 'true' otherwise
    }
    ENBd.TRACE = True # trace all S1 eNB-related procedures
    UEd.TRACE_S1 = True # trace all S1 UE-related procedures
    UEd.TRACE_NAS = True # trace all NAS procedures
    UEd.NASSEC_MAC = True # enforce NAS security
    UEd.NASSEC_ULCNT = True # enforce NAS UL count
    UEd.AUTH_POL_ATT = 1 # attach authentication policy
    UEd.AUTH_POL_TAU = 1 # TAU authentication policy
    UEd.AUTH_POL_SERV = 10 # service request authentication policy
    UEd.AUTH_AMF = b'\x80\x00' # Authentication Management Field
    UEd.SMC_IMEI_POL = 1 # request IMEISV only once during security mode ctrl
    UEd.SMC_EEA = [0, 1, 2, 3] # encryption algorithm priority: 0:None, 1:SNOW, 2:AES, 3:ZUC
    UEd.SMC_EIA = [1, 2, 3] # integrity protection algorithm priority: 0:None (emergency call only), 1:SNOW, 2:AES, 3:ZUC
    UEd.ESM_APN_DEF = 'corenet' # default APN
    UEd.ESM_PDN = {
        'corenet': {
            'IP':[1, '0.0.0.0'], # PDN type (1:IPv4, 2:IPv6, 3:IPv4v6), UE IP@ will be set at runtime
            'DNS':['192.168.1.1', '8.8.8.8'], # 2 IP@ for DNS servers
            'QCI': 9, # QoS class id (9: internet browsing), NAS + S1 parameter
            'PriorityLevel': 15, # no priority (S1 parameter)
            'PreemptCap': 'shall-not-trigger-pre-emption', # or 'may-trigger-pre-emption' (S1 parameter)
            'PreemptVuln': 'not-pre-emptable', # 'pre-emptable' (S1 parameter)
            },
        } # list of configured APN
    
    # start AuC, ARPd and GTPUd, MMEd
    log('\n\n\n', withdate=False)
    log('--------########<<<<<<<<////////:::::::: CORENET ::::::::\\\\\\\\\\\\\\\\>>>>>>>>########--------')
    log('...')
    AUCd = AuC()
    GTPd = GTPUd() # this starts ARPd automatically
    MME = MMEd(config={'server':('10.1.1.1', 36412),
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
