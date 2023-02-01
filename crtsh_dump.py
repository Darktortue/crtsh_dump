#!/usr/bin/env python3

import sys
import urllib.request
import urllib.parse
import re
import csv
import requests
import argparse
import threading
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Fetch SSL certificates from crt.sh and write the result to a CSV file.')
parser.add_argument('domain', help='The domain to fetch SSL certificates for.')
parser.add_argument('-c', '--check', action='store_true', help='Check if the domain/subdomains are reachable.')

args = parser.parse_args()

domain = args.domain
domains = set()
with urllib.request.urlopen('https://crt.sh/?q=' + urllib.parse.quote('%.' + domain)) as f:
    code = f.read().decode('utf-8')
    with open(domain + '.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if args.check:
            writer.writerow(['Domain', 'Status'])
        domains.add(domain)
        if args.check:
            try:
                response = requests.get('https://' + domain, timeout=5)
                if response.status_code == 200:
                    writer.writerow([domain, 'Reachable'])
                else:
                    writer.writerow([domain, 'Unreachable'])
            except:
                writer.writerow([domain, 'Unreachable'])
        else:
            writer.writerow([domain])
        for cert, domain_name in tqdm(re.findall('<tr>(?:\s|\S)*?href="\?id=([0-9]+?)"(?:\s|\S)*?<td>([*_a-zA-Z0-9.-]+?\.' + re.escape(domain) + ')</td>(?:\s|\S)*?</tr>', code, re.IGNORECASE), desc='Fetching Data'):
            domain_name = domain_name.split('@')[-1]
            if not domain_name in domains:
                domains.add(domain_name)
                if args.check:
                    try:
                        response = requests.get('https://' + domain_name, timeout=5)
                        if response.status_code == 200:
                            writer.writerow([domain_name, 'Reachable'])
                        else:
                            writer.writerow([domain_name, 'Unreachable'])
                    except:
                        writer.writerow([domain_name, 'Unreachable'])
                else:
                    writer.writerow([domain_name])
