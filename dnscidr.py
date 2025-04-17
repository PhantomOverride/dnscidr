#!/usr/bin/env python3
import argparse
import dns.resolver
import ipaddress
from os.path import isfile
import sys


def dns_resolutions_matching_cidr(input_file, output_file, cidrs):
	counter_tried = counter_found = counter_accepted = 0
	with open(input_file, "r") as infile, open(output_file, "w") as outfile:
		for line in infile:
			host_value = line.strip()
			print("Looking up", host_value)
			dns_resolver = dns.resolver.Resolver()
			try:
				counter_tried += 1
				dns_answers = dns.resolver.resolve(host_value, "A")
				for dns_answer in dns_answers:
					counter_found += 1
					dns_answer = str(dns_answer)
					print("Host", host_value, "resolves to", dns_answer)
					for cidr in cidrs:
						if ( ipaddress.IPv4Address(dns_answer) in ipaddress.IPv4Network(cidr, strict=False) ):
							counter_accepted += 1
							print(cidr, "matches", dns_answer, ", adding to results.")
							print("Host", host_value, "with A record", dns_answer,"belongs to network",cidr,"- adding to results.")
							outfile.write(f"{host_value};{dns_answer}\n")
			except KeyboardInterrupt:
				print("Ctrl-C detected, exiting...")
				exit(1)
			except dns.resolver.NXDOMAIN:
				print("Query for", host_value, "resulted in not found.")
			except dns.resolver.NoAnswer:
				print("Query for", host_value, "did not yield an answer.")
			except dns.resolver.NoNameservers:
				print("Query for", host_value, "failed; no nameservers.")
			except dns.resolver.Timeout:
				print("Query for", host_value, "timed out.")
			except dns.exception.DNSException as e:
				print("Query for", host_value, "resulted in other DNS error:", e)
	print("[ + ] Finished.", counter_tried, "names tried,", counter_found, "A records found, and", counter_accepted, "records saved.")


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Iterate over hostnames in file, and return those that map to a network.")
	parser.add_argument("-i", "--input", help="Input file.", required=True)
	parser.add_argument("-o", "--output", help="Output file.", required=True)
	parser.add_argument("networks", nargs='+', help='Networks to keep results for.')
	args = parser.parse_args()

	if ( not isfile(args.input) ):
		print("[ Error ] Input file does not exist.")
		exit(1)
	elif ( isfile(args.output) ):
		print("[ Error ] Output file exists. Please specify new file.")
		exit(1)

dns_resolutions_matching_cidr(args.input, args.output, args.networks)
