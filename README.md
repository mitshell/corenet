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
no support for GTPC or Diameter interfaces, ...).



Installation
============


Operating system and Python version
------------------------------------

The application is made to work with Python 2 (starting with 2.6), just like 
*libmich* library. Python 3 is not supported, mainly because libmich does not 
work with Python 3.
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
   AES computation for EEA2 / EIA2 as provided in CryptoMobile
* [CryptoMobile](https://github.com/mitshell/CryptoMobile/) is used for handling
   Milenage and EEA / EIA computations
* [libmich](https://github.com/mitshell/libmich/) contains all components needed
   for running an LTE / EPC core network

   
Installation
------------

After all dependencies have been installed, there is no further installation 
needed. The *corenet.py* file can be launched as is from the command line.


Launch
------

You can launch the corenet application as is:
```bash
$ python corenet.py
```

You need to have the right to open raw Ethernet socket: for this you need to be root, 
or to set the CAP_NET_RAW capability for your user.

From here, it is waiting for eNodeB to connect, and then to UE to attach.



License
=======

The application is licensed under GPLv2: all licensed files have an header
making it self-explanatory.



Contact and support
==================

As the unique developper of the application, I am the only person to contact:
michau \[dot\] benoit \[at\] gmail \[dot\] com.
Because the application remains a complex piece of software, I may not be able
to answer every request. 



Technical aspects
=================


Basic configuration
-------------------

Several components have to be configured:
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

ENBd instance attributes:
* GID: tuple, eNodeB global ID
* ID_PLMN: str, eNodeB main PLMN ID
* ID_ENB: str, eNodeB identity
* MME: reference to the MMEd instance
* SK: sctp socket instance, or None when the eNodeB is disconnected
* ADDRS: sctp socket endpoint address, or None when the eNodeB is disconnected
* Config: dict, eNodeB configuration information, signalled to the MME in the S1 setup procedure
* Proc: dict {procedure id: ENBSigProc instance}, ongoing eNodeB-related S1AP procedures
* Proc_last: int, identifier of the last S1AP procedure run
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
TODO

UEd instance attributes:
TODO


Basic software structure:
-------------------------
```
MMEd instance
    .GTPd: GTPUd instance reference
    .AUCd: AuC instance reference
    .ENB -> ENBd instances
        .Proc -> ENBSigProc instances
    .UE -> UEd instances
        .Proc -> UES1SigProc instances
              -> UENASSigProc instances
```


Advanced configuration
----------------------

TODO
