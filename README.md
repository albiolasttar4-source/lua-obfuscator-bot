# Lua Obfuscator Discord Bot

A powerful Discord bot that obfuscates Lua code with advanced techniques to protect your scripts.

## Features

✅ **Advanced Obfuscation Techniques**
- Variable name randomization
- String encryption (Base64 encoded)
- Comment and whitespace removal
- Control flow flattening
- Junk code injection

✅ **Discord Integration**
- Slash commands (`/obfuscate`, `/help`)
- Embed-based responses
- Large file support (automatic file download for large outputs)
- Real-time processing

✅ **Easy Deployment**
- Ready for Render.com
- Environment variable configuration
- Minimal dependencies

## Commands

### `/obfuscate <code>`
Obfuscate your Lua code with all available techniques.

**Example:**
```
/obfuscate local x = 5; print(x)
```

**Output:** Obfuscated code with randomized variables, encrypted strings, and junk code.

### `/help`
Display help information and available commands.

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/albiolasttar4-source/lua-obfuscator-bot.git
cd lua-obfuscator-bot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Discord Bot Token

Create a `.env` file in the project root:
```
DISCORD_TOKEN=your_discord_bot_token_here
```

**How to get Discord Bot Token:**
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Go to "Bot" section
4. Click "Add Bot"
5. Copy the token under "TOKEN"

### 4. Run Locally
```bash
python main.py
```

## Deployment on Render.com

### 1. Push to GitHub
Make sure your code is pushed to your GitHub repository.

### 2. Connect to Render
1. Go to [Render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Fill in the details:
   - **Name:** `lua-obfuscator-bot`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python main.py`

### 3. Set Environment Variables
1. In Render dashboard, go to your service
2. Click "Environment"
3. Add new variable:
   - **Key:** `DISCORD_TOKEN`
   - **Value:** Your Discord bot token

### 4. Deploy
Click "Deploy" and wait for the bot to start!

## How It Works

### Obfuscation Process:

1. **Remove Comments & Whitespace**
   - Strips single-line comments (`--`)
   - Strips multi-line comments (`--[[ ]]`)
   - Removes excessive whitespace

2. **Encrypt Strings**
   - Converts string literals to Base64
   - Generates decryption code dynamically

3. **Randomize Variables**
   - Changes variable names to random strings
   - Preserves Lua keywords
   - Maintains code functionality

4. **Flatten Control Flow**
   - Adds junk code variables
   - Makes code harder to follow

5. **Compress**
   - Removes all unnecessary spaces
   - Creates compact, obfuscated output

### Example:

**Original Code:**
```lua
-- This is a simple function
local name = "Hello"
print(name)
```

**Obfuscated Code:**
```lua
local aKxYpQmN="SGVsbG8=";local bJzRtWnV=(function()local _s="SGVsbG8=";local _d="";for i=1,#_s,4 do _d=_d..string.char(tonumber(string.sub(_s,i,i+3)))end;return _d end)()print(bJzRtWnV)local _j5432=87
```

## Requirements

- Python 3.8+
- discord.py 2.3+
- python-dotenv 1.0+

## Troubleshooting

### Bot not responding?
- Check if bot token is correct
- Ensure bot has permissions in your Discord server
- Check bot status on Render dashboard

### Obfuscation not working?
- Make sure Lua code is valid
- Check if code doesn't exceed Discord message limits
- Large outputs will be sent as files

### Environment variables not working?
- Restart your Render service after adding env variables
- Use quotes around token if it contains special characters

## Support

For issues or questions:
1. Check the command help: `/help`
2. Verify bot permissions in Discord server
3. Check Render logs for errors

## License

MIT License - Feel free to modify and use!

## Disclaimer

This bot is for educational purposes. Use obfuscated code responsibly and respect copyright laws.

---

Made with ❤️ | Lua Obfuscator Bot v1.0
