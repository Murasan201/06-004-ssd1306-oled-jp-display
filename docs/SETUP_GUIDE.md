# SSD1306 OLED 日本語表示サンプル セットアップガイド

本書は、Raspberry Pi 5 と SSD1306 OLED を使用した日本語表示サンプルの実行環境を構築するための手順書です。

---

## 目次

1. [前提条件](#1-前提条件)
2. [ハードウェアの準備](#2-ハードウェアの準備)
3. [I²C の有効化](#3-i2c-の有効化)
4. [I²C デバイスの確認](#4-i2c-デバイスの確認)
5. [Python ライブラリのインストール](#5-python-ライブラリのインストール)
6. [日本語フォントの配置](#6-日本語フォントの配置)
7. [セットアップ完了の確認](#7-セットアップ完了の確認)
8. [動作確認](#8-動作確認)
9. [トラブルシューティング](#9-トラブルシューティング)

---

## 1. 前提条件

### 必要な機器

| 機器 | 説明 |
|------|------|
| Raspberry Pi 5 | Raspberry Pi OS（Bookworm 以降）インストール済み |
| SSD1306 OLED モジュール | I²C 接続、128×64 または 128×32 |
| I²C レベル変換モジュール | BSS138 方式など（5V OLED 使用時は必須） |
| ジャンパーワイヤー | オス-メス、オス-オスなど |
| ブレッドボード | 推奨 |

### ソフトウェア要件

| 項目 | バージョン |
|------|-----------|
| Python | 3.11 以降推奨 |
| OS | Raspberry Pi OS Bookworm 以降 |
| pip | 最新版推奨 |

---

## 2. ハードウェアの準備

### 重要な注意事項

**5V OLED を Raspberry Pi に直結しないでください**

- Raspberry Pi の GPIO は **3.3V** です
- 5V OLED と直結すると、通信できないだけでなく **GPIO を破損する可能性** があります
- **必ずレベル変換モジュール（BSS138方式）を使用** してください
- 3.3V 動作の OLED モジュールの使用を推奨します

### 配線図

#### レベル変換使用時（5V OLED の場合）

```
[Raspberry Pi 5]         [レベル変換]          [5V OLED]
Pin 1  (3.3V)  --------> LV
Pin 3  (GPIO2/SDA) ----> LV-SDA  ----> HV-SDA  ----> SDA
Pin 5  (GPIO3/SCL) ----> LV-SCL  ----> HV-SCL  ----> SCL
Pin 6  (GND)   --------> GND     <---- GND     <---- GND
                         HV      <---- VCC (5V)
```

#### 3.3V OLED の場合（レベル変換不要）

```
[Raspberry Pi 5]         [3.3V OLED]
Pin 1  (3.3V)  --------> VCC
Pin 3  (GPIO2/SDA) ----> SDA
Pin 5  (GPIO3/SCL) ----> SCL
Pin 6  (GND)   --------> GND
```

### GPIO ピン配置参考

| Pin番号 | 機能 | 用途 |
|--------|------|------|
| 1 | 3.3V | 電源（3.3V OLED）またはレベル変換 LV |
| 3 | GPIO2 | SDA（I²C データ） |
| 5 | GPIO3 | SCL（I²C クロック） |
| 6 | GND | グランド（共通） |

---

## 3. I²C の有効化

### 手順

1. ターミナルを開き、以下のコマンドを実行:

```bash
sudo raspi-config
```

2. メニューで以下を選択:
   - `3 Interface Options` を選択
   - `I5 I2C` を選択
   - `Yes` を選択して有効化
   - `Finish` で終了

3. 再起動:

```bash
sudo reboot
```

### 確認方法

再起動後、以下のコマンドで I²C が有効化されているか確認:

```bash
ls /dev/i2c*
```

**期待される出力**:
```
/dev/i2c-1
```

`/dev/i2c-1` が表示されれば、I²C は有効化されています。

**表示されない場合**:
- `raspi-config` で I²C を再度有効化してください
- `/boot/firmware/config.txt` に `dtparam=i2c_arm=on` が記載されているか確認してください

---

## 4. I²C デバイスの確認

OLED が正しく接続されているか確認します。

### 手順

以下のコマンドを実行:

```bash
i2cdetect -y 1
```

### 期待される出力

```
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- 3c -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
```

- `3c`（0x3C）が表示されれば OLED は正しく検出されています
- `3d`（0x3D）が表示される OLED モジュールもあります

### デバイスが表示されない場合

以下を確認してください:

1. **配線の確認**
   - SDA: GPIO2（Pin 3）に接続
   - SCL: GPIO3（Pin 5）に接続
   - GND: GND（Pin 6）に接続
   - VCC: 電源に接続

2. **レベル変換の確認**（5V OLED の場合）
   - LV 側: Raspberry Pi の 3.3V と GPIO
   - HV 側: OLED の電源電圧と SDA/SCL

3. **電源の確認**
   - OLED に電源が供給されているか確認

詳細は [TROUBLESHOOTING.md](TROUBLESHOOTING.md) を参照してください。

---

## 5. Python ライブラリのインストール

### 必要なライブラリ

| ライブラリ | 用途 |
|-----------|------|
| luma.oled | SSD1306 OLED 制御 |
| Pillow | 画像・テキスト描画 |

### インストールコマンド

```bash
pip install luma.oled pillow
```

### 確認方法

```bash
pip list | grep -E "luma|Pillow"
```

**期待される出力**:
```
luma.core        2.4.2
luma.oled        3.13.0
Pillow           10.2.0
```

バージョン番号は異なる場合があります。`luma.core`、`luma.oled`、`Pillow` の3つが表示されれば OK です。

### エラーが出た場合

#### pip3 を使う場合

```bash
pip3 install luma.oled pillow
```

#### 権限エラーの場合

```bash
pip install --user luma.oled pillow
```

#### 仮想環境を使用する場合

```bash
python3 -m venv venv
source venv/bin/activate
pip install luma.oled pillow
```

---

## 6. 日本語フォントの配置

日本語表示に必要なフォントをダウンロードして配置します。

### 使用フォント

| フォント | ライセンス | 備考 |
|---------|-----------|------|
| Noto Sans CJK JP | SIL Open Font License (OFL-1.1) | 商用利用可、推奨 |

### 手順

1. プロジェクトルートに移動:

```bash
cd /home/pi/work/project/kodansya/06-004-ssd1306-oled-jp-display
```

2. フォントディレクトリに移動:

```bash
cd assets/fonts/
```

3. フォントファイルをダウンロード:

```bash
wget https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTF/Japanese/NotoSansCJKjp-Regular.otf
```

4. ライセンスファイルをダウンロード:

```bash
wget https://raw.githubusercontent.com/googlefonts/noto-cjk/main/LICENSE
```

5. プロジェクトルートに戻る:

```bash
cd ../..
```

### 確認方法

```bash
ls -lh assets/fonts/
```

**期待される出力**:
```
-rw-r--r-- 1 pi pi 4.4K Dec 30 12:00 LICENSE
-rw-r--r-- 1 pi pi  16M Dec 30 12:00 NotoSansCJKjp-Regular.otf
-rw-r--r-- 1 pi pi 2.4K Dec 30 12:00 README.md
```

`NotoSansCJKjp-Regular.otf`（約16MB）が存在すれば OK です。

### 注意事項

- フォントファイルは約 16MB と大きいですが、日本語の全文字をカバーするために必要です
- ライセンスファイル（LICENSE）は必ず同梱してください

---

## 7. セットアップ完了の確認

すべてのセットアップが完了したか、一括で確認します。

### 確認スクリプト

プロジェクトルートで以下のコマンドを実行:

```bash
cd /home/pi/work/project/kodansya/06-004-ssd1306-oled-jp-display

echo "=========================================="
echo "セットアップ確認"
echo "=========================================="

# 1. I²C デバイスの確認
echo ""
echo "[1] I²C デバイス"
if i2cdetect -y 1 2>/dev/null | grep -qE "3c|3d"; then
    echo "    ✓ OLED 検出済み"
    i2cdetect -y 1 | grep -E "3c|3d"
else
    echo "    ✗ OLED 未検出"
fi

# 2. Python ライブラリの確認
echo ""
echo "[2] Python ライブラリ"
if python3 -c "import luma.oled" 2>/dev/null; then
    echo "    ✓ luma.oled インストール済み"
else
    echo "    ✗ luma.oled 未インストール"
fi

if python3 -c "from PIL import Image" 2>/dev/null; then
    echo "    ✓ Pillow インストール済み"
else
    echo "    ✗ Pillow 未インストール"
fi

# 3. フォントファイルの確認
echo ""
echo "[3] フォントファイル"
if [ -f "assets/fonts/NotoSansCJKjp-Regular.otf" ]; then
    echo "    ✓ フォント配置済み"
    ls -lh assets/fonts/NotoSansCJKjp-Regular.otf | awk '{print "      サイズ: " $5}'
else
    echo "    ✗ フォント未配置"
fi

echo ""
echo "=========================================="
```

### 期待される出力

```
==========================================
セットアップ確認
==========================================

[1] I²C デバイス
    ✓ OLED 検出済み
30: -- -- -- -- -- -- -- -- -- -- -- -- 3c -- -- --

[2] Python ライブラリ
    ✓ luma.oled インストール済み
    ✓ Pillow インストール済み

[3] フォントファイル
    ✓ フォント配置済み
      サイズ: 16M

==========================================
```

すべて ✓ が表示されれば、セットアップ完了です。

---

## 8. 動作確認

### サンプル1: スクロール表示（scroll_oled.py）

```bash
cd /home/pi/work/project/kodansya/06-004-ssd1306-oled-jp-display/src
python3 scroll_oled.py
```

**期待される動作**:
- OLED に「こんにちは Raspberry Pi！」が右から左へスクロール表示される
- 3回ループ後に自動終了
- コンソールに「スクロールテスト開始（3回ループ）」「テスト完了」と表示される

### サンプル2: 固定表示（simple_oled.py）

```bash
cd /home/pi/work/project/kodansya/06-004-ssd1306-oled-jp-display/src
python3 simple_oled.py
```

**期待される動作**:
- OLED に複数行の日本語テキストが固定表示される

### 停止方法

スクロール表示中に停止したい場合:
```
Ctrl + C
```

---

## 9. トラブルシューティング

### よくあるエラーと対処法

| エラー | 原因 | 対処法 |
|--------|------|--------|
| `ModuleNotFoundError: No module named 'luma'` | ライブラリ未インストール | `pip install luma.oled pillow` |
| `i2cdetect` でデバイス未検出 | 配線誤り、I²C 未有効化 | 配線確認、`raspi-config` で I²C 有効化 |
| `[Errno 121] Remote I/O error` | I²C 通信失敗 | 配線・レベル変換確認 |
| `cannot open resource` | フォント未配置 | フォントをダウンロード |
| 日本語が「□」になる | フォントパス誤り | `FONT_PATH` を確認 |
| `Permission denied: '/dev/i2c-1'` | i2c グループ未所属 | `sudo usermod -aG i2c $USER` |

### 詳細なトラブルシューティング

[TROUBLESHOOTING.md](TROUBLESHOOTING.md) を参照してください。

---

## セットアップ手順まとめ

| ステップ | 内容 | 確認コマンド |
|---------|------|-------------|
| 1 | ハードウェア接続 | 目視確認 |
| 2 | I²C 有効化 | `ls /dev/i2c*` |
| 3 | OLED 接続確認 | `i2cdetect -y 1` |
| 4 | ライブラリインストール | `pip list \| grep luma` |
| 5 | フォント配置 | `ls assets/fonts/*.otf` |
| 6 | 動作確認 | `python3 src/scroll_oled.py` |

---

## 参考資料

- [luma.oled ドキュメント](https://luma-oled.readthedocs.io/)
- [Pillow ドキュメント](https://pillow.readthedocs.io/)
- [Noto Fonts](https://fonts.google.com/noto)
- [Raspberry Pi I²C 設定](https://www.raspberrypi.com/documentation/computers/configuration.html)

---

**作成日**: 2025-12-30
**対象**: 初心者向け Raspberry Pi + OLED 日本語表示教材
