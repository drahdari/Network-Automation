    def Interface__Identification(self, conn):
        ## Description, IP Address and VRF Membership
        output = conn.send_command("show runn | inc interface|ip address|desc|ip vrf|channel-group", delay_factor=2, expect_string='#')
        output = str(output).strip()
        output = output.split("\n")
        started = False
        interface = Interface()
        Finished=False
        for line in output:
            #print(line)
            if len(line) > 1:
                line2=line.split()
                if started:
                    line=line.strip()
                    if line.startswith("description"):
                        line = line.split()
                        c1 = 1
                        while c1 < len(line):
                            interface.Description += line[c1]
                            c1 += 1
                    elif line.startswith("ip vrf forwarding"):
                        line = line.split()
                        interface.VRF=line[3]
                    elif line.startswith("no ip"):
                        IP_Init = IP()
                        interface.IP.append(IP_Init)
                    elif line.startswith("ip address"):
                        line = line.split()
                        Int_IP=IP()
                        CIDR=IPAddress(str(line[3])).netmask_bits()
                        Entire_IP = line[2]+"/"+str(CIDR)
                        Int_IP.Set_IP(Entire_IP)
                        interface.IP.append(Int_IP)
                    elif line.startswith("interface"):
                        line = line.split()
                        if str(interface.Name) != str(line[1]):
                            if len(interface.Description) == 0:
                                interface.Description="N/A"
                            if len(interface.VRF) == 0:
                                interface.VRF="Global"
                            if len(interface.IP) == 0:
                                IP_Init=IP()
                                interface.IP.append(IP_Init)
                            if "Vlan" in interface.Name:
                                self.Vlan_Quanityt+=1
                            elif "owire" in interface.Name:
                                self.Pseudo_Wire_Quanityt+=1
                            self.Interfaces[str(interface.Name)]=interface
                            self.VRFs[interface.VRF].Intf_Qty+=1
                            interface = Interface()
                        interface.Name = line[1]
 
                        if "Ten" in interface.Name:
                            #self.Interfaces[interface.Name].Bandwidth.Physical_Bandwidth = 10737418240
                            interface.Bandwidth.Physical_Bandwidth = 10737418240
                        elif "Gig" in interface.Name:
                            #self.Interfaces[interface.Name].Bandwidth.Physical_Bandwidth = 1073741824
                             interface.Bandwidth.Physical_Bandwidth = 1073741824
                        elif "Fast" in interface.Name:
                            #self.Interfaces[interface.Name].Bandwidth.Physical_Bandwidth = 104857600
                            interface.Bandwidth.Physical_Bandwidth = 104857600
 
                    elif "channel-group" in line:
                        line = line.split()
                        interface.Parent_Eth = str(line[1])
                    else:
                        if len(interface.Description) == 0:
                            line = line.split()
                            if "Vlan" in interface.Name:
                                self.Vlan_Quanityt += 1
                            elif "owire" in interface.Name:
                                self.Pseudo_Wire_Quanityt += 1
                            self.Interfaces[str(interface.Name)]=interface
                        if not "specify" in line:
                            break
                elif "interface" == line2[0]:
                    line = line.split()
                    started = True
                    interface.Name = line[1]
        if len(interface.Description) == 0:
            interface.Description = "N/A"
        if len(interface.VRF) == 0:
            interface.VRF = "Global"
        if len(interface.IP) == 0:
            IP_Init = IP()
            interface.IP.append(IP_Init)
        if "Vlan" in interface.Name:
            self.Vlan_Quanityt += 1
        elif "owire" in interface.Name:
            self.Pseudo_Wire_Quanityt += 1
        self.Interfaces[str(interface.Name)] = interface
        self.VRFs[interface.VRF].Intf_Qty += 1


