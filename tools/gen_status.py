#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""docs/STATUS.md 의 집계 구간을 strings.json 에서 다시 만든다.

`<!-- STATS:BEGIN -->` ~ `<!-- STATS:END -->` 사이만 갈아끼우므로, 그 밖의 서술
(완료된 씬·남은 것·작업 방법 등)은 손대지 않는다. **커밋할 때마다 돌린다** —
손으로 고치면 반드시 어긋난다.

    python tools/gen_status.py
"""
import json, io, os, re, sys, collections, datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ujyu.titleconfig import config as C
from ujyu import filter_text as F

DOC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "STATUS.md")
BEGIN, END = "<!-- STATS:BEGIN -->", "<!-- STATS:END -->"

ROUTE = [("공통", "공통(본편)"), ("l", "루우 (`l`)"), ("r", "렌자크 (`r`)"),
         ("f", "후카마치 (`f`)"), ("a", "마나베 (`a`)"), ("h", "하칸 (`h`)"),
         ("hr", "하칸·렌자크 (`hr`)"), ("af", "마나베·후카마치 (`af`)"),
         ("sc", "회상 (`sc_*`)"), ("ex", "번외편 (`ex*`)"), ("기타", "엔딩·시스템")]
ROUTE_NAME = dict(ROUTE)

# 날짜별 등장 루트 (파일명 접두에서 자동 도출)
ABBR = {"l": "루", "r": "렌", "f": "후", "a": "마", "h": "하", "hr": "하렌",
        "af": "마후", "공통": "공통"}


def route_of(fname):
    if fname.startswith("sc_"):
        return "sc"
    if fname.startswith("ex"):
        return "ex"
    m = re.match(r"^([a-z]*)\d{4}_", fname)
    if not m:
        return "기타"
    return m.group(1) or "공통"


def main():
    S = json.load(io.open(C.STRINGS, encoding="utf-8"))
    tgt = done = 0
    ch = dch = 0
    kind = collections.Counter(); kdone = collections.Counter()
    quote = 0
    files = set()
    route = collections.defaultdict(lambda: [0, 0, 0])       # 조각, 문자, 번역
    date = collections.defaultdict(lambda: [set(), 0, 0, 0, set()])  # 파일,조각,문자,번역,루트

    for r in S:
        if r.get("kind") == "quote":
            quote += 1
        if F.classify(r.get("jp")) != "text":
            continue
        k = r.get("kind"); jp = r.get("jp") or ""
        ok = bool((r.get("kr") or "").strip())
        tgt += 1; ch += len(jp)
        kind[k] += 1
        if ok:
            done += 1; dch += len(jp); kdone[k] += 1
        f = r["file"]; files.add(f)
        if k in ("dlg", "narr"):
            g = route[route_of(f)]
            g[0] += 1; g[1] += len(jp); g[2] += ok
            m = re.match(r"^([a-z]*)(\d{4})_", f)
            if m:
                d = date[m.group(2)]
                d[0].add(f); d[1] += 1; d[2] += len(jp); d[3] += ok
                d[4].add(ABBR.get(m.group(1) or "공통", m.group(1)))

    L = [BEGIN, ""]
    L.append("## 전체")
    L.append("")
    L.append("| 지표 | 값 |")
    L.append("|---|---|")
    L.append("| 추출 조각 (전체) | %s |" % f"{len(S):,}")
    L.append("| **번역 대상 조각** | **%s** |" % f"{tgt:,}")
    L.append("| 번역 완료 | **%s (%.1f%%)** |" % (f"{done:,}", 100 * done / tgt))
    L.append("| 원문 분량 (대상) | %s자 |" % f"{ch:,}")
    L.append("| 번역 완료 분량 | %s자 (%.1f%%) |" % (f"{dch:,}", 100 * dch / ch))
    L.append("| 파일 | %d |" % len(files))
    L.append("")
    L.append("## 종류(kind)별")
    L.append("")
    L.append("| kind | 뜻 | 대상 | 번역 | % |")
    L.append("|---|---|---:|---:|---:|")
    MEAN = {"dlg": "대사", "narr": "나레이션",
            "sym": "심볼 문자열 (화자명·선택지·씬 제목·시스템 문구)",
            "cstr": "데이터 화면 문자열 (곡 해설·씬 제목)", "cmd": "명령 문자열 인자"}
    for k in ("dlg", "narr", "sym", "cstr", "cmd"):
        if not kind[k]:
            continue
        p = 100 * kdone[k] / kind[k]
        v = "**100%**" if p >= 99.95 else "%.1f%%" % p
        L.append("| `%s` | %s | %s | %s | %s |"
                 % (k, MEAN[k], f"{kind[k]:,}", f"{kdone[k]:,}", v))
    L.append("| `quote` | 여는 괄호 블록 | — | — | 번역 불필요 (%s건) |" % f"{quote:,}")
    L.append("")
    L.append("## 루트별")
    L.append("")
    L.append("파일명 규칙 `[루트]MMDD_NN[분기]` 의 접두 루트로 묶었다.")
    L.append("**`본편 %`** = 대사·나레이션 조각 중 번역된 비율.")
    L.append("")
    L.append("| 루트 | 본편 조각 | 본편 문자 | 번역 | 본편 % |")
    L.append("|---|---:|---:|---:|---:|")
    tot = [0, 0, 0]
    for key, name in sorted(ROUTE, key=lambda kv: -route[kv[0]][0]):
        g = route[key]
        if not g[0]:
            continue
        tot[0] += g[0]; tot[1] += g[1]; tot[2] += g[2]
        p = 100 * g[2] / g[0]
        L.append("| %s | %s | %s | %s | %s |"
                 % (name, f"{g[0]:,}", f"{g[1]:,}", f"{g[2]:,}",
                    "**100%**" if p >= 99.95 else "%.1f%%" % p))
    L.append("| **합계** | **%s** | **%s** | **%s** | **%.1f%%** |"
             % (f"{tot[0]:,}", f"{tot[1]:,}", f"{tot[2]:,}", 100 * tot[2] / tot[0]))
    L.append("")
    L.append("## 날짜별 (게임 내 날짜)")
    L.append("")
    L.append("파일명 순 = 이야기 순. 날짜형이 아닌 번외편·엔딩·회상·시스템은 빠져 있어")
    L.append("합계가 루트 표보다 작다.")
    L.append("")
    L.append("| 날짜 | 파일 | 본편 조각 | 본편 문자 | 번역 | 본편 % | 등장 루트 |")
    L.append("|---|---:|---:|---:|---:|---:|---|")
    dt = [0, 0, 0, 0]
    for k in sorted(date):
        f_, n, c, b, rt = date[k]
        dt[0] += len(f_); dt[1] += n; dt[2] += c; dt[3] += b
        p = 100 * b / n
        L.append("| %s/%s | %d | %s | %s | %s | %s | %s |"
                 % (k[:2], k[2:], len(f_), f"{n:,}", f"{c:,}", f"{b:,}",
                    "**100%**" if p >= 99.95 else "%.1f%%" % p,
                    " ".join(sorted(rt))))
    L.append("| **날짜분 계** | **%d** | **%s** | **%s** | **%s** | **%.1f%%** | |"
             % (dt[0], f"{dt[1]:,}", f"{dt[2]:,}", f"{dt[3]:,}", 100 * dt[3] / dt[1]))
    L.append("")
    L.append(END)

    doc = io.open(DOC, encoding="utf-8").read()
    if BEGIN not in doc or END not in doc:
        raise SystemExit("STATUS.md 에 %s / %s 마커가 없다" % (BEGIN, END))
    head, rest = doc.split(BEGIN, 1)
    _mid, tail = rest.split(END, 1)
    today = datetime.date.today().isoformat()
    head = re.sub(r"\*\*\d{4}-\d{2}-\d{2} 재집계\*\*", "**%s 재집계**" % today, head)
    io.open(DOC, "w", encoding="utf-8").write(head + "\n".join(L) + tail)
    print("STATUS.md 갱신: 대상 %s / 번역 %s (%.1f%%)"
          % (f"{tgt:,}", f"{done:,}", 100 * done / tgt))


main()
