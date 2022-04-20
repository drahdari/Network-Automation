from .Sub_City import Sub_City
from .IP import IP
from .OSPF_Process import OSPF_Process
from netmiko import ConnectHandler
from .Interface import Interface
from .VRF import VRF
from.VRF_Address_Families import VRF_Address_Family
from .ARP import ARP
from .Transceiver import Transceiver
from .IfError import IfError
from netaddr import IPAddress
from ipaddress import ip_address
from .Congestion import Congestion





class Device:
    Mgmt = IP()
    Hostname = str()
    Sub_City = Sub_City()
    Chassy = str()
    SN = str()
    OSPFs = list()  # List of OSPF Processes
    BGP_N = list()
    LDP_N = list()
    VRFs = dict()  # List of VRFs
    Modules = list()
    NOS = str()
    Last_Restart_Time = str()
    Last_Restart_Reason = str()
    Up_Time = str()
    NOS = str()
    Interfaces = dict()
    Etherchannels=list()
    Hundred_Quantity=int()
    ARP_Qty=int()
    Ten_Quantity=int()
    Gig_Quantity=int()
    Fast_Quanityt=int()
    LAG_Quantity=int()
    Vlan_Quanityt=int()
    UP_Quantity=int()
    Down_Quantity=int()
    Pseudo_Wire_Quanityt=int()
    Totall_Sites=int()
    Totall_Inc=int()
    ARP_list=list()
    def __init__(self, Mgmt):
        self.Mgmt = Mgmt
        self.Hostname = str()
        self.Sub_City = Sub_City()
        self.Chassy = str()
        self.SN = str()
        self.OSPFs = list()  # List of OSPF Processes
        self.BGP_N = list()
        self.LDP_N = list()
        self.VRFs = dict()  # List of VRFs
        self.Interfaces=dict()
        self.Hundred_Quantity=int()
        self.Ten_Quantity=int()
        self.Gig_Quantity=int()
        self.Fast_Quanityt=int()
        self.LAG_Quantity=int()
        self.UP_Quantity=int()
        self.Down_Quantity=int()
        self.Vlan_Quanityt=int()
        self.Pseudo_Wire_Quanityt=int()
        self.ARP_Qty=int()
        self.Totall_Inc=int()
        self.Totall_Sites=int()
        self.ARP_list=list()

    def Empty_OSPF(self):
        if len(self.OSPFs) >= 1:
            return False
        return True

    def set_Mgmt(self, Mgmt: IP):
        if Mgmt.Check_IP():
            self.Mgmt = Mgmt
        else:
            print("Wrong IP Address Format")

    ## Option 7 of the List##
    def Initial_Info_Gathering(self, conn):
        conn.send_command("terminal width 0", delay_factor=2, expect_string='#')
        conn.send_command("terminal length 0", delay_factor=2, expect_string='#')

        self.Hostname = str(conn.send_command("show runn | inc hostname")).split()[1]
        self.Sub_City.Name = self.Hostname[0:str(self.Hostname).find("-")]
        self.VRF_Info_Identification(conn)
        self.Interface__Identification(conn)

    def Change_Interface_Spec(self,IntName:str,N_Interface:Interface,Congestion:Congestion()):
        Old_Intf=Interface()
        Old_Intf=self.Interfaces[IntName]
        Old_Intf.Pr_Status=N_Interface.Pr_Status
        Old_Intf.Ph_Status=N_Interface.Ph_Status
        Old_Intf.CRC=N_Interface.CRC
        Old_Intf.Output_Rate=N_Interface.Output_Rate
        Old_Intf.Input_Rate=N_Interface.Input_Rate
        Old_Intf.Speed=N_Interface.Speed
        Old_Intf.duplex=N_Interface.duplex
        Old_Intf.DLY=N_Interface.DLY
        Old_Intf.Bandwidth=N_Interface.Bandwidth
        Old_Intf.bia=N_Interface.bia
        Old_Intf.MTU=N_Interface.MTU
        self.Interfaces[IntName]=Old_Intf
        self.Interfaces[IntName].Bandwidth.Congested(Congestion.N_V,Congestion.C_V)

    # def Module_Identification(self,conn):

    def Identify_Arp(self,conn):
        conn.send_command("terminal width 0", delay_factor=2, expect_string='#')
        conn.send_command("terminal length 0", delay_factor=2, expect_string='#')
        output=conn.send_command("show ip arp ", expect_string="#", delay_factor=2)
        self.Identify_ARP_Text_Processing("Global",output,conn)
        for VRF_N in self.VRFs.values():
            if VRF_N.Name != "Global":
                VRF_Output = conn.send_command("show ip arp vrf {}".format(VRF_N.Name), expect_string="#", delay_factor=2)
                output += "\n"
                output+=VRF_Output
                self.Identify_ARP_Text_Processing(VRF_N.Name,VRF_Output,conn)
        return output


    def Identify_Interface(self,Prev_Interface,IP_Cu,VRF, conn):
        Intf=str()
        if len(Prev_Interface)>0:
            IP=ip_address(IP_Cu)
            c=0
            Intf_IPs=self.Interfaces[Prev_Interface].IP
            while c < len(Intf_IPs):
                if IP in Intf_IPs[c].IP.network:
                    Intf=Prev_Interface
                    break
                c+=1
            output=str()
            if len(Intf) == 0:
                if VRF == "Global":
                    output=conn.send_command("show ip route {}".format(IP_Cu), delay_factor=2, expect_string='#')
                else:
                    output = conn.send_command("show ip route vrf {} {}".format(VRF,IP_Cu), delay_factor=2, expect_string='#')
                output=output.split("\n")
                for line in output:
                    if "directly" in line:
                        line=line.split()
                        Intf=str(line[len(line)-1])

        return Intf

    def Router_ARP_Check(self,IP,Intf_Name):
        c=0
        Intf_IPs = self.Interfaces[Intf_Name].IP
        IP=ip_address(IP)
        while c < len(Intf_IPs):
            c1=1
            while c1<=3:
                if IP == Intf_IPs[c].IP.network[c1]:
                   return True
                c1+=1
            c += 1
        return False
    def Identify_ARP_Text_Processing(self, VRF:str, Text, conn):
        f_output = Text.split("\n")
        del f_output[0]
        ARP_N = ARP()
        prev_interface=str()
        for line in f_output:
            line = line.split()
            if len(line) > 1:
                ARP_N.IP.IP = str(line[1])
                ARP_N.IP.VRF = VRF
                ARP_N.MAC = str(line[3])
                self.ARP_list.append(ARP_N)
                Inc_If=str()
                if str(line[3]).startswith("Incomplete"):
                    Inc_If = self.Identify_Interface(prev_interface,str(line[1]),VRF, conn)
                if ARP_N.MAC.startswith("Incomplete"):
                    if not self.Router_ARP_Check(str(line[1]),Inc_If):
                        self.VRFs[VRF].Inc_Qty += 1
                        self.Totall_Inc += 1
                        self.Interfaces[Inc_If].Inc_Qty += 1
                        self.Down_Quantity+=1
                else:
                    if not self.Router_ARP_Check(str(line[1]), str(line[5])):
                        self.Interfaces[str(line[5])].ARP[ARP_N.IP.IP] = ARP_N
                        self.VRFs[VRF].Site_Qty += 1
                        self.Totall_Sites += 1
                        self.UP_Quantity+=1
                        self.Interfaces[str(line[5])].Site_Qty += 1
                    prev_interface=str(line[5])
                ARP_N = ARP()

    def Power_Specification(self,conn,Outclass):
        output = self.Filter_Output(conn.send_command("show interfaces transceiver", delay_factor=2, expect_string='#') ,"5")
        if Outclass.F_Type == "extensive":
            return output
        else:
            self.Transceiver_Info_Assignment(output,Outclass)

    def Transceiver_Info_Assignment(self,Text,Outclass):
        Text = Text.split("\n")
        c = 0
        for line in Text:
            str_row = list()
            if len(line) > 1 and c >= 1:
                if "--" in line:
                    line = line.replace("--", "")
                if "++" in line:
                    line = line.replace("++", "")

                line = line.split()

                if len(line) > 6:
                    if str(line[5]) == "+" or str(line[5]) == "-":
                        del line[5]
                Trans_N=Transceiver()
                Name = str(line[0])
                if "Gi" in Name:
                    Name = Name.replace("Gi", "GigabitEthernet")
                elif "Te" in Name:
                    Name = Name.replace("Te", "TenGigabitEthernet")
                elif "Fa" in Name:
                    Name = Name.replace("Fa", "FastEthernet")
                Intf = self.Interfaces[Name]

                if Outclass.N_Rx_Power_Down > float(line[5]) or float(
                        line[5]) > Outclass.N_Rx_Power_Up or Outclass.N_Tx_Power_Down > float(
                        line[4]) or float(line[4]) > Outclass.N_Tx_Power_Up:
                    Trans_N.Problematic=True
                else:
                    Trans_N.Problematic=False

                Trans_N.Rx=str(line[5])
                Trans_N.Tx=str(line[4])
                Trans_N.Temp=str(line[1])
                Trans_N.Voltage=str(line[2])
                Trans_N.Current=str(line[3])
                Intf.Transceiver=Trans_N
            c += 1

    def Filter_Output(self, output, OPs:str):
        Filtered_Output = str()
        LC = 0
        output = output.split("\n")
        if OPs == "3" or OPs == "4":
            for line in output:
                if 0 < LC < 3:
                    LC += 1
                else:
                    if LC == 3:
                        LC = 0
                    if not "delet" in line and not "." in line:
                        if "down" in line or "Loopback" in line or "Vlan" in line or "BDI" in line:
                            LC += 1
                        elif OPs == "4" and ("Tunnel" in line or "Port-channel" in line):
                            LC += 1
                        else:
                            Filtered_Output += line + "\n"
        elif OPs == "5":
            started = False
            for line in output:
                # print(line)
                if len(line) > 1:
                    if not started and "---" in line:
                        started = True
                    elif not started and "Temperature" in line:
                        Filtered_Output += line + "\n"
                    elif started and not "#" in line:
                        line_2 = line.split()
                        # print("Line2: {}".format(str(line_2)))
                        if not str(line_2[4]) == "N/A" and not str(line_2[5]) == "N/A":
                            Filtered_Output += line + "\n"
        return str(Filtered_Output)

    def Error_Check(self,conn, Pr_Type):
        output = self.Filter_Output(conn.send_command("show interfaces | inc line protocol|error", delay_factor=2, expect_string='#'),"4")
        if Pr_Type == "extensive":
            return output
        else:
            self.Error_Info_Assignment(output)

  
    def Error_Info_Assignment(self,Text):
        Text = Text.split("\n")
        c = 0
        IfName = str()
        Input_Error = float()
        Output_Error = float()
        CRC = float()
        Collision = float()
        overrun = float()
        reset = float()

        for line in Text:
            if len(line) > 1 and not "#" in line:
                line = line.strip()
                line = line.split()
                if c == 0:
                    IfName = line[0]
                    c += 1
                elif c == 1:
                    Input_Error = float(line[0])
                    CRC = float(line[3])
                    overrun = float(line[7])
                    c += 1
                elif c == 2:
                    Output_Error = float(line[0])
                    Collision = float(line[3])
                    reset = float(line[5])
                    Intf=self.Interfaces[IfName]
                    Intf.IfError.CRC=CRC
                    Intf.IfError.Input_Err=Input_Error
                    Intf.IfError.Output_Err=Output_Error
                    Intf.IfError.Overrun=overrun
                    Intf.IfError.Collision=Collision
                    Intf.IfError.Reset=reset
                    if CRC > 0 or Input_Error > 0 or Output_Error > 0 or overrun > 0 or Collision > 0 or reset > 0:
                        Intf.IfError.Problematic=True
                    else:
                        Intf.IfError.Problematic = False
                    self.Interfaces[IfName]=Intf
                    c=0

