import subprocess
import json
import re
from dateutil import parser as date_parser

def parse_tcpdump_output(line):
    # Modify this function to parse the output according to your needs
    try:
        parts = line.split()
        timestamp = date_parser.parse(parts[0])
        src = parts[2]
        dst = parts[4].rstrip(':')
        return {
            "timestamp": str(timestamp),
            "source": src,
            "destination": dst
        }
    except Exception as e:
        print(f"Error parsing line: {e}")
        return None

def capture_traffic(interface, count=10):
    # Run tcpdump and capture a specified number of packets
    command = ["sudo", "tcpdump", "-i", interface, "-c", str(count), "-n"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, text=True)

    packet_data = []
    while True:
        line = process.stdout.readline()
        if not line:
            break
        packet_info = parse_tcpdump_output(line)
        if packet_info:
            packet_data.append(packet_info)

    return packet_data

# Example usage
interface = "eth0"  # Replace with your network interface
packet_count = 10   # Number of packets to capture
packets = capture_traffic(interface, packet_count)
print(json.dumps(packets, indent=4))
