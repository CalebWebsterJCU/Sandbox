"""
Top Videos
2020
This program uses a web request to find the top trending youtube videos.
"""

import sys
from googleapiclient.discovery import build

DEFAULT_NUM = 10
DEFAULT_REGION = 'AU'
API_KEY = 'AIzaSyB2IJ-j6nENGSFhZ3IxDym5uFvyIRTFUnA'


def main():
    """Get number of videos, get details for popular videos, and print details."""
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    region_snippets = youtube.i18nRegions().list(part='snippet').execute()
    valid_region_codes = {code['snippet']['gl']: code['snippet']['name'] for code in region_snippets['items']}
    num_of_videos = get_num_videos(DEFAULT_NUM)
    region_code = get_valid_region_code(valid_region_codes, DEFAULT_REGION)
    videos = get_top_videos(youtube, num_of_videos, region_code)
    print_videos(videos, valid_region_codes[region_code])
    print(valid_region_codes)


def get_num_videos(default=10):
    """Get and return number of videos from run command, otherwise return default."""
    try:
        return int(sys.argv[1])
    except ValueError:
        return default
    except IndexError:
        return default


def get_valid_region_code(valid_codes, default='AU'):
    """Get and return region code from run command, otherwise return default."""
    try:
        region_code = sys.argv[2].upper()
        return region_code if region_code in valid_codes else default
    except IndexError:
        return default


def get_top_videos(yt_api, n, r_c):
    """Use the youtube API to retreive details of the most popular videos."""
    videos = []
    # Perform 2 requests to youtube API for video details and statistics
    snippets = yt_api.videos().list(part='snippet', chart='mostPopular', maxResults=n, regionCode=r_c).execute()
    statistics = yt_api.videos().list(part='statistics', chart='mostPopular', maxResults=n, regionCode=r_c).execute()
    # Create lists of provided information
    ids = [video['id'] for video in snippets['items']]
    channel_ids = [video['snippet']['channelId'] for video in snippets['items']]
    titles = [video['snippet']['title'] for video in snippets['items']]
    view_counts = [int(video['statistics']['viewCount']) for video in statistics['items']]

    for i in range(len(titles)):
        # Get channel name from channel id
        channel = yt_api.channels().list(part='snippet', id=channel_ids[i], maxResults=1).execute()['items'][0]['snippet']['title']
        # Compile information into a single dictionary for each video
        video = {'title': titles[i], 'view_count': view_counts[i], 'channel': channel, 'url': f'https://www.youtube.com/watch?v={ids[i]}'}
        videos.append(video)

    return videos


def print_videos(videos, region):
    """Display details for all videos in a list."""
    print(f"Top {len(videos)} Youtube Videos in {region}:")
    for x in range(len(videos)):
        print(f"{x + 1}. {videos[x]['title']} - {videos[x]['view_count']:,} views")
        print(f"{videos[x]['channel']}")
        print(f"{videos[x]['url']}")


if __name__ == '__main__':
    main()
