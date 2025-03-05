import json
import argparse
from typing import TypedDict
from collections import defaultdict, deque

SUBWAY_ALL_INFO: dict[str, list["SubwayStation"]] = defaultdict(list)
RAW_DATA_PATH = './data/raw_subway_info.json'
SUBWAY_INFO_PATH = './data/subway_info.json'


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
    with open(RAW_DATA_PATH, 'r') as f:
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
    
    with open(SUBWAY_INFO_PATH, 'w') as f:
        info = json.dumps(SUBWAY_ALL_INFO)
        f.write(info)

def load_subway_info():
    with open(SUBWAY_INFO_PATH, 'r') as f:
        raw_data = f.read()
    info = json.loads(raw_data)
    SUBWAY_ALL_INFO.update(info)

def bfs(station:str , distance: int, 
       banned_stations: set[str] = set(), 
       banned_lines: set[str] = set(), 
       max_changes: int | None = None) -> list[tuple[str, str]]:
    queue = deque([(st, float('inf') if max_changes is None else max_changes) for st in SUBWAY_ALL_INFO[station] if st['name'] not in banned_stations and st['line'] not in banned_lines])
    result = set()

    while queue:
        for _ in range(len(queue)):
            st, remaining_changes = queue.popleft()
            if (st['name'], st['line']) in result or st['name'] in banned_stations or st['line'] in banned_lines or remaining_changes < 0:
                continue
            result.add((st['name'], st['line']))
            if st['prev'] and st['prev'] not in banned_stations:
                prev_infos = SUBWAY_ALL_INFO[st['prev']]
                for info in prev_infos:
                    if info['line'] in banned_lines:
                        continue
                    queue.append((info, remaining_changes - int(info['line'] != st['line'])))
            if st['next'] and st['next'] not in banned_stations:
                next_infos = SUBWAY_ALL_INFO[st['next']]
                for info in next_infos:
                    if info['line'] in banned_lines:
                        continue
                    queue.append((info, remaining_changes - int(info['line'] != st['line'])))
        distance -= 1
        if distance < 0:
            return list(result)
    return list(result)

def format_output(result: list[tuple[str, str]]) -> dict:
    output_result = defaultdict(list)
    for station, line in result:
        output_result[line].append(station)
    for line, stations in output_result.items():
        print(f'{line}:', ' '.join(stations))
    return output_result


def main(
    station: str, distance: int, 
    banned_stations: set[str] = set(), banned_lines: set[str] = set(), 
    max_changes: int | None = None):
    load_subway_info()
    parsed_banned_lines = {f'{line}号线' for line in banned_lines}
    result = bfs(station, distance, banned_stations=banned_stations, banned_lines=parsed_banned_lines, max_changes=max_changes)
    format_output(result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Shanghai Subway Station Finder')
    parser.add_argument('station', type=str, help='Starting station name')
    parser.add_argument('distance', type=int, help='Search distance')
    parser.add_argument('--build', action='store_true', help='Build subway info from raw data')
    parser.add_argument('--banned-station', nargs='*', default=set(), type=str,
                       help='Banned station names (can specify multiple)')
    parser.add_argument('--banned-lines', nargs='*', default=set(), type=str,
                       help='Banned line numbers (can specify multiple)')
    parser.add_argument('--max-changes', type=int, default=None, help='Maximum number of changes allowed')
    args = parser.parse_args()
    if args.build:
        build_subway_info()
    main(args.station, args.distance, banned_stations=set(args.banned_station), banned_lines=set(args.banned_lines),
         max_changes=args.max_changes)
