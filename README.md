# Bard
Source Code for the Discord Bot of the Bardians Discord Server. If you're here to propose new Features, please open an Issue!

### Planned Features
- [ ] Currency Generation & Gambling 
- [ ] Minigames
- [ ] Administration Commands
- [ ] Twitch Stream Online / Offline Notifications
- [ ] Reddit Feed
- [ ] League Commands

### How it works
You need to export an environment variable called `DISCORD_TOKEN` which the bot will use to login, and one called `TWITCH_TOKEN` which is your Twitch API Client ID.

### Setup
*Dependencies:*
- discord.py, rewrite branch
- dataset
- stuf

Most importantly, enter your Discord Token in options.json. Without it, the Bot is not able to login.
Administrators and Moderators need to be supplied via the Arrays in options.json, refer to those as an example. Get their User ID via Discord Developer Mode and right click - Copy ID. 

### Questions, requests, anything?
Open an issue!
