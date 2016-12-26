What is corenet
===============

Corenet is a minimal LTE / EPC core network. It implements the minimal set of 
functions to handle eNodeBs through an S1 interface, and UEs through NAS 
and GTPU interfaces:

```
          LTE-Uu                       S1                    SGi
UE <-----Radio/UP------> eNodeB <---GTPU/UP----> corenet <---UP---> LAN
UE <---Radio/RRC/NAS---> eNodeB <---S1AP/NAS---> corenet
                         eNodeB <-----S1AP-----> corenet
```

No other interfaces are supported by corenet (no interface to S-GW, P-GW, HSS, 
no support for GTP-C or Diameter interfaces, ...).
It has been successfully tested with the open-source Eurecom OpenAirInterface eNodeB, 
the commercial Amarisoft eNodeB, and handsets from multiple vendors (Qualcomm, 
Samsung, Mediatek, ...).


Installation
============


Operating system and Python version
------------------------------------

The application is made to work with Python 2.7, just like 
*libmich* library. Python 3 is not supported, mainly because libmich does not 
work with it.
It works on Linux, because of the need for SCTP support and Ethernet raw sockets. 
It may work on other UNIX-like system, but this has not been tested.


Dependencies
------------

The following libraries are required for corenet to work:
* [ipython](http://ipython.org/) is used to wrap the execution of corenet and
   to provide a friendly ipython-shell interface
* [pysctp](https://github.com/philpraxis/pysctp) is used to wrap the Linux
   kernel SCTP stack, and provides a Python API that is used by the MME server
* [pycrypto](https://www.dlitz.net/software/pycrypto/) is used for handling the
   AES computation for EEA2 / EIA2 and Milenage as provided in CryptoMobile
* [CryptoMobile](https://github.com/mitshell/CryptoMobile/) is used for handling
   Milenage and all EEA / EIA computations
* [libmich](https://github.com/mitshell/libmich/) contains all components needed
   for running an LTE / EPC core network

   
Installation
------------

After all dependencies have been installed, there is no further installation 
needed. The *corenet.py* file can be launched as is from the command line, 
after adapting its main settings.


Launch
------

You can launch the corenet application as is:
```bash
$ python ./corenet.py
S1AP: 894 objects loaded into GLOBAL
RRCLTE: 859 objects loaded into GLOBAL_RRCLTE
RRC3G: 4197 objects loaded into GLOBAL_RRC3G
EPC 0.2.0 loaded -- interactive Evolved Packet Core
ASN.1 classes: ASN1Obj, PER, GLOBAL
Protocol stack classes: ENBd, UEd
instances:
	MME: MME server, handling .UE and .ENB
	AUCd: AuC Authentication center
	GTPd: GTPU tunnel manager
	SMSd: SMS relay
functions:
	stop: stops all 3 running instances
	show: nicely prints signalling packets
	parse_L3: parses NAS-PDU
MME-initiated procedures:
	Identification, GUTIReallocation, Authentication, SecurityModeControl, EMMInformation, MMEDetach

In [1]: MME
Out[1]: <libmich.mobnet.MME.MMEd at 0x7fef648e86d0>

In [2]: MME.ENB
Out[2]: {('20869', '1a2d0'): <libmich.mobnet.ENBmgr.ENBd at 0x7fe0bb8b7d50>}

In [3]: MME.UE
Out[3]: {}

In [4]: MME.UEConfig
Out[4]: 
{'001010000000001': {'IP': '192.168.1.201', 'Num': '0001'},
 '001010000000002': {'IP': '192.168.1.202', 'Num': '0002'}}

In [5]: # A Sony handset has connected

In [6]: MME.UE
Out[6]: {'001010000000001': <libmich.mobnet.UEmgr.UEd at 0x7fe0bb9ac550>}

In [7]: sony = MME.UE['001010000000001']

In [8]: # Here is the list of signaling procedure run with the handset

In [9]: sony._proc
Out[9]: 
[<libmich.mobnet.UES1proc.InitialUEMessage at 0x7fe0bb676050>,
 <libmich.mobnet.UENASproc.Attach at 0x7fe0bf9c9f50>,
 <libmich.mobnet.UENASproc.Authentication at 0x7fe0bb6a0bd0>,
 <libmich.mobnet.UES1proc.DownlinkNASTransport at 0x7fe0bb694550>,
 <libmich.mobnet.UES1proc.UplinkNASTransport at 0x7fe0bb692f50>,
 <libmich.mobnet.UES1proc.DownlinkNASTransport at 0x7fe0bf9c9e90>,
 <libmich.mobnet.UES1proc.UplinkNASTransport at 0x7fe0bb690ad0>,
 <libmich.mobnet.UENASproc.SecurityModeControl at 0x7fe0bb6a7390>,
 <libmich.mobnet.UES1proc.DownlinkNASTransport at 0x7fe0bb68e390>,
 <libmich.mobnet.UES1proc.UplinkNASTransport at 0x7fe0bb68ebd0>,
 <libmich.mobnet.UENASproc.PDNConnectRequest at 0x7fe0bb67cfd0>,
 <libmich.mobnet.UENASproc.ESMInformation at 0x7fe0bb67cb10>,
 <libmich.mobnet.UES1proc.DownlinkNASTransport at 0x7fe0bb68e3d0>,
 <libmich.mobnet.UES1proc.UplinkNASTransport at 0x7fe0bb68eb90>,
 <libmich.mobnet.UENASproc.DefaultEPSBearerCtxtAct at 0x7fe0bba01490>,
 <libmich.mobnet.UES1proc.InitialContextSetup at 0x7fe0bb67a0d0>,
 <libmich.mobnet.UES1proc.UECapabilityInfoInd at 0x7fe0bb67a2d0>,
 <libmich.mobnet.UES1proc.UplinkNASTransport at 0x7fe0bb6a5150>,
 <libmich.mobnet.UES1proc.UplinkNASTransport at 0x7fe0bb693450>,
 <libmich.mobnet.UENASproc.PDNConnectRequest at 0x7fe0bba12dd0>,
 <libmich.mobnet.UENASproc.DefaultEPSBearerCtxtAct at 0x7fe0bba12c50>,
 <libmich.mobnet.UES1proc.ERABSetup at 0x7fe0bb8dc7d0>,
 <libmich.mobnet.UES1proc.UplinkNASTransport at 0x7fe0bb6a5390>]

In [10]: # We can access the PDU exchanged at the S1 layer and the NAS layer

In [11]: sony._proc[-1]._pdu
Out[11]: 
[(1470388288.693879,
  'UL',
  ('initiatingMessage',
   {'criticality': 'ignore',
    'procedureCode': 13,
    'value': ('UplinkNASTransport',
     {'protocolIEs': [...]})}))]

In [12]: sony._proc[-2]._pdu
Out[12]: 
[(1470388288.62925,
  'DL',
  ('initiatingMessage',
   {'criticality': 'reject',
    'procedureCode': 5,
    'value': ('E-RABSetupRequest',
     {'protocolIEs': [...]})})),
 (1470388288.685159,
  'UL',
  ('successfulOutcome',
   {'criticality': 'reject',
    'procedureCode': 5,
    'value': ('E-RABSetupResponse',
     {'protocolIEs': [...]})}))]

In [13]: sony._proc[-3]._pdu
Out[13]: 
[(1470388288.615469,
  'DL',
  <[ACTIVATE_DEFAULT_EPS_BEARER_CTX_REQUEST]: EBT(EPS Bearer Type):6, PD(Protocol Discriminator):'2 : EPS session management messages', TI(Procedure Transaction ID):2, Type():'193 : Activate default EPS bearer context request', EQoS(EPS QoS):<EPS QoS[EQoS]: L():1, V():'\t'>, APN(Access Point Name):<Access Point Name[APN]: L():6, V():'\x05 sony'>, PDNAddr(PDN Address):<PDN Address[PDNAddr]: L():5, V():'\x01\xc0\xa8\x01\xc9'>, ProtConfig(Protocol Configuration options):<Protocol Configuration options[ProtConfig]: ...>>),
 (1470388288.696052,
  'UL',
  <[ACTIVATE_DEFAULT_EPS_BEARER_CTX_ACCEPT]: EBT(EPS Bearer Type):6, PD(Protocol Discriminator):'2 : EPS session management messages', TI(Procedure Transaction ID):0, Type():'194 : Activate default EPS bearer context accept'>)]

In [14]: # The GTPd server provides the statistics of the connection made by the handset

In [15]: GTPd.stats
Out[15]: 
{'192.168.1.201': {'DNS': ['192.168.1.1'],
  'ICMP': [],
  'NTP': [],
  'TCP': [('172.217.18.232', 443),
   [...]
   ('54.72.204.20', 443)],
  'UDP': [('192.168.253.1', 53)],
  'alien': [],
  'resolved': ['www.googletagmanager.com',
   [...]
   'www.googleapis.com']}}

In [16]: # We can send an SMS from the handset, it is collected into the SMSd server (it is not forwarded)

In [17]: SMSd._SMQ
Out[17]: deque([<[SMS_SUBMIT]: TP_SRR(TP Status Report Request):'0 : A status report is not requested', TP_UDHI(TP User Data Header Indicator):0b0, TP_RP(TP Reply Path):'0 : TP Reply Path parameter is not set in this SMS SUBMIT/DELIVER', TP_VPF(TP Validity Period Format):'0 : TP VP field not present', TP_RD(TP Reject Duplicates):0b0, TP_MTI(TP Message Type Indicator):'1 : SMS-SUBMIT', TP_MR(TP Message Reference):9, TP_Destination_Address():<[TP_Destination_Address]: Length(length of digits):10, Ext(Extension):1, Type(Type of number):'0 : unknown', NumPlan(Numbering plan identification):'1 : ISDN / telephony numbering plan (E.164 / E.163)', Num():1234566789>, TP_PID():<[TP_PID]: Format():'0 : telematic indication', Telematic():'0 : no telematic interworking, but SME-to-SME protocol', Protocol():'0 : Short Message Type 0'>, TP_DCS():<[TP_DCS]: Group():'0 : General Data Coding', GroupExt():'0 : uncompressed - no class meaning', Charset():'0 : GSM 7 bit default alphabet', Class():0, IndActive():0, Reserved():0, IndType():'0 : Voicemail Message Waiting'>, TP_VP():'', TP_UDL(User Data Length (in character)):13, TP_UD():Hello corenet>])

In [18]: # And we can send an SMS from the SMSd server

In [19]: SMSd.send_text('0001', 'hello sony', fromnum='0011223344')

In [20]: # We can do much more, by acting e.g. with the 'sony' instance and the many methods it exposes, all logs are available in the /tmp/corenet.log file, and the verbosity is configurable for each class and instances, through the MME.DEBUG, MME.TRACE_*, ENBd.TRACE_* and UEd.TRACE_* attributes

In [20]: sony.page() # when the handset gets disconnected, it is possible to page it

In [21]: exit()
leaving corenet now...
```

You need to have the right to open raw Ethernet socket: for this you need to be 
root (e.g. *sudo python corenet.py*), or to set the CAP_NET_RAW capability for 
the Python interpreter (*sudo setcap cap_net_raw+eip /usr/lib/python27*).

From here, the application is waiting for eNodeB to connect, and then for UE to attach.
All logs are written to the */tmp/corenet.log* file.

```bash
[2016-08-05 11:08:40.637] --------########<<<<<<<<////////:::::::: CORENET ::::::::\\\\\\\\>>>>>>>>########--------
[2016-08-05 11:08:40.637] ...
[2016-08-05 11:08:40.637] [INF] [AuC] Starting AuC
[2016-08-05 11:08:40.646] [INF] [GTPUd] GTPU handler started
[2016-08-05 11:08:40.673] [INF] [ARPd] ARP resolver started
[2016-08-05 11:08:40.716] [INF] [MME: 001.01.0001.01] SCTP server listening on address ('10.1.1.1', 36412)
[2016-08-05 11:09:46.512] [INF] [MME: 001.01.0001.01] [eNB: ('00101', '10000')] S1AP stream established
[2016-08-05 11:11:21.809] [WNG] [MME: 001.01.0001.01] [UE: 001010000000001] mobile using an unknown security context
[2016-08-05 11:11:22.209] [WNG] [MME: 001.01.0001.01] [UE: 001010000000001] [(7, 82): Authentication] authentication failure: '21 : Synch failure'
[2016-08-05 11:11:22.848] [WNG] [MME: 001.01.0001.01] [UE: 001010000000001] mobile using an unknown security context
[2016-08-05 11:11:23.272] [INF] [GTPUd] setting GTP tunnel for mobile with IP 192.168.1.201
[2016-08-05 11:11:23.285] [INF] [MME: 001.01.0001.01] [UE: 001010000000001] [(2, 193): DefaultEPSBearerCtxtAct] default bearer activated for EPS bearer ID 5, APN sony
[2016-08-05 11:11:23.285] [INF] [MME: 001.01.0001.01] [UE: 001010000000001] [(7, 65): Attach] completed, GUTI reallocated, TMSI 0e040ec5
[2016-08-05 11:11:28.685] [INF] [GTPUd] setting GTP tunnel for mobile with IP 192.168.1.201
[2016-08-05 11:11:28.696] [INF] [MME: 001.01.0001.01] [UE: 001010000000001] [(2, 193): DefaultEPSBearerCtxtAct] default bearer activated for EPS bearer ID 6, APN sony
[2016-08-05 11:14:45.202] [INF] [MME: 001.01.0001.01] [UE: 001010000000001] [ENB (S1AP): ('20869', '1a2d0')] [18: UEContextReleaseRequest] Cause: ('radioNetwork', 'user-inactivity')
[2016-08-05 11:14:45.216] [INF] [GTPUd] unsetting GTP tunnel for mobile with IP 192.168.1.201
[2016-08-05 11:14:53.252] [INF] [GTPUd] setting GTP tunnel for mobile with IP 192.168.1.201
[2016-08-05 11:14:53.252] [WNG] [GTPUd] unknown GTP TEID from RAN: 2075244062
[2016-08-05 11:14:53.253] [INF] [GTPUd] setting GTP tunnel for mobile with IP 192.168.1.201
[2016-08-05 11:15:41.228] [INF] [SMSRelay] received SMS_SUBMIT for 1234566789: Hello corenet
[2016-08-05 11:17:17.854] [INF] [SMSRelay] sending SMS text (charset 0) from 0011223344 to 0001: hello sony
[2016-08-05 11:17:33.974] [INF] [MME: 001.01.0001.01] [UE: 001010000000001] [(7, 69): UEDetach] type: '11 : Combined EPS/IMSI detach; UE switch off'
[2016-08-05 11:17:33.974] [INF] [GTPUd] unsetting GTP tunnel for mobile with IP 192.168.1.201
[2016-08-05 11:18:02.748] [INF] [AuC] AuC stopped
[2016-08-05 11:18:02.833] [INF] [ARPd] ARP resolver stopped
[2016-08-05 11:18:02.957] [INF] [GTPUd] GTPU handler stopped
[2016-08-05 11:18:03.413] [INF] [MME: 001.01.0001.01] SCTP server stopped
```


License
=======

The application is licensed under GPLv2: all licensed files have an header
making it self-explanatory.



Contact and support
==================

As the unique developper of the application, I am the only person to contact:
michau \[dot\] benoit \[at\] gmail \[dot\] com.
Every feedback is very welcomed ; however, because the application remains a 
complex piece of software, I may not be able to answer every request. 



Technical aspects
=================


Basic configuration
-------------------

First of all, it is required to have USIM cards, that are personalized with 
known secret keys K. When this is done, IMSI, K and SQN (authentication counter)
need to be configured in the *libmich/mobnet/AuC.db* file accordingly.

Then, several components of corenet have to be configured:
* AuC: the authentication center, needs to be configured according to USIM cards
  * AuC.OP: MNO OP authentication parameter
  * AuC.db file: list of {IMSI, K, SQN} of USIM cards
* ARPd: the ARP resolver which handles ARP resolution on behalf of UE on SGi
  * ARPd.GGSN_ETH_IF: ethernet interface name on SGi
  * ARPd.GGSN_MAC_ADDR: ethernet MAC address of the interface on SGi
  * ARPd.GGSN_IP_ADDR: IP address of the interface on SGi
  * ARPd.SUBNET_PREFIX: IP prefix of the LAN on SGi (/24 only)
  * ARPd.IP_POOL: list of IP addresses allocated to UE
  * ARPd.ROUTER_MAC_ADDR: Ethernet MAC address of the IP router on the LAN on SGi
  * ARPd.ROUTER_IP_ADDR: IP address of the IP router on the LAN on SGi
* GTPUd: the GTP User-Plane packets forwarder
  * GTPUd.INT_IP: IP address that terminates GTP tunnel initiated by eNodeBs on S1
  * GTPUd.INT_PORT: UDP port that serves GTPU tunnels on S1 (keeps the default 
   value, 2152)
  * GTPUd.EXT_IF: ethernet interface name on SGi (same as ARPd.GGSN_ETH_IF)
  * GTPUd.GGSN_MAC_ADDR: ethernet MAC address of the interface on SGi (same as 
   ARPd.GGSN_MAC_ADDR)
* SMSRelay: the SMS Relay which receives and sends SMS
  * SMSRelay.SMSC_RP_NUM: SMS Relay phone number
  * SMSRelay.TIMEZONE: timezone offset

MME and UE-related parameters may also be configured: see information below
on the software architecture, to know what parameters you may want to change.
All configuration parameters have to be edited directly in the *corenet.py* 
file directly.

Software architecture
---------------------

The MMEd instance is the main component. It runs the SCTP server and the ASN.1 
encoder / decoder for S1AP PDU. It handles a list of connected eNodeBs with
its *ENB* attribute (dict {enb global id: ENBd instance}), and a list of 
attached UEs with its *UE* attribute (dict {imsi: UEd instance}).
Moreover, it has a *GTPd* class attribute, which references the GTPUd instance, 
and an *AUCd* class attribute, which references the AuC instance. Finally, the 
MME has some attributes containing configuration information: *ConfigS1* (MME 
identification information used on S1AP), *TA* (list of Tracking Area served by 
connected eNodeBs) , *UEConfig* (list of IMSI / IP addresses of UE allowed to 
attach).

The MMEd class is defined in *libmich/mobnet/MME.py*.

MMEd class attributes:
* DEBUG: tuple of str, levels of debug info to display in the log file
* TRACE_SK: bool, to trace all sctp sockets IO in the log file
* TRACE_ASN1: bool, to trace all S1AP signalling message IO in the log file
* TRACE_SEC: bool, to trace all NAS security headers IO in the log file
* TRACE_NAS: bool, to trace all NAS EMM / ESM message IO in the log file
* SERVER_BUFLEN: int, default to 2048, SCTP socket server buffer length
* SERVER_MAXCLI: int, default to 16, SCTP socket server maximum number of clients
* SCHED_RES: float, default to 0.1, time resolution (in sec.) for the MME scheduler
* SCHED_UE_TO: bool, to regularly verify if UE procedures are in timeout and potentially end them
* GTPd: reference to a GTPUd instance
* AUCd: reference to an AuC instance
* ConfigS1: dict, MME configuration information, signalled to eNodeBs in the S1 setup procedure

MMEd instance attributes:
* ENB: dict {eNB global id: ENBd instance}, lists all connected eNodeBs
* TA: dict {TA: set of eNB global id}, lists all tracking area served by connected eNodeB
* UEConfig: dict {imsi: dict of UE parameters}, UE IP address is configured here
* UE: dict {imsi: UEd instance}, lists all UE attached
* UE_MME_ID: dict {mme_ue_s1ap_id: imsi}, lists all attributed MME_UE_S1AP_ID
* TMSI: dict {tmsi: imsi}, lists all attributed TMSI

An ENBd instance is responsible for dealing with the S1AP signalling of a given 
eNodeB, which is identified uniquely by its ENodeB Global ID. It deals with 
*ENBSigProc* which is the parent class for all S1AP procedures that are 
eNodeB-related. All ongoing procedures are stored in the *Proc* attribute. 
Moreover, if the *TRACE* attribute is set to True, all passed and ongoing 
procedures are kept in the *_proc* attribute (so they are not garbage-collected).

The ENBd class and ENBSigProc classes are defined in *libmich/mobnet/ENBmgr.py*.

ENBd class attributes:
* TRACE: bool, to keep track of all passed eNB-related S1 procedures in _proc attribute

ENBd instance attributes:
* GID: tuple, eNodeB global ID
* ID_PLMN: str, eNodeB main PLMN ID
* ID_ENB: str, eNodeB identity
* MME: reference to the MMEd instance
* SK: sctp socket instance, or None when the eNodeB is disconnected
* ADDRS: sctp socket endpoint address, or None when the eNodeB is disconnected
* Config: dict, eNodeB configuration information, signalled to the MME in the S1 setup procedure
* Proc: dict {procedure id: ENBSigProc instance}, ongoing eNodeB-related S1AP procedures
* Proc_last: uint, code of the last S1AP procedure run
* _proc: list, list of all passed S1AP procedures

An UEd instance is responsible for dealing with the S1AP and NAS signalling for 
a given UE, which is identified uniquely by its IMSI. It deals with *UES1SigProc* 
and *UENASSigProc* which are the parent classes respectively for all S1AP 
procedures that are UE-related and all NAS EMM, ESM and security procedures. 
All S1, EMM and ESM ongoing procedures are stored in the *Proc* attribute. 
Moreover, it the *TRACE* attribute is set to True all passed and ongoing 
procedures are kept in the *_proc* attribute (they are not garbage-collected). 
Each UEd instance makes use of the MME.GTPd references to set and unset GTP 
tunnels. Each Authentication (UENASSigProc) instance makes use of the MME.AUCd 
references to get authentication vectors. 

The UEd class is defined in *libmich/mobnet/UEmgr.py*. UES1SigProc classes are 
defined in *libmich/mobnet/UES1proc.py* and UENASSigProc classes are defined in
*libmich/mobnet/UENASproc.py*.

UEd class attributes:
* TRACE_S1: bool, to keep track of all passed UE-related S1 procedures in _proc attribute
* TRACE_NAS: bool, to keep track of all passed NAS procedures in _proc attribute
* NASSEC_MAC: bool, if set to False, corenet will accept NASPDU with invalid MAC
* NASSEC_ULCNT: bool, if set to False, corenet will accept NASPDU with invalid NAS uplink count
* AUTH_POL_ATT: uint, authentication rate for attach procedure (1/AUTH_POL_ATT)
* AUTH_POL_TAU: uint, authentication rate for tracking area update procedure (1/AUTH_POL_TAU)
* AUTH_POL_SERV: uint, authentication rate for service request procedure (1/AUTH_POL_SERV)
* AUTH_AMF: 2-bytes, AMF field to be set in authentication vectors
* SMC_EEA: list of preferred EEA NAS algorithm identifiers (0, 1, 2, 3)
* SMC_EIA: list of preferred EIA NAS algorithm identifiers (1, 2, 3)
* ESM_PDN: dict of PDN parameters, indexed by APN
* ESM_APN_DEF: str, default APN for corenet 
* ESM_CTXT_ACT: bool, if set to False, no data channel will be established (useful for exchanging NAS PDU only)

UEd instance attributes:
* IMSI: str, IMSI of the UE
* MME: reference to the MMEd instance
* ENB: reference to the ENBd instance handling the UE, or None (when UE is IDLE)
* S1: dict, contains S1 info related to the UE
* SEC: dict, contains info related to the UE NAS security context
* EMM: dict, contains info related to the UE EMM state
* ESM: dict, contains info related to the UE ESM state, including negotiated and active RAB
* CAP: dict, UE capabilities
* Proc: dict, ongoing UE-related S1 / EMM / ESM procedures
* Proc_last: uint, code of the last S1 procedure run
* _proc: list, list of all passed S1AP and NAS procedures


Basic software structure:
-------------------------
```
MMEd instance (libmich/mobnet/MME.py)
    .GTPd: GTPUd instance reference (libmich/mobnet/GTPmgr.py)
    .SMSd: SMSRelayd instance reference (libmich/mobnet/SMSmgr.py)
    .AUCd: AuC instance reference (libmich/mobnet/AuC.py)
    .ENB -> ENBd instances (libmich/mobnet/ENBmgr.py)
        .Proc -> ENBSigProc instances (libmich/mobnet/ENBmgr.py)
    .UE -> UEd instances (libmich/mobnet/UEmgr.py)
        .Proc -> S1: UES1SigProc instances (libmich/mobnet/UES1proc.py)
              -> EMM: UENASSigProc instances (libmich/mobnet/UENASproc.py)
              -> ESM: UENASSigProc instances (libmich/mobnet/UENASproc.py)
```
