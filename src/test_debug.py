#!/usr/bin/env python3
"""
デバッグ用テストプログラム
OLEDの描画機能を段階的にテストします
"""

from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont
import time

WIDTH = 128
HEIGHT = 64
I2C_ADDRESS = 0x3C
FONT_PATH = "../assets/fonts/NotoSansCJKjp-Regular.otf"

def main():
    print("=" * 60)
    print("デバッグテスト開始")
    print("=" * 60)

    # デバイス初期化
    serial = i2c(port=1, address=I2C_ADDRESS)
    device = ssd1306(serial, width=WIDTH, height=HEIGHT)
    device.contrast(255)
    print("✅ デバイス初期化完了\n")

    # テスト1: 白い矩形を描画
    print("[テスト1] 白い矩形を描画")
    image = Image.new("1", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    draw.rectangle((10, 10, 118, 54), outline=255, fill=255)
    device.display(image)
    print("✅ 白い矩形を表示しました（3秒間）")
    time.sleep(3)

    # テスト2: デフォルトフォントでテキスト描画
    print("\n[テスト2] デフォルトフォントでテキスト描画")
    image = Image.new("1", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
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
        print(f"❌ フォント読み込み失敗: {e}")
        return

    image = Image.new("1", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)

    # 1行目
    draw.text((5, 10), "こんにちは", font=font, fill=255)
    print("   1行目: 'こんにちは' を (5, 10) に描画")

    # 2行目
    draw.text((5, 36), "Raspberry Pi 5", font=font, fill=255)
    print("   2行目: 'Raspberry Pi 5' を (5, 36) に描画")

    device.display(image)
    print("✅ 日本語テキストを表示しました")

    print("\n" + "=" * 60)
    print("デバッグテスト完了")
    print("各テストで何が表示されたか確認してください")
    print("=" * 60)

if __name__ == "__main__":
    main()
