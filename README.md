# wwm-guild-manager

OCR-powered guild roster & weekly tracker for **Where Winds Meet (WWM)**.

---

## English

### Overview
This project is a Python GUI tool that manages guild member profiles, quests, weekly raid/activities, notes, and relationships. Users provide up to 95 in-game screenshots of member profiles. The app crops the relevant panel, runs OCR (Korean/English/numbers), verifies results, and exports/edits data in a CSV-like table UI.

### Core Features
1. **Screenshot intake (1~95 images)** of member profile screens.
2. **Crop to the relevant panel** (remove useless UI areas).
3. **Auto-numbering** for each screenshot.
4. **OCR for Korean/English/numbers** on the cropped panel.
5. **Double OCR verification** (cross-check):
   - If results match → commit to text automatically.
   - If mismatch → pause, show the image + both OCR results in a GUI dialog for user selection or manual correction.
6. **CSV formatting** in the requested schema order.
7. **Excel-like GUI editing** with ability to add custom columns/rows.
8. **Configurable default CSV** on startup (open existing, create new, or open another file).

### Recommended Architecture
- **Multi-module development**, **single-file executable on release** (PyInstaller).
- Modular structure (planned):
  - `app.py` (entry)
  - `config.py`, `models.py`
  - `ui/` (main window, review dialog, crop calibration)
  - `core/` (cropper, preprocess, OCR engine, parser, validator, exporter, project store)

### Libraries (free/open-source)
- GUI: **PySide6**
- OCR: **EasyOCR + Tesseract** (cross-validation)
- Image processing: **OpenCV + Pillow**
- Data: **pandas**, built-in `csv`
- Similarity: **rapidfuzz** (optional)
- Packaging: **PyInstaller**

### Security & Privacy
- OCR runs **locally** (no cloud OCR by default).
- Provide options to store or discard original images.
- Project folder can include: `input/`, `cropped/`, `ocr_raw/`, `output.csv`, `log.txt`.
- For distribution, pin dependencies and track hashes.

### Limitations
- OCR is not 100% accurate, especially with stylized fonts.
- Crop presets/one-time calibration needed for different resolutions.
- Some fields may require regex parsing + range checks.

---

## 한국어

### 개요
이 프로젝트는 **WWM(연운십부)** 길드원의 인적 사항, 주간 활동, 특이사항 등을 관리하는 **파이썬 GUI 도구**입니다. 사용자가 최대 95장의 길드원 프로필 스크린샷을 제공하면, 필요한 영역만 크롭하여 OCR(한글/영문/숫자)을 수행하고 결과를 검증한 뒤 CSV로 정리·편집합니다.

### 핵심 기능
1. **스크린샷 최대 95장 입력**
2. **필요 영역만 크롭**하여 불필요 UI 제거
3. **이미지 순번 자동 부여**
4. **한글/영문/숫자 OCR 수행**
5. **OCR 2회 교차검증**
   - 결과 일치 → 자동 확정
   - 불일치 → 작업 중단, 이미지 + OCR A/B 결과를 GUI에서 선택/수정
6. **CSV 양식으로 자동 정리**
7. **엑셀 유사 GUI 편집** + 사용자 추가 열/행 지원
8. **시작 시 기본 CSV 자동 로드** (기존 열기/새로 만들기/다른 CSV 열기)

### 권장 아키텍처
- **멀티 모듈 개발**, **배포 시 단일 실행파일**(PyInstaller)
- 모듈 구조(예시):
  - `app.py` (진입점)
  - `config.py`, `models.py`
  - `ui/` (메인 윈도우, 확인 다이얼로그, 크롭 캘리브레이션)
  - `core/` (크롭, 전처리, OCR, 파싱, 검증, CSV 저장)

### 무료 라이브러리
- GUI: **PySide6**
- OCR: **EasyOCR + Tesseract**
- 이미지 처리: **OpenCV + Pillow**
- 데이터: **pandas**, 내장 `csv`
- 유사도 비교: **rapidfuzz** (선택)
- 패키징: **PyInstaller**

### 보안/개인정보 고려
- OCR은 **로컬 처리**를 기본으로 설계
- 원본 이미지 저장 여부 옵션 제공
- 프로젝트 폴더 구성 예시: `input/`, `cropped/`, `ocr_raw/`, `output.csv`, `log.txt`
- 배포 시 의존성 버전 고정과 해시 관리 권장

### 한계 및 제약
- OCR 정확도는 100% 불가(폰트/배경 영향)
- 해상도별 크롭 프리셋 또는 1회 캘리브레이션 필요
- 일부 필드는 정규식 파싱 + 범위 검증 필요
