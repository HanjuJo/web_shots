import streamlit as st
import yt_dlp
import random

# 🎯 유튜브 쇼츠 트렌드 분석 (제목 스타일, 해시태그 분석)
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


# 🎯 해시태그 추출 함수
def extract_hashtags(title):
    words = title.split()
    hashtags = [word for word in words if word.startswith("#")]
    return hashtags if hashtags else ["#유튜브트렌드", "#쇼츠인기"]


# 🎯 유튜브 채널 분석 (채널명, 구독자 수, 총 조회수)
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


# 🎯 유튜브 예상 수익 분석 (CPM 기반)
def calculate_youtube_earnings(views, cpm=2.0):
    earnings = (views / 1000) * cpm
    return round(earnings, 2)


# 🎯 유튜브 경쟁 채널 분석 (유사 채널 추천)
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


# 🎯 유튜브 콘텐츠 일정 추천 (요일 및 시간대)
def recommend_upload_time():
    best_days = ["금요일", "토요일", "일요일"]
    best_times = ["오전 10시", "오후 2시", "오후 6시"]

    return f"✅ 추천 업로드 요일: {random.choice(best_days)}, 추천 업로드 시간: {random.choice(best_times)}"


# 🎯 Streamlit UI 설정
st.set_page_config(page_title="유튜브 크리에이터 분석 도구", layout="wide")

st.title("📊 유튜브 크리에이터 & 쇼츠 분석 시스템")

# 🔥 유튜브 쇼츠 트렌드 분석
st.subheader("🔥 유튜브 쇼츠 트렌드 분석")
shorts_keyword = st.text_input("🔍 인기 쇼츠 영상을 찾을 키워드를 입력하세요")

if st.button("📈 쇼츠 트렌드 분석 시작"):
    with st.spinner(f"'{shorts_keyword}' 관련 인기 쇼츠 영상 검색 중..."):
        shorts_trends = get_shorts_trends(shorts_keyword)

    if shorts_trends:
        for video in shorts_trends:
            st.markdown(f"""
                <div>
                    <p>🎬 <strong>{video['제목']}</strong></p>
                    <p>🔗 <a href="{video['영상 URL']}" target="_blank">{video['영상 URL']}</a></p>
                    <p>👀 조회수: {video['조회수']:,}회</p>
                    <p>🏷 해시태그: {' '.join(video['해시태그'])}</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("❌ 인기 쇼츠 영상을 찾을 수 없습니다.")


# 🔥 유튜브 채널 분석
st.subheader("📊 유튜브 채널 분석")
channel_url = st.text_input("🔍 분석할 유튜브 채널 URL을 입력하세요")

if st.button("📢 채널 분석 시작"):
    with st.spinner("채널 정보 수집 중..."):
        channel_info = get_channel_info(channel_url)

    if channel_info:
        st.markdown(f"""
            <div>
                <p>📺 <strong>{channel_info['채널명']}</strong></p>
                <p>👥 구독자 수: {channel_info['구독자 수']:,}명</p>
                <p>📊 총 조회수: {channel_info['총 조회수']:,}회</p>
                <p>🎥 업로드 동영상 수: {channel_info['동영상 수']}개</p>
            </div>
        """, unsafe_allow_html=True)


# 🔥 유튜브 예상 수익 계산기
st.subheader("💰 유튜브 예상 수익 계산기")
views = st.number_input("📊 예상 조회수 입력 (예: 1000000)", min_value=0)

if st.button("💵 예상 수익 계산"):
    earnings = calculate_youtube_earnings(views)
    st.success(f"📢 예상 유튜브 수익: ${earnings}")


# 🔥 유튜브 경쟁 채널 분석
st.subheader("📊 유튜브 경쟁 채널 분석")
competitor_keyword = st.text_input("🔍 경쟁 채널을 찾을 키워드를 입력하세요")

if st.button("🏆 경쟁 채널 추천"):
    with st.spinner(f"'{competitor_keyword}' 관련 유사 채널 검색 중..."):
        competitors = recommend_competitor_channels(competitor_keyword)

    if competitors:
        for ch in competitors:
            st.markdown(f"📺 [{ch['채널명']}]({ch['채널 URL']})")
    else:
        st.warning("❌ 경쟁 채널을 찾을 수 없습니다.")


# 🔥 유튜브 콘텐츠 일정 추천
st.subheader("⏰ 유튜브 콘텐츠 업로드 일정 추천")
if st.button("📢 추천 일정 보기"):
    schedule = recommend_upload_time()
    st.success(schedule)
