import asyncio
import json
import random
import time
import discord
from discord.ext import commands
import redis
from grafana_api.grafana_face import GrafanaFace
import boto3

# Configurações
REDIS_HOST = 'redis'
GRAFANA_URL = 'http://grafana:3000'
RATE_LIMIT_DELAY = 1

intents = discord.Intents.default()
intents.guilds = True
intents.channels = True
intents.roles = True
bot = commands.Bot(command_prefix='!', intents=intents)

async def clone_role(guild, role, r, log_level):
    result = {'role_id': role.id, 'type': 'role', 'status': 'failed', 'data': None}
    try:
        if random.random() < 0.05:
            result['data'] = 'Worker failed (simulated)'
            return result
        new_role = await guild.create_role(
            name=role.name,
            permissions=role.permissions,
            colour=role.colour,
            hoist=role.hoist,
            mentionable=role.mentionable
        )
        result['status'] = 'success'
        result['data'] = f'Role {role.name} cloned'
        if log_level == 'detailed':
            result['details'] = {'permissions': str(role.permissions), 'color': str(role.colour)}
        time.sleep(RATE_LIMIT_DELAY)
    except Exception as e:
        result['data'] = str(e)
    return result

async def clone_channel(guild, channel, category, r, log_level):
    result = {'channel_id': channel.id, 'type': channel.type.name, 'status': 'failed', 'data': None}
    try:
        if random.random() < 0.05:
            result['data'] = 'Worker failed (simulated)'
            return result
        if isinstance(channel, discord.TextChannel):
            new_channel = await guild.create_text_channel(
                name=channel.name,
                category=category,
                topic=channel.topic,
                position=channel.position,
                permission_overwrites=channel.overwrites
            )
            result['status'] = 'success'
            result['data'] = f'Text channel {channel.name} cloned'
            if log_level == 'detailed':
                result['details'] = {'topic': channel.topic, 'overwrites': str(channel.overwrites)}
        elif isinstance(channel, discord.VoiceChannel):
            new_channel = await guild.create_voice_channel(
                name=channel.name,
                category=category,
                position=channel.position,
                permission_overwrites=channel.overwrites
            )
            result['status'] = 'success'
            result['data'] = f'Voice channel {channel.name} cloned'
            if log_level == 'detailed':
                result['details'] = {'overwrites': str(channel.overwrites)}
        time.sleep(RATE_LIMIT_DELAY)
    except Exception as e:
        result['data'] = str(e)
    return result

async def clone_category(guild, category, r, log_level):
    result = {'category_id': category.id, 'type': 'category', 'status': 'failed', 'data': None}
    try:
        if random.random() < 0.05:
            result['data'] = 'Worker failed (simulated)'
            return result
        new_category = await guild.create_category(
            name=category.name,
            position=category.position,
            permission_overwrites=category.overwrites
        )
        result['status'] = 'success'
        result['data'] = f'Category {category.name} cloned'
        if log_level == 'detailed':
            result['details'] = {'overwrites': str(category.overwrites)}
        time.sleep(RATE_LIMIT_DELAY)
        return new_category
    except Exception as e:
        result['data'] = str(e)
    return result

def integrate_with_cloud(data):
    s3 = boto3.client('s3')
    bucket = 'seu-bucket-autorizado'
    s3.put_object(Bucket=bucket, Key='disjorkdados_data.json', Body=json.dumps(data))
    print("Dados enviados para AWS S3.")

def create_grafana_dashboard(api_key, data):
    grafana = GrafanaFace(auth=api_key, host=GRAFANA_URL.replace('http://', ''))
    dashboard = {
        "dashboard": {
            "id": None,
            "uid": None,
            "title": "Hygark's DisjorkDados Dashboard",
            "panels": [{
                "id": 1,
                "title": "Cloning Results",
                "type": "graph",
                "targets": [{
                    "refId": "A",
                    "target": "disjorkdados_results"
                }],
                "datasource": "Prometheus"
            }],
            "schemaVersion": 30
        },
        "folderId": 0,
        "overwrite": True
    }
    grafana.dashboard.create_or_update_dashboard(dashboard)
    print("Dashboard criado no Grafana!")

def generate_chart(data):
    labels = [f"Item {d.get('role_id') or d.get('channel_id') or d.get('category_id')}" for d in data]
    values = [1 if d['status'] == 'success' else 0 for d in data]
    types = [d['type'] for d in data]
    
    chart_data = {
        "type": "bar",
        "data": {
            "labels": labels,
            "datasets": [
                {
                    "label": "Status (1=Success, 0=Failed)",
                    "data": values,
                    "backgroundColor": ["#1f77b4" if v == 1 else "#ff7f0e" for v in values],
                    "borderColor": ["#1f77b4" if v == 1 else "#ff7f0e" for v in values],
                    "borderWidth": 1
                },
                {
                    "label": "Item Type",
                    "data": [1 if t != 'unknown' else 0 for t in types],
                    "type": "line",
                    "borderColor": "#2ca02c",
                    "fill": False
                }
            ]
        },
        "options": {
            "scales": {
                "y": {
                    "beginAtZero": True,
                    "max": 1
                }
            },
            "plugins": {
                "title": {
                    "display": True,
                    "text": "Hygark's DisjorkDados Results (Categories, Channels, Roles)"
                }
            }
        }
    }
    
    with open('chart.html', 'w') as f:
        f.write("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Hygark's DisjorkDados Chart</title>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </head>
        <body>
            <canvas id="myChart" style="max-width: 800px;"></canvas>
            <script>
                const ctx = document.getElementById('myChart').getContext('2d');
                new Chart(ctx, %s);
            </script>
        </body>
        </html>
        """ % json.dumps(chart_data))
    print("Gráfico interativo salvo em chart.html")

async def main(token, source_id, dest_id, grafana_key, config=None):
    print("Iniciando Hygark's DisjorkDados")
    config = config or {}
    log_level = config.get('log_level', 'normal')
    order = config.get('order', 'roles,categories,channels').split(',')
    
    r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)
    
    await bot.start(token)
    source_guild = bot.get_guild(int(source_id))
    dest_guild = bot.get_guild(int(dest_id))
    
    if not source_guild or not dest_guild:
        print("Erro: Servidor origem ou destino não encontrado!")
        await bot.close()
        return
    
    # Enviar itens pra Redis
    for item_type in order:
        if item_type == 'roles':
            for role in source_guild.roles:
                if role.name != "@everyone":
                    r.rpush('roles', json.dumps({'role_id': role.id}))
        elif item_type == 'categories':
            for category in source_guild.categories:
                r.rpush('categories', json.dumps({'category_id': category.id}))
        elif item_type == 'channels':
            for channel in source_guild.channels:
                if not channel.category:
                    r.rpush('channels', json.dumps({'channel_id': channel.id}))
    
    # Processar clonagem
    results = []
    category_map = {}
    
    for item_type in order:
        if item_type == 'roles':
            for role in source_guild.roles:
                if role.name != "@everyone":
                    result = await clone_role(dest_guild, role, r, log_level)
                    results.append(result)
        elif item_type == 'categories':
            for category in source_guild.categories:
                result = await clone_category(dest_guild, category, r, log_level)
                results.append(result)
                if result['status'] == 'success':
                    new_category = next(c for c in dest_guild.categories if c.name == category.name)
                    category_map[category.id] = new_category
        elif item_type == 'channels':
            for channel in source_guild.channels:
                category = category_map.get(channel.category_id) if channel.category_id else None
                result = await clone_channel(dest_guild, channel, category, r, log_level)
                results.append(result)
    
    # Exportar
    with open('output.json', 'w') as f:
        json.dump(results, f)
    print("Dados salvos em output.json")
    
    # Gráfico
    generate_chart(results)
    
    # Grafana
    if grafana_key:
        create_grafana_dashboard(grafana_key, results)
    
    # Opcional: AWS
    # integrate_with_cloud(results)
    
    await bot.close()

if __name__ == '__main__':
    token = "YOUR_BOT_TOKEN"
    source_id = "YOUR_SOURCE_SERVER_ID"
    dest_id = "YOUR_DEST_SERVER_ID"
    grafana_key = ""
    config = {"order": "roles,categories,channels", "log_level": "normal"}
    asyncio.run(main(token, source_id, dest_id, grafana_key, config))