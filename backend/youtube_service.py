import yt_dlp
from collections import Counter
import re
from datetime import datetime

class YoutubeAnalyzer:
    def __init__(self):
        self.ydl_opts = {
            "quiet": True,
            "extract_flat": True,
            "force_generic_extractor": True
        }

    def analyze_shorts(self, keyword, max_results=10):
        """쇼츠 영상 분석"""
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            search_results = ydl.extract_info(f"ytsearch{max_results}: {keyword} Shorts", download=False)

        videos = []
        if "entries" in search_results:
            for entry in search_results["entries"]:
                video_info = {
                    "title": entry["title"],
                    "url": entry["url"],
                    "viewCount": entry.get("view_count", 0),
                    "uploadDate": entry.get("upload_date", ""),
                    "channelName": entry.get("uploader", ""),
                    "channelUrl": entry.get("uploader_url", ""),
                    "hashtags": self._extract_hashtags(entry["title"]),
                    "thumbnail": entry.get("thumbnail", ""),
                    "likeCount": entry.get("like_count", 0),
                    "commentCount": entry.get("comment_count", 0)
                }
                
                # 참여율 계산
                if video_info["viewCount"] > 0:
                    engagement = ((video_info["likeCount"] + video_info["commentCount"]) / video_info["viewCount"]) * 100
                    video_info["engagementRate"] = round(engagement, 2)
                else:
                    video_info["engagementRate"] = 0
                    
                videos.append(video_info)

        # 통계 분석
        if videos:
            stats = self._calculate_statistics(videos)
            insights = self._generate_insights(videos)
            
            return {
                "videos": sorted(videos, key=lambda x: x["viewCount"], reverse=True),
                "statistics": stats,
                "insights": insights
            }
        
        return {"videos": [], "statistics": {}, "insights": []}

    def analyze_top_videos(self, keyword, max_results=5):
        """일반 영상 분석"""
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            search_results = ydl.extract_info(f"ytsearch{max_results}: {keyword}", download=False)

        videos = []
        if "entries" in search_results:
            for entry in search_results["entries"]:
                description = entry.get("description", "설명 없음")
                if description is None:
                    description = "설명 없음"
                else:
                    description = description[:200] + "..."

                video_info = {
                    "title": entry["title"],
                    "url": entry["url"],
                    "viewCount": entry.get("view_count", 0),
                    "description": description,
                    "uploadDate": entry.get("upload_date", ""),
                    "duration": entry.get("duration", 0),
                    "channelName": entry.get("uploader", ""),
                    "thumbnail": entry.get("thumbnail", "")
                }
                videos.append(video_info)

        return sorted(videos, key=lambda x: x["viewCount"], reverse=True)

    def _extract_hashtags(self, text):
        """해시태그 추출"""
        hashtags = re.findall(r'#\w+', text)
        return hashtags if hashtags else ["#유튜브트렌드", "#쇼츠인기"]

    def _calculate_statistics(self, videos):
        """통계 계산"""
        if not videos:
            return {}

        total_views = sum(v["viewCount"] for v in videos)
        total_likes = sum(v["likeCount"] for v in videos)
        total_comments = sum(v["commentCount"] for v in videos)
        
        stats = {
            "totalViews": total_views,
            "averageViews": int(total_views / len(videos)),
            "averageEngagement": round(sum(v["engagementRate"] for v in videos) / len(videos), 2),
            "totalVideos": len(videos),
            "popularHashtags": self._get_popular_hashtags([tag for v in videos for tag in v["hashtags"]]),
            "titleAnalysis": {
                "minLength": min(len(v["title"]) for v in videos),
                "maxLength": max(len(v["title"]) for v in videos),
                "averageLength": int(sum(len(v["title"]) for v in videos) / len(videos))
            }
        }
        
        return stats

    def _get_popular_hashtags(self, hashtags, top_n=5):
        """인기 해시태그 추출"""
        counter = Counter(hashtags)
        return dict(counter.most_common(top_n))

    def _generate_insights(self, videos):
        """인사이트 생성"""
        if not videos:
            return []

        insights = []
        
        # 조회수 기반 인사이트
        avg_views = sum(v["viewCount"] for v in videos) / len(videos)
        high_performing = [v for v in videos if v["viewCount"] > avg_views * 1.5]
        if high_performing:
            insights.append(f"상위 {len(high_performing)}개 영상이 평균 조회수의 150% 이상을 기록했습니다.")

        # 해시태그 분석
        all_hashtags = [tag for v in videos for tag in v["hashtags"]]
        popular_tags = self._get_popular_hashtags(all_hashtags, 3)
        insights.append(f"가장 인기 있는 해시태그: {', '.join(popular_tags.keys())}")

        # 제목 길이 분석
        title_lengths = [len(v["title"]) for v in videos]
        avg_length = sum(title_lengths) / len(title_lengths)
        insights.append(f"평균 제목 길이는 {int(avg_length)}자입니다.")

        # 참여율 분석
        high_engagement = [v for v in videos if v["engagementRate"] > 5]
        if high_engagement:
            insights.append(f"{len(high_engagement)}개 영상이 5% 이상의 높은 참여율을 보였습니다.")

        return insights
