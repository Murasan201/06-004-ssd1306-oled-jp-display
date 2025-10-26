#!/usr/bin/env python3
"""
OLED識別テストスクリプト
どちらのOLEDに表示されているかを確認するため、識別用メッセージを表示します
"""

import sys
import time
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont

# ディスプレイ設定
WIDTH = 128
HEIGHT = 64
I2C_ADDRESS = 0x3C
FONT_PATH = "../assets/fonts/NotoSansCJKjp-Regular.otf"
FONT_SIZE = 14

def display_test_message(port_number, message):
    """
    指定されたI²Cポートに識別メッセージを表示

    Args:
        port_number (int): I²Cポート番号
        message (str): 表示するメッセージ
    """
    try:
        # I²C初期化
        serial = i2c(port=port_number, address=I2C_ADDRESS)
        device = ssd1306(serial, width=WIDTH, height=HEIGHT)

        # 日本語フォント読み込み
        try:
            font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
        except IOError:
            print(f"⚠️ フォントが見つかりません: {FONT_PATH}")
            print("   デフォルトフォントを使用します（小さく表示されます）")
            font = ImageFont.load_default()

        # 画像作成
        image = Image.new("1", (WIDTH, HEIGHT))
        draw = ImageDraw.Draw(image)

        # 大きく見やすいテキストを表示
        draw.text((5, 5), message, font=font, fill=255)
        draw.text((5, 25), f"Port: {port_number}", font=font, fill=255)
        draw.text((5, 45), f"0x{I2C_ADDRESS:02X}", font=font, fill=255)

        # 表示
        device.display(image)
        print(f"✅ I2C-{port_number} (0x{I2C_ADDRESS:02X}) に表示しました")
        print(f"   メッセージ: {message}")

        return True

    except Exception as e:
        print(f"❌ I2C-{port_number} への表示に失敗: {e}")
        return False


def main():
    print("=" * 60)
    print("OLED 識別テスト")
    print("=" * 60)
    print()

    # I2C-1にテストメッセージを表示
    print("[テスト 1] I2C-1 (GPIO I2C) に識別メッセージを表示")
    print("-" * 60)
    display_test_message(1, "識別テスト")

    print()
    print("=" * 60)
    print("上記のメッセージがどちらのOLEDに表示されたか確認してください:")
    print("  1. プロジェクト用OLED (今回接続したもの)")
    print("  2. ケース付属のステータス表示OLED")
    print()
    print("両方に表示された場合:")
    print("  → 両方のOLEDが同じI²Cバス・同じアドレスに接続されています")
    print("  → どちらか一方のみに表示するには、物理的な配線変更または")
    print("     I²Cアドレスの変更が必要です")
    print("=" * 60)


if __name__ == "__main__":
    main()
