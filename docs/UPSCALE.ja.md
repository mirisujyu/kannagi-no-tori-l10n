# 『神無ノ鳥』を大きい画面で遊ぶ

このタイトル向けの**実測値と落とし穴**です。手順そのものは
[engine/docs/UPSCALE.ja.md](../engine/docs/UPSCALE.ja.md) を見てください。ここには
「このゲームではどうだったか」だけを書きます。

翻訳とは関係ありません。**日本語のまま解像度だけ上げる**のにそのまま使えます。

---

## 結論

| | 値 |
|---|---|
| 原寸 | 640×480 |
| 推奨 | **2×（1280×960）** |
| 3× | 動くが画面が大きすぎる。1920×1440 |
| 実行 | **Windows 8 互換モードが必要**（exe のプロパティ → 互換性） |

3× は検証済みですが、実用は 2× です。`config.py` の `SCALE` を変えるだけで切り替わります。

---

## 画像の置き場所

```python
CG_UPSCALE_DIR = dev("kannagi-upscale", "2x")   # 既定
```

環境変数 `KANNAGI_CG_UPSCALE` でも指定できます。ここに**同じファイル名・原寸×2** の
PNG を置くと `ujyu build cg` が拾います。無ければ bilinear で伸ばすだけです。

```bash
ujyu scale cg-export <元の cg.axr> --out work/ --prefer <翻訳済み cg.axr>
#   -> work/1x/{art,small,translated}/ + _manifest.tsv
#   （外部アップスケーラで work/2x/ へ。ファイル名はそのまま）
ujyu scale cg-check work/ work/2x/
ujyu build cg
```

---

## 拡大するもの・しないもの

**会話ウィンドウは 1× のまま**です。ここを 2× にすると文字が大きくなりすぎるので、
大きさは据え置いて位置だけ右下にずらしています。

| 設定 | 対象 |
|---|---|
| `SCALE_DIALOG_1X` | `textwin` `namewin` `face` — 会話まわり。1× 維持 + 位置補正 |
| `SCALE_FS_WINDOWS` | `logwin` — 全画面ログは w/h・余白ごと ×N |
| `CG_UI_1X_PREFIX` | `f_` `msg_` `frame_` `cursor_` `winmsg` — 1× のウィンドウに載る枠・カーソル |
| `CG_CONTENT_PREFIX` | 背景・立ち絵・鑑賞画面（`bg` `s_` `event` `cg_` `sa_` `cgtop_` `sc_` `mu_` `log_` …）|

**鑑賞画面の背景は必ず拡大が要ります。** 640×480 の全画面絵なので 1× のままだと
左上 1/4 にしか描かれません（座標のほうは ×N されるため）。

選択肢ウィンドウは特別扱いです。`common.csv` の `textwindow,select`(600×200) と
`int,select_*` はボタン計算にそのまま使われるので ×N すると崩れます。**大きさは据え置き、
位置だけ画面中央へ**寄せます（`COMMON_CENTER = {"select": 320}`）。

---

## このタイトルで踏んだ落とし穴

### 名前欄の文字だけ大きくなった

`system.scn` のシンボル `#42 = 18` が、**ログ画面の矢印の幅**であると同時に
**名前欄のフォントサイズ**でもありました。まとめて ×2 したら名前の文字が一緒に育ちます。

→ `SCN_REPOINT` で、ログ側（`obj16`）から参照している 5 か所だけ新しいシンボルに分けました。

```python
SCN_REPOINT = {"system.scn": [((0x0699, 0x06ae, 0x06c3, 0x06d8, 0x06ef), 18)]}
```

### 曲名が行からはみ出した

`music.scn` の曲名フォントは曲ごとに大きさが違います（長い曲名ほど小さい）。
2× にすると 44 が行に対して大きすぎました。

→ `SCN_VALUE_REMAP` で一段下げます（44→38、40→36。36・28 の組はそのまま）。

### 全体フォントサイズは効かなかった

`common.csv` の `text_size`(22) / `text_line_height`(25) を ×N するスイッチ
（`SCALE_COMMON_INTS`）を用意しましたが、**このタイトルでは見た目が何も変わりません**。
会話・設定・セーブ・鑑賞のどの画面も自前の `m07` でフォントを決めているためです。
空のままにしてあります。

### 選択肢に入るとクラッシュした

`common.csv` を他のアーカイブのもので丸ごと差し替えたのが原因でした。アーカイブ固有の
変数定義（`int` や `version`）が消えて未初期化になります。

→ **アーカイブごとに自分の `common.csv` をその場で編集**します。`ujyu build` はそうします。

### ムービーと選択肢でハングした

シーンを詰め直すと VNEG のジャンプテーブルに古い相対オフセットが残ります。

→ 貼り直しが必須。`ujyu build` が自動でやります。

---

## 座標の在り処は三つ

一か所直しても画面は揃いません。

| 経路 | 説明 |
|---|---|
| `SCN_DIMS_AUTO` | VNEG の int シンボルから自動導出して ×N。**こちらが基本**。翻訳で文字数が変わっても安全 |
| `SCN_DIMS` | ファイル内オフセット直指定。**翻訳で長さが変わると壊れる**ので極力使わない |
| `COMMON_CENTER` | 拡大しないウィンドウを中央へ寄せる |

このタイトルで `SCN_DIMS` に残っているのは、シンボル参照ではなく生の番号でオブジェクトを
呼ぶもの（`system.scn` のログ矢印まわり）と、翻訳対象の文字列が 0 件でオフセットが動かない
`mlogo.scn` / `title.scn` だけです。

`SCN_DIMS_AUTO` は `save` `load` `config` `cg` `music` `scene` `endchk` `titlechk`。

---

## ムービー

```python
MOVIE_NATIVE = True
```

エンジン側の 2 倍拡大を切って、**画面サイズ（原寸×SCALE）で再エンコード**します。
拡大表示より綺麗ですが、`movie` アーカイブを作り直す必要があります。

---

## 参考

- 一般的な手順: [engine/docs/UPSCALE.ja.md](../engine/docs/UPSCALE.ja.md)
- 仕組み: [engine/docs/formats/RESOLUTION.md](../engine/docs/formats/RESOLUTION.md)
- 設定値と根拠: [`config.tmpl.py`](../config.tmpl.py) 冒頭
