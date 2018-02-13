What is corenet
===============

Corenet is a minimal 3G and LTE / EPC core network. It implements the minimal set of 
functions to handle home-NodeBs through Iuh interfaces, e-NodeBs through S1 interfaces, 
and UEs through NAS and GTPU interfaces:

```
          LTE-Uu                       S1                 
UE <-----Radio/UP------> eNodeB <---GTPU/UP-----> corenet <---UP---> LAN
UE <---Radio/RRC/NAS---> eNodeB <---S1AP/NAS----> corenet <---SMS>
                         eNodeB <-----S1AP------> corenet

          3G-Uu                       Iuh
UE <-----Radio/UP------> hNodeB <---GTPU/UP-----> corenet <---UP---> LAN
UE <---Radio/RRC/NAS---> hNodeB <-RUA/RANAP/NAS-> corenet <---SMS>
                         hNodeB <-----HNBAP-----> corenet
```

No other interfaces are supported by corenet (no interface to S-GW, P-GW, HSS / HLR, 
no support for GTP-C or Diameter interfaces, ...).
It has been successfully tested with the open-source Eurecom OpenAirInterface eNodeB, 
the commercial Amarisoft eNodeB, ip.access 3G femtocells, and handsets from multiple 
vendors (Qualcomm, Samsung, Mediatek, ...).



Installation
============


Operating system and Python version
------------------------------------

The application is made to work with Python 3.4 and over, but should also work with 
Python 2.7, just like *Pycrate*. It works on Linux, because of the need for SCTP 
support and Ethernet raw sockets. 
It may work on other UNIX-like system, but this has not been tested.


Dependencies
------------

The following libraries are required for corenet to work:
* [ipython](http://ipython.org/) is used to wrap the execution of corenet and
   to provide a friendly ipython-shell interface
* [pysctp](https://github.com/philpraxis/pysctp) is used to wrap the Linux
   kernel SCTP stack, and provides a Python API that is used by the MME server.
   Take care to install one of the fork that supports Python 3 in case you are
   working with Python 3.
* [pycrypto](https://www.dlitz.net/software/pycrypto/) is used for handling the
   AES computation for EEA2 / EIA2 and Milenage as provided in CryptoMobile
* [CryptoMobile](https://github.com/mitshell/CryptoMobile/) is used for handling
   Milenage and all UEA / UIA / EEA / EIA computations
* [pycrate](https://github.com/anssi-fr/pycrate/) contains all components needed
   for running the 3G and LTE / EPC core network stacks

   
Installation
------------

After all dependencies have been installed, there is no further installation 
needed. The *corenet.py* file can be launched as is from the command line, 
after adapting its main settings: for this, you need to edit the file according
to your required configuration, and edit the *AuC.db* file too.


Launch
------

You need to have the right to open raw Ethernet socket: for this, you need to be 
root (e.g. *sudo python corenet.py*), or to set the CAP_NET_RAW capability for 
the Python interpreter (e.g. *sudo setcap cap_net_raw+eip /usr/lib/python35*).

You can launch the corenet application as is, the application will then wait for
home-NodeBs and eNodeBs to connect, and UEs to attach. All logs are written to the 
*/tmp/corenet.log* file, the verbosity of each log category can be configured within 
the *corenet.py* file.


```bash
$ python ./corenet.py
user@LSF-TELECOM:~/corenet$ ./corenet.py 
CorenetServer: loading all ASN.1 and NAS modules, be patient...
Corenet 0.2.0 loaded -- interactive mobile core network

ASN.1 modules: HNBAP, RUA, RANAP, S1AP, SS, RRC3G, RRCLTE and ASN_GLOBAL
ASN.1 PDU: PDU_HNBAP, PDU_RUA, PDU_RANAP, PDU_S1AP, PDU_SS_Facility
NAS module for messages and IEs: NAS
Protocol procedures modules:
	- ProcHnbap, ProcRua, ProcRanap, ProcS1ap
	- ProcMM, ProcSMS, ProcGMM, ProcSM, ProcEMM, ProcESM
Protocol stack classes (and attribute's names at runtime):
	- HNBd
	- ENBd
	- UEd -> UEIuCSd (IuCS) -> UEMMd  (MM)
	                        -> UESMSd (SMS)
	      -> UEIuPSd (IuPS) -> UEGMMd (GMM)
	                        -> UESMd  (SM)
	      -> UES1d   (S1)   -> UEEMMd (EMM)
	                        -> UESMSd (SMS)
	                        -> UEESMd (ESM)
Instances:
	- Server: signalling server (instance of CorenetServer), 
	          handling instances of HNBd and ENBd under the .RAN attribute
	          handling instances of UEd under the .UE attribute
	- AUCd  : AuC Authentication center
	- GTPUd : GTP-U tunnel manager
	- SMSd  : SMS relay
Functions:
	- show, hex, bin: to represent NAS messages and IEs
	- sleep: to take a break !
Constants:
	- BLACKHOLE_LAN, BLACKHOLE_WAN

In [1]:
```


We can see the home-NodeBs and eNodeBs connected, their config as set during their
signalling link setup, and all procedures handled:

```bash
In [1]: Server.RAN
Out[1]: 
{('00101', '0010002'): <pycrate_corenet.HdlrHNB.HNBd at 0x7fb39798f6a0>,
 ('00101', '1a2d0'): <pycrate_corenet.HdlrENB.ENBd at 0x7fb397aa9eb8>}

In [17]: hnb = Server.RAN[('00101', '0010002')]

In [47]: hnb.Config
Out[47]: 
{'CellIdentity': '0010002',
 'HNB_Cell_Access_Mode': 'open',
 'HNB_Identity': {'hNB-Identity-Info': b'000295-0000124958@ap.ipaccess.com'},
 'HNB_Location_Information': {'iE-Extensions': [{'criticality': 'reject',
    'extensionValue': ('IP-Address',
     {'ipaddress': ('ipv4info', b'\n\x01\x01\x1f')}),
    'id': 17}]},
 'LAC': 1,
 'PLMNidentity': '00101',
 'RAC': 1,
 'SAC': 65535}

In [18]: hnb._proc # track of all procedures handled for the hnb
Out[18]: 
[<pycrate_corenet.ProcCNHnbap.HNBAPHNBRegistration at 0x7fb39798f8d0>,
 <pycrate_corenet.ProcCNHnbap.HNBAPUERegistration at 0x7fb397a980b8>,
 <pycrate_corenet.ProcCNRua.RUAConnect at 0x7fb397a85390>,
 <pycrate_corenet.ProcCNRua.RUADirectTransfer at 0x7fb397a32b38>,
 <pycrate_corenet.ProcCNRua.RUAConnect at 0x7fb39798fbe0>,
 <pycrate_corenet.ProcCNRua.RUADirectTransfer at 0x7fb3946236a0>,
 [...]
 <pycrate_corenet.ProcCNRua.RUADirectTransfer at 0x7fb37f770978>,
 <pycrate_corenet.ProcCNRua.RUADirectTransfer at 0x7fb37f770940>,
 <pycrate_corenet.ProcCNRua.RUADirectTransfer at 0x7fb37f7709e8>,
 <pycrate_corenet.ProcCNRua.RUADisconnect at 0x7fb37f770c18>]

In [19]: enb = Server.RAN[('00101', '1a2d0')]

In [48]: enb.Config
Out[48]: 
{'ENBname': 'enb1a2d0',
 'Global_ENB_ID': {'eNB-ID': ('macroENB-ID', '1a2d0'),
  'pLMNidentity': '00101'},
 'PagingDRX': 'v128',
 'SupportedTAs': [{'broadcastPLMNs': ['00101'], 'tAC': 1}],
 'TAIs': [('00101', 1)]}

In [20]: enb._proc
Out[20]: 
[<pycrate_corenet.ProcCNS1ap.S1APS1Setup at 0x7fb397aa97f0>,
 <pycrate_corenet.ProcCNS1ap.S1APPaging at 0x7fb39408c908>]
```


We can also see UEs attached to the core network, and their last access network used:

```bash
In [3]: Server.UE
Out[3]: {'001011664001104': <pycrate_corenet.HdlrUE.UEd at 0x7fb39798f4a8>}

In [4]: ue = Server.UE['001011664001104']

In [49]: ue._last_ran
Out[49]: <pycrate_corenet.HdlrUEIuCS.UEIuCSd at 0x7fb39798fb38>
```


After a given UE has moved to both the 3G and 4G access networks, all identities, 
localization and capabilities are available:

```bash
In [45]: ue.IMSI, ue.TMSI, ue.PTMSI, ue.MTMSI
Out[45]: ('001011664001104', 3559055791, 3186190919, 1912293922)

In [46]: ue.PLMN, ue.LAC, ue.RAC, ue.TAC
Out[46]: ('00101', 1, 1, 1)

In [30]: list(ue.Cap.keys())
Out[30]: 
['MSCm1',
 'MSCm2',
 'VoiceDomPref',
 'MSNetCap',
 'HNBAP',
 'DRXParam',
 'UESecCap',
 'UERadioCap',
 'MSNetFeatSupp',
 'UENetCap',
 'MSRACap']

In [31]: ue.Cap['MSCm1']
Out[31]: 
(b'W',
 <MSCm1 : <spare : 0><RevLevel : 2 (MS supporting R99 or later)><EarlyCmCap : 1><NoA51 : 0><RFClass : 7>>)

In [32]: show(ue.Cap['MSCm2'][1])
### MSCm2 ###
 <spare : 0>
 <RevLevel : 2 (MS supporting R99 or later)>
 <EarlyCmCap : 1>
 <NoA51 : 0>
 <RFClass : 7>
 <spare : 0>
 <PSCap : 1>
 <SSScreeningCap : 1 (capability of handling of ellipsis notation and phase 2 error handling)>
 <MTSMSCap : 1>
 <VBSNotifCap : 0>
 <VGCSNotifCap : 0>
 <FCFreqCap : 0>
 <MSCm3Cap : 1>
 <spare : 0>
 <LCSVACap : 1>
 <UCS2 : 0>
 <SoLSACap : 0>
 <CMServPrompt : 1>
 <A53 : 1>
 <A52 : 0>

In [33]: show(ue.Cap['MSNetCap'][1])
<MS_network_capability_value_part: [
 <<GEA1_bits: 1>>
 <SM_capabilities_via_dedicated_channels: 1>
 <SM_capabilities_via_GPRS_channels: 1>
 <UCS2_support: 0>
 <SS_Screening_Indicator: 1>
 <SoLSA_Capability: 0>
 <Revision_level_indicator: 1>
 <PFC_feature_mode: 1>
 <<Extended_GEA_bits: [
  <GEA_2: 1>
  <GEA_3: 1>
  <GEA_4: 0>
  <GEA_5: 0>
  <GEA_6: 0>
  <GEA_7: 0>]>>
 <LCS_VA_capability: 0>
 <PS_inter_RAT_HO_from_GERAN_to_UTRAN_Iu_mode_capability: 0>
 <PS_inter_RAT_HO_from_GERAN_to_E_UTRAN_S1_mode_capability: 0>
 <EMM_Combined_procedures_Capability: 1>
 <ISR_support: 0>
 <SRVCC_to_GERAN_UTRAN_capability: 0>
 <EPC_capability: 1>
 <NF_capability: 0>
 <GERAN_network_sharing_capability: 0>]>

In [34]: show(ue.Cap['DRXParam'][1])
### DRXParam ###
 <SPLIT_PG_CYCLE_CODE : 10>
 <DRXCycleLen : 0 (DRX not specified by the MS)>
 <SPLITonCCCH : 0>
 <NonDRXTimer : 1 (max 1 sec non-DRX mode after transfer state)>

In [35]: show(ue.Cap['UESecCap'][1])
### UESecCap ###
 <EEA0 : 1>
 <EEA1_128 : 1>
 <EEA2_128 : 1>
 <EEA3_128 : 1>
 <EEA4 : 0>
 <EEA5 : 0>
 <EEA6 : 0>
 <EEA7 : 0>
 <EIA0 : 0>
 <EIA1_128 : 1>
 <EIA2_128 : 1>
 <EIA3_128 : 1>
 <EIA4 : 0>
 <EIA5 : 0>
 <EIA6 : 0>
 <EIA7 : 0>
 <UEA0 : 1>
 <UEA1 : 1>
 <UEA2 : 0>
 <UEA3 : 0>
 <UEA4 : 0>
 <UEA5 : 0>
 <UEA6 : 0>
 <UEA7 : 0>
 <spare : 0>
 <UIA1 : 1>
 <UIA2 : 0>
 <UIA3 : 0>
 <UIA4 : 0>
 <UIA5 : 0>
 <UIA6 : 0>
 <UIA7 : 0>
 <spare : 0>
 <GEA1 : 1>
 <GEA2 : 1>
 <GEA3 : 1>
 <GEA4 : 0>
 <GEA5 : 0>
 <GEA6 : 0>
 <GEA7 : 0>

In [39]: ue.Cap['UERadioCap'][2]
Out[39]: 
{'eutra': {'accessStratumRelease': 'rel11',
  'featureGroupIndicators': (2144337598, 32),
  'interRAT-Parameters': {'geran': {'interRAT-PS-HO-ToGERAN': 0,
    'supportedBandListGERAN': ['gsm850', 'gsm900E', 'gsm1800', 'gsm1900']},
   'utraFDD': {'supportedBandListUTRA-FDD': ['bandI',
     'bandII',
     'bandIV',
     'bandV',
     'bandVIII']}},
     
     [...],
     
     'rf-Parameters-v1020': {'supportedBandCombination-r10': [[{'bandEUTRA-r10': 7,
         'bandParametersDL-r10': [{'ca-BandwidthClassDL-r10': 'a',
           'supportedMIMO-CapabilityDL-r10': 'twoLayers'}],
         'bandParametersUL-r10': [{'ca-BandwidthClassUL-r10': 'a'}]}],
       [{'bandEUTRA-r10': 20,
         'bandParametersDL-r10': [{'ca-BandwidthClassDL-r10': 'a',
           'supportedMIMO-CapabilityDL-r10': 'twoLayers'}],
         'bandParametersUL-r10': [{'ca-BandwidthClassUL-r10': 'a'}]}],
       [...],
       [{'bandEUTRA-r10': 40,
         'bandParametersDL-r10': [{'ca-BandwidthClassDL-r10': 'c',
           'supportedMIMO-CapabilityDL-r10': 'twoLayers'}],
         'bandParametersUL-r10': [{'ca-BandwidthClassUL-r10': 'a'}]}]]},
     'ue-BasedNetwPerfMeasParameters-r10': {'loggedMeasurementsIdle-r10': 'supported',
      'standaloneGNSS-Location-r10': 'supported'},
     'ue-Category-v1020': 6}},
   'phyLayerParameters-v920': {'enhancedDualLayerTDD-r9': 'supported'},
   'son-Parameters-r9': {'rach-Report-r9': 'supported'}},
  'pdcp-Parameters': {'maxNumberROHC-ContextSessions': 'cs16',
   'supportedROHC-Profiles': {'profile0x0001': 1,
    'profile0x0002': 1,
    'profile0x0003': 0,
    'profile0x0004': 0,
    'profile0x0006': 0,
    'profile0x0101': 0,
    'profile0x0102': 0,
    'profile0x0103': 0,
    'profile0x0104': 0}},
  'phyLayerParameters': {'ue-SpecificRefSigsSupported': 0,
   'ue-TxAntennaSelectionSupported': 0},
  'rf-Parameters': {'supportedBandListEUTRA': [{'bandEUTRA': 7,
     'halfDuplex': 0},
    {'bandEUTRA': 20, 'halfDuplex': 0},
    {'bandEUTRA': 28, 'halfDuplex': 0},
    {'bandEUTRA': 3, 'halfDuplex': 0},
    {'bandEUTRA': 1, 'halfDuplex': 0},
    {'bandEUTRA': 5, 'halfDuplex': 0},
    {'bandEUTRA': 8, 'halfDuplex': 0},
    {'bandEUTRA': 32, 'halfDuplex': 0},
    {'bandEUTRA': 38, 'halfDuplex': 0},
    {'bandEUTRA': 40, 'halfDuplex': 0}]},
  'ue-Category': 4}}

In [41]: show(ue.Cap['UENetCap'][1])
### UENetCap ###
 <EEA0 : 1>
 <EEA1_128 : 1>
 <EEA2_128 : 1>
 <EEA3_128 : 1>
 <EEA4 : 0>
 <EEA5 : 0>
 <EEA6 : 0>
 <EEA7 : 0>
 <EIA0 : 0>
 <EIA1_128 : 1>
 <EIA2_128 : 1>
 <EIA3_128 : 1>
 <EIA4 : 0>
 <EIA5 : 0>
 <EIA6 : 0>
 <EIA7 : 0>
 <UEA0 : 1>
 <UEA1 : 1>
 <UEA2 : 0>
 <UEA3 : 0>
 <UEA4 : 0>
 <UEA5 : 0>
 <UEA6 : 0>
 <UEA7 : 0>
 <UCS2 : 0>
 <UIA1 : 1>
 <UIA2 : 0>
 <UIA3 : 0>
 <UIA4 : 0>
 <UIA5 : 0>
 <UIA6 : 0>
 <UIA7 : 0>
 <ProSe_dd : 0>
 <ProSe : 0>
 <H245_ASH : 0>
 <ACC_CSFB : 1>
 <LPP : 0>
 <LCS : 0>
 <X1_SRVCC : 0>
 <NF : 0>

In [42]: show(ue.Cap['MSRACap'][1])
<MS_RA_capability_value_part: [
 <<MS_RA_capability_value_part_struct: [
  <{'0001' (GSM E  --note that GSM E covers GSM P): [
   <<Access_capabilities_struct: [
    <Length: 85>
    <[
     <<Content: [
      <RF_Power_Capability: 4>
      <{'1', [
       <<A5_bits: [
        <A5_1: 1>
        <A5_2: 0>
        <A5_3: 1>
        <A5_4: 0>
        <A5_5: 0>
        <A5_6: 0>
        <A5_7: 0>]>>]}>
      <ES_IND: 1>
      <PS: 1>
      <VGCS: 0>
      <VBS: 0>
      <{'1', [
       <<Multislot_capability_struct: [
        <{'0', []}>
        <{'1', [
         <GPRS_multislot_class: 12>
         <GPRS_Extended_Dynamic_Allocation_Capability: 1>]}>
        <{'0', []}>
        <{'0', []}>
        <{'1', [
         <EGPRS_multislot_class: 12>
         <EGPRS_Extended_Dynamic_Allocation_Capability: 1>]}>
        <{'0', []}>]>>]}>
      <{'1', [
       <_8PSK_Power_Capability: 2>]}>
      <COMPACT_Interference_Measurement_Capability: 0>
      <Revision_Level_Indicator: 1>
      <UMTS_FDD_Radio_Access_Technology_Capability: 1>
      <UMTS_3_84_Mcps_TDD_Radio_Access_Technology_Capability: 0>
      <CDMA_2000_Radio_Access_Technology_Capability: 0>
      <UMTS_1_28_Mcps_TDD_Radio_Access_Technology_Capability: 0>
      <GERAN_Feature_Package_1: 1>
      <{'0', []}>
      <Modulation_based_multislot_class_support: 0>
      <{'0', []}>
      <'0'>
      <GMSK_Multislot_Power_Profile: 0>
      <_8_PSK_Multislot_Power_Profile: 2>
      <Multiple_TBF_Capability: 0>
      <Downlink_Advanced_Receiver_Performance: 1>
      <Extended_RLC_MAC_Control_Message_Segmentation_Capability: 0>
      <DTM_Enhancements_Capability: 0>
      <{'0', []}>
      <PS_Handover_Capability: 0>
      <DTM_Handover_Capability: 0>
      <{'0', []}>
      <Flexible_Timeslot_Assignment: 0>
      <GAN_PS_Handover_Capability: 0>
      <RLC_Non_persistent_Mode: 0>
      <Reduced_Latency_Capability: 0>
      <Uplink_EGPRS2: 0>
      <Downlink_EGPRS2: 0>
      <E_UTRA_FDD_support: 0>
      <E_UTRA_TDD_support: 0>
      <GERAN_to_E_UTRA_support_in_GERAN_packet_transfer_mode: 0>
      <Priority_based_reselection_support: 1>
      <<Enhanced_Flexible_Timeslot_Assignment_struct: {'0', []}>>
      <Indication_of_Upper_Layer_PDU_Start_Capability_for_RLC_UM: 0>
      <EMST_Capability: 0>
      <MTTI_Capability: 0>
      <UTRA_CSG_Cells_Reporting: 0>
      <E_UTRA_CSG_Cells_Reporting: 0>
      <DTR_Capability: 0>
      <EMSR_Capability: 0>
      <Fast_Downlink_Frequency_Switching_Capability: 0>
      <TIGHTER_Capability: 0>]>>
     <[]>]>]>>]}>
  <{'1', [
   [...]
      <{'0', []}>]>>]}>]>>]}>]>>
 <[<spare_bits: [0,
  0,
  0,
  0,
  0,
  0,
  0]>]>]>
```


After an UE has connected to the mobile network, it is possible to let it connect to
the data services, over 3G and 4G. Connection statistics are then available under
the *GTPUd.stats* attribute:

```bash
In [50]: GTPUd.stats
Out[50]: 
{'192.168.1.204': {'DNS': {'8.8.8.8'},
  'ICMP': set(),
  'NTP': {'97.127.86.125'},
  'TCP': {('172.217.18.195', 80),
   ('172.217.18.202', 443),
   ('172.217.19.228', 443),
   ('172.217.22.131', 80),
   ('172.217.22.132', 443),
   ('216.58.198.195', 80),
   ('216.58.198.202', 443),
   ('216.58.201.234', 443),
   ('216.58.204.100', 443),
   ('216.58.205.10', 443),
   ('216.58.209.234', 443),
   ('216.58.213.138', 443),
   ('216.58.213.170', 443),
   ('216.58.213.174', 443),
   ('216.58.215.42', 443),
   ('66.102.1.188', 5228)},
  'UDP': {('172.217.19.234', 443), ('8.8.8.8', 53), ('97.127.86.125', 123)},
  'alien': set(),
  'resolved': {b'android.clients.google.com',
   b'android.googleapis.com',
   b'chromecontentsuggestions-pa.googleapis.com',
   b'cloudconfig.googleapis.com',
   b'connectivitycheck.gstatic.com',
   b'mtalk.google.com',
   b'north-america.pool.ntp.org',
   b'play.googleapis.com',
   b'telephonyspamprotect-pa.googleapis.com',
   b'translate.googleapis.com',
   b'www.google.com',
   b'www.googleapis.com',
   b'www.nperf.com',
   b'youtubei.googleapis.com'}},
 'fe80::1:0:cc': {'DNS': set(),
  'ICMP': {'ff02::2'},
  'NTP': set(),
  'TCP': set(),
  'UDP': set(),
  'alien': set(),
  'resolved': set()}}
```


It is also possible to exchange SMS between attached UEs. All SMS are forwarded
through the SMSd service handler. It can itself send SMS to given UEs. In case the
destination UE is not connected, it will get paged by the network. All SMS PDU
received and sent by the SMS service handler are stored under the *SMSd._pdu*
attribute (in case SMSd.TRACK_PDU is True in *corenet.py*):

```bash
In [52]: ue.MSISDN
Out[52]: '16641104'

In [9]: SMSd.send_text('hello back', num='16641104')

In [51]: SMSd._pdu
Out[51]: 
[(1518531263.470469,
  'UL',
  <RP_DATA_MO : <spare : 0><MTI : 0 (MS -> Net : RP-DATA)><Ref : 2><RPOriginatorAddress : <L : 0><V : 0x>><RPDestinationAddress : <L : 5><RPDestinationAddress : <Ext : 1><Type : 0 (unknown)><NumberingPlan : 1 (ISDN / telephony numbering plan (E.164 / E.163))><Num : 0015555>>><RPUserData : <L : 17><SMS_SUBMIT : <TP_SRR : 0 (A status report is not requested)><TP_UDHI [UDH Indicator] : 0><TP_RP : 0 (TP Reply Path parameter is not set in this SMS SUBMIT/DELIVER)><TP_VPF : 2 (TP VP field present - relative format)><TP_RD [Reject Duplicates] : 0><TP_MTI : 1 (SMS-SUBMIT-REPORT)><TP_MR [Message Reference] : 28><TP_DA [Destination Address] : <Len : 8><Ext : 1><Type : 1 (international number)><NumberingPlan : 1 (ISDN / telephony numbering plan (E.164 / E.163))><Num : 12341234>><TP_PID : <Format : 0 (telematic indication)><Telematic : <Telematic : 0 (no telematic interworking, but SME-to-SME protocol)><Protocol : 0>><Protocol [transparent] : 0>><TP_DCS : <Group : 0 (general data coding, uncompressed)><Charset : 0 (GSM 7 bit default alphabet)><Class : 0>><TP_VP : 255 (63 week)><TP_VP [transparent] : <Year : 00><Mon : 00><Day : 00><Hour : 00><Min : 00><Sec : 00><TZ: +0.00>><TP_VPe [transparent] : <Ext : 0><SingleShot : 0><reserved : 0><VPFormat : 0 (no VP specified)><VP [transparent] : 0><TP [transparent] : <Hour : 00><Min : 00><Sec : 00>><spare : b''>><TP_UD : <UDL : 5><UDH [transparent] : <UDHL : 0><UDH : ><fill : 0b>><UD : Hello>>>>>),
[...]
]

In [53]: show(SMSd._pdu[0][2])
### RP_DATA_MO ###
 <spare : 0>
 <MTI : 0 (MS -> Net : RP-DATA)>
 <Ref : 2>
 ### RPOriginatorAddress ###
  <L : 0>
  <V : 0x>
 ### RPDestinationAddress ###
  <L : 5>
  ### RPDestinationAddress ###
   <Ext : 1>
   <Type : 0 (unknown)>
   <NumberingPlan : 1 (ISDN / telephony numbering plan (E.164 / E.163))>
   <Num : 0015555>
 ### RPUserData ###
  <L : 17>
  ### SMS_SUBMIT ###
   <TP_SRR : 0 (A status report is not requested)>
   <TP_UDHI [UDH Indicator] : 0>
   <TP_RP : 0 (TP Reply Path parameter is not set in this SMS SUBMIT/DELIVER)>
   <TP_VPF : 2 (TP VP field present - relative format)>
   <TP_RD [Reject Duplicates] : 0>
   <TP_MTI : 1 (SMS-SUBMIT-REPORT)>
   <TP_MR [Message Reference] : 28>
   ### TP_DA [Destination Address] ###
    <Len : 8>
    <Ext : 1>
    <Type : 1 (international number)>
    <NumberingPlan : 1 (ISDN / telephony numbering plan (E.164 / E.163))>
    <Num : 12341234>
   ### TP_PID ###
    <Format : 0 (telematic indication)>
    ### Telematic ###
     <Telematic : 0 (no telematic interworking, but SME-to-SME protocol)>
     <Protocol : 0>
   ### TP_DCS ###
    <Group : 0 (general data coding, uncompressed)>
    <Charset : 0 (GSM 7 bit default alphabet)>
    <Class : 0>
   <TP_VP : 255 (63 week)>
   ### TP_UD ###
    <UDL : 5>
    <UD : Hello>

In [54]: show(SMSd._pdu[1][2])
### RP_ACK_MT ###
 <spare : 0>
 <MTI : 3 (Net -> MS : RP-ACK)>
 <Ref : 2>

In [55]: show(SMSd._pdu[2][2])
### RP_DATA_MO ###
 <spare : 0>
 <MTI : 0 (MS -> Net : RP-DATA)>
 <Ref : 3>
 ### RPOriginatorAddress ###
  <L : 0>
  <V : 0x>
 ### RPDestinationAddress ###
  <L : 5>
  ### RPDestinationAddress ###
   <Ext : 1>
   <Type : 0 (unknown)>
   <NumberingPlan : 1 (ISDN / telephony numbering plan (E.164 / E.163))>
   <Num : 0015555>
 ### RPUserData ###
  <L : 21>
  ### SMS_SUBMIT ###
   <TP_SRR : 0 (A status report is not requested)>
   <TP_UDHI [UDH Indicator] : 0>
   <TP_RP : 0 (TP Reply Path parameter is not set in this SMS SUBMIT/DELIVER)>
   <TP_VPF : 2 (TP VP field present - relative format)>
   <TP_RD [Reject Duplicates] : 0>
   <TP_MTI : 1 (SMS-SUBMIT-REPORT)>
   <TP_MR [Message Reference] : 29>
   ### TP_DA [Destination Address] ###
    <Len : 8>
    <Ext : 1>
    <Type : 1 (international number)>
    <NumberingPlan : 1 (ISDN / telephony numbering plan (E.164 / E.163))>
    <Num : 12341234>
   ### TP_PID ###
    <Format : 0 (telematic indication)>
    ### Telematic ###
     <Telematic : 0 (no telematic interworking, but SME-to-SME protocol)>
     <Protocol : 0>
   ### TP_DCS ###
    <Group : 0 (general data coding, uncompressed)>
    <Charset : 0 (GSM 7 bit default alphabet)>
    <Class : 0>
   <TP_VP : 255 (63 week)>
   ### TP_UD ###
    <UDL : 10>
    <UD : Hello back>
```


The IuCS stack and associated MM and SMS stacks, the IuPS stack and associated GMM and
SM stacks, and the S1 stack and associated EMM and ESM stacks, provide several attributes
for modifying their configuration and inner-workings. Several methods are also provided
for running network-initiated procedures.

```bash
In [12]: ue.IuCS.page?
Type:       method
String Form:<bound method UEIuCSd.page of <pycrate_corenet.HdlrUEIuCS.UEIuCSd object at 0x7fb39798fb38>>
File:       /home/mich/python/pycrate_corenet/HdlrUEIuCS.py
Definition: ue.IuCS.page(self, cause=None)
Docstring:
sends RANAP Paging command to RNC responsible for the UE LAI

cause [RANAP_IEs.PagingCause, ENUMERATED]: str or int (0..5)

In [13]: ue.IuCS.page(2)

In [14]: ue.IuCS.release()
Out[14]: True

In [15]: ue.IuPS.page(3)

In [16]: ue.IuPS.release()
Out[16]: True
```


All procedures run are stored under the *_proc* attribute of each stack and enable 
to easily debug what happened during each of them ; in particular, each procedure 
has a *_pdu* attribute under which are stored PDUs exchanged with the radio access 
equipment or UE.

```bash
In [21]: ue.IuCS._proc
Out[21]: 
[<pycrate_corenet.ProcCNRanap.RANAPInitialUEMessage at 0x7fb397aa9470>,
 <pycrate_corenet.ProcCNRanap.RANAPDirectTransferCN at 0x7fb397a3a080>,
 [...]
 <pycrate_corenet.ProcCNRanap.RANAPDirectTransferRNC at 0x7fb37f7709b0>,
 <pycrate_corenet.ProcCNRanap.RANAPIuRelease at 0x7fb37f770ba8>]

In [22]: ue.IuPS._proc
Out[22]: 
[<pycrate_corenet.ProcCNRanap.RANAPInitialUEMessage at 0x7fb397a32b70>,
 <pycrate_corenet.ProcCNRanap.RANAPDirectTransferCN at 0x7fb394623630>,
 [...]
 <pycrate_corenet.ProcCNRanap.RANAPIuReleaseRequest at 0x7fb37f7649e8>,
 <pycrate_corenet.ProcCNRanap.RANAPIuRelease at 0x7fb37f764a90>]

In [23]: ue.S1._proc
Out[23]: 
[<pycrate_corenet.ProcCNS1ap.S1APInitialUEMessage at 0x7fb3940fecf8>,
 <pycrate_corenet.ProcCNS1ap.S1APDownlinkNASTransport at 0x7fb39409d630>,
 [...]
 <pycrate_corenet.ProcCNS1ap.S1APDownlinkNASTransport at 0x7fb37f7ca630>,
 <pycrate_corenet.ProcCNS1ap.S1APUEContextRelease at 0x7fb37f7ca588>]

In [24]: ue.IuCS.MM._proc
Out[24]: 
[<pycrate_corenet.ProcCNMM.MMLocationUpdating at 0x7fb397a85198>,
 <pycrate_corenet.ProcCNMM.MMIdentification at 0x7fb397a3acf8>,
 <pycrate_corenet.ProcCNMM.MMAuthentication at 0x7fb394623dd8>,
 <pycrate_corenet.ProcCNMM.MMIdentification at 0x7fb39462d4e0>,
 <pycrate_corenet.ProcCNMM.MMTMSIReallocation at 0x7fb39462df28>,
 <pycrate_corenet.ProcCNMM.MMConnectionEstablishment at 0x7fb3945f5198>,
 <pycrate_corenet.ProcCNMM.MMConnectionEstablishment at 0x7fb3946029e8>,
 <pycrate_corenet.ProcCNMM.RRPagingResponse at 0x7fb3945b0358>,
 <pycrate_corenet.ProcCNMM.RRPagingResponse at 0x7fb3945bcb70>,
 <pycrate_corenet.ProcCNMM.MMLocationUpdating at 0x7fb37f7ca7b8>,
 <pycrate_corenet.ProcCNMM.MMTMSIReallocation at 0x7fb37f7d1978>,
 <pycrate_corenet.ProcCNMM.MMLocationUpdating at 0x7fb37f764b70>,
 <pycrate_corenet.ProcCNMM.MMTMSIReallocation at 0x7fb37f76ada0>]

In [25]: ue.IuCS.SMS._proc
Out[25]: 
[<pycrate_corenet.ProcCNSMS.CMSMSProcUE at 0x7fb3945f7048>,
 <pycrate_corenet.ProcCNSMS.CMSMSProcCN at 0x7fb3945fcf98>,
 <pycrate_corenet.ProcCNSMS.CMSMSProcUE at 0x7fb3946099b0>,
 <pycrate_corenet.ProcCNSMS.CMSMSProcCN at 0x7fb394611940>,
 <pycrate_corenet.ProcCNSMS.CMSMSProcCN at 0x7fb394619898>,
 <pycrate_corenet.ProcCNSMS.CMSMSProcUE at 0x7fb3945b68d0>]

In [26]: ue.IuPS.GMM._proc
Out[26]: 
[<pycrate_corenet.ProcCNGMM.GMMAttach at 0x7fb397a32c18>,
 <pycrate_corenet.ProcCNGMM.GMMIdentification at 0x7fb394621390>,
 <pycrate_corenet.ProcCNGMM.GMMAuthenticationCiphering at 0x7fb394629780>,
 <pycrate_corenet.ProcCNGMM.GMMIdentification at 0x7fb39463a358>,
 <pycrate_corenet.ProcCNGMM.GMMPTMSIReallocation at 0x7fb39463ae80>,
 <pycrate_corenet.ProcCNGMM.GMMServiceRequest at 0x7fb39464bcc0>,
 <pycrate_corenet.ProcCNGMM.GMMServiceRequest at 0x7fb3945dae48>,
 <pycrate_corenet.ProcCNGMM.GMMDetachUE at 0x7fb3945ddb70>,
 <pycrate_corenet.ProcCNGMM.GMMAttach at 0x7fb3940eefd0>,
 <pycrate_corenet.ProcCNGMM.GMMAuthenticationCiphering at 0x7fb3945ddfd0>,
 <pycrate_corenet.ProcCNGMM.GMMPTMSIReallocation at 0x7fb3940f55f8>,
 <pycrate_corenet.ProcCNGMM.GMMAttach at 0x7fb37f7d56a0>,
 <pycrate_corenet.ProcCNGMM.GMMAuthenticationCiphering at 0x7fb37f7af400>,
 <pycrate_corenet.ProcCNGMM.GMMPTMSIReallocation at 0x7fb37f7b5668>,
 <pycrate_corenet.ProcCNGMM.GMMServiceRequest at 0x7fb37f7bdb00>,
 <pycrate_corenet.ProcCNGMM.GMMAuthenticationCiphering at 0x7fb37f744a90>]

In [27]: ue.IuPS.SM._proc
Out[27]: 
[<pycrate_corenet.ProcCNSM.SMPDPCtxtAct at 0x7fb3946512b0>,
 <pycrate_corenet.ProcCNSM.SMPDPCtxtDeactUE at 0x7fb3945eba58>,
 <pycrate_corenet.ProcCNSM.SMPDPCtxtAct at 0x7fb37f747e10>,
 <pycrate_corenet.ProcCNSM.SMPDPCtxtDeactUE at 0x7fb37f760a58>]

In [28]: ue.S1.EMM._proc
Out[28]: 
[<pycrate_corenet.ProcCNEMM.EMMAttach at 0x7fb394109f60>,
 <pycrate_corenet.ProcCNEMM.EMMIdentification at 0x7fb39409aa20>,
 <pycrate_corenet.ProcCNEMM.EMMAuthentication at 0x7fb39409db38>,
 <pycrate_corenet.ProcCNEMM.EMMSecurityModeControl at 0x7fb3940a5400>,
 <pycrate_corenet.ProcCNEMM.EMMGUTIReallocation at 0x7fb3940ab588>,
 <pycrate_corenet.ProcCNEMM.EMMServiceRequest at 0x7fb3940ceba8>,
 <pycrate_corenet.ProcCNEMM.EMMServiceRequest at 0x7fb3940ced68>,
 <pycrate_corenet.ProcCNEMM.EMMULNASTransport at 0x7fb394079588>,
 <pycrate_corenet.ProcCNEMM.EMMDLNASTransport at 0x7fb3940828d0>,
 <pycrate_corenet.ProcCNEMM.EMMDLNASTransport at 0x7fb394082cc0>,
 <pycrate_corenet.ProcCNEMM.EMMULNASTransport at 0x7fb394087668>,
 <pycrate_corenet.ProcCNEMM.EMMAttach at 0x7fb394105c88>,
 <pycrate_corenet.ProcCNEMM.EMMAuthentication at 0x7fb3940946d8>,
 <pycrate_corenet.ProcCNEMM.EMMSecurityModeControl at 0x7fb394090438>,
 <pycrate_corenet.ProcCNEMM.EMMGUTIReallocation at 0x7fb39401b4a8>,
 <pycrate_corenet.ProcCNEMM.EMMDLNASTransport at 0x7fb39402d6a0>,
 <pycrate_corenet.ProcCNEMM.EMMULNASTransport at 0x7fb394039cc0>,
 <pycrate_corenet.ProcCNEMM.EMMULNASTransport at 0x7fb394040390>,
 <pycrate_corenet.ProcCNEMM.EMMDLNASTransport at 0x7fb394043588>,
 <pycrate_corenet.ProcCNEMM.EMMTrackingAreaUpdate at 0x7fb39404e438>,
 <pycrate_corenet.ProcCNEMM.EMMAuthentication at 0x7fb394043cc0>,
 <pycrate_corenet.ProcCNEMM.EMMSecurityModeControl at 0x7fb394052da0>,
 <pycrate_corenet.ProcCNEMM.EMMGUTIReallocation at 0x7fb394057eb8>,
 <pycrate_corenet.ProcCNEMM.EMMDetachUE at 0x7fb394057b00>]

In [29]: ue.S1.ESM._proc
Out[29]: 
[<pycrate_corenet.ProcCNESM.ESMPDNConnectivityRequest at 0x7fb3940b6748>,
 <pycrate_corenet.ProcCNESM.ESMInfoRequest at 0x7fb3940afcc0>,
 <pycrate_corenet.ProcCNESM.ESMDefaultEPSBearerCtxtAct at 0x7fb3940b9dd8>,
 <pycrate_corenet.ProcCNESM.ESMPDNConnectivityRequest at 0x7fb394023390>,
 <pycrate_corenet.ProcCNESM.ESMInfoRequest at 0x7fb39401fa90>,
 <pycrate_corenet.ProcCNESM.ESMDefaultEPSBearerCtxtAct at 0x7fb394027e10>]

In [56]: ue.S1.EMM._proc[2]
Out[56]: <pycrate_corenet.ProcCNEMM.EMMAuthentication at 0x7fb39409db38>

In [57]: ue.S1.EMM._proc[2]._pdu
Out[57]: 
[(1518531533.353799,
  'DL',
  <EMMAuthenticationRequest : <EMMHeader : <SecHdr : 0 (No security)><ProtDisc : 7 (EMM)><Type : 82 (Authentication request)>><spare : 0><NAS_KSI : <NAS_KSI : <TSC : 0 ( native security context)><Value : 0>>><RAND : <V : 0xb578b830a45121874eea9440158ab63d>><AUTN : <L : 16><V : 0x03b6734e98a0800033836161c7cb4eaa>>>),
 (1518531533.648836,
  'UL',
  <EMMAuthenticationResponse : <EMMHeader : <SecHdr : 0 (No security)><ProtDisc : 7 (EMM)><Type : 83 (Authentication response)>><RES : <L : 8><V : 0x0e4fd73a94d246eb>>>)]

In [58]: show(ue.S1.EMM._proc[2]._pdu[0][2])
### EMMAuthenticationRequest ###
 ### EMMHeader ###
  <SecHdr : 0 (No security)>
  <ProtDisc : 7 (EMM)>
  <Type : 82 (Authentication request)>
 <spare : 0>
 ### NAS_KSI ###
  ### NAS_KSI ###
   <TSC : 0 ( native security context)>
   <Value : 0>
 ### RAND ###
  <V : 0xb578b830a45121874eea9440158ab63d>
 ### AUTN ###
  <L : 16>
  <V : 0x03b6734e98a0800033836161c7cb4eaa>

In [59]: show(ue.S1.EMM._proc[2]._pdu[1][2])
### EMMAuthenticationResponse ###
 ### EMMHeader ###
  <SecHdr : 0 (No security)>
  <ProtDisc : 7 (EMM)>
  <Type : 83 (Authentication response)>
 ### RES ###
  <L : 8>
  <V : 0x0e4fd73a94d246eb>
```



License
=======

The application is licensed under GPLv2+: all licensed files have an header
making it self-explanatory.



Contact and support
==================

As the unique developper of the application, I am the only person to contact:
michau \[dot\] benoit \[at\] gmail \[dot\] com.
Every feedback is very welcomed ; however, because the application remains a 
complex piece of software, I may not be able to answer every request.

Please prefer to open an issue within the github tracker instead of sending an 
email.



Technical aspects
=================


Basic configuration
-------------------

First of all, it is required to have programmable SIM or USIM cards, that are 
personalized with known secret keys K. To access to the LTE / EPC part, USIM are
required.
The IMSI and authentication keys K (and SQN for USIM) need to be configured in the
*AuC.db* file accordingly.

Then, several components of corenet have to be configured.
Please, open and read the *corenet.py* file that consists essentially in configuring
all network and telecom parameters.


