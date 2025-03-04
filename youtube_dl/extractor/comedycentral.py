from __future__ import unicode_literals

from .mtv import MTVServicesInfoExtractor


class ComedyCentralIE(MTVServicesInfoExtractor):
    _VALID_URL = r'''(?x)https?://(?:www\.)?cc\.com/
        (video-clips|episodes|cc-studios|video-collections|full-episodes|shows)
        /(?P<title>.*)'''
    _FEED_URL = 'http://comedycentral.com/feeds/mrss/'

    _TESTS = [{
        'url': 'http://www.cc.com/video-clips/kllhuv/stand-up-greg-fitzsimmons--uncensored---too-good-of-a-mother',
        'md5': 'c4f48e9eda1b16dd10add0744344b6d8',
        'info_dict': {
            'id': 'cef0cbb3-e776-4bc9-b62e-8016deccb354',
            'ext': 'mp4',
            'title': 'CC:Stand-Up|August 18, 2013|1|0101|Uncensored - Too Good of a Mother',
            'description': 'After a certain point, breastfeeding becomes c**kblocking.',
            'timestamp': 1376798400,
            'upload_date': '20130818',
        },
    }, {
        'url': 'http://www.cc.com/shows/the-daily-show-with-trevor-noah/interviews/6yx39d/exclusive-rand-paul-extended-interview',
        'only_matching': True,
    }]


class ToshIE(MTVServicesInfoExtractor):
    IE_DESC = 'Tosh.0'
    _VALID_URL = r'^https?://tosh\.cc\.com/video-(?:clips|collections)/[^/]+/(?P<videotitle>[^/?#]+)'
    _FEED_URL = 'http://tosh.cc.com/feeds/mrss'

    _TESTS = [{
        'url': 'http://tosh.cc.com/video-clips/68g93d/twitter-users-share-summer-plans',
        'info_dict': {
            'description': 'Tosh asked fans to share their summer plans.',
            'title': 'Twitter Users Share Summer Plans',
        },
        'playlist': [{
            'md5': 'f269e88114c1805bb6d7653fecea9e06',
            'info_dict': {
                'id': '90498ec2-ed00-11e0-aca6-0026b9414f30',
                'ext': 'mp4',
                'title': 'Tosh.0|June 9, 2077|2|211|Twitter Users Share Summer Plans',
                'description': 'Tosh asked fans to share their summer plans.',
                'thumbnail': 're:^https?://.*\.jpg',
                # It's really reported to be published on year 2077
                'upload_date': '20770610',
                'timestamp': 3390510600,
                'subtitles': {
                    'en': 'mincount:3',
                },
            },
        }]
    }, {
        'url': 'http://tosh.cc.com/video-collections/x2iz7k/just-plain-foul/m5q4fp',
        'only_matching': True,
    }]

    @classmethod
    def _transform_rtmp_url(cls, rtmp_video_url):
        new_urls = super(ToshIE, cls)._transform_rtmp_url(rtmp_video_url)
        new_urls['rtmp'] = rtmp_video_url.replace('viacomccstrm', 'viacommtvstrm')
        return new_urls


class ComedyCentralTVIE(MTVServicesInfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?comedycentral\.tv/(?:staffeln|shows)/(?P<id>[^/?#&]+)'
    _TESTS = [{
        'url': 'http://www.comedycentral.tv/staffeln/7436-the-mindy-project-staffel-4',
        'info_dict': {
            'id': 'local_playlist-f99b626bdfe13568579a',
            'ext': 'flv',
            'title': 'Episode_the-mindy-project_shows_season-4_episode-3_full-episode_part1',
        },
        'params': {
            # rtmp download
            'skip_download': True,
        },
    }, {
        'url': 'http://www.comedycentral.tv/shows/1074-workaholics',
        'only_matching': True,
    }, {
        'url': 'http://www.comedycentral.tv/shows/1727-the-mindy-project/bonus',
        'only_matching': True,
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)

        webpage = self._download_webpage(url, video_id)

        mrss_url = self._search_regex(
            r'data-mrss=(["\'])(?P<url>(?:(?!\1).)+)\1',
            webpage, 'mrss url', group='url')

        return self._get_videos_info_from_url(mrss_url, video_id)
