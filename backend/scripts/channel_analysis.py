# backend/scripts/channel_analysis.py
import yt_dlp
import pandas as pd


def analyze_channel_growth(channel_url, max_videos=10):
    """경쟁 채널의 최근 쇼츠와 조회수 증가율 분석"""
    try:
        ydl_opts = {"quiet": True, "extract_flat": True, "force_generic_extractor": True}

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            channel_info = ydl.extract_info(channel_url, download=False)

        video_data = []
        if "entries" in channel_info:
            for entry in channel_info["entries"][:max_videos]:
                video_data.append({
                    "title": entry["title"],
                    "url": entry["url"],
                    "view_count": entry.get("view_count", 0),
                    "upload_date": entry.get("upload_date", "N/A")
                })

        df = pd.DataFrame(video_data)
        df["view_growth"] = df["view_count"].pct_change().fillna(0) * 100  # 조회수 증가율(%)
        return df.to_dict(orient="records")

    except Exception as e:
        return {"status": "error", "message": str(e)}
