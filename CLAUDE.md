# 神無ノ鳥 (Kannagi no Tori) 한글 패치 — 작업 지침

Studio Miris VN 엔진(AXRe + VNEG)의 한글 패치 + 해상도 2× 확대 작업.

**먼저 읽을 것** (엔진 서브모듈, 재사용 계층):
- [engine/GUIDE.md](engine/GUIDE.md) — **작업 원칙·결정 주체(문답/분석/자동)·검증·증상별 진단·실무 함정.** 일반 원칙은 전부 여기 있다.
- [engine/docs/BOOTSTRAP.md](engine/docs/BOOTSTRAP.md) — 명령 순서, [engine/docs/COMMANDS.md](engine/docs/COMMANDS.md) — 명령 목록
- [engine/SKILL.md](engine/SKILL.md) — 엔진 구조와 "찾는 법"

아래는 **이 타이틀에만 해당하는 것과 사용자 지시**다.

## 시작할 때

리포에는 **`config.tmpl.py` 만** 있다. 이걸 `config.py` 로 복사해서 채우는 것이 첫 작업이다
(`config.py` 는 `.gitignore` — 타이틀마다 값이 달라 공유하지 않는다).

`config.tmpl.py` 에는 **이 타이틀에서 실제로 쓴 값이 그대로 남아 있다.** 지우지 말 것 —
어떤 항목이 무슨 뜻인지, 어떤 값이 실제로 동작했는지 보여 주는 참고본이다. 새로 시작할
때는 그대로 두고 `config.py` 쪽만 고친다.

**값이 갈리는 항목은 임의로 정하지 말고 문답으로 결정한다.** 아래 "결정 사항" 표가
비어(`TBD`) 있으면 아직 안 물어본 것이다. `config.py` 를 만들 때 물어서 정하고,
**`config.py` 와 이 표를 같이 갱신한다** — 한쪽만 고치면 다음 세션이 헷갈린다.
저수준 값(exe 오프셋·심볼 인덱스 등)은 물어보지 말고 직접 찾는다 — 분류 기준은
`engine/GUIDE.md §1`.

## 경로

**`config.py` 가 정본** — 상대 경로(`REPO_DIR`/`DEV_DIR` 기준).
`ORIG_DIR`(무패치 JP 원본)은 **절대 수정 금지** — 리버싱·대조의 기준이다.

## 사용자 지시 (반드시 지킬 것)

1. **공동 디버깅 전제.** 사용자가 디스어셈블을 함께 읽으며 돕는다. 산출물·설명을 명확하고
   풍부하게(오프셋·심볼·점프 타겟·힌트 포함) 낸다.
2. **디스어셈블러를 상시 보강한다.** 새 구조(오프너 패턴·opcode 오퍼랜드·심볼콜·점프테이블·
   화자 등)를 파악할 때마다 곧바로 `engine/` 의 `ujyu.formats.vneg` 에 반영하고
   `engine/docs/formats/VNEG.md` 에도 보충한다. 오탐(예: flow 오퍼랜드가 SJIS 로 읽히는
   `钁`)은 패턴으로 제거한다. 지적받기 전에 능동적으로 한다.
3. **발견은 메모리에 저장.** 비자명한 엔진 구조·버그 원인은 `memory/` 에 기록한다.
4. **작업 시작 시 옵션 확인** (2026-07-29 신설). 값이 갈리는 선택 옵션은 **문답으로 결정하고**
   진행한다(기본값 임의 진행 금지). 저수준 값(exe 오프셋·심볼 인덱스 등)은 직접 찾는다.
   분류 기준은 `engine/GUIDE.md §1`.
5. **재사용 스크립트는 리포에 커밋한다.** 스크래치패드에 두지 말고 `tools/`(타이틀 종속) 또는
   `engine/ujyu/`(범용)에 넣는다.

## 이 타이틀의 결정 사항

| 항목 | 값 | 비고 |
|---|---|---|
| `SCALE` | `TBD` | - |
| `FONT_WIDTH_MODE` | `TBD` | - |
| `FONT_FACE` | `TBD` | - |
| `MOVIE_NATIVE` | `TBD` | - |
| 실행 | Windows 8 호환 모드 필수 | |

## 번역

**대사·나레이션 번역을 시작하기 전에** `translation/` 아래 가이드를 **먼저 읽고** 그 규칙을
따른다. 안 보고 임의 스타일로 번역하지 말 것.

- **[tools/translate/STYLE.md](tools/translate/STYLE.md)** — **표기 규칙 정본**
  (전각공백·문장부호·대사 종결부·나레이션 들여쓰기·숫자·후리가나 처리). 엔진 제약과
  이 타이틀 결정이 함께 정리돼 있다.
- **[translation/CHARACTERS.md](translation/CHARACTERS.md)** — 인물·1인칭·말투,
  **상대별 말투**. 화자별 어투를 여기 맞춘다. 미리스(햄스터)=**루우 속마음 대변**,
  울음소리 `うじゅ→우쥬`.
- **[translation/GLOSSARY.md](translation/GLOSSARY.md)** — 고유명사 표기표 + 후리가나 확정 26종.
  예: 神無=칸나기, 常闇の間=**상암의 방**(도코야미 금지), 綿貫琉宇=와타누키 루우,
  深町康哉=후카마치 야스나리, 真部章仁=마나베 아키히토, 紗=우스기누.
  **후리가나 `【읽기】`는 번역문에 넣지 않는다**(음차만).
- **진행 현황**은 `docs/STATUS.md` — `tools/gen_status.py` 가 `strings.json` 에서
  만든다. **커밋할 때마다 돌린다**(손으로 고치면 어긋난다). 파일명 순=이야기 순이라
  공통 루트 `0506_`→`0512_` 부터 순서대로 진행한다.
  이 문서와 `strings.json` 은 원작 대사를 담고 있어 **리포에 올리지 않는다**(`.gitignore`).

### 데이터

- 번역 원본 = `translation/strings.json`. 레코드 `arc/file/id/kind/off/bytelen/jp[/speaker]/kr`,
  `kr` 를 채운다.
- **번역 대상** = `kind` 가 dlg/narr/quote(내용)·cstr 이고 jp 에 표시문자가 있는 것.
  `sym`(화자명·선택지·씬제목)은 완료. `quote` 오프너(`「z`/`（z`)·빈 narr·리소스명은 불필요.
- **동일 원문은 `ujyu filter propagate` 로 전파**(VN 분기 공통 대사가 많다) 후 고유 대사만
  손번역한다. 번역할 때는 `ujyu filter context` 로 앞뒤 대사를 함께 본다.

## 이 타이틀 고유 지식

- **무비·선택지 hang = VNEG 점프테이블의 스테일 flow 상대 오프셋.** 씬 재패킹 시 재매핑
  필수 → memory `kannagi-jumptable-fix`
- **선택지 진입 크래시 = common.csv 를 다른 아카이브 것으로 통째 주입**해 고유 변수 정의가
  사라진 것 → 아카이브마다 자기 것을 제자리 편집 → memory `kannagi-common-csv-per-archive`
- **번역하지 않고 원문으로 남기는 대목**이 있으면 `ujyu jpmap` 으로 문자 매핑을 만들고
  `ujyu font` 로 일본어 글리프를 심는다. CP949 에 없는 한자를 사용자정의영역에 싣는
  구조라, **`jpmap` 을 다시 돌리면 `font` 도 반드시 다시 돌려야 한다**(표가 어긋나면
  화면의 글자가 바뀐다). 원리는 `engine/docs/formats/TEXT_RENDER.md` §4-5.
- 그 외 발견은 `memory/` 참조.
