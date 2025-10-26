#!/usr/bin/env python3
"""
SSD1306 OLED 日本語固定表示サンプル
Raspberry Pi 5とSSD1306搭載OLEDで日本語の複数行テキストを表示します
要件定義書: 06-004-ssd_1306_oled_要件定義書（rev.md
"""

import sys
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont

# ========================================
# 設定（コード冒頭の定数で設定）
# ========================================

# 表示するテキスト（複数行）
TEXT_LINES = [
    "こんにちは",
    "Raspberry Pi",
    "SSD1306 OLED"
]

# フォント設定
FONT_PATH = "../assets/fonts/NotoSansCJKjp-Regular.otf"  # フォントファイルのパス
FONT_SIZE = 12  # フォントサイズ（文字が収まらない場合は調整）

# レイアウト設定
MARGIN_X = 2   # 左右のマージン（ピクセル）
MARGIN_Y = 2   # 上下のマージン（ピクセル）
LINE_SPACING = 2  # 行間隔（ピクセル）

# ディスプレイ設定
WIDTH = 128   # 画面幅（128×64 または 128×32）
HEIGHT = 64   # 画面高さ
I2C_ADDRESS = 0x3C  # I²Cアドレス（通常 0x3C または 0x3D）


def main():
    """
    メイン関数：OLED初期化と日本語テキスト表示を実行
    """

    # I²Cインターフェースの初期化
    # Raspberry Pi 5ではポート1（GPIO2=SDA, GPIO3=SCL）を使用
    try:
        serial = i2c(port=1, address=I2C_ADDRESS)
        print(f"I²C初期化完了: アドレス 0x{I2C_ADDRESS:02X}, ポート 1")
    except Exception as e:
        print(f"[I²C初期化]エラー: {e}")
        print("対処方法: I²C設定と配線を確認してください")
        print("ヒント: raspi-config で I²C を有効化")
        print("ヒント: i2cdetect -y 1 でデバイスを確認")
        sys.exit(1)

    # SSD1306デバイスの初期化
    # widthとheightは画面解像度に応じて設定
    try:
        device = ssd1306(serial, width=WIDTH, height=HEIGHT)
        print(f"OLED初期化完了: {WIDTH}×{HEIGHT}")
    except Exception as e:
        print(f"[OLED初期化]エラー: {e}")
        print("対処方法: デバイスとの通信を確認してください")
        print("ヒント: レベル変換モジュールの配線確認（LV=3.3V, HV=OLED電源）")
        sys.exit(1)

    # Pillowで描画用の画像を作成
    # モード"1"は1ビット（白黒）画像
    image = Image.new("1", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)

    # 日本語フォントの読み込み
    try:
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
        print(f"フォント読み込み完了: {FONT_PATH}, サイズ {FONT_SIZE}")
    except IOError as e:
        print(f"[フォント読み込み]エラー: {e}")
        print(f"対処方法: フォントファイルを {FONT_PATH} に配置してください")
        print("ヒント: Noto Sans CJK JP などの OFL ライセンスフォントを使用")
        print("ヒント: 相対パスの場合、スクリプト実行ディレクトリからのパスを確認")
        sys.exit(1)

    # 複数行テキストの描画
    # 各行を左寄せで順次描画
    y_position = MARGIN_Y  # 描画開始Y座標

    for line_text in TEXT_LINES:
        # 現在の行のテキストを描画（左寄せ固定）
        draw.text((MARGIN_X, y_position), line_text, font=font, fill=255)

        # 次の行の描画位置を計算
        # フォントサイズ + 行間隔で次の行に移動
        y_position += FONT_SIZE + LINE_SPACING

        # 画面からはみ出す場合の警告（実行時に確認用）
        if y_position > HEIGHT:
            print(f"警告: テキストが画面からはみ出しています")
            print(f"対処方法: FONT_SIZE を小さくするか、TEXT_LINES を減らしてください")
            break

    # OLEDディスプレイに表示
    try:
        device.display(image)
        print("表示完了")
        print(f"表示テキスト: {len(TEXT_LINES)}行")
    except Exception as e:
        print(f"[表示]エラー: {e}")
        print("対処方法: デバイス接続を確認してください")
        sys.exit(1)


if __name__ == "__main__":
    main()
