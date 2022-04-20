    def VRF_Info_Identification(self, conn):
        output = conn.send_command("show ip vrf detail", delay_factor=2,
                                   expect_string='#')
        output = str(output).strip()
        output = output.split("\n")
        N_VRF=VRF()
        I_Started=False
        RT_Export=False
        RT_Import=False
        N_VRF_AF=VRF_Address_Family()
        c2=0
        for line in output:
            if len(line)>1 and not "#" in line:
                if "route-map" in line:
                    if "Import" in line:
                        line=line.split()
                        N_VRF_AF.Import_Filtering=str(line[2])
                        RT_Import=False
                    elif "import" in line:
                        RT_Import=False
                elif RT_Export and not "Import" in line:
                    line = line.split()
                    c = 0
                    while c < len(line):
                        EXP_RT = str(line[c]).replace("RT:", "")
                        N_VRF_AF.RT_Export.append(EXP_RT)
                        c += 1
                elif "Export" in line and "route-target" in line:
                    RT_Export=True
                elif RT_Import:
                    line = line.split()
                    c = 0
                    while c < len(line):
                        IMP_RT = str(line[c]).replace("RT:", "")
                        N_VRF_AF.RT_Import.append(IMP_RT)
                        c += 1
                elif "Import" in line and "route-target" in line:
                    RT_Import=True
                    RT_Export=False
                elif "Address family" in line:
                    line=line.split()
                    if len(N_VRF_AF.Name) != 0:
                        N_VRF.Address_Family.append(N_VRF_AF)
                        N_VRF_AF = VRF_Address_Family()
                    I_Started = False
                    N_VRF_AF.Name = str(line[2]) + " "+ str(line[3])
                elif I_Started:
                    line = line.split()
                    c = 0
                    while c < len(line):
                        Name = str(line[c])
                        if "Gi" in Name:
                            Name = Name.replace("Gi", "GigabitEthernet")
                        elif "Te" in Name:
                            Name = Name.replace("Te", "TenGigabitEthernet")
                        elif "Fa" in Name:
                            Name = Name.replace("Fa", "FastEthernet")
                        elif "Vl" in Name:
                            Name = Name.replace("Vl", "Vlan")
                        elif "Lo" in Name:
                            Name=Name.replace("Lo","Loopback")
                        N_VRF.interfaces.append(Name)
                        c += 1
                elif "default RD" in line:
                    if len(N_VRF.Name) != 0:
                        N_VRF.Address_Family.append(N_VRF_AF)
                        self.VRFs[N_VRF.Name]=N_VRF
                        N_VRF=VRF()
                        N_VRF_AF=VRF_Address_Family()
                    line=line.split()
                    N_VRF.Name=str(line[1])
                    N_VRF.RD=str(line[8])[0:str(line[8]).find(";")]
                elif "No interface" in line:
                    N_VRF.interfaces.append("N/A")
                elif "Interfaces:" in line:
                    I_Started=True
                elif "Export route-map:" in line:
                    line = line.split()
                    N_VRF_AF.Export_Filtering = str(line[2])
                elif "allocation mode" in line:
                    line = line.split()
                    N_VRF_AF.Label_Allocation_Type=str(line[4])
            c2+=1
        if len(N_VRF.Name) != 0 and c2==len(output):
            N_VRF.Address_Family.append(N_VRF_AF)
        if len(N_VRF.Name) > 0:
            self.VRFs[N_VRF.Name] = N_VRF
        VRF_G=VRF()
        VRF_G.Name="Global"
        VRF_G.RD="N/A"
        VRF_G_AF=VRF_Address_Family()
        VRF_G_AF.Name="Global"
        VRF_G.Address_Family=VRF_G_AF
        self.VRFs[VRF_G.Name]=VRF_G


