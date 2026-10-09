#!/usr/bin/env python3
"""Compatibility entry point for the earlier public scaffold; never prints tokens."""
import argparse,json
from pathlib import Path
from run_fixture import Client

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--base-url',required=True)
    parser.add_argument('--fixture',type=Path,required=True)
    args=parser.parse_args()
    client=Client(args.base_url)
    client.initialize()
    print(json.dumps(client.run(json.loads(args.fixture.read_text()))))

if __name__=='__main__':main()
