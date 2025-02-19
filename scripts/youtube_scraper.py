import yt_dlp
import random

def get_shorts_trends(keyword, max_results=10):
    ydl_opts = {"quiet": True, "extract_flat": True, "force_generic_extractor": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        search_results = ydl.extract_info(f"ytsearch{max_results}: {keyword} Shorts", download=False)
    videos = []
    if "entries" in search_results:
        for entry in search_results["entries"]:
            videos.append({
                "제목": entry["title"],
                "영상 URL": entry["url"],
                "조회수": entry.get("view_count", 0),
                "해시태그": extract_hashtags(entry["title"])
            })
    return sorted(videos, key=lambda x: x["조회수"], reverse=True)


def extract_hashtags(title):
    words = title.split()
    hashtags = [word for word in words if word.startswith("#")]
    return hashtags if hashtags else ["#유튜브트렌드", "#쇼츠인기"]


def get_channel_info(channel_url):
    ydl_opts = {"quiet": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)
    return {
        "채널명": info.get("title", "정보 없음"),
        "구독자 수": info.get("channel_follower_count", 0),
        "총 조회수": info.get("view_count", 0),
        "동영상 수": info.get("playlist_count", 0)
    }


def calculate_youtube_earnings(views, cpm=2.0):
    return round((views / 1000) * cpm, 2)


def recommend_competitor_channels(keyword, max_results=5):
    ydl_opts = {"quiet": True, "extract_flat": True, "force_generic_extractor": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        search_results = ydl.extract_info(f"ytsearch{max_results}: {keyword} 채널", download=False)
    channels = []
    if "entries" in search_results:
        for entry in search_results["entries"]:
            channels.append({
                "채널명": entry["title"],
                "채널 URL": entry["url"]
            })
    return channels


def recommend_upload_time():
    best_days = ["금요일", "토요일", "일요일"]
    best_times = ["오전 10시", "오후 2시", "오후 6시"]
    return f"✅ 추천 업로드 요일: {random.choice(best_days)}, 추천 업로드 시간: {random.choice(best_times)}"
