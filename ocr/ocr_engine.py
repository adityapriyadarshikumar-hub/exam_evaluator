import easyocr
import numpy as np
import torch

gpu = torch.cuda.is_available()
reader = easyocr.Reader(['en'], gpu=gpu)

def run_ocr(images):
    lines = []
    for img in images:
        img_np = np.array(img)
        results = reader.readtext(img_np, detail=0)
        lines.extend(results)
    return "\n".join(lines)
