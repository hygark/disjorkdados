import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.guilds = True
intents.channels = True
intents.roles = True
bot = commands.Bot(command_prefix='!', intents=intents)

async def create_role(guild, role_data):
    try:
        await guild.create_role(
            name=role_data['name'],
            permissions=discord.Permissions.none(),
            colour=discord.Colour.from_str(role_data.get('color', '#000000')),
            hoist=False,
            mentionable=False
        )
        print(f"Role {role_data['name']} created")
    except Exception as e:
        print(f"Error creating role {role_data['name']}: {e}")

async def create_category(guild, category_data):
    try:
        new_category = await guild.create_category(
            name=category_data['name'],
            position=category_data.get('position', 0)
        )
        print(f"Category {category_data['name']} created")
        return new_category
    except Exception as e:
        print(f"Error creating category {category_data['name']}: {e}")
        return None

async def create_channel(guild, channel_data, category_map):
    try:
        category_name = channel_data.get('category')
        category = category_map.get(category_name) if category_name else None
        if channel_data['type'] == 'text':
            await guild.create_text_channel(
                name=channel_data['name'],
                category=category,
                topic=channel_data.get('topic', ''),
                position=channel_data.get('position', 0)
            )
            print(f"Text channel {channel_data['name']} created")
        elif channel_data['type'] == 'voice':
            await guild.create_voice_channel(
                name=channel_data['name'],
                category=category,
                position=channel_data.get('position', 0)
            )
            print(f"Voice channel {channel_data['name']} created")
        # Adicione outros tipos (forum, stage, etc.) se necessário
    except Exception as e:
        print(f"Error creating channel {channel_data['name']}: {e}")

async def create_server(token, config, automated=False):
    bot = commands.Bot(command_prefix='!', intents=intents)
    await bot.login(token)
    guild = await bot.create_guild(name=config['name'])
    
    category_map = {}
    # Criar categorias
    for category_data in config.get('categories', []):
        new_category = await create_category(guild, category_data)
        if new_category:
            category_map[category_data['name']] = new_category
    
    # Criar canais
    for channel_data in config.get('channels', []):
        await create_channel(guild, channel_data, category_map)
    
    # Criar roles
    for role_data in config.get('roles', []):
        await create_role(guild, role_data)
    
    if automated:
        # Estrutura automatizada (exemplo)
        await guild.create_text_channel("geral")
        await guild.create_role(name="membro")
    
    print(f"Servidor '{config['name']}' criado com sucesso!")
    await bot.close()

if __name__ == '__main__':
    # Exemplo de config manual
    config = {
        "name": "Novo Servidor",
        "categories": [{"name": "Geral", "position": 0}],
        "channels": [{"name": "bem-vindo", "type": "text", "category": "Geral", "topic": "Bem-vindo!", "position": 0}],
        "roles": [{"name": "Membro", "color": "#00ff00"}]
    }
    token = "SEU_TOKEN_AQUI"
    asyncio.run(create_server(token, config, automated=False))