import streamlit as st
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

st.title("📊 **유튜브 분석 대시보드**")
st.markdown("💡 *더 직관적이고 시각적인 UI로 유튜브 성과를 분석해 보세요!*")


# 🌟 ✅ 상단 광고 배너 추가 ✅
st.markdown("""
<div style="text-align: center; margin: 20px 0;">
    <a href="https://link.coupang.com/a/cfwtVx" target="_blank">
        <img src="https://image.coupangcdn.com/image/banner/파트너스배너이미지.jpg" alt="쿠팡 광고" width="100%">
    </a>
</div>
""", unsafe_allow_html=True)


# 🌟 각 기능을 카드 형태로 구성
col1, col2, col3 = st.columns(3)

# 🔥 쇼츠 트렌드 분석 카드 (초록색)
with col1:
    st.markdown("<div class='card card-1'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>🔥 쇼츠 트렌드 분석</div>", unsafe_allow_html=True)
    shorts_keyword = st.text_input("🔍 쇼츠 키워드를 입력하세요", key="shorts_input")
    if st.button("📈 분석 시작", key="shorts_button"):
        shorts_trends = get_shorts_trends(shorts_keyword)
        if shorts_trends:
            for video in shorts_trends[:3]:
                st.markdown(f"🎬 [{video['제목']}]({video['영상 URL']}) - {video['조회수']:,}회")
                st.markdown(f"🏷 {' '.join(video['해시태그'])}")
        else:
            st.warning("❌ 영상을 찾을 수 없습니다.")
    st.markdown("</div>", unsafe_allow_html=True)


# 📺 채널 분석 카드 (파란색)
with col2:
    st.markdown("<div class='card card-2'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>📺 채널 분석</div>", unsafe_allow_html=True)
    channel_url = st.text_input("🔍 채널 URL을 입력하세요", key="channel_input")
    if st.button("📢 분석 시작", key="channel_button"):
        channel_info = get_channel_info(channel_url)
        st.markdown(f"📺 **{channel_info['채널명']}**")
        st.markdown(f"👥 구독자: {channel_info['구독자 수']:,}명")
        st.markdown(f"📊 총 조회수: {channel_info['총 조회수']:,}회")
        st.markdown(f"🎥 동영상 수: {channel_info['동영상 수']}개")
    st.markdown("</div>", unsafe_allow_html=True)


# 💰 수익 계산기 카드 (주황색)
with col3:
    st.markdown("<div class='card card-3'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>💰 수익 계산기</div>", unsafe_allow_html=True)
    views = st.number_input("📊 예상 조회수를 입력하세요", min_value=0, key="earnings_input")
    if st.button("💵 계산하기", key="earnings_button"):
        earnings = calculate_youtube_earnings(views)
        st.success(f"📢 예상 수익: **${earnings}**")
    st.markdown("</div>", unsafe_allow_html=True)


# 🌟 두 번째 행의 카드
col4, col5 = st.columns(2)

# 🏆 경쟁 채널 분석 카드 (보라색)
with col4:
    st.markdown("<div class='card card-4'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>🏆 경쟁 채널 분석</div>", unsafe_allow_html=True)
    competitor_keyword = st.text_input("🔍 키워드를 입력하세요", key="competitor_input")
    if st.button("🔎 채널 찾기", key="competitor_button"):
        competitors = recommend_competitor_channels(competitor_keyword)
        if competitors:
            for ch in competitors:
                st.markdown(f"📺 [{ch['채널명']}]({ch['채널 URL']})")
        else:
            st.warning("❌ 경쟁 채널을 찾을 수 없습니다.")
    st.markdown("</div>", unsafe_allow_html=True)


# ⏰ 업로드 일정 추천 카드 (핑크색)
with col5:
    st.markdown("<div class='card card-5'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>⏰ 업로드 일정 추천</div>", unsafe_allow_html=True)
    if st.button("📅 추천 보기", key="schedule_button"):
        schedule = recommend_upload_time()
        st.success(schedule)
    st.markdown("</div>", unsafe_allow_html=True)


# 🌟 ✅ 하단 광고 배너 추가 ✅
st.markdown("""
<div style="text-align: center; margin: 40px 0;">
    <a href="https://link.coupang.com/a/파트너스링크" target="_blank">
        <img src="https://image.coupangcdn.com/image/banner/파트너스배너이미지.jpg" alt="쿠팡 광고" width="100%">
    </a>
</div>
""", unsafe_allow_html=True)


# 📝 하단 설명 및 도움말
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
st.info("💡 *이 대시보드는 유튜브 크리에이터의 성과 향상을 위해 제작되었습니다.*")
