# 칸나기의 새 이미지 애셋의 번역·렌더링 명세

## 디렉터리 구조

- 물리적 경로는 이 문서에 기록하지 않고 저장소 루트 `config.py`의 이미지 애셋 설정을 사용한다.
  - `IMAGE_ASSET_DIR`: 이미지 애셋 루트
  - `IMAGE_ORIGINAL_DIR`: 일본어 원본 이미지 디렉터리
  - `IMAGE_TEXTLESS_DIR`: 원본에서 번역 대상 글자만 제거한 이미지 디렉터리
  - `IMAGE_TEXTED_PREFIX`: 글꼴별 한국어 렌더링 결과 디렉터리 접두사
- 번역 대상 파일 집합은 `textless`에 있는 PNG를 기준으로 한다.
- `original`에는 있지만 `textless`에는 없는 파일은 번역하지 않기로 한 것이므로 `texted-<글꼴명>`에 만들지 않는다.
- 각 `texted-<글꼴명>`에는 번역된 PNG만 저장한다. 가이드나 글꼴 파일은 복사하지 않는다.

## 렌더·주입 절차

이 문서는 이미지 렌더링 설정의 **단일 원본**이다. 문서 끝의
`image-text-manifest` JSON 블록에 글꼴·파일명·번역문·위치·크기·색·합성 순서를
저장한다. `ujyu image`는 특정 게임 설정을 갖지 않으며 이 블록을
직접 읽는다. 별도의 YAML/JSON 파일로 변환하는 중간 단계는 없다.

1. **렌더** — 폰트별 PNG 생성. 입력(원문/무문자)·폰트·출력 경로는 전부 `config.py`의
   `IMAGE_*` 설정을 따른다(절대경로 박지 말 것).
   ```
   ujyu image --check
   ujyu image --variant Minguk
   ujyu image --all
   ```
   - 기본 폰트 변형은 `config.py`의 `IMAGE_VARIANT`이다.
   - 출력 폴더 = `IMAGE_TEXTED_PREFIX + {폰트}` (예: `texted-Minguk`).
2. **채택** — 여러 폰트를 비교한 뒤 쓸 폴더를 `config.CG_TRANS_DIR`에 지정(기본 `texted-Minguk`).
3. **주입** — `ujyu build`가 그 폴더의 PNG를 `cg.axr`에 주입하고, `SCALE>1`이면 확대한다.
   ```
   python ../studio-miris-engine/ujyu build         # 전체 빌드(이미지 포함)
   python ../studio-miris-engine/ujyu build --no-cg # 이미지 스킵
   ```

## 렌더링 글꼴

| 출력 디렉터리 | Regular/Light | Bold | 글꼴 안내 |
|---|---|---|---|
| `texted-Minguk` | `Minguk-Regular.woff` | `Minguk-Bold.woff` | [민국체](https://noonnu.cc/font_page/337) |
| `texted-경기천년바탕` | `GyeonggiMillenniumBatang-Regular.woff` | `GyeonggiMillenniumBatang-Bold.woff` | [경기천년바탕](https://noonnu.cc/font_page/13) |
| `texted-강원교육모두체` | `GangwonEduModu-Light.woff` | `GangwonEduModu-Bold.woff` | [강원교육모두체](https://noonnu.cc/font_page/802) |
| `texted-교보손글씨 2020 박도연` | `KyoboHandwriting2020ParkDoYeon.woff` | 동일 파일(단일 굵기) | [교보손글씨 2020 박도연](https://noonnu.cc/font_page/782) |

- 명세·렌더러와 글꼴 경로는 `config.py`의 `IMAGE_SPEC`, `IMAGE_RENDERER`,
  `IMAGE_FONT_DIR`을 사용한다.
- 글꼴 파일은 라이선스 조건을 확인한 뒤 별도로 관리하며 이미지 결과 디렉터리에는 포함하지 않는다.

## 공통 렌더링 규칙

- 원본 이미지, 무문자 이미지, 번역 이미지를 별도의 디렉토리에 관리한다.
  - 아래 목록에는 있으나 무문자 이미지에 없는 파일은 사용자가 번역하지 않기로 결정한 것이므로 무시한다.
- 좌표 표기: `(좌상 x, y) - (우하 x, y)`, 우하 좌표는 미포함
- 표의 위치는 레이아웃용 여유 영역이 아니라 원본에서 실제로 보이는 글자·외곽선·그림자의 픽셀 바운딩 박스이다.
- RGB 이미지는 원본–무문자 차이, 글자색 마스크, 확대 오버레이를 함께 확인했고, RGBA 스프라이트는 알파값이 0보다 큰 픽셀을 측정했다.
- 번역문은 원본 바운딩 박스의 정렬 기준점과 세로 중심을 따른다. 텍스트 상자의 가로 overflow는 허용한다. 다만 실제 렌더링된 글자가 이미지 캔버스 밖으로 나가면, 전체 글자가 이미지 안에 들어올 때까지 글꼴 크기만 축소한다. 줄바꿈하거나 잘라내지 않는다.
- 크기/테두리/자간은 원본을 기준으로 한 초기 추정치이며 실제 렌더링 때 미세 조정한다.
- `off`: 흰색 계열 글자 + 검정 외곽선
- `on`: 흰색 계열 글자 + 적색 외곽선
- `select`: 검정 글자 + 적색 외곽선
- 렌더링 결과 폴더에는 PNG만 저장한다. 이 문서는 중앙 명세로만 유지한다.

## 1. 엔딩 제목 카드

공통 스타일: Regular, 테두리 없음, 자간 약 `1px`. `_2` 파일에는 우하단의 `了`도 존재한다.

| 파일 | 원문 → 번역 | 원본 실제 텍스트 bbox | 크기 | 색 | weight | 테두리 | 자간 |
|---|---|---:|---:|---|---|---|---:|
| `be_a02_1.png` | 消えた少年 → 사라진 소년 | `(270,219)-(369,240)` | 17px | `#202020` | Regular | 없음 | 1px |
| `be_a02_2.png` | 消えた少年 → 사라진 소년 | `(270,219)-(369,240)` | 17px | `#202020` | Regular | 없음 | 1px |
| 〃 | 了 → 끝 | `(549,389)-(578,434)` | 28px | `#202020` | Regular | 없음 | 0px |
| `be_f02_1.png` | 魂のカタチ → 혼의 형태 | `(267,220)-(371,241)` | 17px | `#303030` | Regular | 없음 | 1px |
| `be_f02_2.png` | 魂のカタチ → 혼의 형태 | `(267,220)-(371,241)` | 17px | `#303030` | Regular | 없음 | 1px |
| 〃 | 了 → 끝 | `(559,399)-(589,445)` | 28px | `#303030` | Regular | 없음 | 0px |
| `be_l01_1.png` | 遠い記憶 → 아득한 기억 | `(279,219)-(361,240)` | 17px | `#F2F2ED` | Regular | 없음 | 1px |
| `be_l01_2.png` | 遠い記憶 → 아득한 기억 | `(279,219)-(361,240)` | 17px | `#F2F2ED` | Regular | 없음 | 1px |
| 〃 | 了 → 끝 | `(549,389)-(578,434)` | 28px | `#F2F2ED` | Regular | 없음 | 0px |
| `be_l02_1.png` | さよなら → 안녕 | `(281,220)-(358,239)` | 17px | `#F2F2ED` | Regular | 없음 | 2px |
| `be_l02_2.png` | さよなら → 안녕 | `(281,220)-(358,239)` | 17px | `#F2F2ED` | Regular | 없음 | 2px |
| 〃 | 了 → 끝 | `(549,389)-(578,434)` | 28px | `#F2F2ED` | Regular | 없음 | 0px |
| `be_l03_1.png` | ずっと、この場所で → 계속, 이곳에서 | `(226,220)-(414,240)` | 17px | `#F2F2ED` | Regular | 없음 | 2px |
| `be_l03_2.png` | ずっと、この場所で → 계속, 이곳에서 | `(226,220)-(414,240)` | 17px | `#F2F2ED` | Regular | 없음 | 2px |
| 〃 | 了 → 끝 | `(549,389)-(578,434)` | 28px | `#F2F2ED` | Regular | 없음 | 0px |
| `be_r02_1.png` | ただひとつの望み → 단 하나의 소망 | `(239,220)-(401,240)` | 17px | `#F2F2ED` | Regular | 없음 | 2px |
| `be_r02_2.png` | ただひとつの望み → 단 하나의 소망 | `(239,220)-(401,240)` | 17px | `#F2F2ED` | Regular | 없음 | 2px |
| 〃 | 了 → 끝 | `(549,389)-(578,434)` | 28px | `#F2F2ED` | Regular | 없음 | 0px |

## 2. CG 감상 화면

### 배경 제목

공통 스타일: 흰색 `#F5F5F0`, Regular, 검정 `#050505` 외곽선 `2px`, 자간 `1px`, 정렬 `왼쪽, 위`.

| 파일 | 원문 → 번역 | 원본 실제 텍스트 bbox | 크기 |
|---|---|---:|---:|
| `cg_background_etc.png` | その他 → 기타 | `(41,38)-(127,77)` | 30px |
| `cg_background_hakkan.png` | ハッカン → 핫칸 | `(40,40)-(152,77)` | 30px |
| `cg_background_hukamachi.png` | 深町 康哉 → 후카마치 야스나리 | `(41,38)-(173,77)` | 30px |
| `cg_background_ikaru.png` | イカル → 이카루 | `(40,40)-(124,76)` | 30px |
| `cg_background_manabe.png` | 真部 章仁 → 마나베 아키히토 | `(41,38)-(173,78)` | 30px |
| `cg_background_renjaku.png` | レンジャク → 렌자크 | `(40,40)-(178,77)` | 30px |
| `cg_background_ruu.png` | 綿貫 琉宇 → 와타누키 루우 | `(40,38)-(180,78)` | 30px |
| `cgtop_background.png` | CG 鑑賞モード → CG 감상 모드 | `(40,38)-(241,77)` | 30px |

### 투명 버튼 스프라이트

Off 스타일: 흰색 글자 / 검은색 테두리
On 스타일: 빨간색 글자 / 흰색 테두리

| 파일 | 원문 → 번역 | 원본 실제 텍스트 bbox | 크기 | 상태 스타일 |
|---|---|---:|---:|---|
| `cgtop_back_off.png` | 前ページ → 이전 페이지 | `(2,2)-(94,32)` | 22px | off |
| `cgtop_back_on.png` | 前ページ → 이전 페이지 | `(2,2)-(94,32)` | 22px | on |
| `cgtop_next_off.png` | 次ページ → 다음 페이지 | `(2,1)-(94,30)` | 22px | off |
| `cgtop_next_on.png` | 次ページ → 다음 페이지 | `(2,1)-(94,30)` | 22px | on |
| `cgtop_title_off.png` | 戻る → 뒤로 | `(1,1)-(43,30)` | 15px | off |
| `cgtop_title_on.png` | 戻る → 뒤로 | `(1,1)-(43,30)` | 15px | on |

### 작은 타이틀 섬네일

#### `cgtop_thumbnail.png`

- 원문: `神無ノ鳥`
  - 번역문: `칸나기의 새`
  - 원본 실제 텍스트 bbox: `(39,11)-(52,48)`
  - 글꼴 크기: 약 `8px`
  - 글꼴 색: `#ED1C24`
  - weight: Light
  - 테두리: `#C6C0BD`, 약 `1px`
  - 자간: `0px`
- 저작권 문구는 원문 유지.

## 3. 환경설정

### `config_bg.png`

공통 본문 스타일: `#F7F7F0`, Regular, 검정 `#050505` 외곽선 `2px`, 자간 `0px`.

- 정렬은 각 행에 적힌 텍스트 상자의 경계를 기준으로 한다.
- 세로 방향은 모두 가운데 정렬한다.
- 가로 방향은 별도 지시가 없으면 왼쪽 정렬한다.
- 왼쪽 정렬은 렌더링된 텍스트의 왼쪽 끝을 텍스트 상자의 왼쪽 끝과 일치시킨다.
- 오른쪽 정렬은 렌더링된 텍스트의 오른쪽 끝을 텍스트 상자의 오른쪽 끝과 일치시킨다.
- 가운데 정렬은 렌더링된 텍스트의 가로 중심을 텍스트 상자의 가로 중심과 일치시킨다.
- 텍스트 상자보다 번역문이 길어 가로 overflow가 발생해도 이를 허용한다. 단, 실제 글자가 이미지 파일의 바깥으로 넘어가면 전체 글자가 이미지 안에 들어올 때까지 글꼴 크기를 축소한다. 텍스트 상자 폭만을 이유로 축소하지 않으며, 줄바꿈하거나 상자 또는 이미지 경계에서 잘라내지 않는다.
- 화면 제목만 가운데 정렬하고, 슬라이더 왼쪽 값은 오른쪽 정렬하여 슬라이더 쪽에 붙인다.
- 슬라이더 오른쪽 값은 왼쪽 정렬하여 슬라이더 쪽에 붙인다.
- 아래 위치는 원본 글자의 외곽선까지 포함하여 다시 측정한 실제 픽셀 바운딩 박스이다.
- 번역문은 이 박스의 정렬 기준점과 세로 중심을 유지한다. 박스 폭에 맞춰 강제로 늘이거나 줄이지 않는다.
- 크기는 글꼴의 명목 크기가 아니라 외곽선까지 포함한 실제 렌더링 높이의 목표값이다. 글꼴마다 이 높이에 맞는 명목 크기를 따로 선택한다.

| 원문 → 번역 | 원본 실제 바운딩 박스 | 목표 실제 높이 | 가로 정렬 |
|---|---:|---:|---|
| 環境設定 → 환경 설정 | `(267,36)-(372,68)` | 32px | 가운데 |
| 文字の設定 → 문자 설정 | `(90,66)-(192,91)` | 25px | 왼쪽 |
| 表示速度 → 표시 속도 | `(102,101)-(176,123)` | 22px | 왼쪽 |
| オートモード待ち時間 → 자동 모드 대기 시간 | `(103,127)-(290,149)` | 22px | 왼쪽 |
| 文字描画方法 → 문자 표시 방식 | `(103,153)-(214,175)` | 22px | 왼쪽 |
| フォント → 글꼴 | `(104,180)-(171,201)` | 21px | 왼쪽 |
| サンプルテキスト → 예시 문장 | `(103,207)-(209,223)` | 16px | 왼쪽 |
| 遅 → 느림 | `(327,101)-(345,123)` | 22px | 오른쪽 |
| 速 → 빠름 | `(516,102)-(533,123)` | 21px | 왼쪽 |
| 短 → 짧게 | `(327,128)-(344,149)` | 21px | 오른쪽 |
| 長 → 길게 | `(517,127)-(534,149)` | 22px | 왼쪽 |
| 音の設定 → 음향 설정 | `(90,303)-(172,329)` | 26px | 왼쪽 |
| BGM → 배경 음악 | `(105,338)-(157,358)` | 20px | 왼쪽 |
| 効果音 → 효과음 | `(103,363)-(158,385)` | 22px | 왼쪽 |
| 音声 → 음성 | `(102,389)-(138,411)` | 22px | 왼쪽 |
| 小 → 작게 | `(328,338)-(344,358)` | 20px | 오른쪽 |
| 大 → 크게 | `(517,340)-(534,358)` | 18px | 왼쪽 |
| 小 → 작게 | `(328,364)-(344,384)` | 20px | 오른쪽 |
| 大 → 크게 | `(517,366)-(534,385)` | 19px | 왼쪽 |
| 小 → 작게 | `(328,390)-(344,410)` | 20px | 오른쪽 |
| 大 → 크게 | `(517,392)-(534,412)` | 20px | 왼쪽 |

### 환경설정 버튼 스프라이트

Off 스타일: 흰색 글자 / 검은색 테두리
On 스타일: 빨간색 글자 / 흰색 테두리
Selection 스타일: 빨간색 글자 / 검은색 테두리

| 파일 | 원문 → 번역 | 원본 실제 텍스트 bbox | 크기 | 상태 |
|---|---|---:|---:|---|
| `config_anti_off.png` | アンチエイリアス → 안티앨리어싱 | `(0,0)-(149,22)` | 17px | off |
| `config_anti_on.png` | アンチエイリアス → 안티앨리어싱 | `(0,0)-(149,22)` | 17px | on |
| `config_anti_select.png` | アンチエイリアス → 안티앨리어싱 | `(0,0)-(149,22)` | 17px | select |
| `config_back_off.png` | 戻る → 뒤로 | `(0,0)-(37,24)` | 15px | off |
| `config_back_on.png` | 戻る → 뒤로 | `(0,0)-(37,24)` | 15px | on |
| `config_hyoujun_off.png` | 標準 → 기본 | `(0,0)-(38,24)` | 15px | off |
| `config_hyoujun_on.png` | 標準 → 기본 | `(0,0)-(38,24)` | 15px | on |
| `config_hyoujun_select.png` | 標準 → 기본 | `(0,0)-(38,24)` | 15px | select |
| `config_off_off.png` | OFF → OFF | `(0,0)-(32,20)` | 16px | off |
| `config_off_on.png` | OFF → OFF | `(0,0)-(32,20)` | 16px | on |
| `config_off_select.png` | OFF → OFF | `(0,0)-(32,20)` | 16px | select |
| `config_on_off.png` | ON → ON | `(0,0)-(25,20)` | 16px | off |
| `config_on_on.png` | ON → ON | `(0,0)-(25,20)` | 16px | on |
| `config_on_select.png` | ON → ON | `(0,0)-(25,20)` | 16px | select |
| `config_syuuryou_off.png` | ゲームを終了する → 게임 종료 | `(0,0)-(150,26)` | 21px | off |
| `config_syuuryou_on.png` | ゲームを終了する → 게임 종료 | `(0,0)-(150,26)` | 21px | on |
| `config_title_off.png` | タイトルに戻る → 타이틀로 | `(0,0)-(131,24)` | 21px | off |
| `config_title_on.png` | タイトルに戻る → 타이틀로 | `(0,0)-(131,24)` | 21px | on |

## 4. 음악 감상·세이브/로드·장면 회상

| 파일 | 원문 → 번역 | 원본 실제 텍스트 bbox | 크기 | 상태/스타일 |
|---|---|---:|---:|---|
| `mu_background.png` | 音楽鑑賞モード → 음악 감상 모드 | `(65,33)-(278,74)` | 29px | 흰색, 검정 2px |
| `mu_stop_off.png` | 音楽の停止 → 음악 정지 | `(2,1)-(96,27)` | 23px | off |
| `mu_stop_on.png` | 音楽の停止 → 음악 정지 | `(2,1)-(96,27)` | 23px | on |
| `mu_title_off.png` | 戻る → 뒤로 | `(0,0)-(36,25)` | 15px | off |
| `mu_title_on.png` | 戻る → 뒤로 | `(0,0)-(36,25)` | 15px | on |
| `sa_lo_back_off.png` | 戻る → 뒤로 | `(3,2)-(83,37)` | 24px | off |
| `sa_lo_back_on.png` | 戻る → 뒤로 | `(3,2)-(83,37)` | 24px | on |
| `sa_lo_load.png` | ロード → 불러오기 | `(5,4)-(116,36)` | 25px | 흰색, 검정 2px |
| `sa_lo_save.png` | セーブ → 저장 | `(3,1)-(120,36)` | 25px | 흰색, 검정 2px |
| `sc_maepage_off.png` | 前ページ → 이전 페이지 | `(2,2)-(94,32)` | 22px | off |
| `sc_maepage_on.png` | 前ページ → 이전 페이지 | `(2,2)-(94,32)` | 22px | on |
| `sc_title_off.png` | 戻る → 뒤로 | `(1,1)-(43,30)` | 15px | off |
| `sc_title_on.png` | 戻る → 뒤로 | `(1,1)-(43,30)` | 15px | on |
| `sc_tugipage_off.png` | 次ページ → 다음 페이지 | `(2,1)-(94,30)` | 22px | off |
| `sc_tugipage_on.png` | 次ページ → 다음 페이지 | `(2,1)-(94,30)` | 22px | on |

## 5. 타이틀 메뉴

공통 스타일: Regular, 자간 `가변`; off는 흰색 `#F5F5F0` + 검정 `3px`, on은 흰색 `#FFF8F4` + 적색 `#E84B50` `2px`.
아래의 텍스트는 bbox에 가득 차도록 자간을 가변적으로 배치한다.

| 파일 | 원문 → 번역 | 원본 실제 텍스트 bbox | 크기 |
|---|---|---:|---:|
| `title_cg_off.png`     | CG 鑑賞 → CG 감상     | `(7,2)-(146,35)` | 26px |
| `title_cg_on.png`      | CG 鑑賞 → CG 감상     | `(8,3)-(145,34)` | 26px |
| `title_config_off.png` | 設定 → 설정           | `(7,2)-(146,35)` | 26px |
| `title_config_on.png`  | 設定 → 설정           | `(8,3)-(145,34)` | 26px |
| `title_end_off.png`    | 終了 → 종료           | `(27,2)-(123,35)` | 26px |
| `title_end_on.png`     | 終了 → 종료           | `(28,3)-(122,34)` | 26px |
| `title_load_off.png`   | 続きから → 이어하기    | `(7,2)-(146,35)` | 26px |
| `title_load_on.png`    | 続きから → 이어하기    | `(8,3)-(145,34)` | 26px |
| `title_music_off.png`  | 音楽鑑賞 → 음악 감상   | `(7,2)-(146,35)` | 26px |
| `title_music_on.png`   | 音楽鑑賞 → 음악 감상   | `(8,3)-(145,34)` | 26px |
| `title_scene_off.png`  | シーン回想 → 장면 회상 | `(7,2)-(146,35)` | 26px |
| `title_scene_on.png`   | シーン回想 → 장면 회상 | `(8,3)-(145,34)` | 26px |
| `title_start_off.png`  | はじめから → 처음부터  | `(7,2)-(146,35)` | 26px |
| `title_start_on.png`   | はじめから → 처음부터  | `(8,3)-(145,34)` | 26px | 

### `title_background.png`

- 원문: `神無ノ鳥`
  - 번역문: `칸나기의 새`
  - 원본 실제 텍스트 bbox: `(483,82)-(532,246)`, 세로쓰기
  - 글꼴 크기: 약 `38px`
  - 글꼴 색: `#ED1C24`
  - weight: Light
  - 테두리: `#C6C0BD`, 약 `1px`
  - 자간: 약 `2px`
- 원문: `2002 © すたじおみりす Team L←R`
  - 번역문: `2002 © 스튜디오 미리스 Team L←R`
  - 원본 실제 텍스트 bbox: `(383,464)-(607,477)`
  - 글꼴 크기: 약 `11px`
  - 글꼴 색: `#F0F0EA`
  - weight: Regular
  - 테두리 없음
  - 자간: `0px`

## 6. 기타 텍스트

| 파일 | 원문 → 번역 | 원본 실제 텍스트 bbox | 크기 | 스타일 |
|---|---|---:|---:|---|
| `end_bad.png` | To Be Continued... → 계속... | `(238,226)-(402,253)` | 13px | 흰색, Regular, 테두리 없음 |
| `ex_title.png` | 神無ノ鳥 → 칸나기의 새 | `(279,211)-(360,230)` | 실제 글자 높이 18~19px | 흰색, Regular; 글꼴 폭에 맞춘 가로줄 |
| 〃 | 番外編 → 번외편 | `(291,240)-(350,258)` | 위 문구와 동일 | 흰색, Regular |
| `l_end_kan.png` | 完 → 끝 | `(308,228)-(331,252)` | 18px | `#202020`, Regular |
| `log_exit@n.png` | 戻る → 뒤로 | `(0,0)-(58,18)` | 13px | 밝은 회백색, 약한 그림자 |
| `log_exit@s.png` | 戻る → 뒤로 | `(0,0)-(58,18)` | 13px | 밝은 회백색, 선택 강조 |
| `miris_logo3.png` | すたじお みりす → 스튜디오 미리스 | `(22,36)-(206,155)` | 약 36px | 청색, Bold |
| `miris_logo4.png` | Team L←R → Team L←R | `(35,166)-(251,202)` | 약 25px | 회색, Bold |
| `msg_kaisou_on.png` | 回想 → 회상 | `(4,15)-(23,23)` | 약 13px | 선택 아이콘과 조화 |
| `msg_settei_on.png` | 設定 → 설정 | `(4,15)-(23,23)` | 약 13px | 선택 아이콘과 조화 |
| `testroll.png` | ロールテスト → 롤 테스트 | `(396,11)-(598,54)` | 약 17px | 흰색, 검정 2px |
| 〃 | ロールテスト → 롤 테스트 | `(395,140)-(597,183)` | 약 17px | 흰색, 검정 2px |
| 〃 | ロールテスト → 롤 테스트 | `(403,262)-(605,305)` | 약 17px | 흰색, 검정 2px |
| 〃 | ロールテスト → 롤 테스트 | `(402,386)-(604,429)` | 약 17px | 흰색, 검정 2px |

`msg_kaisou_off.png`, `msg_settei_off.png`, `miris_logo1.png`, `miris_logo2.png`에는 번역 대상 문자가 없다.

### `ex_title.png` 원본 재측정값

| 요소 | 원본 실제 바운딩 박스 | 실제 높이 | 중심 |
|---|---|---:|---:|
| `神無ノ鳥` | `(279,211)-(360,230)` | 19px | `x=319.5` |
| 가로줄 | `(275,234)-(364,235)` | 1px | `x=319.5` |
| `番外編` | `(291,240)-(350,258)` | 18px | `x=320.5` |

- `ex_title.png`에는 위 제목, 가운데 가로줄, 아래 부제의 세 요소를 모두 반드시 렌더링한다. 가로줄을 생략하면 안 된다.
- 두 문구는 같은 글꼴 파일, weight, 명목 글꼴 크기를 사용한다.
- 선택한 글꼴에서 두 문구의 실제 글자 높이가 약 `18~19px`이 되도록 하나의 크기를 정하며, `번외편`만 작게 만들지 않는다.
- 두 문구와 가로줄은 모두 `x=320`을 기준으로 가운데 정렬한다.
- 위 문구의 실제 글자 하단과 가로줄 사이에는 `4px`, 가로줄과 아래 문구의 실제 글자 상단 사이에는 `5px`의 빈 간격을 둔다.
- 글꼴마다 ascender와 실제 바운딩 박스가 다르므로 baseline이나 고정 박스가 아니라 렌더링된 글자의 실제 픽셀 바운딩 박스로 위치를 맞춘다.
- 두 문구의 크기와 위치를 확정한 다음, 실제 제목 폭을 측정하여 그 폭보다 좌우 각각 `4px` 긴 가로줄을 두 문구 사이에 직접 그린다.
- 가로줄은 장식 선택 사항이 아니라 원본 구성을 재현하기 위한 필수 그래픽 요소이다.

## 7. 렌더링 후 작성 형식

출력 폴더의 이 문서 사본에서는 각 원문 항목 바로 아래에 다음 블록을 추가한다.

```text
- 번역문 렌더링 결과
  - 번역문: 
  - 실제 위치: (좌상) - (우하)
  - 실제 글꼴: 
  - 실제 글꼴 크기:
  - 실제 글꼴 색:
  - 실제 글꼴 weight:
  - 실제 테두리 색:
  - 실제 테두리 weight:
  - 실제 자간:
```

## 8. 미번역·검토 메모

- 캐릭터 이름은 한국어 음역을 사용한다.
- `OFF`, `ON`, `CG`, `BGM`, `Team L←R` 및 저작권 문구는 원문 표기를 유지한다.
- `ただひとつの望み`는 `단 하나의 소망`으로 번역한다.
- `cgtop_thumbnail.png`은 `title_background.png`의 최종 로고를 축소해 생성하는 편이 일관성이 좋다.
- `ex_title.png`의 원본 가로줄 `(275,234)-(364,235)`은 위치와 분위기를 위한 참고값이다.
- 가로줄은 각 글꼴로 렌더링한 `칸나기의 새`의 실제 글자 바운딩 박스 폭보다 좌우 각각 `4px` 길게 만들고, 글자와 같은 중심축에 정렬한다.
- 가로줄의 굵기는 Light/Regular `1px`, Bold `2px`를 기본으로 하며 글꼴의 획 굵기에 맞춰 조정한다.
- 가로줄의 색과 알파는 제목 글자와 같게 하고, 제목과 `번외편` 사이의 여백 중앙에 배치한다.
- 따라서 가로줄은 원본 픽셀을 그대로 복사하지 않고, 선택한 글꼴의 폭·weight·위치에 맞춰 매번 다시 그린다.

## 9. ?? ?? ??? ??

?? JSON ??? ???? ?? ?? ?? ?? ????. ?? ??? ?? ??? ? ? ??? ?? ????. ?? ?? ??? ???? ???.

<!-- image-text-manifest:start -->
```json
{
  "schema": 1,
  "description": "Kannagi no Tori image text rendering manifest",
  "fonts": [
    {
      "name": "Minguk",
      "regular": "Minguk-Regular.woff",
      "bold": "Minguk-Bold.woff"
    },
    {
      "name": "경기천년바탕",
      "regular": "GyeonggiMillenniumBatang-Regular.woff",
      "bold": "GyeonggiMillenniumBatang-Bold.woff"
    },
    {
      "name": "강원교육모두체",
      "regular": "GangwonEduModu-Light.woff",
      "bold": "GangwonEduModu-Bold.woff"
    },
    {
      "name": "교보손글씨 2020 박도연",
      "regular": "KyoboHandwriting2020ParkDoYeon.woff",
      "bold": "KyoboHandwriting2020ParkDoYeon.woff"
    }
  ],
  "operations": [
    {
      "id": "be_a02_1.1",
      "type": "text",
      "file": "be_a02_1.png",
      "source_text": "消えた少年",
      "text": "사라진 소년",
      "fill": "#202020FF",
      "weight": "Regular",
      "stroke": null,
      "stroke_width": 0,
      "render": {
        "Minguk": {
          "x": 264,
          "y": 219,
          "size": 22,
          "tracking": 1
        },
        "경기천년바탕": {
          "x": 268,
          "y": 219,
          "size": 21,
          "tracking": 1
        },
        "강원교육모두체": {
          "x": 270,
          "y": 219,
          "size": 23,
          "tracking": 1
        },
        "교보손글씨 2020 박도연": {
          "x": 272,
          "y": 219,
          "size": 21,
          "tracking": 1
        }
      }
    },
    {
      "id": "be_a02_2.1",
      "type": "text",
      "file": "be_a02_2.png",
      "source_text": "消えた少年",
      "text": "사라진 소년",
      "fill": "#202020FF",
      "weight": "Regular",
      "stroke": null,
      "stroke_width": 0,
      "render": {
        "Minguk": {
          "x": 264,
          "y": 219,
          "size": 22,
          "tracking": 1
        },
        "경기천년바탕": {
          "x": 268,
          "y": 219,
          "size": 21,
          "tracking": 1
        },
        "강원교육모두체": {
          "x": 270,
          "y": 219,
          "size": 23,
          "tracking": 1
        },
        "교보손글씨 2020 박도연": {
          "x": 272,
          "y": 219,
          "size": 21,
          "tracking": 1
        }
      }
    },
    {
      "id": "be_a02_2.2",
      "type": "text",
      "file": "be_a02_2.png",
      "source_text": "了",
      "text": "끝",
      "fill": "#202020FF",
      "weight": "Regular",
      "stroke": null,
      "stroke_width": 0,
      "render": {
        "Minguk": {
          "x": 546,
          "y": 393,
          "size": 39,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 546,
          "y": 393,
          "size": 40,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 548,
          "y": 396,
          "size": 39,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 548,
          "y": 393,
          "size": 40,
          "tracking": 0
        }
      }
    },
    {
      "id": "be_f02_2.1",
      "type": "text",
      "file": "be_f02_2.png",
      "source_text": "魂のカタチ",
      "text": "혼의 형태",
      "fill": "#303030FF",
      "weight": "Regular",
      "stroke": null,
      "stroke_width": 0,
      "render": {
        "Minguk": {
          "x": 278,
          "y": 220,
          "size": 20,
          "tracking": 1
        },
        "경기천년바탕": {
          "x": 277,
          "y": 220,
          "size": 21,
          "tracking": 1
        },
        "강원교육모두체": {
          "x": 276,
          "y": 220,
          "size": 24,
          "tracking": 1
        },
        "교보손글씨 2020 박도연": {
          "x": 280,
          "y": 220,
          "size": 21,
          "tracking": 1
        }
      }
    },
    {
      "id": "be_f02_2.2",
      "type": "text",
      "file": "be_f02_2.png",
      "source_text": "了",
      "text": "끝",
      "fill": "#303030FF",
      "weight": "Regular",
      "stroke": null,
      "stroke_width": 0,
      "render": {
        "Minguk": {
          "x": 557,
          "y": 404,
          "size": 39,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 556,
          "y": 404,
          "size": 40,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 558,
          "y": 406,
          "size": 39,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 559,
          "y": 404,
          "size": 40,
          "tracking": 0
        }
      }
    },
    {
      "id": "be_l01_1.1",
      "type": "text",
      "file": "be_l01_1.png",
      "source_text": "遠い記憶",
      "text": "아득한 기억",
      "fill": "#F4F4EEFF",
      "weight": "Regular",
      "stroke": null,
      "stroke_width": 0,
      "render": {
        "Minguk": {
          "x": 268,
          "y": 219,
          "size": 21,
          "tracking": 1
        },
        "경기천년바탕": {
          "x": 269,
          "y": 219,
          "size": 21,
          "tracking": 1
        },
        "강원교육모두체": {
          "x": 270,
          "y": 219,
          "size": 23,
          "tracking": 1
        },
        "교보손글씨 2020 박도연": {
          "x": 273,
          "y": 219,
          "size": 21,
          "tracking": 1
        }
      }
    },
    {
      "id": "be_l01_2.1",
      "type": "text",
      "file": "be_l01_2.png",
      "source_text": "遠い記憶",
      "text": "아득한 기억",
      "fill": "#F4F4EEFF",
      "weight": "Regular",
      "stroke": null,
      "stroke_width": 0,
      "render": {
        "Minguk": {
          "x": 268,
          "y": 219,
          "size": 21,
          "tracking": 1
        },
        "경기천년바탕": {
          "x": 269,
          "y": 219,
          "size": 21,
          "tracking": 1
        },
        "강원교육모두체": {
          "x": 270,
          "y": 219,
          "size": 23,
          "tracking": 1
        },
        "교보손글씨 2020 박도연": {
          "x": 273,
          "y": 219,
          "size": 21,
          "tracking": 1
        }
      }
    },
    {
      "id": "be_l01_2.2",
      "type": "text",
      "file": "be_l01_2.png",
      "source_text": "了",
      "text": "끝",
      "fill": "#F4F4EEFF",
      "weight": "Regular",
      "stroke": null,
      "stroke_width": 0,
      "render": {
        "Minguk": {
          "x": 546,
          "y": 393,
          "size": 39,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 546,
          "y": 393,
          "size": 40,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 548,
          "y": 396,
          "size": 39,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 548,
          "y": 393,
          "size": 40,
          "tracking": 0
        }
      }
    },
    {
      "id": "be_l02_1.1",
      "type": "text",
      "file": "be_l02_1.png",
      "source_text": "さよなら",
      "text": "안녕",
      "fill": "#F4F4EEFF",
      "weight": "Regular",
      "stroke": null,
      "stroke_width": 0,
      "render": {
        "Minguk": {
          "x": 304,
          "y": 220,
          "size": 18,
          "tracking": 1
        },
        "경기천년바탕": {
          "x": 304,
          "y": 220,
          "size": 19,
          "tracking": 1
        },
        "강원교육모두체": {
          "x": 304,
          "y": 220,
          "size": 21,
          "tracking": 1
        },
        "교보손글씨 2020 박도연": {
          "x": 306,
          "y": 220,
          "size": 18,
          "tracking": 1
        }
      }
    },
    {
      "id": "be_l02_2.1",
      "type": "text",
      "file": "be_l02_2.png",
      "source_text": "さよなら",
      "text": "안녕",
      "fill": "#F4F4EEFF",
      "weight": "Regular",
      "stroke": null,
      "stroke_width": 0,
      "render": {
        "Minguk": {
          "x": 304,
          "y": 220,
          "size": 18,
          "tracking": 1
        },
        "경기천년바탕": {
          "x": 304,
          "y": 220,
          "size": 19,
          "tracking": 1
        },
        "강원교육모두체": {
          "x": 304,
          "y": 220,
          "size": 21,
          "tracking": 1
        },
        "교보손글씨 2020 박도연": {
          "x": 306,
          "y": 220,
          "size": 18,
          "tracking": 1
        }
      }
    },
    {
      "id": "be_l02_2.2",
      "type": "text",
      "file": "be_l02_2.png",
      "source_text": "了",
      "text": "끝",
      "fill": "#F4F4EEFF",
      "weight": "Regular",
      "stroke": null,
      "stroke_width": 0,
      "render": {
        "Minguk": {
          "x": 546,
          "y": 393,
          "size": 39,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 546,
          "y": 393,
          "size": 40,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 548,
          "y": 396,
          "size": 39,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 548,
          "y": 393,
          "size": 40,
          "tracking": 0
        }
      }
    },
    {
      "id": "be_l03_1.1",
      "type": "text",
      "file": "be_l03_1.png",
      "source_text": "ずっと、この場所で",
      "text": "계속, 이곳에서",
      "fill": "#F4F4EEFF",
      "weight": "Regular",
      "stroke": null,
      "stroke_width": 0,
      "render": {
        "Minguk": {
          "x": 262,
          "y": 220,
          "size": 19,
          "tracking": 1
        },
        "경기천년바탕": {
          "x": 261,
          "y": 220,
          "size": 19,
          "tracking": 1
        },
        "강원교육모두체": {
          "x": 262,
          "y": 220,
          "size": 21,
          "tracking": 1
        },
        "교보손글씨 2020 박도연": {
          "x": 267,
          "y": 220,
          "size": 19,
          "tracking": 1
        }
      }
    },
    {
      "id": "be_l03_2.1",
      "type": "text",
      "file": "be_l03_2.png",
      "source_text": "ずっと、この場所で",
      "text": "계속, 이곳에서",
      "fill": "#F4F4EEFF",
      "weight": "Regular",
      "stroke": null,
      "stroke_width": 0,
      "render": {
        "Minguk": {
          "x": 262,
          "y": 220,
          "size": 19,
          "tracking": 1
        },
        "경기천년바탕": {
          "x": 261,
          "y": 220,
          "size": 19,
          "tracking": 1
        },
        "강원교육모두체": {
          "x": 262,
          "y": 220,
          "size": 21,
          "tracking": 1
        },
        "교보손글씨 2020 박도연": {
          "x": 267,
          "y": 220,
          "size": 19,
          "tracking": 1
        }
      }
    },
    {
      "id": "be_l03_2.2",
      "type": "text",
      "file": "be_l03_2.png",
      "source_text": "了",
      "text": "끝",
      "fill": "#F4F4EEFF",
      "weight": "Regular",
      "stroke": null,
      "stroke_width": 0,
      "render": {
        "Minguk": {
          "x": 546,
          "y": 393,
          "size": 39,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 546,
          "y": 393,
          "size": 40,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 548,
          "y": 396,
          "size": 39,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 548,
          "y": 393,
          "size": 40,
          "tracking": 0
        }
      }
    },
    {
      "id": "be_r02_1.1",
      "type": "text",
      "file": "be_r02_1.png",
      "source_text": "ただひとつの望み",
      "text": "단 하나의 소망",
      "fill": "#F4F4EEFF",
      "weight": "Regular",
      "stroke": null,
      "stroke_width": 0,
      "render": {
        "Minguk": {
          "x": 259,
          "y": 220,
          "size": 19,
          "tracking": 1
        },
        "경기천년바탕": {
          "x": 256,
          "y": 220,
          "size": 20,
          "tracking": 1
        },
        "강원교육모두체": {
          "x": 257,
          "y": 220,
          "size": 22,
          "tracking": 1
        },
        "교보손글씨 2020 박도연": {
          "x": 262,
          "y": 220,
          "size": 20,
          "tracking": 1
        }
      }
    },
    {
      "id": "be_r02_2.1",
      "type": "text",
      "file": "be_r02_2.png",
      "source_text": "ただひとつの望み",
      "text": "단 하나의 소망",
      "fill": "#F4F4EEFF",
      "weight": "Regular",
      "stroke": null,
      "stroke_width": 0,
      "render": {
        "Minguk": {
          "x": 259,
          "y": 220,
          "size": 19,
          "tracking": 1
        },
        "경기천년바탕": {
          "x": 256,
          "y": 220,
          "size": 20,
          "tracking": 1
        },
        "강원교육모두체": {
          "x": 257,
          "y": 220,
          "size": 22,
          "tracking": 1
        },
        "교보손글씨 2020 박도연": {
          "x": 262,
          "y": 220,
          "size": 20,
          "tracking": 1
        }
      }
    },
    {
      "id": "be_r02_2.2",
      "type": "text",
      "file": "be_r02_2.png",
      "source_text": "了",
      "text": "끝",
      "fill": "#F4F4EEFF",
      "weight": "Regular",
      "stroke": null,
      "stroke_width": 0,
      "render": {
        "Minguk": {
          "x": 546,
          "y": 393,
          "size": 39,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 546,
          "y": 393,
          "size": 40,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 548,
          "y": 396,
          "size": 39,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 548,
          "y": 393,
          "size": 40,
          "tracking": 0
        }
      }
    },
    {
      "id": "cg_background_etc.1",
      "type": "text",
      "file": "cg_background_etc.png",
      "source_text": "その他",
      "text": "기타",
      "fill": "#F7F7F0FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 2,
      "render": {
        "Minguk": {
          "x": 41,
          "y": 38,
          "size": 37,
          "tracking": 1
        },
        "경기천년바탕": {
          "x": 41,
          "y": 38,
          "size": 36,
          "tracking": 1
        },
        "강원교육모두체": {
          "x": 41,
          "y": 38,
          "size": 40,
          "tracking": 1
        },
        "교보손글씨 2020 박도연": {
          "x": 41,
          "y": 38,
          "size": 37,
          "tracking": 1
        }
      }
    },
    {
      "id": "cg_background_hakkan.1",
      "type": "text",
      "file": "cg_background_hakkan.png",
      "source_text": "ハッカン",
      "text": "핫칸",
      "fill": "#F7F7F0FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 2,
      "render": {
        "Minguk": {
          "x": 40,
          "y": 40,
          "size": 34,
          "tracking": 1
        },
        "경기천년바탕": {
          "x": 40,
          "y": 40,
          "size": 33,
          "tracking": 1
        },
        "강원교육모두체": {
          "x": 40,
          "y": 40,
          "size": 38,
          "tracking": 1
        },
        "교보손글씨 2020 박도연": {
          "x": 40,
          "y": 40,
          "size": 35,
          "tracking": 1
        }
      }
    },
    {
      "id": "cg_background_hukamachi.1",
      "type": "text",
      "file": "cg_background_hukamachi.png",
      "source_text": "深町 康哉",
      "text": "후카마치 야스나리",
      "fill": "#F7F7F0FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 2,
      "render": {
        "Minguk": {
          "x": 41,
          "y": 38,
          "size": 36,
          "tracking": 1
        },
        "경기천년바탕": {
          "x": 41,
          "y": 38,
          "size": 35,
          "tracking": 1
        },
        "강원교육모두체": {
          "x": 41,
          "y": 38,
          "size": 40,
          "tracking": 1
        },
        "교보손글씨 2020 박도연": {
          "x": 41,
          "y": 38,
          "size": 37,
          "tracking": 1
        }
      }
    },
    {
      "id": "cg_background_ikaru.1",
      "type": "text",
      "file": "cg_background_ikaru.png",
      "source_text": "イカル",
      "text": "이카루",
      "fill": "#F7F7F0FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 2,
      "render": {
        "Minguk": {
          "x": 40,
          "y": 40,
          "size": 33,
          "tracking": 1
        },
        "경기천년바탕": {
          "x": 40,
          "y": 40,
          "size": 33,
          "tracking": 1
        },
        "강원교육모두체": {
          "x": 40,
          "y": 40,
          "size": 37,
          "tracking": 1
        },
        "교보손글씨 2020 박도연": {
          "x": 40,
          "y": 40,
          "size": 33,
          "tracking": 1
        }
      }
    },
    {
      "id": "cg_background_manabe.1",
      "type": "text",
      "file": "cg_background_manabe.png",
      "source_text": "真部 章仁",
      "text": "마나베 아키히토",
      "fill": "#F7F7F0FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 2,
      "render": {
        "Minguk": {
          "x": 41,
          "y": 38,
          "size": 38,
          "tracking": 1
        },
        "경기천년바탕": {
          "x": 41,
          "y": 38,
          "size": 37,
          "tracking": 1
        },
        "강원교육모두체": {
          "x": 41,
          "y": 38,
          "size": 40,
          "tracking": 1
        },
        "교보손글씨 2020 박도연": {
          "x": 41,
          "y": 38,
          "size": 37,
          "tracking": 1
        }
      }
    },
    {
      "id": "cg_background_renjaku.1",
      "type": "text",
      "file": "cg_background_renjaku.png",
      "source_text": "レンジャク",
      "text": "렌자크",
      "fill": "#F7F7F0FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 2,
      "render": {
        "Minguk": {
          "x": 40,
          "y": 40,
          "size": 34,
          "tracking": 1
        },
        "경기천년바탕": {
          "x": 40,
          "y": 40,
          "size": 34,
          "tracking": 1
        },
        "강원교육모두체": {
          "x": 40,
          "y": 40,
          "size": 38,
          "tracking": 1
        },
        "교보손글씨 2020 박도연": {
          "x": 40,
          "y": 40,
          "size": 33,
          "tracking": 1
        }
      }
    },
    {
      "id": "cg_background_ruu.1",
      "type": "text",
      "file": "cg_background_ruu.png",
      "source_text": "綿貫 琉宇",
      "text": "와타누키 루우",
      "fill": "#F7F7F0FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 2,
      "render": {
        "Minguk": {
          "x": 40,
          "y": 38,
          "size": 37,
          "tracking": 1
        },
        "경기천년바탕": {
          "x": 40,
          "y": 38,
          "size": 36,
          "tracking": 1
        },
        "강원교육모두체": {
          "x": 40,
          "y": 38,
          "size": 40,
          "tracking": 1
        },
        "교보손글씨 2020 박도연": {
          "x": 40,
          "y": 38,
          "size": 37,
          "tracking": 1
        }
      }
    },
    {
      "id": "cgtop_background.1",
      "type": "text",
      "file": "cgtop_background.png",
      "source_text": "CG 鑑賞モード",
      "text": "CG 감상 모드",
      "fill": "#F7F7F0FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 2,
      "render": {
        "Minguk": {
          "x": 40,
          "y": 38,
          "size": 35,
          "tracking": 1
        },
        "경기천년바탕": {
          "x": 40,
          "y": 38,
          "size": 35,
          "tracking": 1
        },
        "강원교육모두체": {
          "x": 40,
          "y": 38,
          "size": 40,
          "tracking": 1
        },
        "교보손글씨 2020 박도연": {
          "x": 40,
          "y": 38,
          "size": 36,
          "tracking": 1
        }
      }
    },
    {
      "id": "cgtop_back_off.1",
      "type": "text",
      "file": "cgtop_back_off.png",
      "source_text": "前ページ",
      "text": "이전 페이지",
      "fill": "#F7F7F1FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 0,
          "y": 6,
          "size": 20,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 2,
          "y": 6,
          "size": 20,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 1,
          "y": 6,
          "size": 23,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 0,
          "y": 6,
          "size": 22,
          "tracking": 0
        }
      }
    },
    {
      "id": "cgtop_back_on.1",
      "type": "text",
      "file": "cgtop_back_on.png",
      "source_text": "前ページ",
      "text": "이전 페이지",
      "fill": "#E83E44FF",
      "weight": "Regular",
      "stroke": "#FFFAF5FF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 0,
          "y": 6,
          "size": 20,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 2,
          "y": 6,
          "size": 20,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 1,
          "y": 6,
          "size": 23,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 0,
          "y": 6,
          "size": 22,
          "tracking": 0
        }
      }
    },
    {
      "id": "cgtop_next_off.1",
      "type": "text",
      "file": "cgtop_next_off.png",
      "source_text": "次ページ",
      "text": "다음 페이지",
      "fill": "#F7F7F1FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 0,
          "y": 4,
          "size": 20,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 2,
          "y": 4,
          "size": 20,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 0,
          "y": 4,
          "size": 23,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 2,
          "y": 4,
          "size": 21,
          "tracking": 0
        }
      }
    },
    {
      "id": "cgtop_next_on.1",
      "type": "text",
      "file": "cgtop_next_on.png",
      "source_text": "次ページ",
      "text": "다음 페이지",
      "fill": "#E83E44FF",
      "weight": "Regular",
      "stroke": "#FFFAF5FF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 0,
          "y": 4,
          "size": 20,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 2,
          "y": 4,
          "size": 20,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 0,
          "y": 4,
          "size": 23,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 2,
          "y": 4,
          "size": 21,
          "tracking": 0
        }
      }
    },
    {
      "id": "cgtop_title_off.1",
      "type": "text",
      "file": "cgtop_title_off.png",
      "source_text": "戻る",
      "text": "뒤로",
      "fill": "#F7F7F1FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 0,
          "y": 3,
          "size": 24,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 0,
          "y": 4,
          "size": 23,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 0,
          "y": 2,
          "size": 28,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 0,
          "y": 2,
          "size": 27,
          "tracking": 0
        }
      }
    },
    {
      "id": "cgtop_title_on.1",
      "type": "text",
      "file": "cgtop_title_on.png",
      "source_text": "戻る",
      "text": "뒤로",
      "fill": "#E83E44FF",
      "weight": "Regular",
      "stroke": "#FFFAF5FF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 0,
          "y": 3,
          "size": 24,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 0,
          "y": 4,
          "size": 23,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 0,
          "y": 2,
          "size": 28,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 0,
          "y": 2,
          "size": 27,
          "tracking": 0
        }
      }
    },
    {
      "id": "config_bg.1",
      "type": "text",
      "file": "config_bg.png",
      "source_text": "環境設定",
      "text": "환경 설정",
      "fill": "#F7F7F0FF",
      "weight": "Bold",
      "stroke": "#050505FF",
      "stroke_width": 2,
      "render": {
        "Minguk": {
          "x": 266,
          "y": 36,
          "size": 27,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 267,
          "y": 36,
          "size": 27,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 267,
          "y": 36,
          "size": 31,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 271,
          "y": 36,
          "size": 28,
          "tracking": 0
        }
      }
    },
    {
      "id": "config_bg.2",
      "type": "text",
      "file": "config_bg.png",
      "source_text": "文字の設定",
      "text": "문자 설정",
      "fill": "#F7F7F0FF",
      "weight": "Bold",
      "stroke": "#050505FF",
      "stroke_width": 2,
      "render": {
        "Minguk": {
          "x": 90,
          "y": 66,
          "size": 21,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 90,
          "y": 66,
          "size": 21,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 90,
          "y": 66,
          "size": 23,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 90,
          "y": 66,
          "size": 22,
          "tracking": 0
        }
      }
    },
    {
      "id": "config_bg.3",
      "type": "text",
      "file": "config_bg.png",
      "source_text": "表示速度",
      "text": "표시 속도",
      "fill": "#F7F7F0FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 2,
      "render": {
        "Minguk": {
          "x": 102,
          "y": 101,
          "size": 18,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 102,
          "y": 101,
          "size": 18,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 102,
          "y": 101,
          "size": 20,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 102,
          "y": 101,
          "size": 18,
          "tracking": 0
        }
      }
    },
    {
      "id": "config_bg.4",
      "type": "text",
      "file": "config_bg.png",
      "source_text": "オートモード待ち時間",
      "text": "자동 모드 대기 시간",
      "fill": "#F7F7F0FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 2,
      "render": {
        "Minguk": {
          "x": 103,
          "y": 127,
          "size": 18,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 103,
          "y": 127,
          "size": 18,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 103,
          "y": 127,
          "size": 20,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 103,
          "y": 128,
          "size": 18,
          "tracking": 0
        }
      }
    },
    {
      "id": "config_bg.5",
      "type": "text",
      "file": "config_bg.png",
      "source_text": "文字描画方法",
      "text": "문자 표시 방식",
      "fill": "#F7F7F0FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 2,
      "render": {
        "Minguk": {
          "x": 103,
          "y": 153,
          "size": 18,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 103,
          "y": 153,
          "size": 18,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 103,
          "y": 153,
          "size": 20,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 103,
          "y": 153,
          "size": 18,
          "tracking": 0
        }
      }
    },
    {
      "id": "config_bg.6",
      "type": "text",
      "file": "config_bg.png",
      "source_text": "フォント",
      "text": "글꼴",
      "fill": "#F7F7F0FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 2,
      "render": {
        "Minguk": {
          "x": 104,
          "y": 180,
          "size": 18,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 104,
          "y": 180,
          "size": 18,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 104,
          "y": 180,
          "size": 20,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 104,
          "y": 180,
          "size": 18,
          "tracking": 0
        }
      }
    },
    {
      "id": "config_bg.7",
      "type": "text",
      "file": "config_bg.png",
      "source_text": "サンプルテキスト",
      "text": "예시 문장",
      "fill": "#F7F7F0FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 2,
      "render": {
        "Minguk": {
          "x": 103,
          "y": 207,
          "size": 12,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 103,
          "y": 207,
          "size": 11,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 103,
          "y": 207,
          "size": 14,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 103,
          "y": 207,
          "size": 12,
          "tracking": 0
        }
      }
    },
    {
      "id": "config_bg.8",
      "type": "text",
      "file": "config_bg.png",
      "source_text": "遅",
      "text": "느림",
      "fill": "#F7F7F0FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 2,
      "render": {
        "Minguk": {
          "x": 312,
          "y": 102,
          "size": 17,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 314,
          "y": 102,
          "size": 16,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 312,
          "y": 102,
          "size": 19,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 315,
          "y": 102,
          "size": 17,
          "tracking": 0
        }
      }
    },
    {
      "id": "config_bg.9",
      "type": "text",
      "file": "config_bg.png",
      "source_text": "速",
      "text": "빠름",
      "fill": "#F7F7F0FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 2,
      "render": {
        "Minguk": {
          "x": 516,
          "y": 102,
          "size": 17,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 516,
          "y": 102,
          "size": 16,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 516,
          "y": 102,
          "size": 19,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 516,
          "y": 102,
          "size": 17,
          "tracking": 0
        }
      }
    },
    {
      "id": "config_bg.10",
      "type": "text",
      "file": "config_bg.png",
      "source_text": "短",
      "text": "짧게",
      "fill": "#F7F7F0FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 2,
      "render": {
        "Minguk": {
          "x": 311,
          "y": 128,
          "size": 17,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 311,
          "y": 128,
          "size": 16,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 310,
          "y": 128,
          "size": 19,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 313,
          "y": 128,
          "size": 17,
          "tracking": 0
        }
      }
    },
    {
      "id": "config_bg.11",
      "type": "text",
      "file": "config_bg.png",
      "source_text": "長",
      "text": "길게",
      "fill": "#F7F7F0FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 2,
      "render": {
        "Minguk": {
          "x": 517,
          "y": 128,
          "size": 17,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 517,
          "y": 128,
          "size": 16,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 517,
          "y": 128,
          "size": 19,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 517,
          "y": 128,
          "size": 17,
          "tracking": 0
        }
      }
    },
    {
      "id": "config_bg.12",
      "type": "text",
      "file": "config_bg.png",
      "source_text": "音の設定",
      "text": "음향 설정",
      "fill": "#F7F7F0FF",
      "weight": "Bold",
      "stroke": "#050505FF",
      "stroke_width": 2,
      "render": {
        "Minguk": {
          "x": 90,
          "y": 303,
          "size": 21,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 90,
          "y": 303,
          "size": 21,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 90,
          "y": 303,
          "size": 23,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 90,
          "y": 304,
          "size": 22,
          "tracking": 0
        }
      }
    },
    {
      "id": "config_bg.13",
      "type": "text",
      "file": "config_bg.png",
      "source_text": "BGM",
      "text": "배경 음악",
      "fill": "#F7F7F0FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 2,
      "render": {
        "Minguk": {
          "x": 105,
          "y": 337,
          "size": 18,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 105,
          "y": 337,
          "size": 18,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 105,
          "y": 337,
          "size": 20,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 105,
          "y": 336,
          "size": 18,
          "tracking": 0
        }
      }
    },
    {
      "id": "config_bg.14",
      "type": "text",
      "file": "config_bg.png",
      "source_text": "効果音",
      "text": "효과음",
      "fill": "#F7F7F0FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 2,
      "render": {
        "Minguk": {
          "x": 103,
          "y": 363,
          "size": 18,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 103,
          "y": 363,
          "size": 18,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 103,
          "y": 363,
          "size": 20,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 103,
          "y": 363,
          "size": 18,
          "tracking": 0
        }
      }
    },
    {
      "id": "config_bg.15",
      "type": "text",
      "file": "config_bg.png",
      "source_text": "音声",
      "text": "음성",
      "fill": "#F7F7F0FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 2,
      "render": {
        "Minguk": {
          "x": 102,
          "y": 389,
          "size": 18,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 102,
          "y": 389,
          "size": 18,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 102,
          "y": 389,
          "size": 20,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 102,
          "y": 389,
          "size": 18,
          "tracking": 0
        }
      }
    },
    {
      "id": "config_bg.16",
      "type": "text",
      "file": "config_bg.png",
      "source_text": "小",
      "text": "작게",
      "fill": "#F7F7F0FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 2,
      "render": {
        "Minguk": {
          "x": 311,
          "y": 338,
          "size": 17,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 312,
          "y": 338,
          "size": 16,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 312,
          "y": 338,
          "size": 19,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 313,
          "y": 338,
          "size": 17,
          "tracking": 0
        }
      }
    },
    {
      "id": "config_bg.17",
      "type": "text",
      "file": "config_bg.png",
      "source_text": "大",
      "text": "크게",
      "fill": "#F7F7F0FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 2,
      "render": {
        "Minguk": {
          "x": 517,
          "y": 338,
          "size": 17,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 517,
          "y": 339,
          "size": 16,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 517,
          "y": 339,
          "size": 19,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 517,
          "y": 338,
          "size": 17,
          "tracking": 0
        }
      }
    },
    {
      "id": "config_bg.18",
      "type": "text",
      "file": "config_bg.png",
      "source_text": "小",
      "text": "작게",
      "fill": "#F7F7F0FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 2,
      "render": {
        "Minguk": {
          "x": 311,
          "y": 364,
          "size": 17,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 312,
          "y": 364,
          "size": 16,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 312,
          "y": 364,
          "size": 19,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 313,
          "y": 364,
          "size": 17,
          "tracking": 0
        }
      }
    },
    {
      "id": "config_bg.19",
      "type": "text",
      "file": "config_bg.png",
      "source_text": "大",
      "text": "크게",
      "fill": "#F7F7F0FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 2,
      "render": {
        "Minguk": {
          "x": 517,
          "y": 365,
          "size": 17,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 517,
          "y": 366,
          "size": 16,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 517,
          "y": 366,
          "size": 19,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 517,
          "y": 365,
          "size": 17,
          "tracking": 0
        }
      }
    },
    {
      "id": "config_bg.20",
      "type": "text",
      "file": "config_bg.png",
      "source_text": "小",
      "text": "작게",
      "fill": "#F7F7F0FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 2,
      "render": {
        "Minguk": {
          "x": 311,
          "y": 390,
          "size": 17,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 312,
          "y": 390,
          "size": 16,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 312,
          "y": 390,
          "size": 19,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 313,
          "y": 390,
          "size": 17,
          "tracking": 0
        }
      }
    },
    {
      "id": "config_bg.21",
      "type": "text",
      "file": "config_bg.png",
      "source_text": "大",
      "text": "크게",
      "fill": "#F7F7F0FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 2,
      "render": {
        "Minguk": {
          "x": 517,
          "y": 392,
          "size": 17,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 517,
          "y": 392,
          "size": 16,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 517,
          "y": 392,
          "size": 19,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 517,
          "y": 392,
          "size": 17,
          "tracking": 0
        }
      }
    },
    {
      "id": "config_anti_off.1",
      "type": "text",
      "file": "config_anti_off.png",
      "source_text": "アンチエイリアス",
      "text": "안티앨리어싱",
      "fill": "#F7F7F1FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 24,
          "y": 0,
          "size": 19,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 22,
          "y": 0,
          "size": 20,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 25,
          "y": 0,
          "size": 22,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 28,
          "y": 0,
          "size": 20,
          "tracking": 0
        }
      }
    },
    {
      "id": "config_anti_on.1",
      "type": "text",
      "file": "config_anti_on.png",
      "source_text": "アンチエイリアス",
      "text": "안티앨리어싱",
      "fill": "#E83E44FF",
      "weight": "Regular",
      "stroke": "#FFFAF5FF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 24,
          "y": 0,
          "size": 19,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 22,
          "y": 0,
          "size": 20,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 25,
          "y": 0,
          "size": 22,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 28,
          "y": 0,
          "size": 20,
          "tracking": 0
        }
      }
    },
    {
      "id": "config_anti_select.1",
      "type": "text",
      "file": "config_anti_select.png",
      "source_text": "アンチエイリアス",
      "text": "안티앨리어싱",
      "fill": "#D41C22FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 24,
          "y": 0,
          "size": 19,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 22,
          "y": 0,
          "size": 20,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 25,
          "y": 0,
          "size": 22,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 28,
          "y": 0,
          "size": 20,
          "tracking": 0
        }
      }
    },
    {
      "id": "config_back_off.1",
      "type": "text",
      "file": "config_back_off.png",
      "source_text": "戻る",
      "text": "뒤로",
      "fill": "#F7F7F1FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 0,
          "y": 1,
          "size": 20,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 0,
          "y": 2,
          "size": 19,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 0,
          "y": 1,
          "size": 23,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 0,
          "y": 0,
          "size": 22,
          "tracking": 0
        }
      }
    },
    {
      "id": "config_back_on.1",
      "type": "text",
      "file": "config_back_on.png",
      "source_text": "戻る",
      "text": "뒤로",
      "fill": "#E83E44FF",
      "weight": "Regular",
      "stroke": "#FFFAF5FF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 0,
          "y": 1,
          "size": 20,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 0,
          "y": 2,
          "size": 19,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 0,
          "y": 1,
          "size": 23,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 0,
          "y": 0,
          "size": 22,
          "tracking": 0
        }
      }
    },
    {
      "id": "config_hyoujun_off.1",
      "type": "text",
      "file": "config_hyoujun_off.png",
      "source_text": "標準",
      "text": "기본",
      "fill": "#F7F7F1FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 0,
          "y": 1,
          "size": 21,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 0,
          "y": 1,
          "size": 20,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 0,
          "y": 1,
          "size": 23,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 1,
          "y": 0,
          "size": 23,
          "tracking": 0
        }
      }
    },
    {
      "id": "config_hyoujun_on.1",
      "type": "text",
      "file": "config_hyoujun_on.png",
      "source_text": "標準",
      "text": "기본",
      "fill": "#E83E44FF",
      "weight": "Regular",
      "stroke": "#FFFAF5FF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 0,
          "y": 1,
          "size": 21,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 0,
          "y": 1,
          "size": 20,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 0,
          "y": 1,
          "size": 23,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 1,
          "y": 0,
          "size": 23,
          "tracking": 0
        }
      }
    },
    {
      "id": "config_hyoujun_select.1",
      "type": "text",
      "file": "config_hyoujun_select.png",
      "source_text": "標準",
      "text": "기본",
      "fill": "#D41C22FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 0,
          "y": 1,
          "size": 21,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 0,
          "y": 1,
          "size": 20,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 0,
          "y": 1,
          "size": 23,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 1,
          "y": 0,
          "size": 23,
          "tracking": 0
        }
      }
    },
    {
      "id": "config_off_off.1",
      "type": "text",
      "file": "config_off_off.png",
      "source_text": "OFF",
      "text": "OFF",
      "fill": "#F7F7F1FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 0,
          "y": 2,
          "size": 17,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 0,
          "y": 2,
          "size": 17,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 0,
          "y": 2,
          "size": 22,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 0,
          "y": 2,
          "size": 17,
          "tracking": 0
        }
      }
    },
    {
      "id": "config_off_on.1",
      "type": "text",
      "file": "config_off_on.png",
      "source_text": "OFF",
      "text": "OFF",
      "fill": "#E83E44FF",
      "weight": "Regular",
      "stroke": "#FFFAF5FF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 0,
          "y": 2,
          "size": 17,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 0,
          "y": 2,
          "size": 17,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 0,
          "y": 2,
          "size": 22,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 0,
          "y": 2,
          "size": 17,
          "tracking": 0
        }
      }
    },
    {
      "id": "config_off_select.1",
      "type": "text",
      "file": "config_off_select.png",
      "source_text": "OFF",
      "text": "OFF",
      "fill": "#D41C22FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 0,
          "y": 2,
          "size": 17,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 0,
          "y": 2,
          "size": 17,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 0,
          "y": 2,
          "size": 22,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 0,
          "y": 2,
          "size": 17,
          "tracking": 0
        }
      }
    },
    {
      "id": "config_on_off.1",
      "type": "text",
      "file": "config_on_off.png",
      "source_text": "ON",
      "text": "ON",
      "fill": "#E83E44FF",
      "weight": "Regular",
      "stroke": "#FFFAF5FF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 0,
          "y": 2,
          "size": 18,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 0,
          "y": 2,
          "size": 17,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 0,
          "y": 2,
          "size": 23,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 0,
          "y": 2,
          "size": 18,
          "tracking": 0
        }
      }
    },
    {
      "id": "config_on_on.1",
      "type": "text",
      "file": "config_on_on.png",
      "source_text": "ON",
      "text": "ON",
      "fill": "#E83E44FF",
      "weight": "Regular",
      "stroke": "#FFFAF5FF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 0,
          "y": 2,
          "size": 18,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 0,
          "y": 2,
          "size": 17,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 0,
          "y": 2,
          "size": 23,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 0,
          "y": 2,
          "size": 18,
          "tracking": 0
        }
      }
    },
    {
      "id": "config_on_select.1",
      "type": "text",
      "file": "config_on_select.png",
      "source_text": "ON",
      "text": "ON",
      "fill": "#D41C22FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 0,
          "y": 2,
          "size": 18,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 0,
          "y": 2,
          "size": 17,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 0,
          "y": 2,
          "size": 23,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 0,
          "y": 2,
          "size": 18,
          "tracking": 0
        }
      }
    },
    {
      "id": "config_syuuryou_off.1",
      "type": "text",
      "file": "config_syuuryou_off.png",
      "source_text": "ゲームを終了する",
      "text": "게임 종료",
      "fill": "#F7F7F1FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 27,
          "y": 0,
          "size": 24,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 27,
          "y": 0,
          "size": 24,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 30,
          "y": 0,
          "size": 26,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 32,
          "y": 0,
          "size": 24,
          "tracking": 0
        }
      }
    },
    {
      "id": "config_syuuryou_on.1",
      "type": "text",
      "file": "config_syuuryou_on.png",
      "source_text": "ゲームを終了する",
      "text": "게임 종료",
      "fill": "#E83E44FF",
      "weight": "Regular",
      "stroke": "#FFFAF5FF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 27,
          "y": 0,
          "size": 24,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 27,
          "y": 0,
          "size": 24,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 30,
          "y": 0,
          "size": 26,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 32,
          "y": 0,
          "size": 24,
          "tracking": 0
        }
      }
    },
    {
      "id": "config_title_off.1",
      "type": "text",
      "file": "config_title_off.png",
      "source_text": "タイトルに戻る",
      "text": "타이틀로",
      "fill": "#F7F7F1FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 25,
          "y": 0,
          "size": 22,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 26,
          "y": 0,
          "size": 22,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 28,
          "y": 0,
          "size": 24,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 30,
          "y": 0,
          "size": 23,
          "tracking": 0
        }
      }
    },
    {
      "id": "config_title_on.1",
      "type": "text",
      "file": "config_title_on.png",
      "source_text": "タイトルに戻る",
      "text": "타이틀로",
      "fill": "#E83E44FF",
      "weight": "Regular",
      "stroke": "#FFFAF5FF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 25,
          "y": 0,
          "size": 22,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 26,
          "y": 0,
          "size": 22,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 28,
          "y": 0,
          "size": 24,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 30,
          "y": 0,
          "size": 23,
          "tracking": 0
        }
      }
    },
    {
      "id": "mu_background.1",
      "type": "text",
      "file": "mu_background.png",
      "source_text": "音楽鑑賞モード",
      "text": "음악 감상 모드",
      "fill": "#F7F7F0FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 2,
      "render": {
        "Minguk": {
          "x": 65,
          "y": 33,
          "size": 37,
          "tracking": 1
        },
        "경기천년바탕": {
          "x": 65,
          "y": 33,
          "size": 36,
          "tracking": 1
        },
        "강원교육모두체": {
          "x": 65,
          "y": 33,
          "size": 40,
          "tracking": 1
        },
        "교보손글씨 2020 박도연": {
          "x": 65,
          "y": 33,
          "size": 36,
          "tracking": 1
        }
      }
    },
    {
      "id": "mu_stop_off.1",
      "type": "text",
      "file": "mu_stop_off.png",
      "source_text": "音楽の停止",
      "text": "음악 정지",
      "fill": "#F7F7F1FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 2,
          "y": 1,
          "size": 24,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 2,
          "y": 1,
          "size": 24,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 5,
          "y": 1,
          "size": 26,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 7,
          "y": 1,
          "size": 24,
          "tracking": 0
        }
      }
    },
    {
      "id": "mu_stop_on.1",
      "type": "text",
      "file": "mu_stop_on.png",
      "source_text": "音楽の停止",
      "text": "음악 정지",
      "fill": "#FFFAF5FF",
      "weight": "Regular",
      "stroke": "#E83E44FF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 2,
          "y": 1,
          "size": 24,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 2,
          "y": 1,
          "size": 24,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 5,
          "y": 1,
          "size": 26,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 7,
          "y": 1,
          "size": 24,
          "tracking": 0
        }
      }
    },
    {
      "id": "mu_title_off.1",
      "type": "text",
      "file": "mu_title_off.png",
      "source_text": "戻る",
      "text": "뒤로",
      "fill": "#F7F7F1FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 0,
          "y": 2,
          "size": 19,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 0,
          "y": 2,
          "size": 19,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 0,
          "y": 2,
          "size": 21,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 0,
          "y": 2,
          "size": 21,
          "tracking": 0
        }
      }
    },
    {
      "id": "mu_title_on.1",
      "type": "text",
      "file": "mu_title_on.png",
      "source_text": "戻る",
      "text": "뒤로",
      "fill": "#FFFAF5FF",
      "weight": "Regular",
      "stroke": "#E83E44FF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 0,
          "y": 2,
          "size": 19,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 0,
          "y": 2,
          "size": 19,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 0,
          "y": 2,
          "size": 21,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 0,
          "y": 2,
          "size": 21,
          "tracking": 0
        }
      }
    },
    {
      "id": "sa_lo_back_off.1",
      "type": "text",
      "file": "sa_lo_back_off.png",
      "source_text": "戻る",
      "text": "돌아가기",
      "fill": "#F7F7F1FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 2,
          "y": 7,
          "size": 23,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 2,
          "y": 7,
          "size": 23,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 2,
          "y": 6,
          "size": 26,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 2,
          "y": 6,
          "size": 26,
          "tracking": 0
        }
      }
    },
    {
      "id": "sa_lo_back_on.1",
      "type": "text",
      "file": "sa_lo_back_on.png",
      "source_text": "戻る",
      "text": "돌아가기",
      "fill": "#FFFAF5FF",
      "weight": "Regular",
      "stroke": "#E83E44FF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 2,
          "y": 7,
          "size": 23,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 2,
          "y": 7,
          "size": 23,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 2,
          "y": 6,
          "size": 26,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 2,
          "y": 6,
          "size": 26,
          "tracking": 0
        }
      }
    },
    {
      "id": "sa_lo_load.1",
      "type": "text",
      "file": "sa_lo_load.png",
      "source_text": "ロード",
      "text": "불러오기",
      "fill": "#F7F7F1FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 7,
          "y": 4,
          "size": 30,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 8,
          "y": 4,
          "size": 30,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 8,
          "y": 4,
          "size": 34,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 12,
          "y": 4,
          "size": 31,
          "tracking": 0
        }
      }
    },
    {
      "id": "sa_lo_save.1",
      "type": "text",
      "file": "sa_lo_save.png",
      "source_text": "セーブ",
      "text": "저장",
      "fill": "#F7F7F1FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 31,
          "y": 1,
          "size": 33,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 31,
          "y": 1,
          "size": 33,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 32,
          "y": 1,
          "size": 38,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 34,
          "y": 1,
          "size": 34,
          "tracking": 0
        }
      }
    },
    {
      "id": "sc_maepage_off.1",
      "type": "text",
      "file": "sc_maepage_off.png",
      "source_text": "前ページ",
      "text": "이전 페이지",
      "fill": "#F7F7F1FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 0,
          "y": 6,
          "size": 20,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 2,
          "y": 6,
          "size": 20,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 1,
          "y": 6,
          "size": 23,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 0,
          "y": 6,
          "size": 22,
          "tracking": 0
        }
      }
    },
    {
      "id": "sc_maepage_on.1",
      "type": "text",
      "file": "sc_maepage_on.png",
      "source_text": "前ページ",
      "text": "이전 페이지",
      "fill": "#FFFAF5FF",
      "weight": "Regular",
      "stroke": "#E83E44FF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 0,
          "y": 6,
          "size": 20,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 2,
          "y": 6,
          "size": 20,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 1,
          "y": 6,
          "size": 23,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 0,
          "y": 6,
          "size": 22,
          "tracking": 0
        }
      }
    },
    {
      "id": "sc_title_off.1",
      "type": "text",
      "file": "sc_title_off.png",
      "source_text": "戻る",
      "text": "뒤로",
      "fill": "#F7F7F1FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 0,
          "y": 3,
          "size": 24,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 0,
          "y": 4,
          "size": 23,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 0,
          "y": 2,
          "size": 28,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 0,
          "y": 2,
          "size": 27,
          "tracking": 0
        }
      }
    },
    {
      "id": "sc_title_on.1",
      "type": "text",
      "file": "sc_title_on.png",
      "source_text": "戻る",
      "text": "뒤로",
      "fill": "#FFFAF5FF",
      "weight": "Regular",
      "stroke": "#E83E44FF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 0,
          "y": 3,
          "size": 24,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 0,
          "y": 4,
          "size": 23,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 0,
          "y": 2,
          "size": 28,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 0,
          "y": 2,
          "size": 27,
          "tracking": 0
        }
      }
    },
    {
      "id": "sc_tugipage_off.1",
      "type": "text",
      "file": "sc_tugipage_off.png",
      "source_text": "次ページ",
      "text": "다음 페이지",
      "fill": "#F7F7F1FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 0,
          "y": 4,
          "size": 20,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 2,
          "y": 4,
          "size": 20,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 0,
          "y": 4,
          "size": 23,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 2,
          "y": 4,
          "size": 21,
          "tracking": 0
        }
      }
    },
    {
      "id": "sc_tugipage_on.1",
      "type": "text",
      "file": "sc_tugipage_on.png",
      "source_text": "次ページ",
      "text": "다음 페이지",
      "fill": "#FFFAF5FF",
      "weight": "Regular",
      "stroke": "#E83E44FF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 0,
          "y": 4,
          "size": 20,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 2,
          "y": 4,
          "size": 20,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 0,
          "y": 4,
          "size": 23,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 2,
          "y": 4,
          "size": 21,
          "tracking": 0
        }
      }
    },
    {
      "id": "title_cg_off.1",
      "type": "text",
      "file": "title_cg_off.png",
      "source_text": "CG 鑑賞",
      "text": "CG 감상",
      "fill": "#F7F7F1FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 3,
      "render": {
        "Minguk": {
          "x": 7,
          "y": 3,
          "size": 26,
          "tracking": 11.2
        },
        "경기천년바탕": {
          "x": 7,
          "y": 2,
          "size": 26,
          "tracking": 11.0
        },
        "강원교육모두체": {
          "x": 8,
          "y": 4,
          "size": 26,
          "tracking": 13.7
        },
        "교보손글씨 2020 박도연": {
          "x": 7,
          "y": 4,
          "size": 26,
          "tracking": 13.5
        }
      }
    },
    {
      "id": "title_cg_on.1",
      "type": "text",
      "file": "title_cg_on.png",
      "source_text": "CG 鑑賞",
      "text": "CG 감상",
      "fill": "#FFFAF5FF",
      "weight": "Regular",
      "stroke": "#E83E44FF",
      "stroke_width": 2,
      "render": {
        "Minguk": {
          "x": 8,
          "y": 4,
          "size": 26,
          "tracking": 11.2
        },
        "경기천년바탕": {
          "x": 8,
          "y": 4,
          "size": 26,
          "tracking": 11.0
        },
        "강원교육모두체": {
          "x": 8,
          "y": 5,
          "size": 26,
          "tracking": 13.7
        },
        "교보손글씨 2020 박도연": {
          "x": 8,
          "y": 4,
          "size": 26,
          "tracking": 13.5
        }
      }
    },
    {
      "id": "title_config_off.1",
      "type": "text",
      "file": "title_config_off.png",
      "source_text": "設定",
      "text": "설정",
      "fill": "#F7F7F1FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 3,
      "render": {
        "Minguk": {
          "x": 5,
          "y": 2,
          "size": 26,
          "tracking": 91.0
        },
        "경기천년바탕": {
          "x": 5,
          "y": 2,
          "size": 26,
          "tracking": 91.1
        },
        "강원교육모두체": {
          "x": 5,
          "y": 4,
          "size": 26,
          "tracking": 99.0
        },
        "교보손글씨 2020 박도연": {
          "x": 5,
          "y": 3,
          "size": 26,
          "tracking": 95.1
        }
      }
    },
    {
      "id": "title_config_on.1",
      "type": "text",
      "file": "title_config_on.png",
      "source_text": "設定",
      "text": "설정",
      "fill": "#FFFAF5FF",
      "weight": "Regular",
      "stroke": "#E83E44FF",
      "stroke_width": 2,
      "render": {
        "Minguk": {
          "x": 6,
          "y": 4,
          "size": 26,
          "tracking": 91.0
        },
        "경기천년바탕": {
          "x": 6,
          "y": 3,
          "size": 26,
          "tracking": 91.1
        },
        "강원교육모두체": {
          "x": 6,
          "y": 4,
          "size": 26,
          "tracking": 99.0
        },
        "교보손글씨 2020 박도연": {
          "x": 6,
          "y": 4,
          "size": 26,
          "tracking": 95.1
        }
      }
    },
    {
      "id": "title_end_off.1",
      "type": "text",
      "file": "title_end_off.png",
      "source_text": "終了",
      "text": "종료",
      "fill": "#F7F7F1FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 3,
      "render": {
        "Minguk": {
          "x": 27,
          "y": 2,
          "size": 26,
          "tracking": 43.0
        },
        "경기천년바탕": {
          "x": 27,
          "y": 2,
          "size": 26,
          "tracking": 41.1
        },
        "강원교육모두체": {
          "x": 27,
          "y": 4,
          "size": 26,
          "tracking": 47.1
        },
        "교보손글씨 2020 박도연": {
          "x": 27,
          "y": 4,
          "size": 26,
          "tracking": 49.0
        }
      }
    },
    {
      "id": "title_end_on.1",
      "type": "text",
      "file": "title_end_on.png",
      "source_text": "終了",
      "text": "종료",
      "fill": "#FFFAF5FF",
      "weight": "Regular",
      "stroke": "#E83E44FF",
      "stroke_width": 2,
      "render": {
        "Minguk": {
          "x": 28,
          "y": 4,
          "size": 26,
          "tracking": 43.0
        },
        "경기천년바탕": {
          "x": 28,
          "y": 4,
          "size": 26,
          "tracking": 41.1
        },
        "강원교육모두체": {
          "x": 28,
          "y": 6,
          "size": 26,
          "tracking": 47.1
        },
        "교보손글씨 2020 박도연": {
          "x": 28,
          "y": 4,
          "size": 26,
          "tracking": 49.0
        }
      }
    },
    {
      "id": "title_load_off.1",
      "type": "text",
      "file": "title_load_off.png",
      "source_text": "続きから",
      "text": "이어하기",
      "fill": "#F7F7F1FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 3,
      "render": {
        "Minguk": {
          "x": 3,
          "y": 4,
          "size": 26,
          "tracking": 15.1
        },
        "경기천년바탕": {
          "x": 3,
          "y": 4,
          "size": 26,
          "tracking": 15.4
        },
        "강원교육모두체": {
          "x": 3,
          "y": 5,
          "size": 26,
          "tracking": 20.4
        },
        "교보손글씨 2020 박도연": {
          "x": 3,
          "y": 4,
          "size": 26,
          "tracking": 19.1
        }
      }
    },
    {
      "id": "title_load_on.1",
      "type": "text",
      "file": "title_load_on.png",
      "source_text": "続きから",
      "text": "이어하기",
      "fill": "#FFFAF5FF",
      "weight": "Regular",
      "stroke": "#E83E44FF",
      "stroke_width": 2,
      "render": {
        "Minguk": {
          "x": 4,
          "y": 5,
          "size": 26,
          "tracking": 15.1
        },
        "경기천년바탕": {
          "x": 4,
          "y": 4,
          "size": 26,
          "tracking": 15.4
        },
        "강원교육모두체": {
          "x": 4,
          "y": 6,
          "size": 26,
          "tracking": 20.4
        },
        "교보손글씨 2020 박도연": {
          "x": 4,
          "y": 5,
          "size": 26,
          "tracking": 19.1
        }
      }
    },
    {
      "id": "title_music_off.1",
      "type": "text",
      "file": "title_music_off.png",
      "source_text": "音楽鑑賞",
      "text": "음악 감상",
      "fill": "#F7F7F1FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 3,
      "render": {
        "Minguk": {
          "x": 4,
          "y": 2,
          "size": 26,
          "tracking": 7.7
        },
        "경기천년바탕": {
          "x": 4,
          "y": 2,
          "size": 26,
          "tracking": 7.7
        },
        "강원교육모두체": {
          "x": 3,
          "y": 3,
          "size": 26,
          "tracking": 11.2
        },
        "교보손글씨 2020 박도연": {
          "x": 4,
          "y": 2,
          "size": 26,
          "tracking": 10.7
        }
      }
    },
    {
      "id": "title_music_on.1",
      "type": "text",
      "file": "title_music_on.png",
      "source_text": "音楽鑑賞",
      "text": "음악 감상",
      "fill": "#FFFAF5FF",
      "weight": "Regular",
      "stroke": "#E83E44FF",
      "stroke_width": 2,
      "render": {
        "Minguk": {
          "x": 4,
          "y": 3,
          "size": 26,
          "tracking": 7.7
        },
        "경기천년바탕": {
          "x": 4,
          "y": 2,
          "size": 26,
          "tracking": 7.7
        },
        "강원교육모두체": {
          "x": 4,
          "y": 4,
          "size": 26,
          "tracking": 11.2
        },
        "교보손글씨 2020 박도연": {
          "x": 4,
          "y": 3,
          "size": 26,
          "tracking": 10.7
        }
      }
    },
    {
      "id": "title_scene_off.1",
      "type": "text",
      "file": "title_scene_off.png",
      "source_text": "シーン回想",
      "text": "장면 회상",
      "fill": "#F7F7F1FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 3,
      "render": {
        "Minguk": {
          "x": 6,
          "y": 2,
          "size": 26,
          "tracking": 7.2
        },
        "경기천년바탕": {
          "x": 6,
          "y": 2,
          "size": 26,
          "tracking": 7.5
        },
        "강원교육모두체": {
          "x": 6,
          "y": 4,
          "size": 26,
          "tracking": 11.2
        },
        "교보손글씨 2020 박도연": {
          "x": 6,
          "y": 2,
          "size": 26,
          "tracking": 10.2
        }
      }
    },
    {
      "id": "title_scene_on.1",
      "type": "text",
      "file": "title_scene_on.png",
      "source_text": "シーン回想",
      "text": "장면 회상",
      "fill": "#FFFAF5FF",
      "weight": "Regular",
      "stroke": "#E83E44FF",
      "stroke_width": 2,
      "render": {
        "Minguk": {
          "x": 7,
          "y": 3,
          "size": 26,
          "tracking": 7.2
        },
        "경기천년바탕": {
          "x": 7,
          "y": 3,
          "size": 26,
          "tracking": 7.5
        },
        "강원교육모두체": {
          "x": 7,
          "y": 4,
          "size": 26,
          "tracking": 11.2
        },
        "교보손글씨 2020 박도연": {
          "x": 7,
          "y": 4,
          "size": 26,
          "tracking": 10.2
        }
      }
    },
    {
      "id": "title_start_off.1",
      "type": "text",
      "file": "title_start_off.png",
      "source_text": "はじめから",
      "text": "처음부터",
      "fill": "#F7F7F1FF",
      "weight": "Regular",
      "stroke": "#050505FF",
      "stroke_width": 3,
      "render": {
        "Minguk": {
          "x": 6,
          "y": 1,
          "size": 26,
          "tracking": 13.7
        },
        "경기천년바탕": {
          "x": 5,
          "y": 0,
          "size": 26,
          "tracking": 14.4
        },
        "강원교육모두체": {
          "x": 5,
          "y": 2,
          "size": 26,
          "tracking": 19.1
        },
        "교보손글씨 2020 박도연": {
          "x": 5,
          "y": 1,
          "size": 26,
          "tracking": 17.7
        }
      }
    },
    {
      "id": "title_start_on.1",
      "type": "text",
      "file": "title_start_on.png",
      "source_text": "はじめから",
      "text": "처음부터",
      "fill": "#FFFAF5FF",
      "weight": "Regular",
      "stroke": "#E83E44FF",
      "stroke_width": 2,
      "render": {
        "Minguk": {
          "x": 6,
          "y": 2,
          "size": 26,
          "tracking": 13.7
        },
        "경기천년바탕": {
          "x": 6,
          "y": 1,
          "size": 26,
          "tracking": 14.4
        },
        "강원교육모두체": {
          "x": 6,
          "y": 2,
          "size": 26,
          "tracking": 19.1
        },
        "교보손글씨 2020 박도연": {
          "x": 6,
          "y": 2,
          "size": 26,
          "tracking": 17.7
        }
      }
    },
    {
      "id": "title_background.logo",
      "type": "vertical_text",
      "file": "title_background.png",
      "source_text": "神無ノ鳥",
      "text": "칸나기의새",
      "box": [
        483,
        82,
        532,
        246
      ],
      "size": 38,
      "fill": "#ED1C24FF",
      "weight": "Regular",
      "stroke": "#C6C0BDFF",
      "stroke_width": 1,
      "gap": 2,
      "character_scale": {
        "의": 0.7
      }
    },
    {
      "id": "title_background.copyright",
      "type": "copy_original",
      "file": "title_background.png",
      "source_box": [
        350,
        458,
        625,
        480
      ],
      "destination": [
        350,
        458
      ]
    },
    {
      "id": "cgtop_thumbnail.derived",
      "type": "resize_from",
      "file": "cgtop_thumbnail.png",
      "source_file": "title_background.png",
      "size": [
        78,
        58
      ],
      "resample": "lanczos",
      "convert": "RGB"
    },
    {
      "id": "end_bad.1",
      "type": "text",
      "file": "end_bad.png",
      "source_text": "To Be Continued...",
      "text": "계속...",
      "fill": "#F2F2EEFF",
      "weight": "Regular",
      "stroke": null,
      "stroke_width": 0,
      "render": {
        "Minguk": {
          "x": 286,
          "y": 226,
          "size": 28,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 285,
          "y": 226,
          "size": 28,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 284,
          "y": 226,
          "size": 30,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 290,
          "y": 226,
          "size": 27,
          "tracking": 0
        }
      }
    },
    {
      "id": "l_end_kan.1",
      "type": "text",
      "file": "l_end_kan.png",
      "source_text": "完",
      "text": "끝",
      "fill": "#202020FF",
      "weight": "Regular",
      "stroke": null,
      "stroke_width": 0,
      "render": {
        "Minguk": {
          "x": 308,
          "y": 228,
          "size": 25,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 308,
          "y": 228,
          "size": 25,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 308,
          "y": 228,
          "size": 28,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 310,
          "y": 228,
          "size": 25,
          "tracking": 0
        }
      }
    },
    {
      "id": "ex_title.1",
      "type": "text",
      "file": "ex_title.png",
      "source_text": "神無ノ鳥",
      "text": "칸나기의 새",
      "fill": "#F2F2EEFF",
      "weight": "Regular",
      "stroke": null,
      "stroke_width": 0,
      "render": {
        "Minguk": {
          "x": 278,
          "y": 212,
          "size": 18,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 275,
          "y": 211,
          "size": 19,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 276,
          "y": 211,
          "size": 21,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 282,
          "y": 212,
          "size": 18,
          "tracking": 0
        }
      }
    },
    {
      "id": "ex_title.2",
      "type": "text",
      "file": "ex_title.png",
      "source_text": "番外編",
      "text": "번외편",
      "fill": "#F2F2EEFF",
      "weight": "Regular",
      "stroke": null,
      "stroke_width": 0,
      "render": {
        "Minguk": {
          "x": 297,
          "y": 240,
          "size": 18,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 296,
          "y": 240,
          "size": 19,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 297,
          "y": 240,
          "size": 21,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 300,
          "y": 240,
          "size": 18,
          "tracking": 0
        }
      }
    },
    {
      "id": "ex_title.rule",
      "type": "line_relative",
      "file": "ex_title.png",
      "relative_to": "ex_title.1",
      "center_x": 320,
      "y": 234,
      "width_add": 8,
      "height": 1,
      "fill": "#F2F2EEFF"
    },
    {
      "id": "log_exit@n.1",
      "type": "text",
      "file": "log_exit@n.png",
      "source_text": "戻る",
      "text": "돌아가기",
      "fill": "#F2F2EEFF",
      "weight": "Bold",
      "stroke": "#3A3A4EFF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 1,
          "y": 0,
          "size": 15,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 2,
          "y": 0,
          "size": 15,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 1,
          "y": 0,
          "size": 17,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 2,
          "y": 0,
          "size": 16,
          "tracking": 0
        }
      }
    },
    {
      "id": "log_exit@s.1",
      "type": "text",
      "file": "log_exit@s.png",
      "source_text": "戻る",
      "text": "돌아가기",
      "fill": "#F2F2EEFF",
      "weight": "Bold",
      "stroke": "#3A3A4EFF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 1,
          "y": 0,
          "size": 15,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 2,
          "y": 0,
          "size": 15,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 1,
          "y": 0,
          "size": 17,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 2,
          "y": 0,
          "size": 16,
          "tracking": 0
        }
      }
    },
    {
      "id": "testroll.1",
      "type": "text",
      "file": "testroll.png",
      "source_text": "ロールテスト",
      "text": "롤 테스트",
      "fill": "#F5F5F0FF",
      "weight": "Bold",
      "stroke": "#0A0A0CFF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 418,
          "y": 12,
          "size": 40,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 414,
          "y": 12,
          "size": 40,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 424,
          "y": 14,
          "size": 40,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 427,
          "y": 12,
          "size": 40,
          "tracking": 0
        }
      }
    },
    {
      "id": "testroll.2",
      "type": "text",
      "file": "testroll.png",
      "source_text": "ロールテスト",
      "text": "롤 테스트",
      "fill": "#F5F5F0FF",
      "weight": "Bold",
      "stroke": "#0A0A0CFF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 418,
          "y": 141,
          "size": 40,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 414,
          "y": 140,
          "size": 40,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 423,
          "y": 142,
          "size": 40,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 426,
          "y": 141,
          "size": 40,
          "tracking": 0
        }
      }
    },
    {
      "id": "testroll.3",
      "type": "text",
      "file": "testroll.png",
      "source_text": "ロールテスト",
      "text": "롤 테스트",
      "fill": "#F5F5F0FF",
      "weight": "Bold",
      "stroke": "#0A0A0CFF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 426,
          "y": 263,
          "size": 40,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 422,
          "y": 262,
          "size": 40,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 431,
          "y": 264,
          "size": 40,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 434,
          "y": 263,
          "size": 40,
          "tracking": 0
        }
      }
    },
    {
      "id": "testroll.4",
      "type": "text",
      "file": "testroll.png",
      "source_text": "ロールテスト",
      "text": "롤 테스트",
      "fill": "#F5F5F0FF",
      "weight": "Bold",
      "stroke": "#0A0A0CFF",
      "stroke_width": 1,
      "render": {
        "Minguk": {
          "x": 424,
          "y": 387,
          "size": 40,
          "tracking": 0
        },
        "경기천년바탕": {
          "x": 420,
          "y": 386,
          "size": 40,
          "tracking": 0
        },
        "강원교육모두체": {
          "x": 430,
          "y": 388,
          "size": 40,
          "tracking": 0
        },
        "교보손글씨 2020 박도연": {
          "x": 433,
          "y": 387,
          "size": 40,
          "tracking": 0
        }
      }
    }
  ]
}
```
<!-- image-text-manifest:end -->
