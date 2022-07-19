from pyarr import SonarrAPI
from sys import argv

def unmonitor_all_downloaded(host, api_key):
    sonarr = SonarrAPI(host, api_key)
    series_list = sonarr.get_series()
    counter = {}
    try:
        for series in series_list:
            episodes = sonarr.get_episodes_by_series_id(series['id'])
            for episode in episodes:
                if episode['hasFile'] and episode['monitored']:
                    episode['monitored'] = False
                    sonarr.upd_episode(episode['id'], episode)
                    counter[series['title']] = counter.get(series['title'], 0) + 1
    finally:
        print('Unmonitored:')
        [print(f'\t{title}: {count} episodes') for title, count in counter.items()]

def main():
    if len(argv) < 3:
        print("Usage: python unmonitor-downloaded-episodes.py baseURL API-KEY")
        return

    API_KEY = argv[2]
    host = argv[1]
    unmonitor_all_downloaded(host, API_KEY)


if __name__ == "__main__":
    main()