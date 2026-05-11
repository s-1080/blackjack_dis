# 🎰 Discord Blackjack Bot

Discord上で手軽にブラックジャックが楽しめるエンタメBotです。ボタン操作で直感的に遊ぶことができます。

## ✨ 主な機能
- 🃏 **本格ルール**: ヒット（引く）やスタンド（勝負）をボタンで操作。
- 🎭 **リッチな演出**: ディーラーのターンや集計をリアルタイムに表示。
- 📊 **戦績管理**: 自分の累計勝敗数や勝率をいつでも確認可能。

## 🎮 スラッシュコマンド
| コマンド | 説明 |
|---------|------|
| `/blackjack` | 新しいゲームを開始します。 |
| `/stats` | あなたの通算戦績（勝率など）を表示します。 |

## 🛠️ 技術要件
- **Python**: 3.11+
- **Library**: discord.py
- **Infrastructure**: Docker / docker-compose

## 🔑 必要な権限 (Discord Bot)
- **テキストチャンネル権限**: メッセージを送信、埋め込みリンク（ゲーム画面の表示用）

## 📁 フォルダ構成
```
blackjack_dis/
├── main.py                  # エントリーポイント
├── discord_bot.py           # Discord UI/コマンド処理
├── blackjack_game.py        # ゲームロジック
├── Dockerfile
├── README.md                # 概要・技術ドキュメント
├── Tutorial.md              # ユーザー向けマニュアル
└── DEPLOY.md                # デプロイ手順（Git管理外）
```
