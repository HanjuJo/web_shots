# backend/utils/thumbnail_generator.py
from PIL import Image, ImageDraw, ImageFont
import os


def generate_thumbnail(image_path, title, hashtags, output_path, font_size=50, text_color="white", position="top",
                       border_color="black", border_width=3, bg_color=None):
    """이미지에 제목과 해시태그를 추가하여 썸네일을 생성합니다."""
    try:
        # 이미지 불러오기
        image = Image.open(image_path).convert("RGBA")
        draw = ImageDraw.Draw(image)

        # 폰트 로드
        font_path = "/Library/Fonts/Arial.ttf" if os.name == 'posix' else "arial.ttf"
        font = ImageFont.truetype(font_path, font_size)

        # 배경 색상 추가 (옵션)
        if bg_color:
            overlay = Image.new("RGBA", image.size, bg_color)
            image = Image.alpha_composite(image, overlay)

        # 제목 추가 (위치에 따라)
        text_position = (20, 20) if position == "top" else (20, image.height - font_size - 40)
        draw.text(text_position, title, font=font, fill=text_color, stroke_width=border_width, stroke_fill=border_color)

        # 해시태그 추가 (하단 고정)
        draw.text((20, image.height - font_size - 20), " ".join(hashtags), font=font, fill=text_color)

        # 이미지 저장
        image.save(output_path)
        return {"status": "success", "output_path": output_path}

    except Exception as e:
        return {"status": "error", "message": str(e)}
