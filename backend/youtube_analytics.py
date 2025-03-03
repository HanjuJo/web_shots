import streamlit as st
import yt_dlp
import random
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
from textblob import TextBlob
import re
from collections import Counter

class YoutubeAnalytics:
    def __init__(self):
        self.ydl_opts = {
            "quiet": True,
            "extract_flat": True,
            "force_generic_extractor": True,
            "extract_info": True
        }

    def get_shorts_trends(self, keyword, max_results=10):
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            search_results = ydl.extract_info(f"ytsearch{max_results}: {keyword} Shorts", download=False)

        videos = []
        if "entries" in search_results:
            for entry in search_results["entries"]:
                # 더 자세한 정보 추출
                video_info = {
                    "제목": entry["title"],
                    "영상 URL": entry["url"],
                    "조회수": entry.get("view_count", 0),
                    "업로드 날짜": entry.get("upload_date", ""),
                    "채널명": entry.get("uploader", ""),
                    "채널 URL": entry.get("uploader_url", ""),
                    "해시태그": self.extract_hashtags(entry["title"]),
                    "썸네일": entry.get("thumbnail", ""),
                    "좋아요 수": entry.get("like_count", 0),
                    "댓글 수": entry.get("comment_count", 0)
                }
                
                # 참여율 계산 (engagement rate)
                if video_info["조회수"] > 0:
                    engagement = ((video_info["좋아요 수"] + video_info["댓글 수"]) / video_info["조회수"]) * 100
                    video_info["참여율"] = round(engagement, 2)
                else:
                    video_info["참여율"] = 0
                    
                videos.append(video_info)

        return sorted(videos, key=lambda x: x["조회수"], reverse=True)

    def extract_hashtags(self, text):
        """해시태그 추출 및 분석"""
        hashtags = re.findall(r'#\w+', text)
        if not hashtags:
            return ["#유튜브트렌드", "#쇼츠인기"]
        return hashtags

    def analyze_title_sentiment(self, title):
        """제목의 감정 분석"""
        blob = TextBlob(title)
        sentiment = blob.sentiment.polarity
        if sentiment > 0:
            return "긍정적"
        elif sentiment < 0:
            return "부정적"
        return "중립적"

    def get_video_statistics(self, videos):
        """영상 통계 분석"""
        if not videos:
            return None

        stats = {
            "총 조회수": sum(v["조회수"] for v in videos),
            "평균 조회수": int(sum(v["조회수"] for v in videos) / len(videos)),
            "평균 참여율": round(sum(v["참여율"] for v in videos) / len(videos), 2),
            "인기 해시태그": self.get_popular_hashtags([tag for v in videos for tag in v["해시태그"]]),
            "제목 길이 분석": {
                "최소": min(len(v["제목"]) for v in videos),
                "최대": max(len(v["제목"]) for v in videos),
                "평균": int(sum(len(v["제목"]) for v in videos) / len(videos))
            }
        }
        return stats

    def get_popular_hashtags(self, hashtags, top_n=5):
        """가장 많이 사용된 해시태그 추출"""
        counter = Counter(hashtags)
        return dict(counter.most_common(top_n))

    def generate_trend_insights(self, videos):
        """트렌드 인사이트 생성"""
        if not videos:
            return []

        insights = []
        
        # 조회수 기반 인사이트
        avg_views = sum(v["조회수"] for v in videos) / len(videos)
        high_performing = [v for v in videos if v["조회수"] > avg_views * 1.5]
        if high_performing:
            insights.append(f"🔥 상위 {len(high_performing)}개 영상이 평균 조회수의 150% 이상을 기록했습니다.")

        # 해시태그 분석
        all_hashtags = [tag for v in videos for tag in v["해시태그"]]
        popular_tags = self.get_popular_hashtags(all_hashtags, 3)
        insights.append(f"📌 가장 인기 있는 해시태그: {', '.join(popular_tags.keys())}")

        # 제목 길이 분석
        title_lengths = [len(v["제목"]) for v in videos]
        avg_length = sum(title_lengths) / len(title_lengths)
        insights.append(f"📝 평균 제목 길이는 {int(avg_length)}자입니다.")

        # 참여율 분석
        high_engagement = [v for v in videos if v["참여율"] > 5]  # 5% 이상을 높은 참여율로 간주
        if high_engagement:
            insights.append(f"👥 {len(high_engagement)}개 영상이 5% 이상의 높은 참여율을 보였습니다.")

        return insights

    def create_visualization(self, videos):
        """데이터 시각화"""
        if not videos:
            return None

        # 조회수 vs 참여율 산점도
        df = pd.DataFrame(videos)
        fig = px.scatter(df, 
                        x="조회수", 
                        y="참여율",
                        size="조회수",
                        hover_data=["제목", "채널명"],
                        title="조회수 vs 참여율 분석")
        
        return fig

def main():
    st.set_page_config(page_title="고급 유튜브 크리에이터 분석 도구", layout="wide")
    
    st.title("📊 고급 유튜브 크리에이터 & 쇼츠 분석 시스템")
    st.markdown("""
    ### 🎯 이 도구로 할 수 있는 것:
    - 인기 쇼츠 영상 심층 분석
    - 상세한 통계 및 인사이트 제공
    - 트렌드 시각화
    - 참여율 분석
    - 해시태그 효과성 분석
    """)

    analyzer = YoutubeAnalytics()

    # 쇼츠 트렌드 분석
    st.subheader("🔥 유튜브 쇼츠 트렌드 분석")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        shorts_keyword = st.text_input("🔍 분석할 쇼츠 키워드를 입력하세요")
        max_results = st.slider("분석할 영상 수", 5, 30, 10)

    if st.button("📈 심층 분석 시작"):
        with st.spinner(f"'{shorts_keyword}' 관련 쇼츠 영상 분석 중..."):
            videos = analyzer.get_shorts_trends(shorts_keyword, max_results)

            if videos:
                # 통계 및 인사이트
                stats = analyzer.get_video_statistics(videos)
                insights = analyzer.generate_trend_insights(videos)
                
                # 통계 표시
                st.subheader("📊 통계 분석")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("총 조회수", f"{stats['총 조회수']:,}")
                with col2:
                    st.metric("평균 조회수", f"{stats['평균 조회수']:,}")
                with col3:
                    st.metric("평균 참여율", f"{stats['평균 참여율']}%")

                # 인사이트 표시
                st.subheader("🎯 트렌드 인사이트")
                for insight in insights:
                    st.write(insight)

                # 시각화
                st.subheader("📈 데이터 시각화")
                fig = analyzer.create_visualization(videos)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)

                # 상세 영상 정보
                st.subheader("🎬 분석된 영상 목록")
                for video in videos:
                    with st.expander(f"📺 {video['제목']}"):
                        col1, col2 = st.columns([2, 1])
                        with col1:
                            st.write(f"👁 조회수: {video['조회수']:,}")
                            st.write(f"❤️ 좋아요: {video['좋아요 수']:,}")
                            st.write(f"💬 댓글수: {video['댓글 수']:,}")
                            st.write(f"📊 참여율: {video['참여율']}%")
                        with col2:
                            st.write("🏷 해시태그:")
                            for tag in video['해시태그']:
                                st.write(f"  {tag}")
                            st.write(f"🔗 [영상 보기]({video['영상 URL']})")

            else:
                st.warning("❌ 분석할 영상을 찾을 수 없습니다.")

if __name__ == "__main__":
    main()
