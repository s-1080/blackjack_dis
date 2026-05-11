"""
Discord ブラックジャックBot
"""
import discord
from discord import app_commands
from discord.ui import Button, View
from blackjack_game import BlackjackGame

import os
from dotenv import load_dotenv

load_dotenv()

# Bot tokenを環境変数から読み込み
TOKEN = os.getenv("DISCORD_TOKEN", "your_discord_bot_token_here")

# Intents設定
intents = discord.Intents.default()
intents.message_content = True

# Clientの初期化
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# ゲーム状態を管理する辞書（ユーザーIDごと）
games = {}

# 戦績を管理する辞書（ユーザーIDごと）
# stats[user_id] = {"wins": 0, "losses": 0, "draws": 0}
stats = {}


class BlackjackView(View):
    """ブラックジャックのボタンUI"""
    
    def __init__(self, user_id: int):
        super().__init__(timeout=300)  # 5分でタイムアウト
        self.user_id = user_id
    
    @discord.ui.button(label="Hit（カードを引く）", style=discord.ButtonStyle.primary, emoji="🎴")
    async def hit_button(self, interaction: discord.Interaction, button: Button):
        """Hitボタンが押されたとき"""
        import asyncio
        
        # 本人確認
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("これはあなたのゲームではありません！", ephemeral=True)
            return
        
        # ゲーム取得
        game = games.get(self.user_id)
        if not game:
            await interaction.response.send_message("ゲームが見つかりません。`/blackjack` で新しいゲームを開始してください。", ephemeral=True)
            return
        
        # カードを引く
        game.player_hit()
        
        # ゲーム状態を更新
        if game.game_over:
            # ゲーム終了の場合は、最初から段階的に表示
            # 戦績を記録
            _record_game_result(self.user_id, game)
            
            # ディーラーの手札を見せる（まだ結果は表示しない）
            await interaction.response.edit_message(
                content=game.get_game_status(show_dealer_full=True, show_result=False) + "\n\n⏳ **ディーラーの手札を公開中...**",
                view=self
            )
            await asyncio.sleep(1.2)
            
            # 結果集計メッセージ
            await interaction.edit_original_response(
                content=game.get_game_status(show_dealer_full=True, show_result=False) + "\n\n⏳ **結果を集計中...**",
                view=self
            )
            await asyncio.sleep(1.5)
            
            # HitとStandを無効化、もう一度遊ぶを有効化
            self.children[0].disabled = True  # Hit
            self.children[1].disabled = True  # Stand
            self.children[2].disabled = False  # もう一度遊ぶ
            
            # 最終結果を表示（結果発表を含む）
            await interaction.edit_original_response(
                content=game.get_game_status(show_dealer_full=True, show_result=True),
                view=self
            )
        else:
            # ゲーム継続中の場合は、普通に表示
            await interaction.response.edit_message(
                content=game.get_game_status(),
                view=self
            )
    
    @discord.ui.button(label="Stand（勝負する）", style=discord.ButtonStyle.success, emoji="✋")
    async def stand_button(self, interaction: discord.Interaction, button: Button):
        """Standボタンが押されたとき"""
        import asyncio
        
        # 本人確認
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("これはあなたのゲームではありません！", ephemeral=True)
            return
        
        # ゲーム取得
        game = games.get(self.user_id)
        if not game:
            await interaction.response.send_message("ゲームが見つかりません。`/blackjack` で新しいゲームを開始してください。", ephemeral=True)
            return
        
        # まず「考え中...」のメッセージを表示
        await interaction.response.edit_message(
            content=game.get_game_status() + "\n\n⏳ **ディーラーのターン...**",
            view=self
        )
        
        # 演出: ディーラーがカードを引くまで少し待つ
        await asyncio.sleep(1.2)
        
        # スタンド → ディーラーターン → 勝敗判定
        game.player_stand()
        
        # 戦績を記録
        _record_game_result(self.user_id, game)
        
        # ディーラーの手札を公開（まだ結果は表示しない）
        await interaction.edit_original_response(
            content=game.get_game_status(show_dealer_full=True, show_result=False) + "\n\n⏳ **ディーラーの手札を公開中...**"
        )
        await asyncio.sleep(1.0)
        
        # 結果集計
        await interaction.edit_original_response(
            content=game.get_game_status(show_dealer_full=True, show_result=False) + "\n\n⏳ **結果を集計中...**"
        )
        await asyncio.sleep(1.5)
        
        # HitとStandを無効化、もう一度遊ぶを有効化
        self.children[0].disabled = True  # Hit
        self.children[1].disabled = True  # Stand
        self.children[2].disabled = False  # もう一度遊ぶ
        
        # 最終結果を表示（結果発表を含む）
        await interaction.edit_original_response(
            content=game.get_game_status(show_dealer_full=True, show_result=True),
            view=self
        )
    
    @discord.ui.button(label="もう一度遊ぶ", style=discord.ButtonStyle.secondary, emoji="🔄", disabled=True)
    async def restart_button(self, interaction: discord.Interaction, button: Button):
        """もう一度遊ぶボタンが押されたとき"""
        # 本人確認
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("これはあなたのゲームではありません！", ephemeral=True)
            return
        
        # 新しいゲームを作成
        game = BlackjackGame()
        game.deal_initial_cards()
        games[self.user_id] = game
        
        # 新しいビューを作成
        view = BlackjackView(self.user_id)
        
        # メッセージを更新
        await interaction.response.edit_message(
            content=f"🎰 **ブラックジャック開始！**\\n\\n{game.get_game_status()}",
            view=view
        )




def _record_game_result(user_id: int, game):
    """ゲーム結果を戦績に記録"""
    # 戦績辞書の初期化
    if user_id not in stats:
        stats[user_id] = {"wins": 0, "losses": 0, "draws": 0}
    
    # 勝敗を判定して記録（より正確に）
    result_msg = game.result_message
    
    if "プレイヤーの勝利" in result_msg:
        stats[user_id]["wins"] += 1
    elif "引き分け" in result_msg:
        stats[user_id]["draws"] += 1
    elif "ディーラーの勝利" in result_msg or "ディーラーがバースト" in result_msg:
        # ディーラーがバーストした場合はプレイヤーの勝ち
        if "ディーラーがバースト" in result_msg:
            stats[user_id]["wins"] += 1
        else:
            stats[user_id]["losses"] += 1
    elif "プレイヤーがバースト" in result_msg:
        stats[user_id]["losses"] += 1
    else:
        # 念のため、どれにも当てはまらない場合はログ出力（デバッグ用）
        print(f"未知の結果メッセージ: {result_msg}")


@tree.command(name="stats", description="あなたの勝敗記録を表示します")
async def stats_command(interaction: discord.Interaction):
    """戦績表示コマンド"""
    user_id = interaction.user.id
    
    # 戦績取得
    user_stats = stats.get(user_id, {"wins": 0, "losses": 0, "draws": 0})
    wins = user_stats["wins"]
    losses = user_stats["losses"]
    draws = user_stats["draws"]
    total = wins + losses + draws
    
    # 勝率計算
    win_rate = (wins / total * 100) if total > 0 else 0
    
    # 戦績表示
    stats_msg = "```\n"
    stats_msg += "╔════════════════════════════════╗\n"
    stats_msg += "║         📊 あなたの戦績 📊         ║\n"
    stats_msg += "╚════════════════════════════════╝\n"
    stats_msg += "```\n"
    stats_msg += f"**総試合数**: {total}試合\n"
    stats_msg += f"```\n"
    stats_msg += f"🎉 勝利: {wins}回\n"
    stats_msg += f"😢 敗北: {losses}回\n"
    stats_msg += f"🤝 引分: {draws}回\n"
    stats_msg += f"\n"
    stats_msg += f"勝率: {win_rate:.1f}%\n"
    stats_msg += "```"
    
    await interaction.response.send_message(stats_msg, ephemeral=False)


@tree.command(name="blackjack", description="ブラックジャックを開始します")
async def blackjack_command(interaction: discord.Interaction):
    """ブラックジャック開始コマンド"""
    user_id = interaction.user.id
    
    # 新しいゲームを作成
    game = BlackjackGame()
    game.deal_initial_cards()
    games[user_id] = game
    
    # ボタンUIを作成
    view = BlackjackView(user_id)
    
    # 初期状態を表示
    await interaction.response.send_message(
        content=f"🎰 **ブラックジャック開始！**\n\n{game.get_game_status()}",
        view=view
    )


@client.event
async def on_ready():
    """Bot起動時の処理"""
    await tree.sync()  # スラッシュコマンドを同期
    print(f"✅ {client.user} としてログインしました！")
    print(f"招待されているサーバー数: {len(client.guilds)}")


# Bot起動
if __name__ == "__main__":
    client.run(TOKEN)
