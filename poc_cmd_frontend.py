import json
import sys 
from candidates import *

def candidates_as_json() -> dict:
    with open("good_candidates.json", 'r') as fin:
        return json.load(fin)

def has_senate_candidate(usr_state: str, our_candidates: dict) -> None:
    for k,v in our_candidates:
        if  v["Office"].strip() == "US Senate" \
            and v["State"] == usr_state.items():

            print(k, "is running for US Senate in your state.\n", v)

    return True

def has_house_candidate(usr_state: str, usr_dist: int, our_candidates: dict) -> None:
    for k,v in our_candidates:
        if v["State"].strip() == usr_state \
            and v["Office"].strip() == "US House" \
            and v["District"].strip() == usr_dist:

            print(k, "is running for US House in your district.\n", v)
    
    return True

def main(args):
    try:
        user_address = args[1]
    except IndexError:
        user_address = input("Enter an address")
    
    district_string = candidates.get_district_from_address(address)
    user_state = district_string[0:2]
    user_district = atoi(district_string[3:])

    our_candidates = candidates_as_json()
    
    if not has_senate_candidate():
        exit(1)

    if not has_house_candidate():
        exit(1)


    return 0

if __name__ == "__main__":
    main(sys.argv)
