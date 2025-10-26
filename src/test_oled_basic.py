#!/usr/bin/env python3
"""
OLED 基本動作テスト
画面全体を白で塗りつぶして、OLEDが正常に動作するか確認します
"""

from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image
import time

# ディスプレイ設定
WIDTH = 128
HEIGHT = 64
I2C_ADDRESS = 0x3C

def main():
    print("=" * 60)
    print("OLED 基本動作テスト")
    print("=" * 60)
    print()

    try:
        # I²C初期化
        serial = i2c(port=1, address=I2C_ADDRESS)
        print(f"✅ I²C初期化完了: アドレス 0x{I2C_ADDRESS:02X}")

        # SSD1306デバイス初期化
        device = ssd1306(serial, width=WIDTH, height=HEIGHT)
        print(f"✅ OLED初期化完了: {WIDTH}×{HEIGHT}")

        # コントラストを最大に設定
        device.contrast(255)
        print("✅ コントラスト設定: 255 (最大)")

        print()
        print("テスト1: 画面全体を白で塗りつぶします...")
        print("       → OLEDの全ピクセルが点灯するはずです")

        # 画面全体を白で塗りつぶす（全ピクセルON）
        image = Image.new("1", (WIDTH, HEIGHT), 255)
        device.display(image)

        print("✅ 白画面を表示しました")
        print()
        print("【確認】OLEDの画面全体が白く光っていますか？")
        print("   YES → OLEDは正常動作しています")
        print("   NO  → ハードウェアまたは配線に問題がある可能性")
        print()

        # 5秒待機
        print("5秒後に画面をクリアします...")
        time.sleep(5)

        print()
        print("テスト2: 画面をクリア（黒）します...")

        # 画面をクリア（全ピクセルOFF）
        device.clear()

        print("✅ 画面をクリアしました")
        print()
        print("【確認】OLEDの画面が真っ黒（消灯）になりましたか？")

    except Exception as e:
        print(f"❌ エラー: {e}")
        print()
        print("対処方法:")
        print("  1. I²C配線を確認してください")
        print("  2. i2cdetect -y 1 でデバイスが検出されるか確認")
        print("  3. OLEDの電源供給を確認")
        return 1

    print()
    print("=" * 60)
    print("テスト完了")
    print("=" * 60)
    return 0

if __name__ == "__main__":
    exit(main())
