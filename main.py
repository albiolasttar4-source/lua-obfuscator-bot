import os
import discord
from discord.ext import commands
from obfuscator import LuaObfuscator
from dotenv import load_dotenv

load_dotenv()

# Bot setup with proper intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_messages = True

bot = commands.Bot(command_prefix='/', intents=intents)

# Initialize obfuscator
obfuscator = LuaObfuscator()

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is ready to use!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.event
async def on_error(event, *args, **kwargs):
    print(f'Error in {event}:', file=__import__('sys').stderr)
    import traceback
    traceback.print_exc()

@bot.tree.command(name="obfuscate", description="Obfuscate Lua code with advanced techniques")
async def obfuscate(interaction: discord.Interaction, code: str):
    """
    Obfuscate Lua code with multiple techniques:
    - Variable name randomization
    - String encryption
    - Remove comments and whitespace
    - Control flow flattening
    """
    await interaction.response.defer()
    
    try:
        obfuscated_code = obfuscator.obfuscate(code)
        
        # Check if code is too long for Discord embed
        if len(obfuscated_code) > 4096:
            # Create file
            with open('obfuscated_code.lua', 'w') as f:
                f.write(obfuscated_code)
            
            await interaction.followup.send(
                "✅ Code obfuscated successfully! (Output too large for embed)",
                file=discord.File('obfuscated_code.lua')
            )
            os.remove('obfuscated_code.lua')
        else:
            embed = discord.Embed(
                title="🔐 Lua Code Obfuscated",
                description="Your code has been obfuscated successfully!",
                color=discord.Color.green()
            )
            embed.add_field(name="Obfuscated Code", value=f"```lua\n{obfuscated_code}\n```", inline=False)
            embed.add_field(name="Original Length", value=f"{len(code)} characters", inline=True)
            embed.add_field(name="Obfuscated Length", value=f"{len(obfuscated_code)} characters", inline=True)
            
            await interaction.followup.send(embed=embed)
    
    except Exception as e:
        print(f"Error in obfuscate command: {e}")
        embed = discord.Embed(
            title="❌ Error",
            description=f"Failed to obfuscate code: {str(e)}",
            color=discord.Color.red()
        )
        await interaction.followup.send(embed=embed)

@bot.tree.command(name="help", description="Get help about available commands")
async def help_command(interaction: discord.Interaction):
    """Display help information"""
    embed = discord.Embed(
        title="📚 Lua Obfuscator Bot - Help",
        description="A powerful Discord bot for obfuscating Lua code",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="/obfuscate",
        value="Obfuscate your Lua code with advanced techniques:\n"
              "- Variable name randomization\n"
              "- String encryption\n"
              "- Whitespace and comment removal\n"
              "- Control flow flattening\n\n"
              "**Usage:** `/obfuscate <code>`",
        inline=False
    )
    
    embed.add_field(
        name="/help",
        value="Display this help message",
        inline=False
    )
    
    embed.add_field(
        name="Features",
        value="✅ Advanced obfuscation techniques\n"
              "✅ Fast processing\n"
              "✅ Support for large code files\n"
              "✅ Automatic output format selection",
        inline=False
    )
    
    embed.set_footer(text="Made with ❤️ | Lua Obfuscator Bot v1.0")
    
    await interaction.response.send_message(embed=embed)

# Run the bot
TOKEN = os.getenv('DISCORD_TOKEN')
if not TOKEN:
    print("ERROR: DISCORD_TOKEN environment variable is not set!")
    print("Please set DISCORD_TOKEN in your environment variables")
    exit(1)

try:
    bot.run(TOKEN)
except Exception as e:
    print(f"Failed to start bot: {e}")
    exit(1)
