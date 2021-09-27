import os
import socket
from netmiko import ConnectHandler
from getpass import getpass
from multiprocessing import Queue
import threading
import _thread
import getpass
from collections import defaultdict
from openpyxl import workbook
from openpyxl.styles import Color, Font
from openpyxl.styles import Alignment
from openpyxl.styles.colors import GREEN
import csv
import xlrd

def Session_Configuration(target, Configs, USR, PSW, Result_dic):
    try:
        print(target)
        device = ConnectHandler(device_type='cisco_ios', ip=str(target), username=USR, password=PSW)
        "device.find_prompt()"
        hostname=device.send_command("show runn | inc hostname")
        hostname=hostname[9::] 
        Result_dic[str(target)].append(False)
        for config in Configs:
            config_type=config[0]
            config=config[1::] 
            command = "show runn | inc " + str(config)
            output=list()
            output=device.send_command(command)
            output=output.split("\n")
            checked=False
            print("Config :" + str(config) + "  " + str(target))
            for statement in output:   
                statement=statement.strip()
                if checked==False:
                    if config_type == "e":
                        if str(statement) == str(config):
                            value=list()
                            value.append(config)
                            value.append(True) 
                            Result_dic[str(target)].append(value)
                            checked=True
                    else: 
                        if str(config) in str(statement):
                            value=list()
                            value.append(config)
                            value.append(True) 
                            Result_dic[str(target)].append(value)
                            checked= True             
            if checked==False:
                value=list()
                value.append(config)
                value.append(False) 
                Result_dic[str(target)].append(value)
    except Exception as P:
        print(P)
    return(Result_dic)
     

def Compliance_Check(IP_Addresses, Out_DIR,Configs, USR, PSW):
    
    Result_dic = defaultdict(list) 
    for target in IP_Addresses:
        Result_dic = Session_Configuration(target, Configs, USR, PSW, Result_dic)


def Single_Configuration(target, USR, PSW, Configs):
    print(target)
    try:
        device = ConnectHandler(device_type='cisco_ios', ip=str(target), username=USR, password=PSW)
        hostname=device.send_command_timing("show runn | inc hostname")
        hostname=hostname[9::] 
        for config in Configs:
            device.send_command_timing(str(config))
        device.disconnect()

    except Exception as P:
        print(P)

def Direct_Configuration(IP_Addresses, USR, PSW, Configs):
    for target in IP_Addresses:
        Single_Configuration(target, USR, PSW, Configs)

def Proxy_Configuration(Proxy_IP, IP_Addresses, USR, PSW, Configs):
    try:
        device = ConnectHandler(device_type='cisco_ios', ip=str(Proxy_IP), username=USR, password=PSW)
        print("Proxy Connected " + " IP: " + str(Proxy_IP))
        for target in IP_Addresses:
            try:
                output=device.send_command_timing("ssh -l " + str(USR) + " "+ str(target))
                print(output)
                if 'password' in output:
                    device.send_command_timing(str(PSW))
                    for config in Configs:
                        print (str(target) + " " + " Config: " + str(config))
                        device.send_command_timing(str(config))
                    device.send_command_timing("exit")
            except:
                print(str(target) + "Not Reachable")
        device.disconnect()
    except Exception as P:
        print("fail")
        print(P)

def Get_Devices():
    Hosts_File=input("IP File: ") 
    IPs=list()
    with open(Hosts_File, 'r') as Hosts:
        for line in Hosts.readlines():
            if len(str(line)) > 1:
                line.strip()
                line=str(line).strip("\n")        
                IPs.append(line)
    return IPs



def Get_Configs(): 
    Config_File=input("Configuration File: ") 
    Configurations=list()
    with open(Config_File, 'r') as Configs:
        for line in Configs.readlines():
            if len(str(line)) > 1:
                line.strip()
                line=str(line).strip("\n")
                Configurations.append(line)
    return Configurations

def Get_Authentication():
    USR = input("Username: ")
    PSW=getpass.getpass(prompt='Password: ', stream=None) 
    Authentication=list()
    Authentication.append(USR)
    Authentication.append(PSW)
    return Authentication

def OSPF_Configuration(OSPF_Dictionary, Proxy_IP, USR, PSW):
    try:
        device = ConnectHandler(device_type='cisco_ios', ip=str(Proxy_IP), username=USR, password=PSW)
        print("Proxy Connected " + " IP: " + str(Proxy_IP))
        for target,C1,C2 in OSPF_Dictionary:
            try:
                output=device.send_command_timing("ssh "+ str(target))
                print(output)
                if 'password' in output:
                    device.send_command_timing(str(PSW))
                    output=device.send_command_timing("show ip ospf neigh")
                    output=output.split("\n")
                    
            except:
                print(str(target) + "Not Reachable")
        device.disconnect()
    except Exception as P:
        print("fail")
        print(P)



print("***********************************************************")
print("***********************************************************")
print("***********************************************************")
print("*********                                         *********")
print("*********      Configuration Automation Tool      *********")
print("*********                                         *********")
print("***********************************************************")
print("***********************************************************")
print("***********************************************************")
print("\n \n")
print("Select Your Choice from Below: ")
print("Bulk Configuration : 1")
print("Compliance Check   : 2")
print("OSPF Cost Configuration : 3")

Option = input("Choice: ")


IPs=list()
Configs=list()
USR=str()
PSW=str()
Authentication=list()

" Option 3 is regarding the project where we want to change all the cost of ospf "
OSPF_Config_dir=dict()
if int(Option) == 3:
    File_All=input("Configuration File: ") 
    Proxy_IP= input("Proxy Device IP: ")
    with open(File_All, 'r') as F1:
        for line in F1.readlines():
            if len(str(line)) > 1:
                line.strip()
                line=str(line).strip("\n")        
                line_Sec=list()
                line_Sec=line.split()                
                OSPF_Config_dir[str(line_Sec[0])].append(str(line_Sec[1])) 
                OSPF[str(line_Sec[0])].append(str(line_Sec[2]))
    Authentication=Get_Authentication()
    USR=str(Authentication[0])
    PSW=str(Authentication[1])
    OSPF_Configuration(OSPF_Config_dir, Proxy_IP, USR, PSW)

if int(Option) == 1 or int(Option) == 2:
    IPs=Get_Devices()
    Configs=Get_Configs()

if int(Option) == 1: 
    print("\n \n")
    print("Please Select Configuration Type from Below ")
    print("Direct Access: 1 ")
    print("Proxy Access: 2")
    Conf_Type=input("Config Type: ")
    if int(Conf_Type) == 1:    
        Authentication=Get_Authentication()
        USR=str(Authentication[0])
        PSW=str(Authentication[1])
        Direct_Configuration(IPs,USR,PSW,Configs)
    elif int(Conf_Type) == 2:
        Proxy_IP = input("Proxy Device IP: ") 
        Authentication=Get_Authentication()
        USR=str(Authentication[0])
        PSW=str(Authentication[1])
        Proxy_Configuration(Proxy_IP,IPs,USR,PSW,Configs)

elif int(Option) == 2:
    Authentication=Get_Authentication()
    USR=str(Authentication[0])
    PSW=str(Authentication[1])
    Compliance_Check(IPs, Out_DIR, Configurations, USR, PSW)


