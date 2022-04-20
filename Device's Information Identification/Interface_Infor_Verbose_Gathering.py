    def Interface_Detail(self, conn,Congestion):
        output=conn.send_command("\n")
        output = conn.send_command("\n")
        output = conn.send_command("\n")
        output = conn.send_command("show interfaces ", delay_factor=2, expect_string='#')
        output = str(output).strip()
        output = output.split("\n")

        interface=Interface()
        First=str()
        Jump=False
        for line in output:
            if len(line) > 1 and not "#" in line:
                #print("line: {}".format(line))
                if "line protocol" in line:
                    if len(First) != 0 and not Jump:
                        if "Ten" in str(First[0]):
                            self.Ten_Quantity+=1
                        elif "Gig" in str(First[0]):
                            self.Gig_Quantity+=1
                        elif "Fast" in str(First[0]):
                            self.Fast_Quanityt+=1
                        elif "channel" in str(First[0]):
                            self.LAG_Quantity+=1
                        if interface.Ph_Status == "up" and interface.Pr_Status == "up":
                            self.UP_Quantity+=1
                        else:
                            self.Down_Quantity+=1
                        self.Change_Interface_Spec(str(First[0]), interface,Congestion)
                    if "Tunnel" in line: #or "Vlan" in line:
                        Jump=True
                    else:
                        Jump=False
                        line=line.split(",")
                        First=str(line[0]).split()
                        Second=str(line[1]).split()
                        if len(First)==4:
                            interface.Ph_Status="Administratively Down"
                        else:
                            interface.Ph_Status=str(First[2])
                        interface.Pr_Status=Second[3]
                        if interface.Ph_Status=="deleted":
                            Jump=True
                            interface=Interface()
                elif "pseudowire" in line:
                    line=line.split()
                    Int_N=Interface()
                    Int_N.Name=line[0]
                    IP_N=IP()
                    Int_N.IP.append(IP_N)
                    self.Interfaces[line[0]]=Int_N
                    self.Pseudo_Wire_Quanityt+=1
                    Jump=True
                elif not Jump:
                    if "MTU" in line:
                        line=line.split()
                        interface.MTU=int(line[1])
                        interface.Bandwidth=int(line[4])
                        interface.DLY=int(line[7])
                    elif "bia" in line:
                        line=line.split()
                        interface.bia=str(line[7])
                    elif "duplex" in line:
                        line=line.split()
                        interface.duplex=str(line[0])[0:str(line[0]).find(",")]
                        interface.Speed=str(line[1])[0:str(line[1]).find(",")]
                    elif "output drops:" in line:
                        line=line.split()
                        interface.output_drops=line[7]
                    elif "input rate" in line:
                        line = line.split()
                        interface.Bandwidth.Input_Rate=int(line[4])
                    elif "output rate" in line:
                        line=line.split()
                        interface.Bandwidth.Output_Rate=float(line[4])
                    elif "CRC" in line:
                        line=line.split()
                        interface.CRC=int(line[3])
                        interface.Input_Error=int(line[0])
                        started = True
        if len(First) != 0:
            self.Change_Interface_Spec(str(First[0]), interface,Congestion)


