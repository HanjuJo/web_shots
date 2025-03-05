import yt_dlp
from datetime import datetime
import pandas as pd
from typing import Dict, List, Optional
import json

class YouTubeAnalyzer:
    def __init__(self):
        self.ydl_opts = {
            'quiet': True,
            'extract_flat': True,
            'force_generic_extractor': True
        }

    def get_channel_info(self, channel_url: str) -> Dict:
        """채널 기본 정보를 가져옵니다."""
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                channel_info = ydl.extract_info(channel_url, download=False)
                return {
                    'channel_id': channel_info.get('id'),
                    'channel_name': channel_info.get('title'),
                    'subscriber_count': channel_info.get('subscriber_count'),
                    'view_count': channel_info.get('view_count'),
                    'video_count': len(channel_info.get('entries', [])),
                    'channel_description': channel_info.get('description'),
                    'channel_url': channel_url,
                    'entries': channel_info.get('entries', [])
                }
        except Exception as e:
            return {'error': str(e)}

    def get_video_info(self, video_url: str) -> Dict:
        """비디오 상세 정보를 가져옵니다."""
        try:
            opts = {**self.ydl_opts, 'extract_flat': False}
            with yt_dlp.YoutubeDL(opts) as ydl:
                video_info = ydl.extract_info(video_url, download=False)
                return {
                    'id': video_info.get('id'),
                    'title': video_info.get('title'),
                    'view_count': video_info.get('view_count'),
                    'like_count': video_info.get('like_count'),
                    'comment_count': video_info.get('comment_count'),
                    'duration': video_info.get('duration'),
                    'upload_date': video_info.get('upload_date'),
                    'description': video_info.get('description'),
                    'tags': video_info.get('tags', []),
                    'categories': video_info.get('categories', []),
                    'thumbnail': video_info.get('thumbnail'),
                    'is_shorts': video_info.get('duration', 0) <= 60
                }
        except Exception as e:
            return {'error': str(e)}

    def analyze_channel_content(self, channel_info: Dict) -> Dict:
        """채널 콘텐츠를 분석합니다."""
        videos = channel_info.get('entries', [])
        if not videos:
            return {'error': 'No videos found'}

        # 기본 통계
        total_views = sum(v.get('view_count', 0) for v in videos)
        avg_views = total_views / len(videos) if videos else 0

        # 업로드 시간 분석
        upload_times = [
            int(v.get('upload_date', '000000')[8:10])
            for v in videos if v.get('upload_date')
        ]
        
        time_distribution = pd.Series(upload_times).value_counts().to_dict()

        # 인기 동영상
        sorted_videos = sorted(videos, key=lambda x: x.get('view_count', 0), reverse=True)
        top_videos = sorted_videos[:5]

        return {
            'total_videos': len(videos),
            'total_views': total_views,
            'average_views': avg_views,
            'upload_time_distribution': time_distribution,
            'top_videos': top_videos
        }

    def analyze_video_performance(self, video_info: Dict) -> Dict:
        """비디오 성과를 분석합니다."""
        if 'error' in video_info:
            return video_info

        engagement_rate = 0
        if video_info.get('view_count'):
            likes = video_info.get('like_count', 0)
            comments = video_info.get('comment_count', 0)
            engagement_rate = ((likes + comments) / video_info['view_count']) * 100

        # 영상 길이에 따른 카테고리 분류
        duration = video_info.get('duration', 0)
        video_type = 'Shorts' if duration <= 60 else 'Regular'
        
        return {
            'engagement_rate': round(engagement_rate, 2),
            'video_type': video_type,
            'duration': duration,
            'tags_count': len(video_info.get('tags', [])),
            'has_description': bool(video_info.get('description')),
            'upload_time': datetime.strptime(
                video_info.get('upload_date', '20240101'), '%Y%m%d'
            ).strftime('%Y-%m-%d')
        }

    def get_shorts_analytics(self, channel_info: Dict) -> Dict:
        """쇼츠 분석을 수행합니다."""
        videos = channel_info.get('entries', [])
        if not videos:
            return {'error': 'No videos found'}

        # 쇼츠 vs 일반 영상 비율
        shorts_count = 0
        shorts_views = 0
        regular_count = 0
        regular_views = 0

        for video in videos:
            duration = video.get('duration', 0)
            views = video.get('view_count', 0)
            
            if duration <= 60:  # Shorts
                shorts_count += 1
                shorts_views += views
            else:  # Regular videos
                regular_count += 1
                regular_views += views

        total_videos = shorts_count + regular_count
        total_views = shorts_views + regular_views

        return {
            'shorts_count': shorts_count,
            'regular_count': regular_count,
            'shorts_percentage': (shorts_count / total_videos * 100) if total_videos else 0,
            'shorts_views': shorts_views,
            'regular_views': regular_views,
            'shorts_avg_views': shorts_views / shorts_count if shorts_count else 0,
            'regular_avg_views': regular_views / regular_count if regular_count else 0
        }
