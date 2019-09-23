import json
import re
import sys
import os
from functools import reduce
from typing import List, Tuple
from collections import Counter

import requests
from argparse import ArgumentParser


class RequestError(Exception):
    pass


class MechanicCountExtractor:
    geeklist = "geeklist"
    mechanics = "mechanics"

    def __init__(self, api_address: str, geeklists: List[int]):
        self._geeklists = geeklists
        self._api_address = api_address

    def get_top_mechanics_for_geeklists(self, topn: str = None) -> List[Tuple[str, int]]:
        mechanics = []
        for list_id in self._geeklists:
            structured_response = self._get_geeklist(list_id)
            mechanics = mechanics + self._flatten_mechanics(structured_response)
        return self._count_mechanics(mechanics, int(topn) if topn else None)

    def _get_geeklist(self, list_id) -> json:
        headers = {'Bgg-Field-Whitelist': MechanicCountExtractor.mechanics}
        r = requests.get(f'http://{self._api_address}/geeklist/{list_id}', headers=headers)
        if r.status_code != 200:
            raise RequestError(f"Unknown status code received from api - {r.status_code}")
        return r.json()

    @staticmethod
    def _flatten_mechanics(games: List[dict]) -> List[str]:
        mechanics = [game[MechanicCountExtractor.mechanics]
                     for game in games if MechanicCountExtractor.mechanics in game]
        return reduce(lambda x, y: x + y, mechanics)

    def _count_mechanics(self, mechanics: List[str], topn=None) -> List[Tuple[str, int]]:
        mechanics = [self._strip_bgg_prefix(mechanic) for mechanic in mechanics]
        counter = Counter(mechanics)
        return counter.most_common(topn)

    @staticmethod
    def _strip_bgg_prefix(mechanic_name):
        return re.sub(r'^\w{2,3}-[\d\w]{2,3}\s+', '', mechanic_name)


def main(prog):
    usage = f"{prog} args"
    parser = ArgumentParser(usage)
    parser.add_argument('--geeklist', action='append', required=True)
    parser.add_argument('--api', default="game-selector.sixfootsoftware.com:8080")
    parser.add_argument('--topn')

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('--show-counts', dest='show_counts', action='store_true')
    group.add_argument('--hide-counts', dest='show_counts', action='store_false')
    parser.set_defaults(show_counts=True)

    args = vars(parser.parse_args())

    mechanics_count = MechanicCountExtractor(args.get("api"), args.get(MechanicCountExtractor.geeklist))
    for row in mechanics_count.get_top_mechanics_for_geeklists(args.get("topn")):
        if args.get("show_counts"):
            print(f"{row[0]}\t({row[1]})")
        else:
            print(f"{row[0]}")


if __name__ == "__main__":
    program_name = os.path.basename(sys.argv[0])
    main(program_name)
