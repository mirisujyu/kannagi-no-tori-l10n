# 폰트

`.ttf` 는 **커밋하지 않는다**(`.gitignore: fonts/*.ttf`). 소스와 스펙만 두고 빌드로 만든다.

| 파일 | 커밋 | 무엇 |
|---|---|---|
| `KannagiKR-Noto.py` | ✅ | 빌드 스펙 — `ujyu font` 가 읽는다 |
| `NotoSansKR-Regular.ttf` | ❌ | 한글 소스 (5.9MB) — 아래에서 받는다 |
| `NotoSansJP-Regular.ttf` | ❌ | 일본어 소스 (5.5MB) — 아래에서 받는다 |
| `KannagiKR-Noto.ttf` | ❌ | **산출물**. 이걸 설치한다 |

## 빌드

```bash
ujyu jpmap     # 미번역 일본어 문자 매핑 (translation/jp_charmap.json)
ujyu font      # -> fonts/KannagiKR-Noto.ttf  (jpmap 도 같이 다시 만든다)
```

`ujyu font` 가 빌드하면서 `jpmap` 을 다시 만든다 — 표와 폰트가 어긋날 일이 없다.
자세한 원리는 `engine/docs/formats/TEXT_RENDER.md` §4-5.

## 소스 받기

Noto Sans KR / JP (SIL OFL 1.1). google/fonts 의 **가변 폰트**를 받아 `wght=400`
으로 고정한다 — 가변인 채로 쓰면 글리프를 다시 그릴 때 `fvar`/`gvar` 가 어긋나
폰트가 깨진다.

```bash
curl -L "https://github.com/google/fonts/raw/main/ofl/notosanskr/NotoSansKR%5Bwght%5D.ttf" -o fonts/NotoSansKR.ttf
curl -L "https://github.com/google/fonts/raw/main/ofl/notosansjp/NotoSansJP%5Bwght%5D.ttf" -o fonts/NotoSansJP.ttf
python -c "
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
for n in ('NotoSansKR','NotoSansJP'):
    f = TTFont('fonts/%s.ttf' % n)
    instancer.instantiateVariableFont(f, {'wght': 400}, updateFontNames=True).save('fonts/%s-Regular.ttf' % n)
"
```

## 일본어 글리프를 어디까지 가져오나

**가나·한자 전체와 `々`·`、`·`。` 는 무조건 일본어 폰트에서 가져온다.** Noto Sans KR
도 한자를 8천여 자 갖고 있지만 **한국식 자형**이라(`直`·`骨`·`海` 등 획이 다르다)
일본어 문장에 섞이면 티가 난다. 온점·반점은 자형이 아니라 위치 문제다 — 한국어
폰트는 칸 가운데에 놓지만 일본어 조판은 왼쪽 아래에 붙인다.

그 밖의 글자는 **한글 폰트에 없을 때만** 일본어에서 가져온다.

이 규칙은 엔진 기본값(`build_font.JP_OVERRIDE_DEFAULT`)이라 스펙에 안 적어도 된다.
바꾸려면 스펙에 `JP_OVERRIDE` 를 주면 되고, `()` 로 두면 끌 수 있다.

## face 이름

**같은 이름의 구버전이 설치돼 있으면 GDI 가 그쪽을 고른다.** 새 폰트를 만들었는데
화면이 그대로면 이걸 의심할 것 — 실제로 겪었다. 폰트를 크게 바꿀 때는 face 이름도
바꾸는 편이 안전하고, 그러면 둘을 나란히 설치해 비교할 수도 있다.

exe 의 글꼴명 슬롯은 16바이트다 — 이름은 15자까지. `config.FILTER_PREFIX`(`Kannagi`)로
시작해야 게임의 글꼴 목록 필터를 통과한다.
