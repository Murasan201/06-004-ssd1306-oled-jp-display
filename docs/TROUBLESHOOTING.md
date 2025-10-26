# SSD1306 + Raspberry Pi 5 トラブルシューティング集

## 目的

本プロジェクトのサンプル実行時に発生したエラーや不具合と、確認手順・解決策を**すべて**集約します。

---

## よくある症状と対処

### 1. `i2cdetect -y 1` にデバイスが表示されない

**症状**:
```bash
$ i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
...
# 0x3C または 0x3D が表示されない
```

**原因候補**:
- I²C が無効化されている
- 配線誤り（SDA/SCL が逆、接続不良）
- レベル変換モジュールの LV/HV 誤接続
- OLED への電源未投入
- I²C アドレスの相違（0x3C/0x3D）
- OLED モジュールの故障

**確認手順**:
1. I²C が有効化されているか確認
   ```bash
   sudo raspi-config
   # 3 Interface Options → I5 I2C → Yes
   sudo reboot
   ```

2. 配線を図面どおりに再確認
   - SDA: GPIO2（Pin 3）
   - SCL: GPIO3（Pin 5）
   - GND: GND（共通）
   - レベル変換: LV=3.3V（Pi側）、HV=OLED電源電圧

3. レベル変換モジュールの接続確認
   - LV 側: Pi の 3.3V と GPIO2/3
   - HV 側: OLED の電源電圧（通常 3.3V または 5V）と SDA/SCL

4. OLED の電源供給確認（VCC に電圧が供給されているか）

5. I²C デバイス一覧を再確認
   ```bash
   ls /dev/i2c*
   # /dev/i2c-1 が表示されることを確認
   ```

**解決策**:
- 配線を修正
- アドレス定数を `I2C_ADDRESS = 0x3D` に変更して試行
- 別の OLED モジュールで試行（モジュール故障の可能性）

---

### 2. 実行時に `OSError: [Errno 121] Remote I/O error`

**症状**:
```
[I²C初期化]エラー: [Errno 121] Remote I/O error
```

**原因**:
- I²C 通信失敗（上記1と同系の原因）
- ケーブルが長すぎる（ノイズ・信号劣化）
- プルアップ抵抗の二重配置
- I²C クロックが高すぎる（デフォルト以外に設定した場合）

**確認手順**:
1. 上記「1. `i2cdetect -y 1` にデバイスが表示されない」の手順を実施
2. ケーブル長を短縮（15cm 以下を推奨）
3. I²C クロック設定を確認
   ```bash
   cat /boot/firmware/config.txt | grep i2c
   # dtparam=i2c_arm=on,i2c_arm_baudrate=100000
   ```

**解決策**:
- 配線・I²C設定の再確認
- ケーブル短縮
- I²C クロックを 100kHz に設定（`/boot/firmware/config.txt` に `dtparam=i2c_arm_baudrate=100000` を追加）

---

### 3. 日本語が「□（豆腐）」になる／文字化け

**症状**:
- OLED に表示されるが、日本語が「□」や「?」になる

**原因**:
- フォント未配置
- フォントファイルに該当文字が含まれていない（Latin フォントを使用している場合）
- フォントパスが誤っている

**確認手順**:
1. フォントファイルの存在確認
   ```bash
   ls -lh assets/fonts/NotoSansCJKjp-Regular.otf
   ```

2. フォントパスの確認（スクリプト内の `FONT_PATH` 定数）
   - `src/` から実行: `../assets/fonts/NotoSansCJKjp-Regular.otf`
   - ルートから実行: `assets/fonts/NotoSansCJKjp-Regular.otf`

**解決策**:
- `assets/fonts/` に Noto Sans CJK JP を配置
- `assets/fonts/README.md` の手順に従ってダウンロード
- フォントパスを実行ディレクトリに応じて調整

---

### 4. フォントが見つからない（`IOError: cannot open resource`）

**症状**:
```
[フォント読み込み]エラー: cannot open resource
```

**原因**:
- フォントファイルパスの誤り
- 相対パスの基準が異なる
- ファイル権限不足
- フォントファイルが存在しない

**確認手順**:
1. フォントファイルの存在と権限を確認
   ```bash
   ls -l assets/fonts/NotoSansCJKjp-Regular.otf
   # -rw-r--r-- のように読み取り権限があることを確認
   ```

2. スクリプトの実行ディレクトリを確認
   ```bash
   pwd
   # どのディレクトリから実行しているかを確認
   ```

3. 絶対パスで試行
   ```python
   FONT_PATH = "/home/pi/work/project/06-004-ssd1306-oled-jp-display/assets/fonts/NotoSansCJKjp-Regular.otf"
   ```

**解決策**:
- フォントファイルをダウンロード（`assets/fonts/README.md` 参照）
- 相対パスを実行ディレクトリに合わせて修正
- ファイル権限を付与
  ```bash
  chmod 644 assets/fonts/NotoSansCJKjp-Regular.otf
  ```

---

### 5. スクロールがカクつく／速すぎる

**症状**:
- スクロール表示がスムーズでない
- スクロール速度が期待と異なる

**原因**:
- フレーム間隔（`FRAME_DELAY_SEC`）が大きすぎる → カクつく
- スクロール速度（`SCROLL_SPEED_PX`）が大きすぎる → 速すぎる
- Raspberry Pi の負荷が高い

**確認手順**:
1. 現在の設定値を確認（`scroll_oled.py` の定数）
   ```python
   SCROLL_SPEED_PX = 2
   FRAME_DELAY_SEC = 0.05
   ```

2. Raspberry Pi の CPU 使用率を確認
   ```bash
   top
   ```

**解決策**:
- カクつく場合: `FRAME_DELAY_SEC` を小さくする（例: 0.05 → 0.03）
- 速すぎる場合: `SCROLL_SPEED_PX` を小さくする（例: 2 → 1）
- 滑らかさ優先: `FRAME_DELAY_SEC = 0.03`, `SCROLL_SPEED_PX = 1`
- バランス重視: `FRAME_DELAY_SEC = 0.05`, `SCROLL_SPEED_PX = 2`（デフォルト）

---

### 6. 文字が画面からはみ出す

**症状**:
```
警告: テキストが画面からはみ出しています
```

**原因**:
- フォントサイズ（`FONT_SIZE`）が大きすぎる
- 表示する行数（`TEXT_LINES`）が多すぎる
- 行間隔（`LINE_SPACING`）が大きい

**確認手順**:
1. 現在の設定を確認
   ```python
   FONT_SIZE = 12
   LINE_SPACING = 2
   TEXT_LINES = ["行1", "行2", "行3"]  # 3行
   ```

2. 必要な高さを計算
   ```
   必要高さ = MARGIN_Y + (FONT_SIZE + LINE_SPACING) × 行数
   ```

**解決策**:
- `FONT_SIZE` を小さくする（例: 12 → 10）
- `TEXT_LINES` の行数を減らす
- `LINE_SPACING` を小さくする（例: 2 → 1）
- 128×32 画面の場合は特に注意（高さが半分）

---

### 7. 画面に何も表示されない

**症状**:
- エラーは出ないが、OLED に何も表示されない
- バックライトだけ点灯している（該当機種のみ）

**原因**:
- 画面サイズ設定（`WIDTH`, `HEIGHT`）の誤り
- テキストが画面外に描画されている
- コントラスト設定が低い（一部モジュール）

**確認手順**:
1. 画面サイズを確認
   ```python
   WIDTH = 128
   HEIGHT = 64  # または 32
   ```

2. テキスト位置を確認
   ```python
   MARGIN_X = 2
   MARGIN_Y = 2
   ```

3. 簡易テストスクリプトを実行
   ```python
   # 画面全体を白で塗りつぶして表示確認
   image = Image.new("1", (WIDTH, HEIGHT), 255)
   device.display(image)
   ```

**解決策**:
- モジュールの実際の解像度に合わせて `WIDTH`, `HEIGHT` を修正
- テキスト描画位置を画面内に調整
- **コントラスト設定を追加**（重要！）:
  ```python
  device = ssd1306(serial, width=WIDTH, height=HEIGHT)
  device.contrast(255)  # 最大の明るさに設定
  ```

**補足**:
- 一部のSSD1306モジュールではコントラスト設定が必須です
- デフォルトのコントラスト値が低く、表示が見えない場合があります
- `device.contrast(255)` で最大の明るさに設定することを推奨

---

### 8. `ImportError: No module named 'luma.oled'` / `'PIL'`

**症状**:
```
ImportError: No module named 'luma.oled'
ImportError: No module named 'PIL'
```

**原因**:
- 必要なライブラリがインストールされていない

**確認手順**:
```bash
pip list | grep luma
pip list | grep Pillow
```

**解決策**:
```bash
pip install luma.oled pillow
# または
pip3 install luma.oled pillow
```

---

### 9. 権限エラー（`PermissionError: [Errno 13] Permission denied`）

**症状**:
```
PermissionError: [Errno 13] Permission denied: '/dev/i2c-1'
```

**原因**:
- ユーザーが `i2c` グループに所属していない

**確認手順**:
```bash
groups
# i2c が含まれているか確認
```

**解決策**:
```bash
sudo usermod -aG i2c $USER
# 再ログインまたは再起動
sudo reboot
```

---

### 10. レベル変換なしで 5V OLED を接続して動かない

**症状**:
- 配線したが動作しない
- I²C デバイスが検出されない

**原因**:
- Raspberry Pi の GPIO は 3.3V のため、5V OLED と直結すると通信できない
- **最悪の場合、GPIO が破損する可能性**

**解決策**:
- **必ずレベル変換モジュール（BSS138 方式など）を使用**
- 3.3V 動作の OLED を使用する（推奨）

**配線例**（レベル変換使用）:
```
[Raspberry Pi 5]       [レベル変換]        [5V OLED]
3.3V    ------------>  LV
GPIO2(SDA) --------->  LV-SDA  ---->  HV-SDA  ----> SDA
GPIO3(SCL) --------->  LV-SCL  ---->  HV-SCL  ----> SCL
GND     ------------>  GND     <----  GND     <---- GND
                       HV      <----  VCC (5V)
```

---

### 11. プログラム終了後すぐに画面がクリアされる

**症状**:
- プログラムは正常に実行されるが、表示がすぐに消える
- 一瞬表示されるが見えない

**原因**:
- Pythonプログラムが終了すると、一部の環境では画面が自動的にクリアされる
- 表示後にプログラムがすぐに終了している

**解決策**:
表示後に待機処理を追加する:

```python
import time

# 表示後に待機
device.display(image)
print("表示完了")

# 無限ループで表示を保持
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("終了します")
    device.clear()
```

または、指定時間だけ表示:
```python
device.display(image)
time.sleep(10)  # 10秒間表示
device.clear()
```

---

### 12. 複数のOLEDが同じI²Cバスに接続されている

**症状**:
- 複数のOLED（例：プロジェクト用とケース付属）に同じ内容が表示される
- 意図しないOLEDにも表示される

**原因**:
- 複数のOLEDが同じI²Cバス、同じアドレス（0x3C）に接続されている
- I²Cは同一バス・同一アドレスのデバイスを区別できない

**確認手順**:
```bash
i2cdetect -y 1
# 0x3C が1つだけ検出される場合、複数デバイスが同じアドレスを使用
```

**解決策**:

**方法A**: 両方に表示されることを許容する
- ケースのステータス表示機能を使用していない場合、そのまま使用可能
- 特に問題がなければ対応不要

**方法B**: I²Cアドレスを変更する
- プロジェクト用OLEDのアドレスを 0x3C → 0x3D に変更
- モジュール裏面の「ADDR」または「SA0」のジャンパー/ハンダパッドを変更
- スクリプトの定数を修正:
  ```python
  I2C_ADDRESS = 0x3D  # 変更後のアドレス
  ```

**方法C**: ケースOLEDを無効化
- ケース付属OLEDの制御サービスを停止
- または物理的に配線を外す

---

## 変更履歴

- 2025-10-26: 初版作成
- 2025-10-26: コントラスト設定、プログラム終了問題、複数OLED問題を追加
- 今後、新しいエラーが発生した場合は随時追記
