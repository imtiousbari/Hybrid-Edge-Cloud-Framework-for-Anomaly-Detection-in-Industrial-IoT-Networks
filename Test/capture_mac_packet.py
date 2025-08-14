from scapy.all import sniff, TCP, UDP, IP, IPv6
import csv
import statistics
import socket
import struct
import os

# Folder to save CSVs
folder = "Test"
os.makedirs(folder, exist_ok=True)

csv_human = os.path.join(folder, "network_packets_human.csv")
csv_numeric = os.path.join(folder, "network_packets_numeric.csv")

# Write headers
headers = [
    "Payload Length","Inter Arrival Time","TCP Window Size","Jitter",
    "Stream 1 Mean","Stream 1 Var","Src IP 1 Mean","Src IP 1 Var",
    "Stream 5 Mean","Src IP 5 Var","Stream 10 Var","Stream 30 Var",
    "Src IP 60 Var","Channel 1 Mean","Protocol"
]

with open(csv_human, "w", newline="") as f:
    csv.writer(f).writerow(headers)
with open(csv_numeric, "w", newline="") as f:
    csv.writer(f).writerow(headers)

flows = {}
packet_count = 0  # Counter
max_packets = 100  # Stop after 20 packets

def ip_to_int(ip):
    try:
        return struct.unpack("!I", socket.inet_aton(ip))[0]
    except:
        try:
            return int(ip.replace(":", ""), 16) % (2**32)
        except:
            return 0

def protocol_to_num(proto):
    return 6 if proto=="TCP" else 17

def process_packet(pkt):
    global packet_count
    if packet_count >= max_packets:
        return False  # Stop sniffing

    if (IP in pkt or IPv6 in pkt) and (TCP in pkt or UDP in pkt):
        proto = "TCP" if TCP in pkt else "UDP"
        src = pkt[IP].src if IP in pkt else pkt[IPv6].src
        dst = pkt[IP].dst if IP in pkt else pkt[IPv6].dst
        payload_len = len(pkt[TCP].payload) if TCP in pkt else len(pkt[UDP].payload)
        tcp_window = pkt[TCP].window if TCP in pkt else 0
        timestamp = pkt.time

        key = (src, dst, proto)
        if key not in flows:
            flows[key] = {'timestamps': [], 'payloads': [], 'tcp_windows': []}

        flows[key]['timestamps'].append(timestamp)
        flows[key]['payloads'].append(payload_len)
        flows[key]['tcp_windows'].append(tcp_window)

        times = flows[key]['timestamps']
        iat = [j - i for i, j in zip(times[:-1], times[1:])] if len(times) > 1 else [0]
        jitter = statistics.stdev(iat) if len(iat) > 1 else 0

        def mean_var(lst, n):
            last_n = lst[-n:] if len(lst) >= n else lst
            return (statistics.mean(last_n), statistics.variance(last_n) if len(last_n) > 1 else 0)

        stream1_mean, stream1_var = mean_var(flows[key]['payloads'], 1)
        stream5_mean, srcip5_var = mean_var(flows[key]['payloads'], 5)
        stream10_var = statistics.variance(flows[key]['payloads'][-10:]) if len(flows[key]['payloads']) >= 10 else 0
        stream30_var = statistics.variance(flows[key]['payloads'][-30:]) if len(flows[key]['payloads']) >= 30 else 0
        srcip60_var = statistics.variance(flows[key]['payloads'][-60:]) if len(flows[key]['payloads']) >= 60 else 0
        channel1_mean = statistics.mean(flows[key]['payloads'])

        row_human = [
            payload_len,
            iat[-1] if iat else 0,
            tcp_window,
            jitter,
            stream1_mean,
            stream1_var,
            stream1_mean,
            stream1_var,
            stream5_mean,
            srcip5_var,
            stream10_var,
            stream30_var,
            srcip60_var,
            channel1_mean,
            proto
        ]

        row_numeric = [
            payload_len,
            iat[-1] if iat else 0,
            tcp_window,
            jitter,
            stream1_mean,
            stream1_var,
            ip_to_int(src),
            stream1_var,
            stream5_mean,
            srcip5_var,
            stream10_var,
            stream30_var,
            srcip60_var,
            channel1_mean,
            protocol_to_num(proto)
        ]

        with open(csv_human, "a", newline="") as f:
            csv.writer(f).writerow(row_human)
        with open(csv_numeric, "a", newline="") as f:
            csv.writer(f).writerow(row_numeric)

        packet_count += 1
        if packet_count >= max_packets:
            return False  # Stop sniffing

# Start sniffing
sniff(iface="en0", prn=process_packet, stop_filter=lambda x: packet_count >= max_packets)
print("Saved flows to", csv_human)
print("Saved flows to", csv_numeric)