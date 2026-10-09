#!/usr/bin/env python3
import argparse, json, urllib.request

def post(url, payload, token=None):
    data=json.dumps(payload).encode()
    req=urllib.request.Request(url,data=data,headers={"Content-Type":"application/json"})
    if token:
        req.add_header("Authorization",f"Bearer {token}")
    with urllib.request.urlopen(req,timeout=30) as r:
        return json.loads(r.read().decode())

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--base-url",required=True)
    p.add_argument("--fixture",required=True)
    args=p.parse_args()
    with open(args.fixture,"r",encoding="utf-8") as f:
        fixture=json.load(f)
    session=post(args.base_url.rstrip("/")+"/v1/challenge/session",{})
    print(json.dumps({"session":session,"fixture":fixture},indent=2))
    print("Client scaffold only: record/query submission is enabled when the public endpoint publishes its token contract.")

if __name__=="__main__":
    main()
