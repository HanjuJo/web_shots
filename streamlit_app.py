import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from utils.youtube_analyzer import YouTubeAnalyzer

# 페이지 설정
st.set_page_config(
    page_title="YouTube 크리에이터 도구",
    page_icon="📊",
    layout="wide"
)

# 초기화
if 'youtube_analyzer' not in st.session_state:
    st.session_state.youtube_analyzer = YouTubeAnalyzer()

# 사이드바
with st.sidebar:
    st.image("https://www.youtube.com/img/desktop/yt_1200.png", width=150)
    st.title("크리에이터 도구")
    
    # 네비게이션
    pages = {
        "📊 채널 분석": "channel_analysis",
        "📱 쇼츠 분석": "shorts_analysis",
        "🎥 동영상 분석": "video_analysis"
    }
    
    selected_page = st.radio("메뉴 선택", list(pages.keys()))

# 채널 분석 페이지
def show_channel_analysis():
    st.title("YouTube 채널 분석")
    
    channel_url = st.text_input(
        "채널 URL을 입력하세요",
        help="예: https://www.youtube.com/@channelname"
    )
    
    if channel_url:
        with st.spinner("채널 정보를 분석중입니다..."):
            channel_info = st.session_state.youtube_analyzer.get_channel_info(channel_url)
            
            if 'error' in channel_info:
                st.error(f"채널 정보를 가져오는데 실패했습니다: {channel_info['error']}")
                return
            
            # 채널 기본 정보 표시
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("구독자 수", f"{channel_info.get('subscriber_count', 0):,}")
            with col2:
                st.metric("총 조회수", f"{channel_info.get('view_count', 0):,}")
            with col3:
                st.metric("동영상 수", str(channel_info.get('video_count', 0)))
            
            # 채널 콘텐츠 분석
            analysis = st.session_state.youtube_analyzer.analyze_channel_content(channel_info)
            
            st.subheader("업로드 시간 분석")
            time_data = pd.DataFrame(
                list(analysis['upload_time_distribution'].items()),
                columns=['Hour', 'Count']
            )
            fig = px.bar(
                time_data,
                x='Hour',
                y='Count',
                title='시간대별 업로드 수',
                labels={'Hour': '시간', 'Count': '업로드 수'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # 인기 동영상
            st.subheader("인기 동영상 Top 5")
            for video in analysis['top_videos']:
                with st.expander(video['title']):
                    st.write(f"조회수: {video.get('view_count', 0):,}")
                    st.write(f"업로드: {datetime.strptime(video.get('upload_date', '20240101'), '%Y%m%d').strftime('%Y-%m-%d')}")
                    if video.get('duration'):
                        st.write(f"길이: {video['duration']}초")

# 쇼츠 분석 페이지
def show_shorts_analysis():
    st.title("YouTube 쇼츠 분석")
    
    channel_url = st.text_input(
        "채널 URL을 입력하세요",
        help="예: https://www.youtube.com/@channelname",
        key="shorts_channel_url"
    )
    
    if channel_url:
        with st.spinner("쇼츠 데이터를 분석중입니다..."):
            channel_info = st.session_state.youtube_analyzer.get_channel_info(channel_url)
            
            if 'error' in channel_info:
                st.error(f"채널 정보를 가져오는데 실패했습니다: {channel_info['error']}")
                return
            
            shorts_analytics = st.session_state.youtube_analyzer.get_shorts_analytics(channel_info)
            
            # 쇼츠 vs 일반 영상 비율
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("쇼츠 비율", f"{shorts_analytics['shorts_percentage']:.1f}%")
                st.metric("쇼츠 평균 조회수", f"{int(shorts_analytics['shorts_avg_views']):,}")
            
            with col2:
                st.metric("전체 쇼츠 수", str(shorts_analytics['shorts_count']))
                st.metric("일반 영상 수", str(shorts_analytics['regular_count']))
            
            # 조회수 비교 차트
            fig = go.Figure(data=[
                go.Bar(
                    name='쇼츠',
                    x=['평균 조회수'],
                    y=[shorts_analytics['shorts_avg_views']],
                    marker_color='#FF0000'
                ),
                go.Bar(
                    name='일반 영상',
                    x=['평균 조회수'],
                    y=[shorts_analytics['regular_avg_views']],
                    marker_color='#065FD4'
                )
            ])
            fig.update_layout(title='쇼츠 vs 일반 영상 평균 조회수 비교')
            st.plotly_chart(fig, use_container_width=True)

# 동영상 분석 페이지
def show_video_analysis():
    st.title("YouTube 동영상 분석")
    
    video_url = st.text_input(
        "동영상 URL을 입력하세요",
        help="예: https://www.youtube.com/watch?v=..."
    )
    
    if video_url:
        with st.spinner("동영상을 분석중입니다..."):
            video_info = st.session_state.youtube_analyzer.get_video_info(video_url)
            
            if 'error' in video_info:
                st.error(f"동영상 정보를 가져오는데 실패했습니다: {video_info['error']}")
                return
            
            performance = st.session_state.youtube_analyzer.analyze_video_performance(video_info)
            
            # 기본 정보 표시
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("조회수", f"{video_info.get('view_count', 0):,}")
            with col2:
                st.metric("좋아요", f"{video_info.get('like_count', 0):,}")
            with col3:
                st.metric("댓글", f"{video_info.get('comment_count', 0):,}")
            
            # 상세 분석
            st.subheader("상세 분석")
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("참여율", f"{performance['engagement_rate']}%")
                st.metric("영상 유형", performance['video_type'])
            
            with col2:
                st.metric("영상 길이", f"{performance['duration']}초")
                st.metric("태그 수", str(performance['tags_count']))
            
            # 태그 표시
            if video_info.get('tags'):
                st.subheader("사용된 태그")
                st.write(", ".join(video_info['tags']))

# 페이지 라우팅
if selected_page == "📊 채널 분석":
    show_channel_analysis()
elif selected_page == "📱 쇼츠 분석":
    show_shorts_analysis()
elif selected_page == "🎥 동영상 분석":
    show_video_analysis()
