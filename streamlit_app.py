import streamlit as st
import yt_dlp
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import json
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Backend API URL
BACKEND_URL = os.getenv('BACKEND_URL', 'https://creatortool-backend-123-c965e7aaa680.herokuapp.com')

# 페이지 설정 및 스타일 적용
st.set_page_config(
    page_title="YouTube 크리에이터 도구",
    page_icon="📊",
    layout="wide"
)

# CSS 로드
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# 사이드바 네비게이션
with st.sidebar:
    st.image("https://www.youtube.com/img/desktop/yt_1200.png", width=150)
    st.title("크리에이터 도구")
    
    # 네비게이션 메뉴
    menu_items = {
        "📊 채널 분석": "채널 분석",
        "📱 쇼츠 분석": "쇼츠 분석",
        "🎨 썸네일 분석": "썸네일 분석",
        "🏷️ 해시태그 분석": "해시태그 분석",
        "📈 경쟁 채널 분석": "경쟁 채널 분석",
        "🔍 트렌드 키워드": "트렌드 키워드",
        "🤖 AI 도구 가이드": "AI 도구 가이드"
    }
    
    for icon_label, value in menu_items.items():
        if st.sidebar.button(icon_label, key=f"nav_{value}", use_container_width=True):
            st.session_state.page = value
    
    # 구분선
    st.sidebar.markdown("---")
    
    # 광고 섹션
    st.sidebar.markdown("### 💡 추천 도구")
    
    # 쿠팡 파트너스 광고
    st.sidebar.markdown("""
    <div class="ad-container">
        <h4>🛒 크리에이터 추천 장비</h4>
        <a href="YOUR_COUPANG_PARTNERS_LINK" target="_blank" class="ad-link">
            <div class="ad-content">
                <img src="https://image.coupangcdn.com/image/retail/images/2020/09/01/17/2/95f2b9cc-4c63-4cde-84a3-2ed56d固定画像.jpg" alt="추천 마이크"/>
                <p>프로용 마이크 최대 30% 할인</p>
            </div>
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    # Google AdSense
    st.sidebar.markdown("""
    <div class="ad-container">
        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=YOUR_ADSENSE_CLIENT_ID"
             crossorigin="anonymous"></script>
        <!-- 사이드바 광고 -->
        <ins class="adsbygoogle"
             style="display:block"
             data-ad-client="YOUR_ADSENSE_CLIENT_ID"
             data-ad-slot="YOUR_AD_SLOT_ID"
             data-ad-format="auto"
             data-full-width-responsive="true"></ins>
        <script>
             (adsbygoogle = window.adsbygoogle || []).push({});
        </script>
    </div>
    """, unsafe_allow_html=True)

# 초기 페이지 상태 설정
if 'page' not in st.session_state:
    st.session_state.page = "홈"

def get_channel_info(channel_url):
    response = requests.get(f"{BACKEND_URL}/channel-info", params={"channel_url": channel_url})
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"채널 정보를 가져오는데 실패했습니다: {response.text}")
        return None

def get_video_info(video_url):
    response = requests.get(f"{BACKEND_URL}/video-info", params={"video_url": video_url})
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"비디오 정보를 가져오는데 실패했습니다: {response.text}")
        return None

def show_home():
    st.title("YouTube 크리에이터를 위한 올인원 분석 도구")
    
    # 환영 메시지
    st.markdown("""
    <div class="welcome-card">
        <h2>👋 환영합니다!</h2>
        <p>이 도구는 YouTube 크리에이터들이 채널을 성장시키는 데 필요한 모든 분석 기능을 제공합니다.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 주요 기능 소개
    st.subheader("🎯 주요 기능")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 📊 채널 분석
        - 최적의 업로드 시간대 파악
        - 인기 동영상 패턴 분석
        - 시청자 참여도 트래킹
        """)
    
    with col2:
        st.markdown("""
        ### 📱 쇼츠 분석
        - 쇼츠 성과 측정
        - 참여율 계산
        - 최적의 태그 추천
        """)
    
    with col3:
        st.markdown("""
        ### 🎨 썸네일 최적화
        - 썸네일 체크리스트
        - 디자인 가이드라인
        - 성과 높은 썸네일 패턴
        """)
    
    # 시작하기 가이드
    st.subheader("🚀 시작하기")
    st.markdown("""
    1. 왼쪽 사이드바에서 원하는 기능을 선택하세요
    2. 각 페이지의 안내에 따라 URL이나 키워드를 입력하세요
    3. 자세한 분석 결과와 개선 방안을 확인하세요
    """)

def analyze_channel():
    st.title("YouTube 채널 분석")
    
    with st.container():
        channel_url = st.text_input("채널 URL을 입력하세요", help="예: https://www.youtube.com/@channelname")
        if channel_url:
            with st.spinner("채널 정보를 분석 중입니다..."):
                channel_info = get_channel_info(channel_url)
                
                if channel_info:
                    # 채널 기본 정보
                    st.subheader("채널 정보")
                    metrics_container = st.container()
                    col1, col2, col3 = metrics_container.columns(3)
                    
                    with col1:
                        st.metric("구독자 수", f"{channel_info.get('subscriber_count', 0):,}")
                    with col2:
                        st.metric("총 조회수", f"{channel_info.get('view_count', 0):,}")
                    with col3:
                        st.metric("동영상 수", f"{len(channel_info.get('entries', [])):,}")
                    
                    # 동영상 분석
                    videos = channel_info.get('entries', [])
                    if videos:
                        st.subheader("콘텐츠 분석")
                        
                        # 업로드 시간 분석
                        upload_times = [int(v.get('upload_date', '000000')[8:10]) for v in videos if v.get('upload_date')]
                        if upload_times:
                            time_df = pd.DataFrame(Counter(upload_times).items(), columns=['Hour', 'Count'])
                            fig = px.bar(time_df, x='Hour', y='Count', title='시간대별 업로드 수')
                            st.plotly_chart(fig, use_container_width=True)
                        
                        # 인기 동영상
                        st.subheader("인기 동영상 Top 5")
                        sorted_videos = sorted(videos, key=lambda x: x.get('view_count', 0), reverse=True)[:5]
                        for video in sorted_videos:
                            with st.expander(video['title']):
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.write(f"조회수: {video.get('view_count', 0):,}")
                                    st.write(f"좋아요: {video.get('like_count', 0):,}")
                                with col2:
                                    st.write(f"업로드: {video.get('upload_date', 'N/A')}")
                                    st.write(f"URL: {video.get('url', 'N/A')}")

def analyze_shorts():
    st.title("YouTube Shorts 분석")
    
    with st.container():
        video_url = st.text_input("Shorts URL을 입력하세요", help="예: https://www.youtube.com/shorts/VIDEO_ID")
        if video_url:
            with st.spinner("Shorts 정보를 분석 중입니다..."):
                video_info = get_video_info(video_url)
                
                if video_info:
                    # 기본 메트릭
                    metrics_container = st.container()
                    col1, col2, col3, col4 = metrics_container.columns(4)
                    
                    with col1:
                        st.metric("조회수", f"{video_info.get('view_count', 0):,}")
                    with col2:
                        st.metric("좋아요", f"{video_info.get('like_count', 0):,}")
                    with col3:
                        st.metric("댓글", f"{video_info.get('comment_count', 0):,}")
                    with col4:
                        engagement = ((video_info.get('like_count', 0) + video_info.get('comment_count', 0)) / 
                                   video_info.get('view_count', 1) * 100)
                        st.metric("참여율", f"{engagement:.1f}%")
                    
                    # 상세 정보
                    with st.expander("상세 정보"):
                        st.write(f"제목: {video_info.get('title')}")
                        st.write(f"업로드: {video_info.get('upload_date')}")
                        st.write(f"길이: {video_info.get('duration')}초")
                        
                        if video_info.get('tags'):
                            st.write("태그:")
                            st.write(", ".join(video_info['tags']))

def analyze_thumbnail():
    st.title("썸네일 분석")
    
    with st.container():
        video_url = st.text_input("비디오 URL을 입력하세요")
        if video_url:
            with st.spinner("썸네일을 분석 중입니다..."):
                video_info = get_video_info(video_url)
                
                if video_info and video_info.get('thumbnail'):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.image(video_info['thumbnail'], caption="현재 썸네일")
                    
                    with col2:
                        st.subheader("썸네일 체크리스트")
                        checklist = {
                            "선명한 이미지": "고해상도, 선명한 이미지 사용",
                            "텍스트 가독성": "읽기 쉬운 텍스트 크기와 폰트",
                            "색상 대비": "눈에 띄는 색상 조합",
                            "브랜딩": "채널 브랜딩 요소 포함",
                            "감정 유발": "호기심이나 감정을 자극하는 요소"
                        }
                        
                        for item, desc in checklist.items():
                            st.checkbox(item, help=desc)

def analyze_hashtags():
    st.title("해시태그 분석")
    
    with st.container():
        keyword = st.text_input("분석할 키워드를 입력하세요")
        if keyword:
            with st.spinner("해시태그를 분석 중입니다..."):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("추천 해시태그")
                    tags = [
                        f"#{keyword}",
                        f"#{keyword}tutorial",
                        f"#{keyword}tips",
                        f"#{keyword}howto",
                        f"#{keyword}guide"
                    ]
                    for tag in tags:
                        st.write(tag)
                
                with col2:
                    st.subheader("인기도 분석")
                    tag_data = {
                        'tag': tags,
                        'score': [95, 85, 75, 70, 65]
                    }
                    fig = px.bar(tag_data, x='tag', y='score', title='해시태그 인기도')
                    st.plotly_chart(fig, use_container_width=True)

def analyze_competitors():
    st.title("경쟁 채널 분석")
    
    with st.container():
        channel_url = st.text_input("채널 URL을 입력하세요")
        if channel_url:
            with st.spinner("경쟁 채널을 분석 중입니다..."):
                competitors = [
                    {"name": "경쟁채널1", "subs": 100000, "views": 1000000},
                    {"name": "경쟁채널2", "subs": 200000, "views": 2000000},
                    {"name": "경쟁채널3", "subs": 150000, "views": 1500000}
                ]
                
                # 경쟁사 비교 차트
                df = pd.DataFrame(competitors)
                fig = go.Figure()
                fig.add_trace(go.Bar(name='구독자', x=df['name'], y=df['subs']))
                fig.add_trace(go.Bar(name='조회수', x=df['name'], y=df['views']))
                fig.update_layout(title='경쟁 채널 비교', barmode='group')
                st.plotly_chart(fig, use_container_width=True)

def analyze_trends():
    st.title("트렌드 키워드")
    
    categories = ["게임", "음악", "영화", "뷰티", "테크", "요리", "여행"]
    selected_category = st.selectbox("카테고리 선택", categories)
    
    if selected_category:
        with st.spinner("트렌드를 분석 중입니다..."):
            # 트렌드 데이터 (예시)
            trends = [
                {"keyword": "트렌드1", "volume": 10000, "growth": 150},
                {"keyword": "트렌드2", "volume": 20000, "growth": 200},
                {"keyword": "트렌드3", "volume": 15000, "growth": 180}
            ]
            
            # 트렌드 차트
            df = pd.DataFrame(trends)
            fig = px.scatter(df, x='volume', y='growth', text='keyword',
                           title='키워드 트렌드 맵',
                           labels={'volume': '검색량', 'growth': '성장률 (%)'})
            st.plotly_chart(fig, use_container_width=True)

def show_ai_tools_guide():
    st.title("YouTube 크리에이터를 위한 AI 도구 가이드")
    
    # AI 도구 카테고리별 탭
    tabs = st.tabs(["콘텐츠 기획", "영상 제작", "썸네일 제작", "SEO 최적화"])
    
    with tabs[0]:
        st.subheader("🎬 콘텐츠 기획 도구")
        tools = [
            {
                "name": "ChatGPT",
                "description": "아이디어 발굴, 스크립트 작성",
                "price": "$20/월",
                "time_saved": "~2시간/영상"
            },
            {
                "name": "Midjourney",
                "description": "시각 자료 생성",
                "price": "$10/월",
                "time_saved": "~1시간/디자인"
            }
        ]
        
        for tool in tools:
            with st.expander(tool["name"]):
                st.write(f"용도: {tool['description']}")
                st.write(f"가격: {tool['price']}")
                st.write(f"시간 절약: {tool['time_saved']}")

# 페이지 라우팅
if st.session_state.page == "홈":
    show_home()
elif st.session_state.page == "채널 분석":
    analyze_channel()
elif st.session_state.page == "쇼츠 분석":
    analyze_shorts()
elif st.session_state.page == "썸네일 분석":
    analyze_thumbnail()
elif st.session_state.page == "해시태그 분석":
    analyze_hashtags()
elif st.session_state.page == "경쟁 채널 분석":
    analyze_competitors()
elif st.session_state.page == "트렌드 키워드":
    analyze_trends()
else:
    show_ai_tools_guide()
