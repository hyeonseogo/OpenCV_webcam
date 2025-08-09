# 🎥 OpenCV 영상 필터 & 스티커

비디오(웹캠 또는 파일)에 다양한 필터를 적용하고,  
마우스 클릭으로 PNG 스티커를 붙일 수 있게 만들었습니다.

---

## ✨ 주요 기능
- **실시간 필터 적용**  
  - Original, Gray, Canny, Blur, Sepia, Negative, Cartoon
- **마우스 클릭으로 스티커 합성**  
  - PNG 스티커의 알파 채널(투명도) 지원
- **비디오/웹캠 입력 모두 지원**
- **키보드 단축키로 필터·스티커 전환**
- **결과 영상 저장(camera.avi / output.avi)**

---

## 📂 프로젝트 구조
```
project/
├── stickers/ # PNG 스티커 이미지
│ ├── heart.png
│ ├── star.png
│ ├── lovely_face.png
│ ├── stupid_face.png
│ └── angry_face.png
├── main_webcam.py # 웹캠 버전
├── main_video.py # 비디오 파일 버전
├── movies/
│ └── keyboard.mp4 # 예시 비디오
├── README.md
└── .gitignore
```

---

## 🎮 조작 방법

### 🖌 필터 선택
| 키         | 필터                |
| ---------- | ------------------- |
| **o**      | Original            |
| **g**      | Gray                |
| **c**      | Canny               |
| **b**      | Blur                |
| **s**      | Sepia               |
| **v**      | Negative (Horror)   |
| **t**      | Cartoon             |
| **n / N**  | 다음 필터           |
| **p / P**  | 이전 필터           |

### 🌟 스티커 선택
| 키     | 스티커       |
| ------ | ------------ |
| **1**  | Heart        |
| **2**  | Star         |
| **3**  | Love         |
| **4**  | Stupid       |
| **5**  | Angry        |
| **X**  | 모든 스티커 제거 |

### ⚙ 기타
| 키         | 기능             |
| ---------- | ---------------- |
| **h / H**  | 도움말 표시/숨김 |
| **ESC**    | 종료             |

---

## 🖱 스티커 사용 방법
1. 스티커 번호(1~5) 선택  
2. 마우스로 원하는 위치 클릭 → 스티커 붙이기  
3. 여러 번 클릭 시 스티커 누적 가능  
4. **X** 키로 모든 스티커 제거  

---

## 📝 주의사항
- `stickers/` 폴더에 PNG 스티커가 반드시 있어야 합니다.
- `.gitignore`에 의해 `camera.avi` / `output.avi`는 저장소에 업로드되지 않습니다.
- `movies/keyboard.mp4`는 예시 영상이므로, 필요 시 다른 영상을 직접 준비하세요.

