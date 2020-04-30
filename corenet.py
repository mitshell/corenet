#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#/**
# * Software Name : corenet 
# * Version : 0.2
# *
# * Copyright 2015. Benoit Michau. ANSSI.
# * Copyright 2020. Benoit Michau. P1Sec.
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
import os, sys
from time import sleep
from IPython.terminal.embed import InteractiveShellEmbed
#
from pycrate_core.repr          import *
from pycrate_corenet.utils      import *
from pycrate_corenet.Server     import CorenetServer
from pycrate_corenet.ServerGTPU import ARPd, GTPUd, MOD, DNSRESP, TCPSYNACK, BLACKHOLE_LAN, BLACKHOLE_WAN
from pycrate_corenet.ServerAuC  import AuC
from pycrate_corenet.ServerSMS  import SMSd
from pycrate_corenet.HdlrHNB    import HNBd
from pycrate_corenet.HdlrENB    import ENBd
from pycrate_corenet.HdlrGNB    import GNBd
from pycrate_corenet.HdlrUE     import UEd
from pycrate_corenet.HdlrUEIuCS import UEIuCSd, UEMMd, UECCd, UESSd
from pycrate_corenet.HdlrUEIuPS import UEIuPSd, UEGMMd, UESMd
from pycrate_corenet.HdlrUESMS  import UESMSd
from pycrate_corenet.HdlrUES1   import UES1d, UEEMMd, UEESMd
from pycrate_corenet.HdlrUENG   import UENGd
from pycrate_corenet import ProcCNHnbap
from pycrate_corenet import ProcCNRua
from pycrate_corenet import ProcCNRanap
from pycrate_corenet import ProcCNS1ap
from pycrate_corenet import ProcCNNgap
from pycrate_corenet import ProcCNMM
from pycrate_corenet import ProcCNSMS
from pycrate_corenet import ProcCNGMM
from pycrate_corenet import ProcCNSM
from pycrate_corenet import ProcCNEMM
from pycrate_corenet import ProcCNESM


#------------------------------------------------------------------------------#
# configuration for connecting 3G HomeNodeBs
#------------------------------------------------------------------------------#
# IP, port is for listening for SCTP connections from HNBs
# GTPU is for listening for GTPU connections from HNB
# Warning: currently, only IPv4 is supported as GTPU address
CorenetServer.SERVER_HNB['IP']   = '127.1.1.1'
CorenetServer.SERVER_HNB['port'] = 29169 # SCTP port for HNBAP and RUA protocols
CorenetServer.SERVER_HNB['GTPU'] = '127.1.1.1'
# uncomment to deactivate the HNB server
#CorenetServer.SERVER_HNB = {}

#------------------------------------------------------------------------------#
# configuration for connecting LTE eNodeBs
#------------------------------------------------------------------------------#
# IP, port is for listening for SCTP connections from eNBs
# GTPU is for listening for GTPU connections from eNB
# Warning: currently, only IPv4 is supported as GTPU address
CorenetServer.SERVER_ENB['IP']   = '127.2.1.1'
CorenetServer.SERVER_ENB['port'] = 36412 # SCTP port for S1AP protocol
CorenetServer.SERVER_ENB['GTPU'] = '127.2.1.1'
# uncomment to deactivate the ENB server
#CorenetServer.SERVER_ENB = {}

#------------------------------------------------------------------------------#
# configuration for connecting 5G gNodeBs
#------------------------------------------------------------------------------#
# IP, port is for listening for SCTP connections from gNBs
# GTPU is for listening for GTPU connections from gNB
# Warning: currently, only IPv4 is supported as GTPU address
CorenetServer.SERVER_GNB['IP']   = '127.3.1.1'
CorenetServer.SERVER_GNB['port'] = 38412 # SCTP port for NGAP protocol
CorenetServer.SERVER_GNB['GTPU'] = '127.3.1.1'
# uncomment to deactivate the GNB server
#CorenetServer.SERVER_GNB = {}

#------------------------------------------------------------------------------#
# Authentication center configuration
#------------------------------------------------------------------------------#
# Milenage OP parameter (16 bytes)
AuC.OP = b'AAAAAAAAAAAAAAAA'
# path to the AuC.db file (here, this returns the path where corenet.py is)
AuC.AUC_DB_PATH = os.path.dirname(os.path.abspath( __file__ )) + os.sep


#------------------------------------------------------------------------------#
# GTPUd and ARPd configuration
#------------------------------------------------------------------------------#

### external interfaces (toward Internet or other service networks)

# ARPd interface info
ARPd.GGSN_ETH_IF     = 'eth0'
ARPd.GGSN_MAC_ADDR   = '08:00:00:01:02:03'
ARPd.GGSN_IP_ADDR    = '192.168.1.100'
# ARPd LAN prefix and router info
ARPd.SUBNET_PREFIX   = '192.168.1.0/24'
ARPd.ROUTER_MAC_ADDR = 'f4:00:00:01:02:03'
ARPd.ROUTER_IP_ADDR  = '192.168.1.1'
# set of IP addresses dedicated to UEs
ARPd.IP_POOL = set()
for i in range(149, 250):
    ARPd.IP_POOL.add('192.168.1.%i' % i)

# GTPUd interface info
GTPUd.EXT_IF         = ARPd.GGSN_ETH_IF
GTPUd.EXT_MAC_ADDR   = ARPd.GGSN_MAC_ADDR
# IPv6 network prefix
GTPUd.EXT_IPV6_PREF  = '2001:123:456:abcd'
# GTPUd BLACKHOLING feature
# to enable the blackholing of UE LAN / WAN traffic, set the appropriate flag(s)
GTPUd.BLACKHOLING    = 0
GTPUd.WL_ACTIVE      = False
#GTPUd.BLACKHOLING    = BLACKHOLE_WAN
#GTPUd.BLACKHOLING    = BLACKHOLE_LAN | BLACKHOLE_WAN
#GTPUd.WL_ACTIVE      = True
#GTPUd.WL_PORTS       = [('UDP', 53), ('UDP', 123)]
# GTPUd to generate statistics for each UE's source IP address
GTPUd.DPI            = True
# GTPUd to drop uplink packet with spoofed source IP address
GTPUd.DROP_SPOOF     = True


### internal interfaces (toward RAN equipments)

# GTPUd internal IP interfaces (do not change)
GTPUd.GTP_PORT       = 2152 # UDP port for GTP-U protocol
GTPUd.GTP_IF         = (CorenetServer.SERVER_HNB['GTPU'],
                        CorenetServer.SERVER_ENB['GTPU'],
                        CorenetServer.SERVER_GNB['GTPU'])


#------------------------------------------------------------------------------#
# global corenet telecom configuration
#------------------------------------------------------------------------------#
# main PLMN served
CorenetServer.PLMN = '00101'
#
# equivalent PLMNs served, used over S1, IuCS and IuPS
# None or list of PLMNs ['30124', '763326', ...]
CorenetServer.EQUIV_PLMN = None
#
# emergency number lists, used over S1, IuCS and IuPS
# None or list of 2-tuple [(number_category, number), ...]
# number_category is a set of strings: 'Police', 'Ambulance', 'Fire', 'Marine', 'Mountain'
# number is a digits string
# e.g.
#CorenetServer.EMERG_NUMS = [
#    ({'Police', 'Ambulance', 'Fire'}, '112112'),
#    ({'Marine', 'Mountain'}, '112113')]
CorenetServer.EMERG_NUMS = None


# Connection from RAN equipments:
# Home-NodeB, eNodeB and gNodeB indexed by their global ID
# (PLMN, CellId) for home-NodeB and eNodeB
# (PLMN, CellType, CellId) for gNodeB
# the RAN dict can be initialized with {(PLMN, *Cell*): None} here
# this provides a whitelist of allowed basestations.
CorenetServer.RAN = {}
#
# Otherwise, this is a flag to allow any RAN equipment to connect to the server
# in case its PLMN is in the RAN_ALLOWED_PLMN list.
# If enabled, RAN dict will be populated at runtime
    # If disabled, RAN keys (PLMN, *Cell*) needs to be setup by configuration (see above)
CorenetServer.RAN_CONNECT_ANY = True
#
# This is the list of accepted PLMN for RAN equipment connecting, 
# when RAN_CONNECT_ANY is enabled
CorenetServer.RAN_ALLOWED_PLMN = [CorenetServer.PLMN]


#------------------------------------------------------------------------------#
# AMF NG connection parameters
#------------------------------------------------------------------------------#
# AMF ID for each served PLMN
# PLMN (str): AMF ID 3-tuple (RegionID uint8, SetID uint10, Pointer uint6)
CorenetServer.AMF_GUAMI = {
    CorenetServer.PLMN: (1, 1, 0),
    }
#
# arbitrary dict of indexed slices identifiers
# S-NSSAI is at least an SST (uint8) and eventually an SD (uint24)
CorenetServer.AMF_SNSSAI = {
    0  : (0x00, ), # default S-NSSAI
    1  : (0x01, ),
    2  : (0x02, ),
    21 : (0x02, 0x000001),
    }
# list of slice supported for each served PLMN
CorenetServer.AMF_PLMNSupp = {
    CorenetServer.PLMN: [CorenetServer.AMF_SNSSAI[0]],
    #$plmn1: [CorenetServer.AMF_SNSSAI[1]],
    #$plmn2: [CorenetServer.AMF_SNSSAI[2], CorenetServer.AMF_SNSSAI[21]],
    }
#
# NG connection AMF parameters
CorenetServer.ConfigNG    = {
    'AMFName'             : 'CorenetAMF',
    'RelativeAMFCapacity' : 10,
    #'UERetentionInformation': 'ues-retained',
    }


#------------------------------------------------------------------------------#
# MME S1 connection parameters
#------------------------------------------------------------------------------#
# MME GroupID and Code
CorenetServer.MME_GID  = 1
CorenetServer.MME_CODE = 1
# S1 connection MME parameters
CorenetServer.ConfigS1 = {
    'MMEname': 'CorenetMME',
    'ServedGUMMEIs' : [
        {'servedPLMNs'   : [plmn_str_to_buf(CorenetServer.PLMN)],
         'servedGroupIDs': [uint_to_bytes(CorenetServer.MME_GID, 16)],
         'servedMMECs'   : [uint_to_bytes(CorenetServer.MME_CODE, 8)]}
        ],
    'RelativeMMECapacity': 10,
    'EquivPLMNList'      : CorenetServer.EQUIV_PLMN,
    'EmergNumList'       : CorenetServer.EMERG_NUMS,
    }

# dict of configured Packet Data Network for EPC, indexed by APN
#
# each PDN configuration is a dict with the following keys and values:
#   'QCI' : uint8 representing the global QoS for the default connection
#   'DNS' : tuple of DNS server addr (in PDNAddr format style: 
#           1->IPv4 2-tuple addr, 2->IPv6 2-tuple addr)
#   'PAP' : dict of {peerid : passwd}
#   'CHAP': not implemented
#   'MTU' : 2-tuple of uint or None (IPv4 link MTU, non-IP link MTU)
CorenetServer.ConfigPDN = {
    'corenet': {
        'QCI': 9,
        'DNS': ((1, '8.8.8.8'), # Google DNS servers
                (1, '8.8.4.4'),
                (2, '2001:4860:4860::8888'),
                (2, '2001:4860:4860::8844')),
        'MTU': (None, None),
        },
    }

# It is possible to set a wildcard config to accept any requested APN
# and use the given configuration with the connecting UE
CorenetServer.ConfigPDN['*'] = {
        'QCI': 9,
        'DNS': ((1, '8.8.8.8'), # Google DNS servers
                (1, '8.8.4.4'),
                (2, '2001:4860:4860::8888'),
                (2, '2001:4860:4860::8844')),
        'MTU': (None, None),
        }


#------------------------------------------------------------------------------#
# IuCS and IuPS connection parameters
#------------------------------------------------------------------------------#
# CS and PS parameters
CorenetServer.ConfigIuCS  = {
    'EquivPLMNList': CorenetServer.EQUIV_PLMN,
    'EmergNumList' : CorenetServer.EMERG_NUMS,
    }
CorenetServer.ConfigIuPS  = {
    'EquivPLMNList': CorenetServer.EQUIV_PLMN,
    'EmergNumList' : CorenetServer.EMERG_NUMS,
    }

# dict of configured Packet Data Protocol for the PS domain, indexed by APN
#
# each PDN configuration is a dict with the following keys and values:
#   'DNS' : tuple of DNS server addr (in PDNAddr format style: 
#           1->IPv4 2-tuple addr, 2->IPv6 2-tuple addr)
#   'PAP' : dict of {peerid : passwd}
#   'CHAP': not implemented
#   'MTU' : 2-tuple of uint or None (IPv4 link MTU, non-IP link MTU)
CorenetServer.ConfigPDP = {
    'corenet': {
        'DNS': ((1, '8.8.8.8'), # Google DNS servers
                (1, '8.8.4.4'),
                (2, '2001:4860:4860::8888'),
                (2, '2001:4860:4860::8844')),
        'MTU': (None, None),
        },
    }

# It is possible to set a wildcard config to accept any requested APN
# and use the given configuration with the connecting UE
CorenetServer.ConfigPDP['*'] = {
        'DNS': ((1, '8.8.8.8'), # Google DNS servers
                (1, '8.8.4.4'),
                (2, '2001:4860:4860::8888'),
                (2, '2001:4860:4860::8844')),
        'MTU': (None, None),
        }


#------------------------------------------------------------------------------#
# UE configuration
#------------------------------------------------------------------------------#
# Warning: (U)SIM IMSI / authentication keys need to be configured in AuC.db too

# dict of configured UE, indexed by IMSI
#
# each UE configuration is a dict with the following keys and values:
#   'USIM'  : bool, True if subscriber is equiped with a USIM (supports Milenage),
#             False if equiped with a SIM
#   'MSISDN': str of digits, phone number to be used for CS and SMS services 
#   'PDP'   : list of tuple with authorized PDP connections (3G),
#             each tuple being (APN (str), PDPType (1, 2 or 3), IPv4addr,
#                               IPv6 if PDPType is 2 or 3)
#   'PDN'   : list of tuple with authorized PDN connections (LTE),
#             each tuple being (APN (str), PDNType (1, 2 or 3), IPv4addr, 
#                               IPv6 /64 interface suffix if PDNType is 2 or 3)
#
#   for IPv4 addresses, take care to configure ARPd.IP_POOL correctly
#   for IPv6 addresses, no NDP proxies are yet run by corenet, this need to be 
#       setup independently
CorenetServer.ConfigUE = {
    '001010000000001': {
        'USIM'  : True,
        'MSISDN': '012345',
        'PDP'   : [('*', 1, '192.168.1.151'),
                   ('corenet', 3, '192.168.1.151', GTPUd.EXT_IPV6_PREF + ':0:1:0:97')],
        'PDN'   : [('*', 1, '192.168.1.151'),
                   ('corenet', 3, '192.168.1.151', '0:1:0:97')]
        },
    '001010000000002': {
        'USIM'  : True,
        'MSISDN': '012346',
        'PDP'   : [('*', 1, '192.168.1.152'),
                   ('corenet', 3, '192.168.1.152', GTPUd.EXT_IPV6_PREF + ':0:1:0:98')],
        'PDN'   : [('*', 1, '192.168.1.152'),
                   ('corenet', 3, '192.168.1.152', '0:1:0:98')]
        }
    }

# It is possible to set an IMSI filter to accept attachment from given IMSI,
# together with a wildcard config that will be applied to any accepted UE without 
# a proper config in CorenetServer.ConfigUE
# 
# Warning: for IMSI that are not preconfigured (no config in the AuC.db database),
# further UE-related procedure will fail because of missing crypto material.
# When an non-preconfigured UE attaches the CorenetServer, ConfigUE['*'] is used
# to provide a default config and need to be defined.
# Warning: when several UEs are connecting with this configuration, data and other
# services will likely fail (only MM, GMM, EMM could work properly).
#
# Use UE_ATTACH_FILTER = None to disable this permissive configuration
CorenetServer.UE_ATTACH_FILTER = '^00101'
CorenetServer.ConfigUE['*'] = {
        'USIM'  : True,
        'MSISDN': '000111',
        'PDP'   : [('*', 1, '192.168.1.149'),
                   ('corenet', 3, '192.168.1.149', GTPUd.EXT_IPV6_PREF + ':0:1:0:95')],
        'PDN'   : [('*', 1, '192.168.1.149'),
                   ('corenet', 3, '192.168.1.149', '0:1:0:95')]
        }

# global LTE NAS security algorithm priority configuration for the MME signalling service
# 0: null ciphering
# 1: SNOW-3G based, EEA1, EIA1
# 2: AES based, EEA2, EIA2
# 3: ZUC based, EEA3, EIA3
UEEMMd.SMC_EEA_PRIO = [0] # do not cipher NAS signalling
UEEMMd.SMC_EIA_PRIO = [2, 1]


#------------------------------------------------------------------------------#
# verbosity and debug levels
#------------------------------------------------------------------------------#

# services debug level
CorenetServer.DEBUG   = ('ERR', 'WNG', 'INF', 'DBG')
AuC.DEBUG             = ('ERR', 'WNG', 'INF', 'DBG')
ARPd.DEBUG            = ('ERR', 'WNG', 'INF', 'DBG')
GTPUd.DEBUG           = ('ERR', 'WNG', 'INF', 'DBG')
SMSd.DEBUG            = ('ERR', 'WNG', 'INF', 'DBG')
SMSd.TRACK_PDU        = True

# global HNBd debug level
HNBd.DEBUG            = ('ERR', 'WNG', 'INF', 'DBG')
HNBd.TRACE_ASN_HNBAP  = False
HNBd.TRACE_ASN_RUA    = False
HNBd.TRACE_ASN_RANAP  = False
HNBd.TRACK_PROC_HNBAP = True
HNBd.TRACK_PROC_RUA   = True
HNBd.TRACK_PROC_RANAP = True

# global ENBd debug level
ENBd.DEBUG = ('ERR', 'WNG', 'INF', 'DBG')
ENBd.TRACE_ASN_S1AP   = False
ENBd.TRACK_PROC_S1AP  = True

# global GNBd debug level
GNBd.DEBUG = ('ERR', 'WNG', 'INF', 'DBG')
GNBd.TRACE_ASN_NGAP   = True
GNBd.TRACK_PROC_NGAP  = True

# global UEd debug level
UEd.DEBUG  = ('ERR', 'WNG', 'INF', 'DBG')
# UE 3G
UEd.TRACE_RANAP_CS    = False
UEd.TRACE_RANAP_PS    = False
UEd.TRACE_NAS_CS      = True
UEd.TRACE_NAS_PS      = True
# UE 4G
UEd.TRACE_S1AP        = False
UEd.TRACE_NAS_EPS_SEC = False
UEd.TRACE_NAS_EPS     = True
# UE 5G
UEd.TRACE_NGAP        = False
UEd.TRACE_NAS_5GS_SEC = False
UEd.TRACE_NAS_5GS     = True
# UE SMS
UEd.TRACE_NAS_SMS     = True
#
# UE 3G
UEIuCSd.TRACK_PROC    = True
UEMMd.TRACK_PROC      = True
#UECCd.TRACK_PROC      = True
#UESSd.TRACK_PROC      = True
UESMSd.TRACK_PROC     = True
UEIuPSd.TRACK_PROC    = True
UEGMMd.TRACK_PROC     = True
UESMd.TRACK_PROC      = True
# UE 4G
UES1d.TRACK_PROC      = True
UEEMMd.TRACK_PROC     = True
UEESMd.TRACK_PROC     = True
# UE 5G
UENGd.TRACK_PROC      = True


#------------------------------------------------------------------------------#
# application launcher
#------------------------------------------------------------------------------#

def main():
    
    # start AuC, ARPd and GTPUd, MMEd
    log('\n\n\n', withdate=False)
    log('--------########<<<<<<<<////////:::::::: CORENET ::::::::\\\\\\\\\\\\\\\\>>>>>>>>########--------')
    
    # configure the CorenetServer reference to AuC, GTPUd and SMSRelay
    CorenetServer.AUCd  = AuC
    CorenetServer.GTPUd = GTPUd
    CorenetServer.SMSd  = SMSd
    
    # start the server
    Server = CorenetServer()
    sleep(0.1)
    
    # You can add modules to the GTPUd:
    # - TCPSYNACK module auto-answers to UE TCP-SYN packets
    # - DNSRESP module auto-answers to UE DNS requests
    # (do not forget to enable GTPUd.BLACKHOLING in this case)
    MOD.GTPUd = Server.GTPUd
    #Server.GTPUd.MOD = [DNSRESP, TCPSYNACK]
    Server.GTPUd.MOD = []
    
    def stop():
        Server.stop()
    
    # configure IPython corenet banner
    _ipy_banner = \
        'Corenet 0.2.0 loaded -- interactive mobile core network\n\n'\
        'ASN.1 modules: HNBAP, RUA, RANAP, S1AP, SS, RRC3G, RRCLTE, RRCNR and ASN_GLOBAL\n'\
        'ASN.1 PDU: PDU_HNBAP, PDU_RUA, PDU_RANAP, PDU_S1AP, PDU_NGAP, PDU_SS_Facility\n'\
        'NAS module for messages and IEs: NAS\n'\
        'Protocol procedures modules:\n'\
        '\t- ProcHnbap, ProcRua, ProcRanap, ProcS1ap, ProcNgap\n'\
        '\t- ProcMM, ProcSMS, ProcGMM, ProcSM, ProcEMM, ProcESM\n'\
        'Protocol stack classes (and attribute\'s names at runtime):\n'\
        '\t- HNBd\n'\
        '\t- ENBd\n'\
        '\t- GNBd\n'\
        '\t- UEd -> UEIuCSd (IuCS) -> UEMMd  (MM)\n'\
        '\t                        -> UESMSd (SMS)\n'\
        '\t      -> UEIuPSd (IuPS) -> UEGMMd (GMM)\n'\
        '\t                        -> UESMd  (SM)\n'\
        '\t      -> UES1d   (S1)   -> UEEMMd (EMM)\n'\
        '\t                        -> UESMSd (SMS)\n'\
        '\t                        -> UEESMd (ESM)\n'\
        '\t      -> UENGd   (NG)   -> None (yet)\n'\
        'Instances:\n'\
        '\t- Server: signalling server (instance of CorenetServer), \n'\
        '\t          handling instances of HNBd and ENBd under the .RAN attribute\n'\
        '\t          handling instances of UEd under the .UE attribute\n' \
        '\t- AUCd  : AuC Authentication center\n'\
        '\t- GTPUd : GTP-U tunnel manager\n'\
        '\t- SMSd  : SMS relay\n'\
        'Functions:\n'\
        '\t- show, hex, bin: to represent NAS messages and IEs\n'\
        '\t- sleep: to take a break !\n'\
        'Constants:\n'\
        '\t- BLACKHOLE_LAN, BLACKHOLE_WAN\n'
    
    # configure IPython kernel namespace
    _ipy_ns = {}
    
    # ASN.1 modules and PDU
    _ipy_ns['ASN_GLOBAL']   = S1AP.GLOBAL
    _ipy_ns['HNBAP']        = HNBAP
    _ipy_ns['RUA']          = RUA
    _ipy_ns['RANAP']        = RANAP
    _ipy_ns['S1AP']         = S1AP
    _ipy_ns['NGAP']         = NGAP
    _ipy_ns['SS']           = SS
    _ipy_ns['RRC3G']        = RRC3G
    _ipy_ns['RRCLTE']       = RRCLTE
    _ipy_ns['RRCNR']        = RRCNR
    _ipy_ns['PDU_HNBAP']    = PDU_HNBAP
    _ipy_ns['PDU_RUA']      = PDU_RUA
    _ipy_ns['PDU_RANAP']    = PDU_RANAP
    _ipy_ns['PDU_S1AP']     = PDU_S1AP
    _ipy_ns['PDU_NGAP']     = PDU_NGAP
    _ipy_ns['PDU_SS_Facility'] = PDU_SS_Facility
    # NAS module
    _ipy_ns['NAS']          = NAS
    # Protocols' procedures modules
    _ipy_ns['ProcHnbap']    = ProcCNHnbap
    _ipy_ns['ProcRua']      = ProcCNRua
    _ipy_ns['ProcRanap']    = ProcCNRanap
    _ipy_ns['ProcS1ap']     = ProcCNS1ap
    _ipy_ns['ProcNgap']     = ProcCNNgap
    _ipy_ns['ProcMM']       = ProcCNMM
    _ipy_ns['ProcSMS']      = ProcCNSMS
    #_ipy_ns['ProcCC']       = ProcCNCC
    #_ipy_ns['ProcSS']       = ProcCNSS
    _ipy_ns['ProcGMM']      = ProcCNGMM
    _ipy_ns['ProcSM']       = ProcCNSM
    _ipy_ns['ProcEMM']      = ProcCNEMM
    _ipy_ns['ProcESM']      = ProcCNESM
    # Protocol stack classes
    _ipy_ns['HNBd']         = HNBd
    _ipy_ns['ENBd']         = ENBd
    _ipy_ns['GNBd']         = GNBd
    _ipy_ns['UEd']          = UEd
    _ipy_ns['UEIuCSd']      = UEIuCSd
    _ipy_ns['UEMMd']        = UEMMd
    _ipy_ns['UESMSd']       = UESMSd
    _ipy_ns['UEIuPSd']      = UEIuPSd
    _ipy_ns['UEGMMd']       = UEGMMd
    _ipy_ns['UESMd']        = UESMd
    _ipy_ns['UES1d']        = UES1d
    _ipy_ns['UEEMMd']       = UEEMMd
    _ipy_ns['UEESMd']       = UEESMd
    _ipy_ns['UENGd']        = UENGd
    # servers' instances
    _ipy_ns['Server']       = Server
    _ipy_ns['GTPUd']        = Server.GTPUd
    _ipy_ns['AUCd']         = Server.AUCd
    _ipy_ns['SMSd']         = Server.SMSd
    # GTPUd blackholing
    _ipy_ns['BLACKHOLE_LAN'] = BLACKHOLE_LAN
    _ipy_ns['BLACKHOLE_WAN'] = BLACKHOLE_WAN
    # functions
    _ipy_ns['show']         = show
    _ipy_ns['hex']          = hex
    _ipy_ns['bin']          = bin
    _ipy_ns['sleep']        = sleep
    
    # interactive epc session
    ipshell = InteractiveShellEmbed(user_ns=_ipy_ns, \
                                    banner1=_ipy_banner, \
                                    exit_msg='leaving Corenet now...')
    ipshell()
    #
    # before exiting, we need to close everything properly
    stop()
    return 0

if __name__ == '__main__':
    sys.exit(main())
