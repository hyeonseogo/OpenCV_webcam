import cv2
import numpy as np

def f_original(img):
    return img

def f_gray(img):
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.cvtColor(g, cv2.COLOR_GRAY2BGR)

def f_canny(img):
    med_val = np.median(img)
    lower = int(max(0, 0.7 * med_val))
    upper = int(min(255, 1.3 * med_val))
    dst1 = cv2.GaussianBlur(img, (3, 3), 0)
    edges = cv2.Canny(dst1, lower, upper, 3)
    return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

def f_blur(img):
    return cv2.GaussianBlur(img, (15, 15), 0)

def f_sepia(img):
    # BGR 기준 sepia 변환 (갈색톤 빈티지 느낌)
    kernel = np.array([[0.272, 0.534, 0.131],
                       [0.349, 0.686, 0.168],
                       [0.393, 0.769, 0.189]])
    out = cv2.transform(img, kernel)
    return np.clip(out, 0, 255).astype(np.uint8)

def f_negative(img):
    return 255 - img

def f_cartoon(img):
    c = cv2.bilateralFilter(img, 9, 75, 75)
    g = cv2.cvtColor(c, cv2.COLOR_BGR2GRAY)
    edges = cv2.adaptiveThreshold(
        g, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY, 9, 2
    )
    edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    return cv2.bitwise_and(c, edges_bgr)

filters = [
    ("Original (o)", f_original),
    ("Gray (g)", f_gray),
    ("Canny (c)", f_canny),
    ("Blur (b)", f_blur),
    ("Sepia (s)", f_sepia),
    ("Horror (v)", f_negative),
    ("Cartoon (t)", f_cartoon),
]

filter_keys = {
    ord('o'): 0,  # Original
    ord('g'): 1,  # Gray
    ord('c'): 2,  # Canny
    ord('b'): 3,  # Blur
    ord('s'): 4,  # Sepia
    ord('v'): 5,  # Horror
    ord('t'): 6,  # Cartoon
}

# 스티커 PNG 로드 함수
def load_sticker(path, size):
    img_rgba = cv2.imread(path, cv2.IMREAD_UNCHANGED)  # RGBA
    if img_rgba is None:
        raise FileNotFoundError(f"Sticker not found: {path}")
    img_rgba = cv2.resize(img_rgba, (size, size), interpolation=cv2.INTER_AREA)
    return img_rgba

# 합성 함수
def overlay_png(dst, sticker_rgba, center_xy):
    x, y = center_xy
    h, w = sticker_rgba.shape[:2]
    x0, y0 = int(x - w//2), int(y - h//2)

    H, W = dst.shape[:2]
    if x0 >= W or y0 >= H or x0 + w <= 0 or y0 + h <= 0:
        return

    # 좌표 클리핑
    x1_src = max(0, -x0); y1_src = max(0, -y0)
    x2_src = min(w, W - x0); y2_src = min(h, H - y0)
    x1_dst = max(0, x0); y1_dst = max(0, y0)
    x2_dst = x1_dst + (x2_src - x1_src); y2_dst = y1_dst + (y2_src - y1_src)

    roi = dst[y1_dst:y2_dst, x1_dst:x2_dst]
    sticker_crop = sticker_rgba[y1_src:y2_src, x1_src:x2_src]

    if sticker_crop.shape[2] == 4:  # 알파 채널 존재
        alpha = sticker_crop[:, :, 3] / 255.0
        for c in range(3):
            roi[:, :, c] = roi[:, :, c] * (1 - alpha) + sticker_crop[:, :, c] * alpha
        dst[y1_dst:y2_dst, x1_dst:x2_dst] = roi


# 상태 / UI 텍스트
help_text = [
    "Keys:",
    "  o/g/c/b/s/v/t : Select filter",
    "     o: Original, g: Gray, c: Canny",
    "     b: Blur, s: Sepia, v: Horror, t: Cartoon",
    "  N / P : Next / Prev filter",
    "  H     : Toggle help",
    "  ESC   : Quit",
]

sticker_names = {
    1: "Heart",
    2: "Star",
    3: "Love",
    4: "Stupid",
    5: "Angry"
}

cur_idx = 0
show_help = True
current_sticker_id = 1
placed_stickers = []  # (sticker_id, (x,y))

def on_mouse(event, x, y, flags, param):
    global placed_stickers
    if event == cv2.EVENT_LBUTTONDOWN:
        placed_stickers.append((current_sticker_id, (x, y)))


cap = cv2.VideoCapture(0)
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

fourcc = cv2.VideoWriter.fourcc(*'DIVX')
out = cv2.VideoWriter('camera.avi', fourcc, fps, (w, h))

sticker_size = max(48, min(w, h)//8)
sticker_bank = {
    1: load_sticker("stickers/heart.png", sticker_size),
    2: load_sticker("stickers/star.png", sticker_size),
    3: load_sticker("stickers/lovely_face.png", sticker_size),
    4: load_sticker("stickers/stupid_face.png", sticker_size),
    5: load_sticker("stickers/angry_face.png", sticker_size)
}

cv2.namedWindow('frame')
cv2.setMouseCallback('frame', on_mouse)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    title, f = filters[cur_idx]
    filtered = f(frame)

    cv2.putText(filtered, f"Filter: {title}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    cv2.putText(filtered, f"Sticker: {sticker_names[current_sticker_id]} (1/2/3/4/5)",
                (10, 56), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    if show_help:
        y0 = 86
        for line in help_text:
            cv2.putText(filtered, line, (10, y0),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            y0 += 24

    for sid, (px, py) in placed_stickers:
        overlay_png(filtered, sticker_bank[sid], (px, py))

    cv2.imshow('frame', filtered)
    out.write(filtered)

    key = cv2.waitKey(10) & 0xFF
    if key == 27:  # ESC
        break
    elif key in filter_keys:
        cur_idx = filter_keys[key]
    elif key in (ord('n'), ord('N')):
        cur_idx = (cur_idx + 1) % len(filters)
    elif key in (ord('p'), ord('P')):
        cur_idx = (cur_idx - 1) % len(filters)
    elif key in (ord('h'), ord('H')):
        show_help = not show_help
    elif key in (ord('1'), ord('2'), ord('3'), ord('4'), ord('5')):
        current_sticker_id = int(chr(key))
    elif key in (ord('x'), ord('X')):
        placed_stickers.clear()

cap.release()
out.release()
cv2.destroyAllWindows()
