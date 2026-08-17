#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
神無ノ鳥 (칸나기의 새) 설정 — **실제로 동작한 값이 그대로 들어 있는 참고본**.

이걸 `config.py` 로 복사해 새 타이틀 값으로 고쳐 쓴다(`config.py` 는 .gitignore).
값을 지우지 말 것 — "무엇을 넣어야 하는가"보다 **"어떤 값이 실제로 통했는가"** 가
훨씬 알기 어렵다. 아래는 그 값들이 어떤 근거로 정해졌는지다.

■ 항목은 세 종류다 (engine/GUIDE.md §1)

  1. **문답으로 정할 것** — 값이 갈리고 취향·판단이 들어가는 것.
     `SCALE` · `FONT_WIDTH_MODE` · `FONT_FACE` · `MOVIE_NATIVE` · `COMMON_CSV.title`
     기본값으로 임의 진행하지 말고 물어본다. 정하면 CLAUDE.md 의 "결정 사항" 표에 적는다.

  2. **직접 찾을 것** — exe 오프셋·심볼 인덱스처럼 답이 하나뿐인 것.
     `OFF_*` · `SJIS_IDIOM` · `INLINE_RECODE` · `CAVE_VA` · `IAT_*`
     물어보지 말고 디스어셈블·바이트 대조로 확정한다. 확정한 근거를 주석에 남긴다
     (이 파일의 `2026-07-26 exe diff`, `동작 중인 배포 exe 와 원본을 대조해 확정` 처럼).

  3. **자동으로 도출되는 것** — `SCN_DIMS_AUTO` 처럼 빌드 때 계산한다.

■ 해상도 ×N 에서 삽질한 것들 — 같은 길을 다시 걷지 않도록

  · **좌표는 한 곳에 있지 않다.** 세 경로를 다 처리해야 화면이 맞는다:
      `SCN_DIMS`      씬 파일에 박힌 치수. 오프셋 동결이라 **번역으로 길이가 바뀌면 깨진다.**
                      가능하면 쓰지 말고 `SCN_DIMS_AUTO` 로 넘길 것. 이 파일에 남은 것은
                      심볼 참조가 아니라 생짜 번호로 부르는 객체(`system.scn`)뿐이다.
      `SCN_DIMS_AUTO` VNEG int 심볼에서 자동 도출. **이쪽이 기본**이다.
      `COMMON_CENTER` 확대 대상이 아니라 1× 로 남는 창을 화면 가운데로 옮긴다.

  · **심볼이 공유된다.** 한 값이 두 군데서 쓰이면 ×N 이 엉뚱한 곳까지 키운다.
    `system.scn #42=18` 이 로그 화살표 폭이면서 **이름표 글꼴 크기**여서, 통째로 ×2 하니
    이름 글자가 같이 커졌다 → `SCN_REPOINT` 로 참조 일부만 새 심볼로 갈랐다.

  · **×N 이 항상 정답은 아니다.** `music.scn` 곡 제목 글꼴은 ×2 하면 행에 비해 커서
    `SCN_VALUE_REMAP` 으로 한 단계 낮췄다(44→38, 40→36).

  · **이미지와 좌표는 짝이다.** `.scn` 좌표를 ×N 했으면 그 화면 배경도 ×N 해야 한다
    (`CG_CONTENT_PREFIX`). 안 하면 배경이 좌상단 1/4 에만 그려진다. 반대로 1× 로 두는
    대화창 위에 얹히는 것은 같이 1× 로 둔다(`CG_UI_1X_PREFIX`).

  · **common.csv 는 아카이브마다 자기 것을 제자리 편집한다.** 다른 아카이브 것을 통째로
    넣으면 그 아카이브 고유 변수 정의가 사라져 선택지에서 크래시한다.

  · 씬을 재패킹하면 **VNEG 점프테이블 재매핑**이 필수다. 안 하면 무비·선택지에서 hang.

  · `SCALE_COMMON_INTS`(전역 글꼴 크기 ×N)는 이 타이틀에선 **효과가 없었다.** 화면마다
    자기 `m07` 로 글꼴을 정하기 때문. 비워 두고, 기본값으로 그리는 창이 나오면 그때 켠다.

■ 그 밖

  · `ORIG_DIR`(무패치 원본)은 **절대 수정 금지**. 모든 대조의 기준이다.
  · 경로는 전부 `REPO_DIR`/`DEV_DIR` 기준 상대 경로로 쓴다. 절대경로를 박지 말 것.
  · 실행에 Windows 8 호환 모드가 필요했다(`RELEASE_NOTES`). 3× 검증 때 확인.
"""
import os

# ─────────────────────────────────────────── 경로
# 모든 작업물은 f:\dev-kannagi (이 리포의 부모) 아래에 둔다. 절대경로 금지 —
# 원본·배포·이미지 애셋·엔진 서브모듈이 전부 그 아래에 있다.
REPO_DIR = os.path.dirname(os.path.abspath(__file__))   # …\kannagi-no-tori (이 리포)
DEV_DIR  = os.path.dirname(REPO_DIR)                     # …\dev-kannagi (작업 루트)

def repo(*p):  return os.path.join(REPO_DIR, *p)
def dev(*p):   return os.path.join(DEV_DIR, *p)

GAME_DIR = os.environ.get("MIRIS_GAME_DIR", dev("kannagi-2xkr"))  # 배포(패치 결과)
ORIG_DIR = os.environ.get("MIRIS_ORIG_DIR", dev("kannagi-org"))   # 무패치 JP 원본 (읽기 전용)
WORK_DIR = os.environ.get("MIRIS_WORK_DIR", dev("_work"))         # 임시 작업물 (재생성 가능)

def game(*p):  return os.path.join(GAME_DIR, *p)
def orig(*p):  return os.path.join(ORIG_DIR, *p)
def work(*p):  return os.path.join(WORK_DIR, *p)

# ─────────────────────────────────────────── 이미지 번역 애셋
# translation/IMAGES.md 에는 물리적 경로를 적지 않고 여기에서만 관리한다.
IMAGE_ASSET_DIR = os.environ.get("KANNAGI_IMAGE_ASSETS", dev("kannagi-image-assets"))
IMAGE_FONT_DIR  = os.environ.get("KANNAGI_IMAGE_FONTS", os.path.join(IMAGE_ASSET_DIR, "fonts"))
IMAGE_RENDERER  = repo("engine", "ujyu", "inject_image_text.py")   # 또는 `ujyu image` CLI
IMAGE_SPEC      = repo("translation", "IMAGES.md")
IMAGE_VARIANT   = os.environ.get("KANNAGI_IMAGE_VARIANT", "Minguk")
IMAGE_ORIGINAL_DIR  = os.path.join(IMAGE_ASSET_DIR, "original")   # 원문(글자 有), 측정 기준
IMAGE_TEXTLESS_DIR  = os.path.join(IMAGE_ASSET_DIR, "textless")   # 글자 지운 베이스
IMAGE_TEXTED_PREFIX = os.path.join(IMAGE_ASSET_DIR, "texted-")    # 렌더 출력 접두(+폰트변형)

# cg 아카이브 이미지 주입 (studio-miris-engine/tools/build_patch.py step_cg)
CG_ARCHIVE   = "cg.axr"
CG_TRANS_DIR = os.environ.get(          # 주입할 번역 PNG 폴더 = inject_image_text.py 출력
    "KANNAGI_CG_TRANS", IMAGE_TEXTED_PREFIX + IMAGE_VARIANT)

# ─────────────────────────────────────────── 아카이브
ARCHIVES      = ["scenario.axr", "scenario.ax2", "scenario.ax3", "scenario.ax4"]
BASE_ARCHIVE  = "scenario.axr.orig"
OUT_ARCHIVE   = "scenario.axr.kr"

# ─────────────────────────────────────────── 텍스트/번역
# v2 포맷 (engine/tools/scn.py extract): [{arc,file,id,kind,off,bytelen,jp[,speaker],kr}]
STRINGS       = repo("translation", "strings.json")
UI_STRINGS    = repo("translation", "ui_strings.json")
NAMEPLATES    = repo("translation", "nameplates.json")
NAMEPLATES_MD = repo("translation", "NAMEPLATES.md")

# ── 검수 (ujyu filter review / apply)
# REVIEW_TSV : 검수용 TSV 를 뽑을지. 경로를 주면 `ujyu filter review` 가 거기에 쓴다.
#              None 이면 뽑지 않는다 — 번역문이 통째로 들어가는 파일이라 공개 리포에
#              올릴 수 없으면 꺼 둔다.
# REVIEW_MARK: 판단이 갈린 번역 앞에 붙이는 표시. 번역자(사람이든 에이전트든)가
#              "이건 검토해 달라" 는 뜻으로 단다. 게임 화면에도 그대로 보이므로
#              검토가 끝나면 지운다.
#              **None/"" 이면 표시를 쓰지 않는다** — `filter apply` 가 들어온 번역에서
#              그 문자를 떼고 넣는다. 값이 있으면 그대로 살려 둔다.
#              CP949 로 인코딩 가능하고 원문에 안 쓰이는 글자를 골라야 한다.
REVIEW_TSV    = repo("translation", "strings_review.tsv")
REVIEW_MARK   = "♠"

RESOURCE_RE   = r'^(f_|k6\d|bg\d|se_|m_a|event\d|movie/|.*_se$|se$)'
# 텍스트처럼 디코드되지만 실제론 커맨드 오퍼랜드인 바이트열.
# 공통 패턴: **끝 바이트가 0x76('v')** 이고 앞이 u16 오퍼랜드다.
#   钁 = E8 76 (331회) / 権v = 8C A0 76 / 廖v = 9C 40 76 / 鸛v = EA 60 76 / e迅 = 65 90 76
# 번역해 넣으면 바이트열이 깨진다. 전부 기번역 0건이고 대사 문맥이 없다.
# 같은 모양(bytelen 3, 끝이 v)이 또 나오면 여기 추가한다 — 길이 제한 없이
# "끝이 0x76" 만으로 거르면 `　말캉、*v` 같은 정상 대사까지 잡힌다.
MARKERS       = {"钁", "権v", "廖v", "鸛v", "e迅"}
CMD_SEQS      = [chr(92) + "n", "4"]      # 줄바꿈 커맨드 · 반각 4(0x34)
# `4` 는 엔진 리더의 0x30-0x4F 구간(2바이트 커맨드)이다. f0601_01.scn 의 두 조각
# (`4ちゃ……ん……！」%` / `4お父さんと*v`) 앞에만 나오고, 원문 전체에 반각 숫자는
# 이것뿐이라 통째로 커맨드로 잡아도 안전하다. 표시 문자로 오판해 빼면 그 자리에서
# 게임이 죽는다(실제로 겪음).
QUOTE_LEAD_SPACE = False                  # 문두 들여쓰기는 공백 아니라 여는 괄호 글리프 lsb로(build_font). 엔진이 quote 오프너 앞 공백을 무시함(특히 전각（)

# ── 글꼴 렌더링 폭 (작업 시작 시 사용자에게 확인 — CLAUDE.md §9). 전체 글자에 적용:
#   "fullwidth"    : 모든 글자 전각 고정폭. 문장부호도 전각 그대로(고정폭이라 간격 자연).
#   "proportional" : 가변폭 — 괄호·낫표·기호를 폰트 스펙(fonts/)대로 조정하고,
#                    마침표(。)·쉼표(、) 뒤에 공백을 추가한다(가변폭 간격 보정).
FONT_WIDTH_MODE = "proportional"

# ─────────────────────────────────────────── common.csv
COMMON_CSV = {
    "title": "칸나기의 새 ",
}

# ─────────────────────────────────────────── 해상도 (engine/docs/formats/RESOLUTION.md)
# 도구 = ujyu scale. 빌드 = ujyu build (SCALE>1 이면 스케일 단계가 자동 포함).
# 3×(1920×1440)도 검증됐으나 화면이 과하게 커서 **2×(1280×960)를 기본**으로 한다.
SCALE = 2               # 정수 배율
ORIG_W, ORIG_H = 640, 480

# SCALE>1 일 때 콘텐츠 이미지의 **외부 AI 업스케일 결과**(Topaz 등) 폴더. 같은 파일명·
# 원본×SCALE 치수를 build cg 가 여기서 가져온다(art·translated 포함, 하위폴더 재귀).
# 없으면 bilinear 리샘플로 폴백. 기본 = dev/kannagi-upscale/<N>x (예: 2x).
CG_UPSCALE_DIR = os.environ.get("KANNAGI_CG_UPSCALE", dev("kannagi-upscale", "%dx" % SCALE))

# 스케일 **비대상**이라 1× 크기로 남는 창 → 확대 화면 가운데로 옮긴다.
# 선택지(분기) 창은 common.csv 의 `textwindow,select`(600×200)와 `int,select_*` 로
# 그려지는데, 이 값들은 버튼·글꼴 계산에 그대로 쓰여 ×N 하면 어긋난다. 그래서 크기는
# 두고 위치만 잡는다. 값 = 세로 정렬 기준 높이(런타임 select_height 대표값, 화면 px).
COMMON_CENTER = {"select": 320}

SCALE_DIALOG_1X  = ["textwin", "namewin", "face"]   # 크기 1× + 우하단 시프트 (§15-6)
SCALE_FS_WINDOWS = ["logwin"]                        # 풀스크린 로그: w/h·패딩 ×N
# 전역 글꼴 크기(text_size 22 / text_line_height 25)를 ×N 하는 스위치. 이 타이틀은
# 비워 둔다 — 대사창·설정·저장·감상 화면 모두 자기 m07 로 글꼴을 정해서 눈에 보이는
# 변화가 없었다. 어딘가 기본값으로 그리는 창이 발견되면 그때 켠다.
SCALE_COMMON_INTS = []
# .scn 명시 치수 (2026-07-26 pre3x↔3xwork diff 로 도출·동결. 오프셋=씬 파일 내, BE)
SCN_DIMS = {
    "mlogo.scn": [(0xd, 4, 320), (0x12, 4, 240), (0x17, 4, 280), (0x1c, 4, 240),
                  (0x34, 4, 320), (0x39, 4, 240), (0x3e, 4, 280), (0x43, 4, 240),
                  (0x5b, 4, 320), (0x60, 4, 240), (0x65, 4, 280), (0x6a, 4, 240),
                  (0x82, 4, 320), (0x87, 4, 240), (0x8c, 4, 280), (0x91, 4, 240)],
    "title.scn": [(0x17, 4, 640), (0x1c, 4, 480), (0x2a, 4, 71), (0x33, 4, 202),
                  (0x3c, 4, 153), (0x45, 4, 36), (0x88, 4, 238), (0xc9, 4, 274),
                  (0x106, 4, 310), (0x149, 4, 346), (0x18c, 4, 382), (0x1d1, 4, 418)],
    # 로그(회상) 화면의 스크롤 화살표·돌아가기. system.scn 은 객체를 생짜 번호로
    # 부르고(`obj16.m1c(x,y,w,h,n,off,on,id)`) 심볼 참조가 아니라 자동 도출이 못 잡는다.
    # 같은 메서드를 대화창 아이콘(obj13/obj17)도 쓰므로 **로그 전용 심볼만** 고른다
    # — #42/#59 는 obj16 호출에서만 쓰인다(전수 확인). 번역 대상 문자열이 0건이라
    # 오프셋이 고정이다.
    "system.scn": [(814, 4, 620),   # #57  화살표 x
                   (823, 4, 280),   # #58  ▲▲ y
                   (832, 4, 38),    # #59  화살표 h
                   (887, 4, 320),   # #62  ▲  y
                   (951, 4, 360),   # #66  ▼  y
                   (1010, 4, 400),  # #69  ▼▼ y
                   (1078, 4, 580),  # #73  돌아가기 x
                   (1087, 4, 460),  # #74  돌아가기 y
                   (1096, 4, 58)],  # #75  돌아가기 w
}

# 공유 심볼을 참조 단위로 갈라 ×N 한다. {scn: [((참조오프셋...), 원본값)]}
# system.scn #42=18 은 로그 화살표 폭(=돌아가기 높이)이면서 **이름창 글꼴 크기**이기도
# 하다(`obj14.m07(#42)` @0x060e). 통째로 ×2 하면 이름 글자가 같이 커지므로 obj16(로그)
# 호출의 참조 5개만 새 심볼로 돌린다. 이름창은 1× 대화창 위에 있으니 18 그대로 둔다.
SCN_REPOINT = {
    "system.scn": [((0x0699, 0x06ae, 0x06c3, 0x06d8, 0x06ef), 18)],
}

# 좌표가 전부 VNEG int 심볼인 화면 — 빌드 시점에 자동 도출해 ×N 한다
# (tools/scn_dims.py 규칙. 오프셋 동결이 아니라 번역으로 길이가 바뀌어도 안전)
# config.scn 의 다원소 심볼 슬롯과 button.m02 좌표도 엔진 파서에서 확정됐다.
SCN_DIMS_AUTO = ("save.scn", "load.scn", "config.scn",
                 # 메인 화면에서 들어가는 감상 화면들 + 확인 대화상자.
                 # cg.scn 은 예전에 SCN_DIMS 로 4개만 동결했는데 auto 가 32개를
                 # 전부 도출하므로 이쪽으로 옮겼다(둘 다 두면 ×4 가 된다).
                 "cg.scn", "music.scn", "scene.scn",
                 "endchk.scn", "titlechk.scn",
                 # 캐스트·스태프롤. 가림막 layer(640×60)와 스크롤 창(20,60,600,360)이
                 # 1× 로 남아 화면 좌상단 1/4 에만 나왔다. 스크롤 시작(-360)·끝(4120)도
                 # 좌표라 같이 ×N 한다 — 시간 인자(100000ms)는 그대로 둬야 배속이 같다.
                 "staffroll.scn", "ending2.scn")

# ×N 하기 전에 갈아끼울 씬 심볼 값. {scn: [((시작심볼, 끝심볼), {옛값: 새값})]}
# music.scn #130~#161 = 곡별 제목 글꼴 크기(제목이 길수록 작다). ×2 하면 44 가 행에
# 비해 커서 한 단계씩 낮춘다 — 화면 크기로 44->38, 40->36 (36·28 그룹은 그대로).
SCN_VALUE_REMAP = {
    "music.scn": [((130, 162), {22: 19, 20: 18})],
}
# 저장·불러오기(sa_lo_*)는 .scn 치수를 ×N 하므로 이미지도 ×N 한다.
CG_CONTENT_PREFIX = ("bg", "s_", "event", "cg_", "be_", "ex_", "edef_", "map",
                     "ru_", "ika_", "ha_", "aki_", "hu_", "ren_", "miris_", "title_",
                     "l_", "end_", "testroll", "roll", "sa_", "config_",
                     # 메인화면에서 들어가는 감상 화면 — 배경이 640x480 전체 화면이라
                     # 1x 로 두면 좌상단 1/4 에만 그려진다 (.scn 좌표는 ×N 되므로 어긋난다)
                     "cgtop_", "sc_", "mu_",
                     # 로그 화면 스크롤 화살표·돌아가기 (좌표도 SCN_DIMS 로 ×N)
                     "log_")
# 명시 치수를 확대하지 않는 UI만 1×로 유지한다.
# msg_/f_ 는 크기 1× 로 두는 대화창 위에 그려지므로 같이 1× 다.
CG_UI_1X_PREFIX   = ("f_", "msg_", "frame_", "cursor_", "winmsg")
CG_FORCE_1X       = ()      # bg00b.png(미리스 로고 뒤 흰 배경)도 ×N 해야 화면을 채운다
OFF_SCREEN_W = [0x764e, 0xb879, 0xcdb6, 0x110a0]     # 640 dword (2026-07-26 exe diff)
OFF_SCREEN_H = [0x7653, 0xb870, 0xcdb1, 0x110a5]     # 480 dword

# 무비 네이티브 재생 (RESOLUTION.md §6-1, tools/patch_movie.py)
# True 면 무비 2배 확대를 끄므로 movie 아카이브도 화면 치수(=ORIG×SCALE)로 인코딩할 것.
MOVIE_NATIVE    = True
OFF_MOVIE_SCALE = 0x58ee8                            # VA 0x458EE7 `6a 02` 의 즉치 바이트

# 비번역 대용량 아카이브 — `ujyu unpack` 이 기본 제외한다(--all 로 포함).
PASSTHROUGH_ARCHIVES = ["bgm.axr", "movie.axr", "se.axr",
                        "voice.axr", "voice.ax2", "voice.ax3", "voice.ax4"]

# ─────────────────────────────────────────── 배포(release)
# `ujyu release` diff 에서 제외할 glob. 세이브(사용자 데이터)와 작업 스냅샷은
# 패치에 들어가면 안 된다. 칸나기는 해시 태그 스냅샷(cg.axr.config2x_58ef40a 등)이
# 배포 폴더에 많이 쌓여 있어 명시적으로 걸러 낸다.
# 배포 README 주의사항 (memory: 3× 검증 때 확인 — 호환 모드 없으면 실행 실패)
RELEASE_NOTES = [
    "게임 exe 속성에서 호환성 > Windows 8 호환 모드를 켜야 정상 실행됩니다.",
]

RELEASE_EXCLUDE = [
    "save/*", "*.sav",
    "*.bak", "*.orig", "*.tmp", "*.log",
    "*.pre*", "*.goto", "_*",
    "*.axr.*", "*.ax2.*", "*.ax3.*", "*.ax4.*",   # 아카이브 스냅샷 전부
    "*.exe.*",
    "*.320topaz", "*.640cap",
]

# ─────────────────────────────────────────── exe 패치
EXE_IN   = orig("kannagi.exe")            # 무패치 JP 원본 (읽기 전용)
EXE_OUT  = game("kannagi.exe")             # 배포 exe (재현성 확인: config 만으로 바이트 동일)

DLGFONT       = "맑은 고딕"          # 다이얼로그 리소스 폰트 (patch_ui)
FONT_FACE     = "KannagiKR-Noto"
FONT_FALLBACK = "KannagiKRC"
FILTER_PREFIX = "Kannagi"

IMAGE_BASE          = 0x400000
OFF_LEAD_BITMAP     = 0x77468
OFF_CHARSET_BODY    = 0x38248
OFF_CHARSET_ENUM    = 0xCBD5
# SJIS 리드 idiom -> CP949 리드 인정 (SKILL 6-3). (파일오프셋, 교체바이트hex) 쌍.
# xor ...,0x20 을 흡수하고 sub ...,0x81 / cmp ...,0x7E + NOP 로 길이를 맞춘다.
# 2026-07-30: 동작 중인 배포 exe 와 원본을 대조해 확정(원래는 오프셋만 있었다).
SJIS_IDIOM = [
    (0x1A9C6, "81 ea 81 00 00 00  83 fa 7e  90 90 90"),   # edx 경로
    (0x1EA23, "81 ea 81 00 00 00  83 fa 7e  90 90 90"),   # edx 경로 (사본)
    (0x02E9B, "90 90 90 90 90 90 90 90"),                 # 반각 가나 범위(A0/DF) 검사 제거
    (0x02EA8, "2d 81 00 00 00  83 f8 7e  90 90 90"),      # eax 경로
]

# 코드에 박힌 2바이트 문자 상수를 CP949 로 재인코딩 (오프셋 명시 = 오탐 방지).
# 원본은 SJIS 817A/8179(괄호류)로, 한글 폰트에서는 CP949 A1BD/A1BC 로 나와야 한다.
# 2026-07-30: 동작 중인 배포 exe 대조로 확정.
INLINE_RECODE = [
    (0x761CC, "a1 bd"),
    (0x761D0, "a1 bc"),
]

OFF_FILTER_PITCH    = [0xC974, 0xC983]
OFF_FILTER_PATTERN  = 0x75CD0
OFF_FILTER_PUSH     = 0xC94B
OFF_FILTER_JCC      = 0xC95B   # `0f 85`(jne) 의 둘째 바이트 -> 0x84(je)

OFF_FONT_GOTHIC     = 0x75690
OFF_FONT_MINCHO     = 0x756A0
OFF_FONT_FALLBACK   = 0x77458

CAVE_VA         = 0x0046DA40
BUF_VA          = 0x00482000
NBYTES_VA       = 0x00482040
SAVE_REL_PATH   = r"save\systemdata.dat"
SAVE_NAME_OFF   = 8
IAT_CreateFileA = 0x0046E084
IAT_ReadFile    = 0x0046E09C
IAT_CloseHandle = 0x0046E0B4

# ─────────────────────────────────────────── 폰트 빌드
# 폰트 빌드 스펙(source·face·shift·가변폭 글리프 조정)은 fonts/<face>.py 로 분리(config 와 무관).
# 빌드: ujyu font   (인자 없으면 FONT_FACE 스펙 + FONT_WIDTH_MODE 를 쓴다)


def require(*names):
    missing = [n for n in names if globals().get(n) in (None, [], "")]
    if missing:
        raise SystemExit("config.py 에 다음 항목을 먼저 채우세요: %s" % ", ".join(missing))
