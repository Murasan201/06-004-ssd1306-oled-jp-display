#!/usr/bin/env python3
"""
SSD1306 OLED 日本語スクロール表示サンプル
Raspberry Pi 5とSSD1306搭載OLEDで日本語テキストを横スクロール表示します
要件定義書: 06-004-ssd_1306_oled_要件定義書（rev.md
"""

import sys
import time
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont

# ========================================
# 設定（コード冒頭の定数で設定）
# ========================================

# スクロールするテキスト（1行）
SCROLL_TEXT = "こんにちは Raspberry Pi 5 で SSD1306 OLED を使った日本語スクロール表示のサンプルです"

# フォント設定
FONT_PATH = "../assets/fonts/NotoSansCJKjp-Regular.otf"  # フォントファイルのパス
FONT_SIZE = 16  # フォントサイズ

# スクロール設定
SCROLL_SPEED_PX = 2  # スクロール速度（ピクセル/フレーム）
FRAME_DELAY_SEC = 0.05  # フレーム間隔（秒）。小さいほど滑らか（0.05秒 = 20 FPS相当）
LOOP_COUNT = None  # ループ回数（None で無限ループ、整数で指定回数）

# レイアウト設定
MARGIN_Y = 24  # テキストの垂直位置（画面中央付近）

# ディスプレイ設定
WIDTH = 128   # 画面幅（128×64 または 128×32）
HEIGHT = 64   # 画面高さ
I2C_ADDRESS = 0x3C  # I²Cアドレス（通常 0x3C または 0x3D）


def main():
    """
    メイン関数：OLED初期化と日本語テキストのスクロール表示を実行
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

    # テキストの幅を事前に計算
    # getbbox() はテキストの境界ボックスを返す（left, top, right, bottom）
    dummy_image = Image.new("1", (1, 1))
    dummy_draw = ImageDraw.Draw(dummy_image)
    bbox = dummy_draw.textbbox((0, 0), SCROLL_TEXT, font=font)
    text_width = bbox[2] - bbox[0]  # right - left = テキストの幅

    print(f"スクロール開始: テキスト幅 {text_width}px")
    print(f"スクロール速度: {SCROLL_SPEED_PX}px/フレーム, 間隔: {FRAME_DELAY_SEC}秒")
    if LOOP_COUNT is not None:
        print(f"ループ回数: {LOOP_COUNT}回")
    else:
        print("ループ回数: 無限（Ctrl+C で終了）")

    # スクロール表示のメインループ
    x_position = WIDTH  # 画面右端から開始
    loop_counter = 0

    try:
        while True:
            # 新しい画像を作成（毎フレーム再描画）
            image = Image.new("1", (WIDTH, HEIGHT))
            draw = ImageDraw.Draw(image)

            # 現在位置にテキストを描画
            draw.text((x_position, MARGIN_Y), SCROLL_TEXT, font=font, fill=255)

            # OLEDに表示
            device.display(image)

            # スクロール位置を更新（右→左へ移動）
            x_position -= SCROLL_SPEED_PX

            # テキストが完全に画面外に出たら右端に戻す
            # テキスト全体が左端を通過したら（x + text_width < 0）リセット
            if x_position + text_width < 0:
                x_position = WIDTH
                loop_counter += 1

                # ループ回数が指定されている場合、カウントして終了判定
                if LOOP_COUNT is not None and loop_counter >= LOOP_COUNT:
                    print(f"スクロール完了: {loop_counter}回")
                    break

            # フレーム間隔待機
            time.sleep(FRAME_DELAY_SEC)

    except KeyboardInterrupt:
        # Ctrl+C で終了
        print("\nスクロール停止: ユーザー割り込み")
        # 画面をクリア
        device.clear()

    except Exception as e:
        print(f"[スクロール表示]エラー: {e}")
        print("対処方法: デバイス接続を確認してください")
        sys.exit(1)


if __name__ == "__main__":
    main()
