import yt_dlp
from collections import Counter
from datetime import datetime, timedelta
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pandas as pd
import numpy as np

class YoutubeAnalyzer:
    def __init__(self):
        # NLTK 데이터 다운로드
        nltk.download('punkt')
        nltk.download('stopwords')
        self.stop_words = set(stopwords.words('english'))
        
    def get_channel_info(self, url):
        ydl_opts = {
            'extract_flat': True,
            'force_generic_extractor': True,
            'quiet': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                return info
            except Exception as e:
                print(f"Error extracting channel info: {e}")
                return None

    def analyze_channel(self, channel_url):
        ydl_opts = {
            'extract_flat': True,
            'quiet': True,
            'ignoreerrors': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                channel_info = ydl.extract_info(channel_url, download=False)
                
                # 기본 채널 정보
                channel_data = {
                    'id': channel_info.get('id', ''),
                    'title': channel_info.get('title', ''),
                    'description': channel_info.get('description', ''),
                    'subscriber_count': channel_info.get('subscriber_count', 0),
                    'view_count': channel_info.get('view_count', 0),
                    'video_count': channel_info.get('video_count', 0),
                    'thumbnail': channel_info.get('thumbnail', '')
                }
                
                # 동영상 정보 수집
                videos = []
                for entry in channel_info.get('entries', []):
                    if entry:
                        videos.append({
                            'title': entry.get('title', ''),
                            'view_count': entry.get('view_count', 0),
                            'like_count': entry.get('like_count', 0),
                            'duration': entry.get('duration', 0),
                            'upload_date': entry.get('upload_date', ''),
                            'description': entry.get('description', '')
                        })
                
                # 분석 수행
                analysis = self._analyze_videos(videos)
                channel_data.update(analysis)
                
                return channel_data
                
            except Exception as e:
                print(f"Error analyzing channel: {e}")
                return None

    def _analyze_videos(self, videos):
        if not videos:
            return {}
            
        df = pd.DataFrame(videos)
        
        # 조회수 분석
        avg_views = df['view_count'].mean()
        median_views = df['view_count'].median()
        
        # 영상 길이 분석
        avg_duration = df['duration'].mean()
        
        # 업로드 패턴 분석
        df['upload_date'] = pd.to_datetime(df['upload_date'], format='%Y%m%d')
        upload_dates = df['upload_date'].sort_values()
        if len(upload_dates) > 1:
            avg_upload_interval = (upload_dates.max() - upload_dates.min()).days / (len(upload_dates) - 1)
        else:
            avg_upload_interval = 0
            
        # 인기 주제 분석
        all_titles = ' '.join(df['title'].str.lower())
        words = word_tokenize(all_titles)
        words = [word for word in words if word.isalnum() and word not in self.stop_words]
        popular_topics = Counter(words).most_common(5)
        
        # 성장 분석
        recent_videos = df.sort_values('upload_date', ascending=False).head(10)
        recent_avg_views = recent_videos['view_count'].mean()
        growth_rate = ((recent_avg_views - avg_views) / avg_views) * 100 if avg_views > 0 else 0
        
        return {
            'avg_views': int(avg_views),
            'median_views': int(median_views),
            'avg_duration': int(avg_duration),
            'upload_frequency': f"{avg_upload_interval:.1f} days",
            'popular_topics': [topic[0] for topic in popular_topics],
            'growth_rate': growth_rate,
            'performance_metrics': {
                'engagement_rate': self._calculate_engagement_rate(df),
                'consistency_score': self._calculate_consistency_score(df),
                'trend_alignment': self._analyze_trends(df)
            }
        }
    
    def _calculate_engagement_rate(self, df):
        if 'view_count' not in df.columns or 'like_count' not in df.columns:
            return 0
        return (df['like_count'].sum() / df['view_count'].sum()) * 100 if df['view_count'].sum() > 0 else 0
    
    def _calculate_consistency_score(self, df):
        if 'upload_date' not in df.columns:
            return 0
        
        # 업로드 간격의 표준편차를 계산하여 일관성 점수 산출
        upload_dates = df['upload_date'].sort_values()
        if len(upload_dates) > 1:
            intervals = upload_dates.diff().dropna().dt.days
            std_dev = intervals.std()
            # 표준편차가 작을수록 일관성이 높음 (최대 100점)
            return max(0, 100 - (std_dev / 7) * 10)  # 7일을 기준으로 점수 계산
        return 0
    
    def _analyze_trends(self, df):
        if len(df) < 5:
            return []
            
        recent_videos = df.sort_values('upload_date', ascending=False).head(5)
        trends = []
        
        # 조회수 트렌드
        view_trend = recent_videos['view_count'].mean() > df['view_count'].mean()
        if view_trend:
            trends.append("조회수 상승 추세")
            
        # 영상 길이 트렌드
        duration_trend = recent_videos['duration'].mean() > df['duration'].mean()
        if duration_trend:
            trends.append("영상 길이 증가 추세")
            
        return trends

    def get_growth_suggestions(self, analysis):
        suggestions = []
        
        # 조회수 기반 제안
        if analysis['avg_views'] < 1000:
            suggestions.append("SEO 최적화를 위해 제목과 설명에 주요 키워드를 포함하세요.")
            suggestions.append("썸네일 디자인을 더 매력적으로 개선해보세요.")
            
        # 업로드 주기 기반 제안
        upload_days = float(analysis['upload_frequency'].split()[0])
        if upload_days > 7:
            suggestions.append("더 규칙적인 업로드로 알고리즘 노출을 증가시키세요.")
            
        # 성장률 기반 제안
        if analysis['growth_rate'] < 10:
            suggestions.append("트렌딩 주제를 활용하여 콘텐츠를 다양화해보세요.")
            
        # 인기 주제 기반 제안
        if len(analysis['popular_topics']) > 0:
            suggestions.append(f"인기 있는 주제 '{analysis['popular_topics'][0]}'를 더 자주 다뤄보세요.")
            
        return suggestions
