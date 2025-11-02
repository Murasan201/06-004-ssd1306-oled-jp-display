#!/usr/bin/env python3
"""
OLED 基本動作テスト
画面全体を白で塗りつぶして、OLEDが正常に動作するか確認します
要件定義書: 06-004-ssd_1306_oled_要件定義書（rev.md
"""

from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image
import time

# ========================================
# 設定（コード冒頭の定数で設定）
# ========================================

# ディスプレイ設定
WIDTH = 128  # 画面幅（ピクセル）
HEIGHT = 64  # 画面高さ（ピクセル）
I2C_ADDRESS = 0x3C  # I²Cアドレス（通常 0x3C または 0x3D）


def main():
    """
    メイン関数：OLED の基本動作テスト（白表示 → クリア）を実行
    """
    print("=" * 60)
    print("OLED 基本動作テスト")
    print("=" * 60)
    print()

    try:
        # I²Cインターフェースの初期化
        # Raspberry Pi 5ではポート1（GPIO2=SDA, GPIO3=SCL）を使用
        serial = i2c(port=1, address=I2C_ADDRESS)
        print(f"✅ I²C初期化完了: アドレス 0x{I2C_ADDRESS:02X}")

        # SSD1306デバイスの初期化
        # widthとheightは画面解像度に応じて設定
        device = ssd1306(serial, width=WIDTH, height=HEIGHT)
        print(f"✅ OLED初期化完了: {WIDTH}×{HEIGHT}")

        # コントラストを最大に設定（明るさ調整）
        device.contrast(255)
        print("✅ コントラスト設定: 255 (最大)")

        print()
        print("テスト1: 画面全体を白で塗りつぶします...")
        print("       → OLEDの全ピクセルが点灯するはずです")

        # 画面全体を白で塗りつぶす（全ピクセルON）
        # モード"1"は1ビット（白黒）画像、255は白を表す
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
        # 表示中のイメージをすべて消去
        device.clear()

        print("✅ 画面をクリアしました")
        print()
        print("【確認】OLEDの画面が真っ黒（消灯）になりましたか？")

    except Exception as e:
        print(f"[基本動作テスト]エラー: {e}")
        print()
        print("対処方法:")
        print("  1. I²C配線を確認してください")
        print("  2. i2cdetect -y 1 でデバイスが検出されるか確認")
        print("  3. OLEDの電源供給を確認")
        print()
        print("ヒント: レベル変換モジュールの配線確認（LV=3.3V, HV=OLED電源）")
        return 1

    print()
    print("=" * 60)
    print("テスト完了")
    print("=" * 60)
    return 0

if __name__ == "__main__":
    exit(main())
