import asyncio
import json
import random
import time
import os
import discord
from discord.ext import commands
from main import clone_role, clone_channel, clone_category

REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
BOT_TOKEN = os.getenv('BOT_TOKEN')
SOURCE_SERVER = os.getenv('SOURCE_SERVER')
DEST_SERVER = os.getenv('DEST_SERVER')
WORKER_ID = random.randint(1, 1000)

intents = discord.Intents.default()
intents.guilds = True
intents.channels = True
intents.roles = True
bot = commands.Bot(command_prefix='!', intents=intents)

async def main():
    print(f"Worker {WORKER_ID} iniciado - Aguardando itens...")
    if not all([BOT_TOKEN, SOURCE_SERVER, DEST_SERVER]):
        print(f"Worker {WORKER_ID}: Variáveis de ambiente faltando!")
        return
    
    r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)
    await bot.start(BOT_TOKEN)
    
    source_guild = bot.get_guild(int(SOURCE_SERVER))
    dest_guild = bot.get_guild(int(DEST_SERVER))
    
    if not source_guild or not dest_guild:
        print(f"Worker {WORKER_ID}: Servidor origem ou destino não encontrado!")
        await bot.close()
        return
    
    category_map = {}
    
    while True:
        if random.random() < 0.05:
            print(f"Worker {WORKER_ID} reconectando (simulado)...")
            time.sleep(2)
            continue
        
        # Processar cargos
        role_data = r.lpop('roles')
        if role_data:
            role_id = json.loads(role_data)['role_id']
            role = discord.utils.get(source_guild.roles, id=role_id)
            if role:
                result = await clone_role(dest_guild, role, r, 'detailed')
                print(f"Worker {WORKER_ID} processou: {result}")
        
        # Processar categorias
        category_data = r.lpop('categories')
        if category_data:
            category_id = json.loads(category_data)['category_id']
            category = discord.utils.get(source_guild.categories, id=category_id)
            if category:
                result = await clone_category(dest_guild, category, r, 'detailed')
                print(f"Worker {WORKER_ID} processou: {result}")
                if result['status'] == 'success':
                    new_category = next(c for c in dest_guild.categories if c.name == category.name)
                    category_map[category.id] = new_category
        
        # Processar canais
        channel_data = r.lpop('channels')
        if channel_data:
            channel_id = json.loads(channel_data)['channel_id']
            channel = discord.utils.get(source_guild.channels, id=channel_id)
            if channel:
                category = category_map.get(channel.category_id) if channel.category_id else None
                result = await clone_channel(dest_guild, channel, category, r, 'detailed')
                print(f"Worker {WORKER_ID} processou: {result}")
        
        time.sleep(1)
    
    await bot.close()

if __name__ == '__main__':
    asyncio.run(main())