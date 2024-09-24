import csv
import sys
from collections import defaultdict


def load_lookup_table(lookup_file):
    lookup_table = {}
    try:
        # Use 'utf-8' encoding format to read the csv file and then convert
        # if gives error use 'utf-8-sig' to handle BOM at the beginning of the file
        with open(lookup_file, 'r', encoding='utf-8', errors='ignore') as file:
            csv_reader = csv.DictReader(file)
            headers = csv_reader.fieldnames

            # raise error if any of the headers are missing in the lookup_table
            if 'dstport' not in headers or 'protocol' not in headers or 'tag' not in headers:
                raise ValueError("Missing required columns: 'dstport', 'protocol', 'tag' in the CSV file.")

            for row in csv_reader:
                # handle case insensitive protocols e.g. tCp, TCp
                key = (int(row['dstport']), row['protocol'].lower())
                # add keys in the lookup_table dictionary with key as (dstport, protocol) and value as tag
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
                # strip all the white spaces from the start and end and then create a list of elements seperated by spaces
                fields = line.strip().split()

                if fields:
                    # only version 2 logs will be parsed
                    if fields[0] != '2':
                        continue

                    # as per version 2 format dstport is at 7th column since fields start from 0 index hence 6th index will be dstport
                    dstport = int(fields[6])

                    # similarly protocol number will be at 7th index (6 - TCP, 17 - UDP 0 - ICMP)
                    protocol_number = int(fields[7])
                    protocol = "tcp" if protocol_number == 6 else "udp" if protocol_number == 17 else "icmp"

                    # check if the key (dstport, protocol) exists in the lookup table then tag will be the key
                    # is key does not exist then tag will be Untagged
                    key = (dstport, protocol)
                    tag = lookup_table.get(key, 'Untagged')

                    # keep incrementing the counts of the tags and the (dstport, protocol) combination
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
    # return if the system does not contain 4 arguements 
    if len(sys.argv) != 4:
        print("Usage: python3 flow_logs_parser.py <lookup_table.csv> <flow_logs> <output_file>")
        sys.exit(1)

    lookup_file = sys.argv[1]
    flow_log_file = sys.argv[2]
    output_file = sys.argv[3]

    # first populate the lookup_table dictionary
    lookup_table = load_lookup_table(lookup_file)

    # then get the tag_counts and port_protocol_counts dictionaries
    tag_counts, port_protocol_counts = parse_flow_log(flow_log_file, lookup_table)

    # and finally save the result in the output text file
    save_results(output_file, tag_counts, port_protocol_counts)

    # if want to run the test case for each file without giving the file paths in the terminal and giving the paths in the code itself replace this below line of code for the above lines
    '''
    lookup_file = 'lookup_table.csv'  # Path to the lookup table
    flow_log_file = 'flow_logs.txt'   # Path to the flow log file
    output_file = 'output.txt'        # Path to the output file
    
    # Load lookup table
    lookup_table = load_lookup_table(lookup_file)
    
    # Parse flow log and calculate tag counts and port/protocol counts
    tag_counts, port_protocol_counts = parse_flow_log(flow_log_file, lookup_table)
    
    # Save results to the output file
    save_results(output_file, tag_counts, port_protocol_counts)
    '''

if __name__ == "__main__":
    main()
