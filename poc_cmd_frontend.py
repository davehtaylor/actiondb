import json
import sys 
import requests 

def get_info_from_address(usr_address: str) -> dict:
    api_key = ""

    with open("test-key.txt", "r") as k:
        api_key = k.read()
    
    payload = {"address": usr_address, "key":api_key, "electionId":2000}
    res = requests.get("https://www.googleapis.com/civicinfo/v2/voterinfo", params=payload).json()

    if "error" in res:
        print(res["error"])
        return False
    
    return res

def has_senate_candidate(usr_state: str, our_candidates: dict) -> None:
    for k in our_candidates.keys():
        c = our_candidates[k]
        if  c["Office"].strip() == "US Senate" \
            and c["State"] == usr_state:

            print(k, "is running for US Senate in your state.\n", c)

    return True

def has_house_candidate(usr_state: str, usr_dist: int, our_candidates: dict) -> None:
    for k in our_candidates:
        c = our_candidates[k]
        if c["State"].strip() == usr_state \
            and c["Office"].strip() == "US House" \
            and c["District"] == usr_dist:

            print(k, "is running for US House in your district.\n", c)
    
    return True

def get_congressional_district(api_info: dict) -> int:
    for c in api_info["contests"]:
        try:
            if any(o in c["office"] for o in {"United States Representative", \
                                              "U. S. Representative", \
                                              "US Representative", \
                                              "U S Representative"}):

                return int(c["office"].split(' ')[-1])
        except KeyError:
            continue

def main(args):
    try:
        usr_address = args[1]
    except IndexError:
        usr_address = input("Enter an address")

    api_info = get_info_from_address(usr_address)
    
    usr_state = api_info["normalizedInput"]["state"]
    usr_district = get_congressional_district(api_info)

    with open("good_candidates.json", 'r') as fin:
        our_candidates = json.load(fin)
    
    if not has_senate_candidate(usr_state, our_candidates):
        exit(1)

    if not has_house_candidate(usr_state, usr_district, our_candidates):
        exit(1)

    return 0

if __name__ == "__main__":
    main(sys.argv)
