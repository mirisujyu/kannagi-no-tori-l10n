# 神無ノ鳥 (칸나기의 새 / 신무의 새) 한글 패치

Studio Miris의 2002년 일본어 비주얼 노벨 **神無ノ鳥(칸나기의 새)** 한글 패치 프로젝트.
이 리포는 **이 타이틀의 번역 데이터와 실측 설정**만 담는다. 엔진 도구·포맷 지식·작업 절차는
서브모듈 [`engine/`](engine/) (studio-miris-engine) 에 있다 — 그쪽 [README](engine/README.md)에서 시작하면 된다.

> ⚠️ 게임 실행 파일·아카이브·폰트 등 저작권 있는 바이너리는 포함하지 않는다.
> 도구·포맷 지식·설정만 담는다. 번역문과 게임 원본은 포함하지 않는다.

## 번역 데이터 (`translation/`)

> **번역문 자체와 진행·검수 문서는 이 리포에 없다.** 원작 대사를 그대로 담고 있어
> 배포하지 않는다(`.gitignore`). 도구가 읽는 경로는 그대로이므로, 가지고 있다면
> `translation/strings.json` 에 두면 된다.
>
> 빠져 있는 것: `strings.json` · `strings_review.tsv` · `REVIEW_NOTES.md` ·
> `docs/REVIEW_MARKS.md` · `docs/PROGRESS.md` · `docs/STATUS.md` · `docs/SKIPPED_H.md`

| 파일 | 내용 |
|---|---|
| `strings.json` | **번역 정본** (v2): `[{arc, file, id, kind, off, bytelen, jp, speaker, kr}]`. `kr` 열을 채운다 |
| [CHARACTERS.md](translation/CHARACTERS.md) | 인물 프로필·1인칭·**상대별 말투** |
| [GLOSSARY.md](translation/GLOSSARY.md) | 고유명사 표기 통일 + 후리가나 확정표 |
| [NAMEPLATES.md](translation/NAMEPLATES.md) | 화자명(이름표) JP→KR 대응표 |
| [IMAGES.md](translation/IMAGES.md) | 이미지에 구워진 텍스트 manifest (`cg.axr`) |
| `ui_strings.json` | Windows UI 문자열 JP→KR |

번역 규칙(표기·엔진 제약·말투)의 정본은 **[tools/translate/STYLE.md](tools/translate/STYLE.md)**.

## 이 타이틀의 실측 설정

`config.py` 가 정본이다 — 경로·아카이브 목록·exe 오프셋·해상도 값이 전부 여기 있다.
`ujyu config show` 로 보고 `ujyu config set` 으로 바꾼다.

- **해상도 2×** (1280×960). 3×(1920×1440)도 검증됐으나 화면이 과해 2× 채택.
  배경·스프라이트는 AI 업스케일(Topaz) 결과를 `CG_UPSCALE_DIR` 에서 주입한다.
- **폰트** `KannagiKR-Noto`(가변폭). 빌드 스펙은 [fonts/](fonts/) 에 face 별로 분리.
- ⚠️ 배포본 exe 는 **Windows 8 호환 모드**로 실행해야 한다.

## 작업

```bash
# 이 리포 루트에서 실행하면 루트 config.py 를 자동으로 읽는다
ujyu inspect                # config 상태와 다음 할 일
ujyu filter context         # 씬을 문맥과 함께 덤프 -> 번역 -> ujyu filter apply
ujyu filter propagate       # 같은 원문에 기번역 전파
ujyu inject check           # 번역문 전수 검증 (0건이 되기 전엔 빌드 금지)
ujyu build                  # 배포본 조립
```

명령 목록은 [engine/docs/COMMANDS.md](engine/docs/COMMANDS.md), 순서는
[engine/docs/BOOTSTRAP.md](engine/docs/BOOTSTRAP.md), 작업 원칙은 [engine/GUIDE.md](engine/GUIDE.md).

## 리포 구조

```
config.tmpl.py            설정 참고본 — config.py 로 복사해 채운다 (config.py 는 .gitignore)
fonts/<face>.py           폰트 빌드 스펙 (config 와 분리)
translation/              번역 데이터·사전 (위 표)
tools/translate/STYLE.md  번역 표기 규칙 정본
engine/                   서브모듈 studio-miris-engine (도구·포맷 지식·절차)
```

## 화면 확대

이 타이틀은 **2×(1280×960)** 로 맞춰져 있다. 실측값과 이 게임에서 겪은 함정은
**[docs/UPSCALE.ja.md](docs/UPSCALE.ja.md)** (日本語) 에 정리했다 — 공유 심볼 때문에
이름 글자만 커진 일, 곡 제목이 행을 넘친 일, 선택지 크래시 원인 같은 것들.
일반적인 절차는 [engine/docs/UPSCALE.ja.md](engine/docs/UPSCALE.ja.md).

번역과 무관하게 **해상도만 올리는 용도로도** 그대로 쓸 수 있다.

## 시나리오 읽는 법

- 시나리오는 날짜 기반 명명(`0506_01` = 5월 6일 첫 장면), 분기는 접미사(a/b/c).
  **파일명 순 = 이야기 순.**
- 텍스트 순서 = 시나리오 내 등장 순서.

## 라이선스·주의

원작 저작권은 Studio Miris 에 있다. 본 리포는 팬 번역·기술 연구 목적의 자료이며,
**원작의 대사·텍스트는 담지 않는다** — 도구와 포맷 지식, 이 타이틀의 실측 설정뿐이다.
