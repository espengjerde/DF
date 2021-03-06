import conf
import subprocess as sp
from stats.logger import Log
class Statistics:
    """
    Shows statistics based on ip_address
    """
    

    def __init__(self):
        self.log = Log()

    
    def get_conntrack(self, ip):
        """
        Returns list of ip_conntrack entries of self.ip
        """
        ipct = open(conf.files.ip_conntrack).read().split("\n")
        return [line for line in ipct if line.find(ip) > 0] #add lines with self.ip to my-list.

    def get_active_connections(self, ip):
        """
        Returns number of active connections to self.ip
        """
        return len(self.get_conntrack(ip))
    
    def get_iptables_io(self, ip):
        """
        Executes call to iptables and filters out info about ip

        Returns dictionary with following info:
            pkt_sent = Packages sent from self.ip (int)
            pkt_received = Packages recieved to self.ip (int)
            bytes_sent  = Bytes sent from self.ip (int)
            bytes_received = Bytes received to self.ip (int)
        """
        ipcmd = ['iptables', '-nvxL']
        ipres  = sp.Popen(ipcmd, stdout=sp.PIPE).communicate()[0].split("\n")
        res = [line for line in ipres if line.find(ip) > 0]

        if res:
            tx_pkts = int(res[0].split(*'')[0])
            rx_pkts = int(res[1].split(*'')[0])
            tx_bytes = int(res[0].split(*'')[1])
            rx_bytes = int(res[1].split(*'')[1])

            return {'pkt_sent':tx_pkts, 'pkt_received':rx_pkts, 'bytes_sent':tx_bytes, 'bytes_received':rx_bytes}
        else:
            self.log.error("df_user_stats.py: Something wrong with iptables-lookup...: "+ip)
