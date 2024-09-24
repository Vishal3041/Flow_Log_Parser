import csv
import sys
from collections import defaultdict


def load_lookup_table(lookup_file):
    lookup_table = {}
    try:
        # Use 'utf-8-sig' to handle BOM at the beginning of the file
        with open(lookup_file, 'r', encoding='utf-8-sig', errors='ignore') as file:
            csv_reader = csv.DictReader(file)

            # Print the header row to debug the problem
            headers = csv_reader.fieldnames
            # print(f"CSV Headers: {headers}")

            # Check if the expected headers are present
            if 'dstport' not in headers or 'protocol' not in headers or 'tag' not in headers:
                raise ValueError("Missing required columns: 'dstport', 'protocol', 'tag' in the CSV file.")

            for row in csv_reader:
                # Use lower case for case-insensitive comparison
                key = (int(row['dstport']), row['protocol'].lower())
                lookup_table[key] = row['tag']
    except Exception as e:
        print(f"Error reading lookup file: {e}")
    return lookup_table


def parse_flow_log(flow_log_file, lookup_table):
    tag_counts = defaultdict(int)
    port_protocol_counts = defaultdict(int)
    # assuming port 22 (SSH) is always open
    tag_counts['sv_P4'] = 1
    port_protocol_counts[(22, 'tcp')] = 1

    try:
        with open(flow_log_file, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                fields = line.strip().split()

                if fields:
                    # Only process version 2 logs
                    if fields[0] != '2':
                        continue

                    dstport = int(fields[6])
                    protocol_number = int(fields[7])
                    protocol = "tcp" if protocol_number == 6 else "udp" if protocol_number == 17 else "icmp"

                    # Lookup in the table using dstport and protocol combination
                    key = (dstport, protocol)
                    tag = lookup_table.get(key, 'Untagged')

                    # Update counts
                    tag_counts[tag] += 1
                    port_protocol_counts[key] += 1
    except Exception as e:
        print(f"Error reading flow log file: {e}")
    return tag_counts, port_protocol_counts


def save_results(output_file, tag_counts, port_protocol_counts):
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write("Tag Counts:\n")
            file.write("Tag,Count\n")
            for tag, count in sorted(tag_counts.items()):
                file.write(f"{tag},{count}\n")

            file.write("\nPort/Protocol Combination Counts:\n")
            file.write("Port,Protocol,Count\n")
            for (port, protocol), count in sorted(port_protocol_counts.items()):
                file.write(f"{port},{protocol},{count}\n")
    except Exception as e:
        print(f"Error writing output file: {e}")


def main():
    # Accept file paths from command-line arguments
    if len(sys.argv) != 4:
        print("Usage: python3 flow_logs_parser.py <lookup_table.csv> <flow_logs> <output_file>")
        sys.exit(1)

    lookup_file = sys.argv[1]
    flow_log_file = sys.argv[2]
    output_file = sys.argv[3]

    lookup_table = load_lookup_table(lookup_file)

    tag_counts, port_protocol_counts = parse_flow_log(flow_log_file, lookup_table)

    save_results(output_file, tag_counts, port_protocol_counts)


if __name__ == "__main__":
    main()
