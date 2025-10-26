# SSD1306 OLED 日本語表示サンプル

Raspberry Pi 5 と SSD1306 OLED（I²C）を使用した**日本語表示の入門サンプル**です。

完全な初心者を対象に、学習ハードルを下げる設計としています。

---

## 📋 目次

- [プロジェクト概要](#プロジェクト概要)
- [ハードウェア要件](#ハードウェア要件)
- [ソフトウェア要件](#ソフトウェア要件)
- [セットアップ](#セットアップ)
- [使用方法](#使用方法)
- [設定のカスタマイズ](#設定のカスタマイズ)
- [トラブルシューティング](#トラブルシューティング)
- [ライセンス](#ライセンス)

---

## プロジェクト概要

このプロジェクトでは、以下の2つのサンプルを提供します：

1. **simple_oled.py**: 日本語の複数行テキストを固定表示
2. **scroll_oled.py**: 日本語テキストを横スクロール表示

**特徴**:
- ✅ 初心者向けの簡潔なコード
- ✅ 設定は全てコード冒頭の定数で変更可能
- ✅ 詳細な日本語コメント
- ✅ 充実したエラーメッセージとトラブルシューティング

**参照ドキュメント**:
- [要件定義書](06-004-ssd_1306_oled_要件定義書（rev.md)
- [コメントスタイルガイド](COMMENT_STYLE_GUIDE.md)
- [作業ルール](CLAUDE.md)

---

## ハードウェア要件

### 必要な機器

- **Raspberry Pi 5**（Raspberry Pi OS Bookworm 以降）
- **SSD1306 OLED モジュール**（I²C接続、128×64 または 128×32）
- **I²C レベル変換モジュール**（BSS138 方式など）
- **ジャンパーワイヤー**
- **ブレッドボード**（推奨）

### ⚠️ 重要な注意事項

**🔴 5V OLED を Raspberry Pi に直結しないでください！**

- Raspberry Pi の GPIO は **3.3V** です
- 5V OLED と直結すると、通信できないだけでなく **GPIO を破損する可能性** があります
- **必ずレベル変換モジュール（BSS138方式）を使用** してください
- 3.3V 動作の OLED モジュールの使用を推奨

### 配線図

**レベル変換使用時**（5V OLED の場合）:

```
[Raspberry Pi 5]       [レベル変換]        [5V OLED]
Pin 1  (3.3V)  ------> LV
Pin 3  (GPIO2) ------> LV-SDA  ----> HV-SDA  ----> SDA
Pin 5  (GPIO3) ------> LV-SCL  ----> HV-SCL  ----> SCL
Pin 6  (GND)   ------> GND     <---- GND     <---- GND
                       HV      <---- VCC (5V)
```

**3.3V OLED の場合**（レベル変換不要）:

```
[Raspberry Pi 5]       [3.3V OLED]
Pin 1  (3.3V)  ------> VCC
Pin 3  (GPIO2) ------> SDA
Pin 5  (GPIO3) ------> SCL
Pin 6  (GND)   ------> GND
```

---

## ソフトウェア要件

- **Python**: 3.11 以降推奨
- **OS**: Raspberry Pi OS（Bookworm 以降）
- **ライブラリ**: `luma.oled`, `Pillow`

---

## セットアップ

### 1. I²C の有効化

```bash
sudo raspi-config
```

- `3 Interface Options` → `I5 I2C` → `Yes`
- 再起動

```bash
sudo reboot
```

### 2. I²C デバイスの確認

```bash
i2cdetect -y 1
```

**期待される出力例**:
```
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- 3c -- -- --
...
```

`3c`（0x3C）または `3d`（0x3D）が表示されればOKです。

### 3. リポジトリのクローン

```bash
cd ~/work/project
git clone <リポジトリURL>
cd 06-004-ssd1306-oled-jp-display
```

### 4. Python ライブラリのインストール

```bash
pip install luma.oled pillow
```

### 5. 日本語フォントの配置

```bash
cd assets/fonts/
wget https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTF/Japanese/NotoSansCJKjp-Regular.otf
wget https://raw.githubusercontent.com/googlefonts/noto-cjk/main/LICENSE
cd ../..
```

詳細は [`assets/fonts/README.md`](assets/fonts/README.md) を参照してください。

---

## 使用方法

### サンプル1: 固定表示（simple_oled.py）

複数行の日本語テキストを OLED に表示します。

```bash
cd src/
python simple_oled.py
```

**出力例**:
```
I²C初期化完了: アドレス 0x3C, ポート 1
OLED初期化完了: 128×64
フォント読み込み完了: ../assets/fonts/NotoSansCJKjp-Regular.otf, サイズ 12
表示完了
表示テキスト: 3行
```

### サンプル2: スクロール表示（scroll_oled.py）

日本語テキストを右から左へスクロール表示します。

```bash
cd src/
python scroll_oled.py
```

**出力例**:
```
I²C初期化完了: アドレス 0x3C, ポート 1
OLED初期化完了: 128×64
フォント読み込み完了: ../assets/fonts/NotoSansCJKjp-Regular.otf, サイズ 16
スクロール開始: テキスト幅 850px
スクロール速度: 2px/フレーム, 間隔: 0.05秒
ループ回数: 無限（Ctrl+C で終了）
```

**停止方法**: `Ctrl + C`

---

## 設定のカスタマイズ

すべての設定は**コード冒頭の定数**で変更できます。

### simple_oled.py の主な設定

```python
# 表示するテキスト（複数行）
TEXT_LINES = [
    "こんにちは",
    "Raspberry Pi",
    "SSD1306 OLED"
]

# フォント設定
FONT_PATH = "../assets/fonts/NotoSansCJKjp-Regular.otf"
FONT_SIZE = 12

# レイアウト設定
MARGIN_X = 2    # 左右のマージン
MARGIN_Y = 2    # 上下のマージン
LINE_SPACING = 2  # 行間隔

# ディスプレイ設定
WIDTH = 128
HEIGHT = 64      # 128×32 の場合は 32 に変更
I2C_ADDRESS = 0x3C  # 0x3D の場合もあり
```

### scroll_oled.py の主な設定

```python
# スクロールするテキスト
SCROLL_TEXT = "こんにちは Raspberry Pi 5 で SSD1306 OLED を使った日本語スクロール表示のサンプルです"

# フォント設定
FONT_SIZE = 16

# スクロール設定
SCROLL_SPEED_PX = 2    # スクロール速度（大きいほど速い）
FRAME_DELAY_SEC = 0.05  # フレーム間隔（小さいほど滑らか）
LOOP_COUNT = None       # None=無限、整数=指定回数

# ディスプレイ設定
WIDTH = 128
HEIGHT = 64
I2C_ADDRESS = 0x3C
```

---

## トラブルシューティング

詳細は **[docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** を参照してください。

### よくあるエラー

| 症状 | 原因 | 対処方法 |
|------|------|----------|
| `i2cdetect` でデバイスが見つからない | I²C 未有効化、配線誤り | I²C 有効化、配線確認 |
| `[Errno 121] Remote I/O error` | I²C 通信失敗 | 配線・レベル変換確認 |
| 日本語が「□」になる | フォント未配置 | Noto Sans CJK JP を配置 |
| `cannot open resource` | フォントパス誤り | パスを確認・修正 |
| スクロールがカクつく | フレーム間隔が大きい | `FRAME_DELAY_SEC` を小さく |
| 文字が画面からはみ出す | フォントサイズが大きい | `FONT_SIZE` を小さく |

---

## プロジェクト構造

```
06-004-ssd1306-oled-jp-display/
├── src/
│   ├── simple_oled.py          # 固定表示サンプル
│   └── scroll_oled.py          # スクロール表示サンプル
├── assets/
│   └── fonts/
│       ├── README.md            # フォント配置手順
│       ├── NotoSansCJKjp-Regular.otf  # 日本語フォント
│       └── LICENSE              # フォントライセンス
├── docs/
│   └── TROUBLESHOOTING.md       # トラブルシューティング集
├── 06-004-ssd_1306_oled_要件定義書（rev.md  # 要件定義書
├── COMMENT_STYLE_GUIDE.md       # コメントスタイルガイド
├── CLAUDE.md                    # Claude Code 作業ルール
├── LICENSE                      # プロジェクトライセンス
└── README.md                    # 本ファイル
```

---

## ライセンス

### プロジェクトコード

本プロジェクトのサンプルコードは **MIT License** で提供されています。

詳細は [LICENSE](LICENSE) ファイルを参照してください。

### フォント

Noto Sans CJK JP は **SIL Open Font License (OFL-1.1)** で提供されています。

- 商用利用可
- 改変可
- 再配布可

ライセンス詳細: [`assets/fonts/LICENSE`](assets/fonts/LICENSE)

---

## 参考資料

- **luma.oled ドキュメント**: https://luma-oled.readthedocs.io/
- **Pillow ドキュメント**: https://pillow.readthedocs.io/
- **Noto Fonts**: https://fonts.google.com/noto
- **Raspberry Pi I²C 設定**: https://www.raspberrypi.com/documentation/computers/configuration.html

---

## 貢献

Issue や Pull Request は歓迎します。

---

## サポート

問題が発生した場合：

1. [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) を確認
2. 上記で解決しない場合は Issue を作成

---

**作成日**: 2025-01-XX
**対象**: 初心者向け Raspberry Pi + OLED 日本語表示教材
