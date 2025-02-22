# backend/utils/data_visualizer.py
import plotly.express as px


def plot_channel_growth(data):
    """Plotly를 사용하여 채널의 조회수 증가율 시각화"""
    fig = px.line(
        data,
        x="upload_date",
        y="view_growth",
        text="title",
        title="채널의 최근 쇼츠 조회수 증가율",
        markers=True
    )
    fig.update_traces(textposition="top center")
    fig.update_layout(xaxis_title="업로드 날짜", yaxis_title="조회수 증가율 (%)")
    return fig.to_html(full_html=False)
