# セットアップガイド

このドキュメントでは、SSD1306 OLED 日本語表示サンプルの環境構築手順を説明します。

---

## 前提条件

- **Raspberry Pi 5**（Raspberry Pi OS Bookworm 以降）
- **インターネット接続**（ライブラリ・フォントのダウンロードに必要）
- **SSD1306 OLED モジュール**（I²C接続）とレベル変換モジュールが配線済み

---

## 1. I²C の有効化

Raspberry Pi で I²C 通信を使用するには、設定を有効にする必要があります。

### 1.1 設定画面を開く

```bash
sudo raspi-config
```

### 1.2 I²C を有効化

1. `3 Interface Options` を選択
2. `I5 I2C` を選択
3. `Yes` を選択して有効化
4. `Finish` で終了

### 1.3 再起動

```bash
sudo reboot
```

### 1.4 I²C デバイスの確認

再起動後、OLED が認識されているか確認します。

```bash
i2cdetect -y 1
```

**期待される出力例**:

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

`3c`（アドレス 0x3C）が表示されれば OK です。
`3d`（アドレス 0x3D）の場合もあります。

**表示されない場合**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md) の「1. `i2cdetect` でデバイスが見つからない」を参照してください。

---

## 2. プロジェクトの取得

### 2.1 作業ディレクトリへ移動

```bash
cd ~/work/project
```

### 2.2 リポジトリのクローン（初回のみ）

```bash
git clone <リポジトリURL>
cd 06-004-ssd1306-oled-jp-display
```

既にクローン済みの場合:

```bash
cd 06-004-ssd1306-oled-jp-display
```

---

## 3. Python 仮想環境の作成

Python の仮想環境を使用することで、システムの Python 環境を汚さずにライブラリを管理できます。

### 3.1 仮想環境の作成

プロジェクトのルートディレクトリで以下を実行します。

```bash
python3 -m venv venv
```

**コマンドの意味**:
- `python3 -m venv`: Python の仮想環境モジュールを実行
- `venv`: 作成する仮想環境のディレクトリ名

実行後、`venv` という名前のディレクトリが作成されます。

### 3.2 仮想環境の有効化

```bash
source venv/bin/activate
```

**成功すると**: プロンプトの先頭に `(venv)` が表示されます。

```
(venv) pi@raspberrypi:~/work/project/06-004-ssd1306-oled-jp-display $
```

この `(venv)` が表示されている間は、仮想環境内で作業していることを意味します。

### 3.3 pip のアップグレード（推奨）

pip（Python のパッケージ管理ツール）を最新版にアップグレードします。

```bash
pip install --upgrade pip
```

---

## 4. ライブラリのインストール

仮想環境が有効化された状態（プロンプトに `(venv)` が表示されている状態）で、必要なライブラリをインストールします。

### 4.1 luma.oled のインストール

SSD1306 OLED を制御するためのライブラリです。

```bash
pip install luma.oled
```

**インストール内容**:
- `luma.oled`: OLED ディスプレイ制御
- `luma.core`: luma シリーズの共通ライブラリ（自動でインストールされます）

### 4.2 Pillow のインストール

画像処理と日本語フォント描画に使用するライブラリです。

```bash
pip install pillow
```

**補足**: Pillow は luma.oled の依存ライブラリとして既にインストールされている場合がありますが、明示的にインストールしておくと確実です。

### 4.3 インストール確認

インストールされたライブラリを確認します。

```bash
pip list
```

以下のライブラリが一覧に表示されれば OK です:

| ライブラリ | 用途 |
|------------|------|
| `luma-oled` | SSD1306 OLED の制御 |
| `Pillow` | 画像処理・日本語フォント描画 |

---

## 5. 日本語フォントのダウンロード

日本語を OLED に表示するには、日本語対応フォントが必要です。

### 5.1 フォントディレクトリへ移動

```bash
cd assets/fonts/
```

### 5.2 フォントファイルのダウンロード

**Noto Sans CJK JP**（Google 提供の日本語フォント）をダウンロードします。

```bash
wget https://github.com/notofonts/noto-cjk/raw/main/Sans/OTF/Japanese/NotoSansCJKjp-Regular.otf
```

**補足**:
- ファイルサイズは約 16MB です
- ダウンロードに数分かかる場合があります

### 5.3 ライセンスファイルのダウンロード

フォントのライセンス文書（OFL: SIL Open Font License）も必ずダウンロードしてください。

```bash
wget https://raw.githubusercontent.com/notofonts/noto-cjk/main/Sans/LICENSE
```

### 5.4 ダウンロード確認

```bash
ls -lh
```

**期待される出力**:

```
-rw-r--r-- 1 pi pi 4.4K Jan  1 12:00 LICENSE
-rw-r--r-- 1 pi pi  16M Jan  1 12:00 NotoSansCJKjp-Regular.otf
-rw-r--r-- 1 pi pi 2.8K Jan  1 12:00 README.md
```

### 5.5 プロジェクトルートへ戻る

```bash
cd ../..
```

---

## 6. 動作確認

### 6.1 仮想環境の有効化を確認

プロンプトに `(venv)` が表示されていることを確認してください。
表示されていない場合は、再度有効化します。

```bash
source venv/bin/activate
```

### 6.2 固定表示サンプルの実行

```bash
cd src/
python simple_oled.py
```

**期待される出力**:

```
I²C初期化完了: アドレス 0x3C, ポート 1
OLED初期化完了: 128×64
コントラスト設定: 255 (最大)
フォント読み込み完了: ../assets/fonts/NotoSansCJKjp-Regular.otf, サイズ 18
表示完了
表示テキスト: 2行

表示を保持しています...
終了する場合は Ctrl+C を押してください
```

OLED に「こんにちは」「Raspberry Pi 5」と表示されれば成功です。

**停止方法**: `Ctrl + C`

### 6.3 スクロール表示サンプルの実行

```bash
python scroll_oled.py
```

**期待される出力**:

```
I²C初期化完了: アドレス 0x3C, ポート 1
OLED初期化完了: 128×64
コントラスト設定: 255 (最大)
フォント読み込み完了: ../assets/fonts/NotoSansCJKjp-Regular.otf, サイズ 16
スクロール開始: テキスト幅 850px
スクロール速度: 2px/フレーム, 間隔: 0.05秒
ループ回数: 3回
```

日本語テキストが右から左へスクロール表示されれば成功です。

---

## 7. 仮想環境の運用

### 7.1 仮想環境の有効化（毎回必要）

新しいターミナルを開くたびに、仮想環境を有効化する必要があります。

```bash
cd ~/work/project/06-004-ssd1306-oled-jp-display
source venv/bin/activate
```

有効化されると、プロンプトに `(venv)` が表示されます。

### 7.2 仮想環境の終了

作業が終わったら、仮想環境を終了できます。

```bash
deactivate
```

プロンプトから `(venv)` が消えます。

---

## セットアップ完了チェックリスト

- [ ] I²C が有効化されている
- [ ] `i2cdetect -y 1` で OLED が認識される（0x3C または 0x3D）
- [ ] 仮想環境 `venv/` が作成されている
- [ ] 仮想環境を有効化できる（`source venv/bin/activate`）
- [ ] `luma-oled` がインストールされている
- [ ] `Pillow` がインストールされている
- [ ] `assets/fonts/NotoSansCJKjp-Regular.otf` が配置されている
- [ ] `assets/fonts/LICENSE` が配置されている
- [ ] `simple_oled.py` で日本語が正しく表示される
- [ ] `scroll_oled.py` でスクロール表示が動作する

---

## トラブルシューティング

問題が発生した場合は、以下を参照してください。

- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)**: よくあるエラーと対処方法

### よくあるエラー

| エラー | 原因 | 対処 |
|--------|------|------|
| `ModuleNotFoundError: No module named 'luma'` | 仮想環境が有効でない、またはライブラリ未インストール | `source venv/bin/activate` を実行後、`pip install luma.oled` |
| `[Errno 121] Remote I/O error` | I²C 通信エラー | 配線とレベル変換モジュールを確認 |
| `cannot open resource` | フォントファイルが見つからない | フォントのダウンロードとパスを確認 |

---

## 参考情報

- **要件定義書**: [06-004-ssd_1306_oled_要件定義書（rev.md](../06-004-ssd_1306_oled_要件定義書（rev.md)
- **README**: [../README.md](../README.md)
- **luma.oled ドキュメント**: https://luma-oled.readthedocs.io/
- **Pillow ドキュメント**: https://pillow.readthedocs.io/

---

**作成日**: 2025-01-04
