    def OSPF_Neighbors(self, conn):
        if self.Empty_OSPF():
            OSPF_P_ID_Output = conn.send_command("show runn | inc router ospf", delay_factor=2, expect_string='#')
            ##Check Neighbors Per OSPF Process ID

            OSPF_P_ID_Output = str(OSPF_P_ID_Output).split("\n")
            for line in OSPF_P_ID_Output:
                line = line.split()
                if len(line) > 1:
                    OSPFPR = OSPF_Process(int(line[2]))
                    OSPFPR.Identify_OSPF_Neighbour_BR(conn, 0)
                    self.OSPFs.append(OSPFPR)


    def Connectivity_Check(self, conn, Depth: int, Ping_Count: int, Ping_Size: int):
        conn.send_command("terminal width 0", delay_factor=2, expect_string='#')
        conn.send_command("terminal length 0", delay_factor=2, expect_string='#')
        df = 100
        soutput = str()
        self.OSPF_Neighbors(conn)
        for O_Process in self.OSPFs:
            for neighbor in O_Process.Neighbors:
                output = conn.send_command(
                    "ping {} re {} size {} source loop 0".format(str(neighbor.RID), str(Ping_Count), str(Ping_Size), expect_string='#', delay_factor=10, max_loops=1000))
                output = output.split("\n")
                output_2 = str()
                for line in output:
                    if "Success" in line:
                        output_2 += line + "   -      "
                soutput += "\n" + "OSPF Neighbour: " + str(neighbor.RID) + "   Result: "
                soutput += str(output_2)


