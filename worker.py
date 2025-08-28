import redis
import json
import asyncio
import discord
from discord.ext import commands
import time

REDIS_HOST = 'redis'
RATE_LIMIT_DELAY = 1

intents = discord.Intents.default()
intents.guilds = True
intents.channels = True
intents.roles = True
bot = commands.Bot(command_prefix='!', intents=intents)

async def process_role(guild, role_data, r, log_level):
    # Similar à função create_role ou clone_role, mas processada em worker
    result = {'role_name': role_data['name'], 'type': 'role', 'status': 'failed', 'data': None}
    try:
        permissions = discord.Permissions(**{perm.strip(): True for perm in role_data.get('permissions', '').split(',') if perm.strip()}) if role_data.get('permissions') else discord.Permissions.none()
        new_role = await guild.create_role(
            name=role_data['name'],
            permissions=permissions,
            colour=discord.Colour(int(role_data.get('color', '#000000').replace('#', ''), 16)),
            hoist=role_data.get('hoist', False),
            mentionable=role_data.get('mentionable', False)
        )
        result['status'] = 'success'
        result['data'] = f'Role {role_data["name"]} created'
        if log_level == 'detailed':
            result['details'] = {'permissions': str(permissions), 'color': role_data.get('color')}
        time.sleep(RATE_LIMIT_DELAY)
    except Exception as e:
        result['data'] = str(e)
    return result

async def process_channel(guild, channel_data, category_map, r, log_level):
    # Similar à função create_channel ou clone_channel
    result = {'channel_name': channel_data['name'], 'type': channel_data['type'], 'status': 'failed', 'data': None}
    try:
        category = category_map.get(channel_data.get('category')) if channel_data.get('category') else None
        if channel_data['type'] == 'text':
            new_channel = await guild.create_text_channel(
                name=channel_data['name'],
                category=category,
                topic=channel_data.get('topic', ''),
                position=channel_data.get('position', 0)
            )
            result['status'] = 'success'
            result['data'] = f'Text channel {channel_data["name"]} created'
        elif channel_data['type'] == 'voice':
            new_channel = await guild.create_voice_channel(
                name=channel_data['name'],
                category=category,
                position=channel_data.get('position', 0)
            )
            result['status'] = 'success'
            result['data'] = f'Voice channel {channel_data["name"]} created'
        elif channel_data['type'] == 'forum':
            new_channel = await guild.create_forum_channel(
                name=channel_data['name'],
                category=category,
                topic=channel_data.get('topic', ''),
                position=channel_data.get('position', 0)
            )
            result['status'] = 'success'
            result['data'] = f'Forum channel {channel_data["name"]} created'
        elif channel_data['type'] == 'announcement':
            new_channel = await guild.create_text_channel(
                name=channel_data['name'],
                category=category,
                topic=channel_data.get('topic', ''),
                position=channel_data.get('position', 0),
                is_news=True
            )
            result['status'] = 'success'
            result['data'] = f'Announcement channel {channel_data["name"]} created'
        elif channel_data['type'] == 'stage':
            new_channel = await guild.create_stage_channel(
                name=channel_data['name'],
                category=category,
                position=channel_data.get('position', 0)
            )
            result['status'] = 'success'
            result['data'] = f'Stage channel {channel_data["name"]} created'
        if log_level == 'detailed':
            result['details'] = {'topic': channel_data.get('topic'), 'category': channel_data.get('category')}
        time.sleep(RATE_LIMIT_DELAY)
    except Exception as e:
        result['data'] = str(e)
    return result

async def process_category(guild, category_data, r, log_level):
    # Similar à função create_category ou clone_category
    result = {'category_name': category_data['name'], 'type': 'category', 'status': 'failed', 'data': None}
    try:
        new_category = await guild.create_category(
            name=category_data['name'],
            position=category_data.get('position', 0)
        )
        result['status'] = 'success'
        result['data'] = f'Category {category_data["name"]} created'
        if log_level == 'detailed':
            result['details'] = {'position': category_data.get('position')}
        time.sleep(RATE_LIMIT_DELAY)
        return new_category
    except Exception as e:
        result['data'] = str(e)
    return result

async def worker():
    r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)
    while True:
        try:
            item = r.blpop(['roles', 'categories', 'channels'], timeout=5)
            if not item:
                continue
            queue, data = item
            data = json.loads(data)
            guild = bot.get_guild(int(data.get('dest_id', 'YOUR_DEST_SERVER_ID')))
            log_level = data.get('log_level', 'normal')
            if queue == 'roles':
                result = await process_role(guild, data, r, log_level)
            elif queue == 'categories':
                result = await process_category(guild, data, r, log_level)
            elif queue == 'channels':
                result = await process_channel(guild, data, {}, r, log_level)
            r.rpush('results', json.dumps(result))
        except Exception as e:
            print(f"Worker error: {e}")
        time.sleep(0.1)

if __name__ == '__main__':
    asyncio.run(bot.start("YOUR_BOT_TOKEN"))
    asyncio.run(worker())