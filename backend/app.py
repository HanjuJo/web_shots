# backend/app.py
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from utils.thumbnail_generator import generate_thumbnail
import os
import shutil

app = FastAPI()

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.post("/api/thumbnail")
async def upload_file(file: UploadFile = File(...), title: str = Form(...), hashtags: str = Form(...), position: str = Form(...),
                      text_color: str = Form(...), border_color: str = Form(...), bg_color: str = Form(None)):
    """썸네일을 생성하고 결과를 반환합니다."""
    try:
        # 이미지 저장
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 썸네일 생성
        output_path = os.path.join(OUTPUT_FOLDER, f"thumbnail_{file.filename}")
        result = generate_thumbnail(file_path, title, hashtags.split(","), output_path, position=position,
                                    text_color=text_color, border_color=border_color, bg_color=bg_color)

        # 결과 반환
        if result["status"] == "success":
            return JSONResponse(content={"message": "썸네일 생성 완료", "output_path": output_path})
        else:
            return JSONResponse(content={"message": result["message"]}, status_code=500)

    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)


@app.get("/api/competitor_analysis")
def competitor_analysis(channel_url: str, max_videos: int = Query(10, ge=1, le=20)):
    """경쟁 채널의 최근 쇼츠 및 조회수 증가율 분석"""
    try:
        data = analyze_channel_growth(channel_url, max_videos)
        if isinstance(data, list):
            graph_html = plot_channel_growth(data)
            return JSONResponse(content={"data": data, "graph_html": graph_html})
        else:
            return JSONResponse(content=data, status_code=500)

    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)
