    def EtherChannel_Check(self, conn):
        output = conn.send_command("show etherchannel summary", delay_factor=2, expect_string='#')
        output = output.split("\n")
        Number = "Null"
        started = False
        l = 1
        Empty = False
        Name=str()
        for line in output:
            if "channel-groups" in line:
                line = line.split()
                if str(line[5]) == "0":
                    Empty = True
            if not Empty:
                if (started and len(line) > 1) or l == len(output):
                    line = line.split()
                    if l== len(output):
                        if len(self.Interfaces["Port-channel" + str(Number)].Eth.Members.values()) > 0:
                            base_multiplier = len(self.Interfaces["Port-channel" + str(Number)].Eth.Members)
                            base = 0
                            if "TenGig" in Name:
                                base = 10737418240
                            elif "Gig" in Name:
                                base = 1073741824
                            else:
                                base = 104857600
                            self.Interfaces["Port-channel" + str(Number)].Bandwidth.Physical_Bandwidth = base_multiplier * base
                    if not "(" in str(line[0]):
                        if not Number == "Null" and str(Number).isdigit():
                            if len(self.Interfaces["Port-channel" + str(Number)].Eth.Members.values()) > 0:
                                base_multiplier = len(self.Interfaces["Port-channel" + str(Number)].Eth.Members)
                                base = 0
                                if "TenGig" in Name:
                                    base = 10737418240
                                elif "Gig" in Name:
                                    base = 1073741824
                                else:
                                    base = 104857600
                                self.Interfaces["Port-channel" + str(Number)].Eth.Bandwidth=base_multiplier * base
                        Number = str(line[0])
                        if not Number == "Null" and str(Number).isdigit():
                            Status = str(str(line[1])[int(str(line[1]).find("(")) + 1:int(str(line[1]).find(")"))])
                            Status2 = str()
                            if "R" in Status:
                                Status2 = "L3"
                            elif "s" in Status:
                                Status2 = "L2"
                            self.Interfaces["Port-channel" + str(Number)].Eth.Layer_Type = Status2
                            if "S" in Status:
                                Status2 = "Suspended"
                            if "U" in Status:
                                Status2 = "Use"
                            elif "D" in Status:
                                Status2 += "Down"
                            self.Interfaces["Port-channel" + str(Number)].Eth.Ops_Status = Status2
                            Protocol = str(line[2])
                            if "-" in str(Protocol):
                                Protocol = "None"
                            self.Interfaces["Port-channel" + str(Number)].Eth.Protocol = str(Protocol)
                            c = 3
                            while c < len(line):
                                Name = str(line[c])[0:str(line[c]).find("(")]
                                if "Gi" in Name:
                                    Name = Name.replace("Gi", "GigabitEthernet")
                                elif "Te" in Name:
                                    Name = Name.replace("Te", "TenGigabitEthernet")
                                elif "Fa" in Name:
                                    Name = Name.replace("Fa", "FastEthernet")

                                Status = str(str(line[c])[int(str(line[c]).find("(")) + 1:int(str(line[c]).find(")"))])
                                if "P" in Status:
                                    Status = "Bundled"
                                elif "D" in Status:
                                    Status = "Down"
                                elif "S" in Status:
                                    Status = "Suspended"
                                else:
                                    Status = "Problematic"

                                if not Status == "Down":
                                    self.Interfaces["Port-channel" + str(Number)].Eth.Members[str(Name)]=str(Status)
                                c += 1

                    else:
                        c = 0
                        while c < len(line):
                            Name = str(line[c])[0:str(line[c]).find("(")]
                            if "Gi" in Name:
                                Name = Name.replace("Gi", "GigabitEthernet")
                            elif "Te" in Name:
                                Name = Name.replace("Te", "TenGigabitEthernet")
                            elif "Fa" in Name:
                                Name = Name.replace("Fa", "FastEthernet")
                            Status = str(str(line[c])[int(str(line[c]).find("(")):int(str(line[c]).find(")"))])
                            if "P" in Status:
                                Status = "Bundled"
                            elif "D" in Status:
                                Status = "Down"
                            elif "S" in Status:
                                Status = "Suspended"
                            else:
                                Status = "Problematic"

                            if not Status == "Down":
                                self.Interfaces["Port-channel" + str(Number)].Eth.Members[str(Name)] = str(Status)
                            c += 1
                else:
                    if "----" in line:
                        started = True
                l += 1

