import streamlit as st
import base64
from scripts.youtube_scraper import (
    get_shorts_trends, get_channel_info, calculate_youtube_earnings,
    recommend_competitor_channels, recommend_upload_time
)

# 🌟 CSS 파일 로드
def load_css(file_name):
    with open(file_name, "r") as f:
        return f"<style>{f.read()}</style>"

# 🌟 페이지 설정 및 스타일 로드
st.set_page_config(page_title="유튜브 분석 대시보드", layout="wide")
st.markdown(load_css("styles.css"), unsafe_allow_html=True)

st.title("📊 유튜브 분석 대시보드")


# 🌟 각 기능을 카드 형태로 구성
col1, col2, col3 = st.columns(3)

# 🔥 쇼츠 트렌드 분석 카드
with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>🔥 유튜브 쇼츠 트렌드 분석</div>", unsafe_allow_html=True)
    shorts_keyword = st.text_input("🔍 키워드를 입력하세요 (예: 음식, 여행)")
    if st.button("📈 분석 시작"):
        shorts_trends = get_shorts_trends(shorts_keyword)
        if shorts_trends:
            for video in shorts_trends[:3]:  # 상위 3개만 표시
                st.markdown(f"🎬 [{video['제목']}]({video['영상 URL']}) - {video['조회수']:,}회")
                st.markdown(f"🏷 {' '.join(video['해시태그'])}")
        else:
            st.warning("❌ 영상을 찾을 수 없습니다.")
    st.markdown("</div>", unsafe_allow_html=True)


# 📺 채널 분석 카드
with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>📺 유튜브 채널 분석</div>", unsafe_allow_html=True)
    channel_url = st.text_input("🔍 채널 URL 입력")
    if st.button("📢 분석 시작"):
        channel_info = get_channel_info(channel_url)
        st.markdown(f"📺 **{channel_info['채널명']}**")
        st.markdown(f"👥 구독자: {channel_info['구독자 수']:,}명")
        st.markdown(f"📊 총 조회수: {channel_info['총 조회수']:,}회")
        st.markdown(f"🎥 동영상 수: {channel_info['동영상 수']}개")
    st.markdown("</div>", unsafe_allow_html=True)


# 💰 수익 계산기 카드
with col3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>💰 유튜브 예상 수익 계산기</div>", unsafe_allow_html=True)
    views = st.number_input("📊 예상 조회수 입력", min_value=0)
    if st.button("💵 계산하기"):
        earnings = calculate_youtube_earnings(views)
        st.success(f"📢 예상 수익: ${earnings}")
    st.markdown("</div>", unsafe_allow_html=True)


# 📊 두 번째 행의 카드
col4, col5 = st.columns(2)

# 🏆 경쟁 채널 분석 카드
with col4:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>🏆 유튜브 경쟁 채널 분석</div>", unsafe_allow_html=True)
    competitor_keyword = st.text_input("🔍 키워드 입력 (예: 요리, 운동)")
    if st.button("🔎 경쟁 채널 찾기"):
        competitors = recommend_competitor_channels(competitor_keyword)
        if competitors:
            for ch in competitors:
                st.markdown(f"📺 [{ch['채널명']}]({ch['채널 URL']})")
        else:
            st.warning("❌ 채널을 찾을 수 없습니다.")
    st.markdown("</div>", unsafe_allow_html=True)


# ⏰ 콘텐츠 업로드 일정 추천 카드
with col5:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>⏰ 업로드 일정 추천</div>", unsafe_allow_html=True)
    if st.button("📅 추천 보기"):
        schedule = recommend_upload_time()
        st.success(schedule)
    st.markdown("</div>", unsafe_allow_html=True)


# 📝 하단 설명 및 도움말
st.markdown("---")
st.info("💡 *이 대시보드는 유튜브 크리에이터들이 더 나은 성과를 내기 위해 제작되었습니다.*")
