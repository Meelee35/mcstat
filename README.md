# mcstat
A command-line tool to get Minecraft server info from your terminal.  
**Currently only supports Java Edition servers.**

## Features
- Display server MOTD with full colour formatting*
- Render server icon in the terminal with coloured blocks*
- Display server version, mods**, and plugins**
- Verbose mode for extra info and logging

\* Requires truecolor (24-bit colours) terminal emulator  
\** Depends on server response. May be unavailable.

## Usage
`mcstat [-h] [-v] [-i [SIZE]] [--version] host [port]`  

**Arguments**  
`host` - Server hostname or IP address  
`port` [optional] - Server port. Default (25565)  
**Options**  
`-h` `--help` - Show help message and exit  
`-v` `--verbose` - Show verbose output  
`-i [SIZE]` `--icon [SIZE]` - Show server icon instead of standard information. Default (16px)

### Examples
```bash
mcstat server.net 
mcstat play.myserver.net 12345
mcstat -i 64 minecraftserver.net 
mcstat -v play.survivalmode.net
```

## Installation
### Binaries (Linux Only)
Download the latest release from the [releases page](https://github.com/Meelee35/mcstat/releases), then:
```bash
chmod +x mcstat
./mcstat
```

### From source
#### Requirements
- Python 3.14+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

#### Building
```bash
git clone https://github.com/Meelee35/mcstat.git
cd mcstat
uv sync
uv run pyinstaller --onefile run.py --name mcstat
```

**Linux / MacOS**
```bash
./dist/mcstat
```
**Windows**
```cmd
dist\mcstat.exe
```

