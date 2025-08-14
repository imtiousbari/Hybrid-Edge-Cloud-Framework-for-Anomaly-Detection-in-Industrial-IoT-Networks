from scapy.all import sniff, TCP, UDP, IP, IPv6
import csv
import time
import os

# Store flows: key = (src_port, dst_port, proto), value = flow info
flows = {}

# CSV file to save flows
folder = "Test"
csv_file = os.path.join(folder, "network_flows.csv")

# Initialize CSV with headers
with open(csv_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Src Port", "Dst Port", "Protocol", "Total Fwd Packet", "Total Bwd packets", "Flow Duration"])

# Function to process each packet
def process(pkt):
    if (IP in pkt or IPv6 in pkt) and (TCP in pkt or UDP in pkt):
        proto = 6 if TCP in pkt else 17
        src_port = pkt[TCP].sport if TCP in pkt else pkt[UDP].sport
        dst_port = pkt[TCP].dport if TCP in pkt else pkt[UDP].dport

        key_fwd = (src_port, dst_port, proto)
        key_bwd = (dst_port, src_port, proto)

        # Initialize flow if not exists
        if key_fwd not in flows and key_bwd not in flows:
            flows[key_fwd] = {'Total_Fwd': 0, 'Total_Bwd': 0, 'start': pkt.time, 'end': pkt.time}

        # Update flow counters
        if key_fwd in flows:
            flows[key_fwd]['Total_Fwd'] += 1
            flows[key_fwd]['end'] = pkt.time
        else:
            flows[key_bwd]['Total_Bwd'] += 1
            flows[key_bwd]['end'] = pkt.time

# Sniff only 20 packets
sniff(iface="en0", prn=process, count=100)

# Write flows to CSV (will be ≤ 20 rows)
with open(csv_file, "a", newline="") as f:
    writer = csv.writer(f)
    for (src_port, dst_port, proto), flow in flows.items():
        duration = flow['end'] - flow['start']
        writer.writerow([src_port, dst_port, proto, flow['Total_Fwd'], flow['Total_Bwd'], round(duration,5)])

print("Saved flows to", csv_file)

