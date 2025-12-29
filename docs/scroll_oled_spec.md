# scroll_oled.py 機能仕様書

## 概要

SSD1306 OLED ディスプレイで日本語テキストを横スクロール表示するライブラリ。
他のプロジェクトからインポートして再利用可能。

## 対象ハードウェア

- Raspberry Pi 5
- SSD1306 OLED（I²C接続、128×64 または 128×32）
- I²C レベル変換モジュール（BSS138方式）

## 依存ライブラリ

```bash
pip install luma.oled pillow
```

---

## クラス仕様

### OLEDScroller

OLED横スクロール表示クラス。

#### コンストラクタ

```python
OLEDScroller(font_path, font_size, width, height, address)
```

| 引数 | 型 | デフォルト | 説明 |
|------|-----|-----------|------|
| font_path | str | `"../assets/fonts/NotoSansCJKjp-Regular.otf"` | フォントファイルパス |
| font_size | int | 16 | フォントサイズ |
| width | int | 128 | 画面幅 |
| height | int | 64 | 画面高さ（64または32） |
| address | int | 0x3C | I²Cアドレス |

#### メソッド

##### scroll()

テキストを右から左へスクロール表示。

```python
scroll(text, speed, delay, loops, y_pos)
```

| 引数 | 型 | デフォルト | 説明 |
|------|-----|-----------|------|
| text | str | （必須） | 表示するテキスト |
| speed | int | 2 | スクロール速度（px/フレーム） |
| delay | float | 0.05 | フレーム間隔（秒） |
| loops | int | None | ループ回数（Noneで無限） |
| y_pos | int | 24 | テキストのY座標 |

##### clear()

画面をクリア。

```python
clear()
```

---

## 使用例

### 基本的な使い方

```python
from scroll_oled import OLEDScroller

# 初期化
scroller = OLEDScroller()

# 3回スクロール
scroller.scroll("こんにちは！", loops=3)

# 画面クリア
scroller.clear()
```

### カスタム設定

```python
from scroll_oled import OLEDScroller

# カスタム設定で初期化
scroller = OLEDScroller(
    font_path="/path/to/font.otf",
    font_size=12,
    height=32,        # 128×32ディスプレイ
    address=0x3D      # 別アドレス
)

# ゆっくりスクロール（無限ループ）
scroller.scroll(
    "ゆっくりスクロール",
    speed=1,          # 遅め
    delay=0.1,        # 間隔長め
    y_pos=8           # 上寄せ
)
```

### 他プロジェクトからのインポート

```python
import sys
sys.path.append("/path/to/06-004-ssd1306-oled-jp-display/src")

from scroll_oled import OLEDScroller

scroller = OLEDScroller()
scroller.scroll("センサー値: 25.5℃", loops=1)
```

---

## 設定定数

ソースコード冒頭で変更可能。

| 定数 | デフォルト値 | 説明 |
|------|-------------|------|
| FONT_PATH | `"../assets/fonts/NotoSansCJKjp-Regular.otf"` | フォントパス |
| FONT_SIZE | 16 | フォントサイズ |
| WIDTH | 128 | 画面幅 |
| HEIGHT | 64 | 画面高さ |
| I2C_ADDRESS | 0x3C | I²Cアドレス |

---

## エラーハンドリング

| エラー | 原因 | 対処 |
|--------|------|------|
| `[OLED初期化]エラー` | I²C通信失敗 | `i2cdetect -y 1` で確認 |
| `[フォント読み込み]エラー` | フォント未配置 | 指定パスにフォント配置 |

---

## 注意事項

- Ctrl+C で無限ループを停止可能（画面自動クリア）
- フォントは OFL ライセンスのものを使用
- I²C レベル変換モジュール必須（5V直結禁止）

---

## 更新履歴

- 2025-12-29: ライブラリ化・MVP化
