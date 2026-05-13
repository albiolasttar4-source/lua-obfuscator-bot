import os
import discord
from discord.ext import commands
from obfuscator import LuaObfuscator
from dotenv import load_dotenv
from flask import Flask, jsonify
import threading

load_dotenv()

# Flask app for Render health checks
app = Flask(__name__)

@app.route('/')
def health():
    return jsonify({"status": "Bot is running"}), 200

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

@bot.tree.command(name="obfuscate", description="Obfuscate Lua code with adjustable levels")
async def obfuscate(interaction: discord.Interaction, code: str, level: int = 1):
    """
    Obfuscate Lua code with multiple techniques and levels:
    - Level 1 (Normal): Basic obfuscation
    - Level 2 (Medium): Advanced obfuscation
    - Level 3 (Max): Maximum obfuscation
    """
    await interaction.response.defer()
    
    # Validate level
    if level not in [1, 2, 3]:
        embed = discord.Embed(
            title="❌ Invalid Level",
            description="Level must be 1 (Normal), 2 (Medium), or 3 (Max)",
            color=discord.Color.red()
        )
        await interaction.followup.send(embed=embed)
        return
    
    try:
        obfuscated_code = obfuscator.obfuscate(code, level=level)
        
        # Check if code is too long for Discord embed
        if len(obfuscated_code) > 4096:
            # Create file
            with open('obfuscated_code.lua', 'w') as f:
                f.write(obfuscated_code)
            
            level_names = {1: "Normal", 2: "Medium", 3: "Max"}
            await interaction.followup.send(
                f"✅ Code obfuscated successfully! (Level {level} - {level_names[level]})\n(Output too large for embed)",
                file=discord.File('obfuscated_code.lua')
            )
            os.remove('obfuscated_code.lua')
        else:
            level_names = {1: "Normal", 2: "Medium", 3: "Max"}
            embed = discord.Embed(
                title="🔐 Lua Code Obfuscated",
                description=f"Your code has been obfuscated successfully!\n**Level: {level} ({level_names[level]})**",
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
        value="Obfuscate your Lua code with adjustable levels:\n\n"
              "**Level 1 (Normal):**\n"
              "- Variable name randomization\n"
              "- Comment removal\n\n"
              "**Level 2 (Medium):**\n"
              "- Variable name randomization\n"
              "- String encryption\n"
              "- Comment & whitespace removal\n\n"
              "**Level 3 (Max):**\n"
              "- Variable name randomization\n"
              "- String encryption\n"
              "- Control flow flattening\n"
              "- Junk code injection\n"
              "- Maximum obfuscation\n\n"
              "**Usage:** `/obfuscate <code> [level]`\n"
              "**Default Level:** 1",
        inline=False
    )
    
    embed.add_field(
        name="/help",
        value="Display this help message",
        inline=False
    )
    
    embed.add_field(
        name="Features",
        value="✅ Multiple obfuscation levels\n"
              "✅ Fast processing\n"
              "✅ Support for large code files\n"
              "✅ Works with Roblox, Delta Executor, and other Lua interpreters\n"
              "✅ Automatic output format selection",
        inline=False
    )
    
    embed.set_footer(text="Made with ❤️ | Lua Obfuscator Bot v2.0")
    
    await interaction.response.send_message(embed=embed)

def run_flask():
    """Run Flask app on port 10000 for Render"""
    app.run(host='0.0.0.0', port=10000, debug=False)

# Run the bot
TOKEN = os.getenv('DISCORD_TOKEN')
if not TOKEN:
    print("ERROR: DISCORD_TOKEN environment variable is not set!")
    print("Please set DISCORD_TOKEN in your environment variables")
    exit(1)

try:
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Run the Discord bot
    bot.run(TOKEN)
except Exception as e:
    print(f"Failed to start bot: {e}")
    exit(1)
