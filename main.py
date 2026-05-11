"""
Discord ブラックジャックBot メインエントリーポイント
"""
import discord_bot

if __name__ == "__main__":
    # Botを起動
    discord_bot.client.run(discord_bot.TOKEN)