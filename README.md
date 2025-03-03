# YouTube 크리에이터 분석 도구

YouTube 크리에이터를 위한 종합 분석 및 최적화 도구입니다. 채널 성과 분석, 쇼츠 분석, 썸네일 최적화 등 다양한 기능을 제공합니다.

## 주요 기능

- 채널 분석
  - 최적의 업로드 시간대 파악
  - 인기 동영상 패턴 분석
  - 시청자 참여도 트래킹

- 쇼츠 분석
  - 쇼츠 성과 측정
  - 참여율 계산
  - 최적의 태그 추천

- 썸네일 분석
  - 썸네일 체크리스트
  - 디자인 가이드라인
  - 성과 높은 썸네일 패턴

- 해시태그 분석
- 경쟁 채널 분석
- 트렌드 키워드
- AI 도구 가이드

## 설치 방법

1. Python 3.10 이상이 필요합니다.

2. 저장소 클론:
```bash
git clone https://github.com/HanjuJo/web_shots.git
cd web_shots
```

3. 가상환경 생성 및 활성화:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

4. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

## 실행 방법

```bash
streamlit run streamlit_app.py
```

## 배포 정보

- Streamlit Cloud: [크리에이터 툴](https://webshortsgrok3-jvkhzwd6dgclluwktmax7q.streamlit.app/)

## 기술 스택

- Python 3.10
- Streamlit 1.42.2
- yt-dlp 2025.2.19
- Plotly 6.0.0
- Pandas 2.2.3
- BeautifulSoup4 4.12.3

## 라이선스

MIT License

## 기여 방법

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request