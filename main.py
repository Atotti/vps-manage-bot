import discord
from discord.ext import commands
import subprocess
import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# 環境変数からトークンを読み込む
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')


# Discord Botのセットアップ
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# サービスを制御する関数
def control_service(action, service_name):
    subprocess.run(['/usr/bin/sudo', 'systemctl', action, service_name], check=True)

def check_service_status(service_name):
    result = subprocess.run(['/usr/bin/sudo', 'systemctl', 'is-active', service_name], stdout=subprocess.PIPE, text=True)
    return result.stdout.strip()  # 'active', 'inactive', 'failed'などの状態を返す


# 生活鯖を起動するコマンド
@bot.command()
async def start_minecraft(ctx):
    # Palworldサーバーを停止
    control_service('stop', 'palworld-dedicated.service')
    # 人狼サーバーを停止
    control_service('stop', 'minecraft-werewolf.service')
    # 生活鯖を起動
    control_service('start', 'minecraft.service')
    await ctx.send('Minecraftサーバーを起動しました。')

# 人狼サーバーを起動するコマンド
@bot.command()
async def start_minecraft(ctx):
    # Palworldサーバーを停止
    control_service('stop', 'palworld-dedicated.service')
    # 生活鯖を停止
    control_service('stop', 'minecraft.service')
    # 人狼サーバーを起動
    control_service('start', 'minecraft-werewolf.service')
    await ctx.send('Minecraftサーバーを起動しました。')

# Palworldサーバーを起動するコマンド
@bot.command()
async def start_palworld(ctx):
    # 生活鯖を停止
    control_service('stop', 'minecraft.service')
    # 人狼サーバーを停止
    control_service('stop', 'minecraft-werewolf.service')
    # Palworldサーバーを起動
    control_service('start', 'palworld-dedicated.service')
    await ctx.send('Palworldサーバーを起動しました。')

# サービスの状態を確認するコマンド
@bot.command()
async def check_services(ctx):
    minecraft_status = check_service_status('minecraft.service')
    palworld_status = check_service_status('palworld-dedicated.service')
    wordwolf_status = check_service_status('minecraft-werewolf.service')
    
    message = f"Minecraftサーバーの状態: {minecraft_status}\nPalworldサーバーの状態: {palworld_status}\n 人狼サーバーの状態: {wordwolf_status}"
    await ctx.send(message)

# Botを起動
bot.run(DISCORD_BOT_TOKEN)
