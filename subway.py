import json
import argparse
from typing import TypedDict
from collections import defaultdict, deque

SUBWAY_ALL_INFO = defaultdict(list)

class SubwayStation(TypedDict):
    name: str
    line: str
    prev: str
    next: str


def build_subway_info():
    '''
    structure: 
    {
        "l": [{
                "ln": "2号线",
                "st": [
                    {
                        "n": "凌空路",
                    },
                    ...
                ]
            },
            ...
        ]
    }
    '''
    with open('./raw_subway_info.json', 'r') as f:
        raw_data = f.read()
    data = json.loads(raw_data)

    for line in data['l']:
        prev = None
        line_name = line['ln']
        for station in line['st']:
            station_name = station['n']
            subway_info = SubwayStation(
                name=station_name,
                line=line_name,
                prev=prev['name'] if prev else None,
                next=None
            )
            if prev is not None:
                prev['next'] = station_name
            prev = subway_info
            SUBWAY_ALL_INFO[station_name].append(subway_info)
    
    with open('./subway_info.json', 'w') as f:
        info = json.dumps(SUBWAY_ALL_INFO)
        f.write(info)

def load_subway_info():
    with open('./subway_info.json', 'r') as f:
        raw_data = f.read()
    info = json.loads(raw_data)
    SUBWAY_ALL_INFO.update(info)

def bfs(station, distance, banned_stations: set[str] = set()) -> list[str]:
    queue = deque([station])
    result = set()

    while queue:
        for _ in range(len(queue)):
            st = queue.popleft()
            if st in result or st in banned_stations:
                continue
            result.add(st)
            for info in SUBWAY_ALL_INFO[st]:
                if info['prev'] and info['prev'] not in banned_stations:
                    queue.append(info['prev'])
                if info['next'] and info['next'] not in banned_stations:
                    queue.append(info['next'])
        distance -= 1
        if distance < 0:
            return list(result)
    return list(result)

def format_output(result: list[str], banned_lines: set[str]=set()) -> dict:
    output_result = defaultdict(set)

    for r in result:
        infos = SUBWAY_ALL_INFO[r]
        for info in infos:
            output_result[info['line']].add(r)

    for key, value in output_result.items():
        if key.split('号')[0] in banned_lines:
            continue
        print(key + ':', ' '.join(value))
    return output_result


def main(station: str, distance: int, banned_stations: set[str] = set(), banned_lines: set[str] = set()):
    load_subway_info()
    result = bfs(station, distance, banned_stations=banned_stations)
    format_output(result, banned_lines=banned_lines)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Shanghai Subway Station Finder')
    parser.add_argument('station', type=str, help='Starting station name')
    parser.add_argument('distance', type=int, help='Search distance')
    parser.add_argument('--build', action='store_true', help='Build subway info from raw data')
    parser.add_argument('--banned-station', nargs='*', default=set(), type=str,
                       help='Banned station names (can specify multiple)')
    parser.add_argument('--banned-lines', nargs='*', default=set(), type=str,
                       help='Banned line numbers (can specify multiple)')
    args = parser.parse_args()
    if args.build:
        build_subway_info()
    main(args.station, args.distance, banned_stations=set(args.banned_station), banned_lines=set(args.banned_lines))
