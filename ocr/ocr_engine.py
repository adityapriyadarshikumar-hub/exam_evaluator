import easyocr

reader = easyocr.Reader(['en'], gpu=False)

def run_ocr(images):
    lines = []
    for img in images:
        results = reader.readtext(img, detail=0)
        lines.extend(results)
    return "\n".join(lines)
