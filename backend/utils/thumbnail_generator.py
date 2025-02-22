# backend/utils/thumbnail_generator.py
from PIL import Image, ImageDraw, ImageFont
import os


def generate_thumbnail(image_path, title, hashtags, output_path, font_size=50, text_color="white"):
    """이미지에 제목과 해시태그를 추가하여 썸네일을 생성합니다."""
    try:
        # 이미지 불러오기
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)

        # 폰트 로드 (시스템 기본 폰트 사용)
        font_path = "/Library/Fonts/Arial.ttf" if os.name == 'posix' else "arial.ttf"
        font = ImageFont.truetype(font_path, font_size)

        # 제목 추가
        draw.text((20, 20), title, font=font, fill=text_color)

        # 해시태그 추가 (이미지 하단에 위치)
        draw.text((20, image.height - font_size - 20), " ".join(hashtags), font=font, fill=text_color)

        # 이미지 저장
        image.save(output_path)
        return {"status": "success", "output_path": output_path}

    except Exception as e:
        return {"status": "error", "message": str(e)}
