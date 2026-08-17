# -*- coding: utf-8 -*-
"""神無ノ鳥 텍스트 폰트 빌드 스펙 — Noto Sans KR + Noto Sans JP.

`ujyu font` 가 이 스펙을 읽어 빌드한다. 값의 의미는 engine/docs/formats/TEXT_RENDER.md §4.

FONT_WIDTH_MODE(config) 에 따라:
  · "fullwidth"    : 아래 가변폭 조정(SPACE/OPEN/CLOSE/FIXED/CMAP_ALIAS)을 건너뛴다.
  · "proportional" : 아래 조정을 적용하고, inject 단계에서 마침표·쉼표 뒤 공백을 넣는다.

소스는 둘 다 **가변 폰트를 wght=400 으로 고정한 정적본**이다. 가변 그대로 쓰면
글리프를 다시 그릴 때 fvar/gvar 가 어긋나 폰트가 깨진다. 받는 법은 README.md.
"""
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(_HERE, "NotoSansKR-Regular.ttf")   # 한글 소스
FACE   = "KannagiKR-Noto"                                 # exe 가 CreateFontIndirectA 로 찾는 이름

# ── 세로 시프트 (렌더가 GetGlyphOutlineA/GGO_GRAY8 라 디센더가 잘림)
TARGET_BOTTOM_EM = 0.031                              # 한글 최저점을 이 위치로 올림
SAMPLE = [0xAC00, 0xD7A3, 0xADF8, 0xC7A5, 0xB755]     # 최저점 표본(가·힣·그·장·뵵)
# 한글 표본만 보는 값이다. 그보다 깊은 디센더(괄호·쉼표 등)는 빌더의 세로 맞춤이
# 따로 걸러 낸다(FIT_WINDOW_EM 기본 0.01~0.99 em). TEXT_RENDER.md §4-1.

# ── 미번역 일본어 표시용 글리프 병합
# 어느 글자를 어디에 심을지는 `ujyu jpmap` 이 만든 translation/jp_charmap.json 이
# 정한다 — `ujyu font` 가 빌드 때 그 표를 다시 만들어 주므로 따로 돌릴 필요는 없다.
JP_SOURCE = os.path.join(_HERE, "NotoSansJP-Regular.ttf")
# JP_OVERRIDE 를 안 주면 엔진 기본값을 쓴다 — 가나·한자 전체 + `々`·`、`·`。`.
# Noto Sans KR 도 한자를 8천여 자 갖고 있지만 **한국식 자형**이라, 일본어 문장에
# 섞이면 획이 다르게 보인다. 그래서 그 범위는 통째로 일본어 쪽을 쓴다.
# 나머지 글자는 한글 폰트에 없을 때만 일본어에서 가져온다.
# JP_SCALE / JP_DY 를 주면 자동 계산(advance 비율 축소 + 상자 중앙 맞춤)을 덮어쓴다.
#
# 0.92 = 한글 advance 920 / 한자 advance 1000. 한자를 한글과 같은 칸에 맞춘다.
# 게임의 문자열 루프가 글리프 advance 를 그대로 자간으로 쓰므로(TEXT_RENDER.md §3)
# 축소하지 않으면 일본어 줄만 글자마다 80 씩 더 벌어진다.
# 균일 축소라 한자 획 높이가 919 -> 845 로 한글(900)보다 조금 작아지는데,
# 1.0 과 나란히 보고 이쪽을 골랐다.
JP_SCALE = 0.92

# ── 가변폭(proportional) 글리프 조정 — FONT_WIDTH_MODE=="proportional" 일 때만
SPACE = {0x3000: 250}                                # 전각공백 advance (한글 폭의 1/4)
OPEN_RSB = 55                                        # 여는 괄호 오른쪽(안쪽) 여백
OPEN  = {0x300C: 500, 0x300E: 500, 0x0028: 500}      # 「『( 여는: 획 오른정렬 → lsb 로 문두 들여쓰기
CLOSE = {0x300D: 83,  0x300F: 83}                    # 」』 닫는: 트인쪽 여백
FIXED = {0x3010: 1000, 0x3011: 1000}                 # 【】 두꺼운 괄호: 고정 advance
CMAP_ALIAS = {0xFF5E: 0x007E}                        # ～(전각물결) → ~ 글리프
