#!/usr/bin/env python3
"""
デバッグ用テストプログラム
OLEDの描画機能を段階的にテストします
要件定義書: 06-004-ssd_1306_oled_要件定義書（rev.md
"""

from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont
import time

# ========================================
# 設定（コード冒頭の定数で設定）
# ========================================

# ディスプレイ設定
WIDTH = 128  # 画面幅（ピクセル）
HEIGHT = 64  # 画面高さ（ピクセル）
I2C_ADDRESS = 0x3C  # I²Cアドレス（通常 0x3C または 0x3D）

# フォント設定
FONT_PATH = "../assets/fonts/NotoSansCJKjp-Regular.otf"  # フォントファイルのパス


def main():
    """
    メイン関数：OLED の段階的デバッグテスト（矩形・英数字・日本語）を実行
    """
    print("=" * 60)
    print("デバッグテスト開始")
    print("=" * 60)

    try:
        # I²Cインターフェースの初期化
        serial = i2c(port=1, address=I2C_ADDRESS)
        device = ssd1306(serial, width=WIDTH, height=HEIGHT)

        # コントラストを最大に設定（明るさ調整）
        device.contrast(255)
        print("✅ デバイス初期化完了\n")
    except Exception as e:
        print(f"[デバッグテスト]エラー: {e}")
        print("対処方法: I²C設定と配線を確認してください")
        print("ヒント: i2cdetect -y 1 でデバイスを確認")
        return 1

    # テスト1: 白い矩形を描画
    print("[テスト1] 白い矩形を描画")
    image = Image.new("1", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    # 矩形を描画（左上10,10 から 右下118,54）、塗りつぶしで白で表示
    draw.rectangle((10, 10, 118, 54), outline=255, fill=255)
    device.display(image)
    print("✅ 白い矩形を表示しました（3秒間）")
    time.sleep(3)

    # テスト2: デフォルトフォントでテキスト描画
    print("\n[テスト2] デフォルトフォントでテキスト描画")
    image = Image.new("1", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    # Pillowのデフォルトフォント（小さい）で英数字を描画
    draw.text((10, 10), "Test 123", fill=255)
    draw.text((10, 30), "ABC DEF", fill=255)
    device.display(image)
    print("✅ 英数字テキストを表示しました（3秒間）")
    time.sleep(3)

    # テスト3: 日本語フォントを読み込んで描画
    print("\n[テスト3] 日本語フォントで描画")
    try:
        font = ImageFont.truetype(FONT_PATH, 18)
        print(f"✅ フォント読み込み成功: {FONT_PATH}")
    except Exception as e:
        print(f"[デバッグテスト]エラー: {e}")
        print("対処方法: フォントファイルを確認してください")
        print("ヒント: 相対パスの場合、スクリプト実行ディレクトリからのパスを確認")
        return 1

    # Pillowで描画用の画像を作成
    # モード"1"は1ビット（白黒）画像
    image = Image.new("1", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)

    # 1行目：日本語テキストを描画
    draw.text((5, 10), "こんにちは", font=font, fill=255)
    print("   1行目: 'こんにちは' を (5, 10) に描画")

    # 2行目：英文字を描画
    draw.text((5, 36), "Raspberry Pi 5", font=font, fill=255)
    print("   2行目: 'Raspberry Pi 5' を (5, 36) に描画")

    # OLEDに表示
    device.display(image)
    print("✅ 日本語テキストを表示しました")

    print("\n" + "=" * 60)
    print("デバッグテスト完了")
    print("各テストで何が表示されたか確認してください")
    print("=" * 60)
    return 0

if __name__ == "__main__":
    exit(main())
