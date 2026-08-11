# LEGO Star Wars III: The Clone Wars — Beta Restoration Project

A community-driven effort to restore and run the 2011 promotional beta of **LEGO Star Wars III: The Clone Wars**, originally hosted on LucasArts.com. The game runs in the browser via [Ruffle](https://ruffle.rs/), a Flash emulator written in Rust/WebAssembly.

<img width="1223" height="928" alt="HomeScreenshot" src="https://github.com/user-attachments/assets/ed7642fe-cee6-4ad5-abd5-8fd28dfb4345" />

---

## Background

The beta was a browser-based Flash game available on the LucasArts website prior to the game's retail release in 2011. It featured a multiplayer hub world set aboard a Star Destroyer, where players could walk around, interact, and unlock characters. The original server infrastructure has long since been shut down.

This project restores as much of the original functionality as possible using a local Python server and Ruffle.

Correct Support Version: 1.2 (Not release out yet)

---

## File Structure

```
Server/
├── index.html              # Main HTML page (uses Ruffle)
├── index.jsp               # Original JavaServer page
├── server.py               # Local Python HTTP server
├── sfs_sniffer.py          # Custom Python multiplayer server (SmartFoxServer 1.x protocol)
├── run_websockify.py       # Installs (if needed) and runs the WebSocket-to-TCP bridge for multiplayer
├── GalaxyLoader.swf        # Original loader SWF
├── LSWIII.swf              # Main game SWF (modified)
├── config.xml              # Variables configuration
├── smartfox.json           # SmartFoxServer confiuration
├── favicon.ico
├── media/
│   ├── characters/
│   │   └── audio/
│   │       └── placeholder.swf              # Hollow temporary file
│   └── logos/
│       ├── esrb.png
│       ├── lucasarts.png
│       ├── ttgames.png
│       └── platforms.png
├── swf/
│   ├── LSWIII.swf          # Copy for GalaxyLoader
│   └── stardestroyer.swf   # Custom map SWF
└── xml/
    ├── config.xml          # Copy for GalaxyLoader
    ├── index.xml
    ├── characters.xml
    ├── achievements.xml
    └── stardestroyer.xml
```

---

**Requirements:** 
- Python 3
- Git (you don't need git if you getting repository from this site)
- WebSockify (optional if you hosting online multiplayer)

## How to Run Offline Server

```
Windows:
open terminal with UAC permissions (win + R, type: "cmd", ctrl + shift + enter)
git clone https://github.com/Nerart0/LSWBRestoration
cd LSWBRestoration/
python3 server.py

Linux/macOS:
git clone https://github.com/Nerart0/LSWBRestoration
cd LSWBRestoration/
sudo python3 server.py
```

## How to Run Online Server

```
Windows:
open terminal with UAC permissions (win + R, type: "cmd", ctrl + shift + enter)
git clone https://github.com/Nerart0/LSWBRestoration
cd LSWBRestoration/
python3 run_websockify.py
python3 sfs_sniffer.py (or "python -m websockify 8181 127.0.0.1:9339" command)
python3 server.py

Linux/macOS:
git clone https://github.com/Nerart0/LSWBRestoration
cd LSWBRestoration/
python3 run_websockify.py
python3 sfs_sniffer.py (or "python -m websockify 8181 127.0.0.1:9339" command)
sudo python3 server.py
```

Then open your browser and go to: `http://127.0.0.1:YourPort` or `http://0.0.0.0:YourPort` (port 80 by default)

> Once: T̶h̶e̶ ̶s̶e̶r̶v̶e̶r̶ ̶m̶u̶s̶t̶ ̶r̶u̶n̶ ̶o̶n̶ ̶p̶o̶r̶t̶ ̶8̶0̶ ̶(̶r̶o̶o̶t̶)̶ ̶b̶e̶c̶a̶u̶s̶e̶ ̶t̶h̶e̶ ̶g̶a̶m̶e̶ ̶h̶a̶r̶d̶c̶o̶d̶e̶s̶ ̶h̶t̶t̶p̶:̶/̶/̶l̶o̶c̶a̶l̶h̶o̶s̶t̶/̶c̶o̶n̶f̶i̶g̶.̶x̶m̶l. (v1.1)
> 
> Now: You can choose port for the server, do it using newest version of server.py. (v1.2)

> Once: Y̶o̶u̶ ̶d̶o̶n̶'̶t̶ ̶n̶e̶e̶d̶ ̶u̶s̶i̶n̶g̶ ̶o̶n̶l̶y̶ ̶p̶y̶t̶h̶o̶n̶ ̶a̶s̶ ̶a̶ ̶s̶e̶r̶v̶e̶r̶.̶ ̶O̶f̶f̶i̶c̶i̶a̶l̶l̶y̶,̶ ̶t̶h̶e̶ ̶g̶a̶m̶e̶ ̶r̶a̶n̶ ̶o̶n̶ ̶a̶ ̶J̶a̶v̶a̶ ̶s̶e̶r̶v̶e̶r. (v1.1)
> 
> Now: This project no longer uses the original Java SmartFoxServer — multiplayer is now handled by a custom Python server (`sfs_server.py`) that reimplements the legacy SmartFoxServer 1.x wire protocol. (v1.2)

<img width="1044" height="808" alt="MultiScreenshot" src="https://github.com/user-attachments/assets/dae75478-d35a-48fb-a14c-56d71aeb9bf2" />

---

## Known Issues / Not Yet Restored

- Character SWF files are missing — characters load as Clone Troopers only
- Character audio SWFs are missing — audio uses a silent placeholder
- Star Destroyer map textures are incomplete
- Collision zones not defined — player uses hardcoded floor position
- Multiplayer works via a custom Python SmartFoxServer-compatible implementation (`sfs_server.py`), not the original Java-based server — some edge cases of the original protocol may not be replicated
- Navigation bar highlights multiple tabs as active simultaneously when they share the same target planet (cosmetic, tied to `index.xml` link structure)
- Overlay SWFs (`Achievements.swf`, `Characters.swf`) are missing

---

## What Was Fixed 1.2 (Supported)

Notes 1.2:
- Multiplayer requires **three** processes running simultaneously: `server.py` (port 80), `sfs_sniffer.py` (port 9339), and `run_websockify.py` (port 8181). If any one of them isn't running, the game silently falls back to single-player/offline mode.
- If you don't need multiplayer, you can skip `sfs_sniffer.py` and `run_websockify.py` entirely — the game works fine offline.
- Player IDs (e.g. "CLONE 3") increase with each new connection and are never reused while the server is running — this matches the original game's behavior, not a bug.
- There is no more inactivity timeout — multiplayer connections stay open indefinitely, even if you're away from keyboard.
- On first load (empty browser cache), the level may take a few extra seconds to appear after the intro — this is normal asset loading (map SWF, textures), not a freeze.
- The intro can be skipped early via the on-screen "Skip" button; both the full intro and the skip path lead to the same transition.
- The online and offline version doesn't really work for microsoft edge browser, and you must type `127.0.0.1` instead of `0.0.0.0`.
- The server was tested by firefox 153.0.1 (64 bits) on fedora linux.

### Multiplayer Server
- Built a custom lightweight SmartFoxServer 1.x–compatible server (`sfs_server.py`) in Python, implementing the exact legacy XML-over-socket protocol used by `it.gotoandplay.smartfoxserver.SmartFoxClient` (decompiled and verified against `SysHandler`)
- Implements version check (`verChk`), login, room list, room creation/joining, user/room variables, and public message broadcasting (used for all player position/state sync)
- Added a WebSocket-to-TCP bridge (`websockify`) and Ruffle `socketProxy` configuration, since browsers can't open raw TCP sockets — required for `XMLSocket` to work at all under Ruffle's web build
- Fixed a room-deletion bug where re-joining the same room the player was already in would incorrectly delete and orphan the room, breaking further `joinRoom` requests
- Fixed the permanent "Lobby" room being deleted when empty, which caused all subsequent connections to receive an empty room list and silently fail to auto-join

### Multiplayer / Intro Timing
- Fixed a race condition between the intro cutscene and the (now near-instant, local) multiplayer connection: `LSWIII.onIntroComplete()`'s transition snapshot was being placed on top of an already-built live map, permanently freezing the screen — fixed by inserting it at display index 0 instead (`GalaxyViewer.placeContent`)
- Fixed the intro-skip button (`SiteIntro.skip`) never appearing, due to a typo (`visable` instead of `visible`) silently throwing and aborting `start()`
- Deferred `GalaxyViewer.connect()` until intro completion so multiplayer join/room-build doesn't visually race ahead of or behind the cutscene, in both full-intro and skip scenarios
- Fixed `IntroMusic`'s cue timing (`start`/`moral`/`moral_end`/`hit`), which relied on `Sound.position` — unreliable under Ruffle — by switching to a `getTimer()`-based clock
- Fixed premature multiplayer disconnects after ~5 seconds of player inactivity, caused by `int(Global.config.data.api.timeout)` reading `0` under Ruffle's E4X implementation; removed the auto-disconnect-on-idle behavior entirely
- Fixed offline (no multiplayer server) mode never triggering its fallback: `Galaxy.onConnectionLost()` only dispatched `CONNECTION_LOST`, never `CONNECTION_FAILED`, so `LSWIII` never fell back to single-player — now dispatches both when the connection never fully succeeded

### Ruffle E4X / JSON Compatibility Workarounds
- Worked around a Ruffle bug where `xml.children[0]`-style E4X access returned `null` despite valid XML (`LegoBox`/`characters.xml` loading), by rewriting the lookup to iterate children by `localName()`
- Worked around `JSON.parse()` returning `null` under Ruffle for `JSONLoader`/`smartfox.json`, by hardcoding the (single, local) server entry instead of parsing at runtime

### GalaxyLoader / LSWIII Bridging
- Added missing public properties (`configXML`, `googleTracker`, `nielsenTracker`) to `GalaxyLoader`, which `LSWIII.setupFromParent()` expected to read directly off its parent but were never exposed, causing `ReferenceError: Property ... not found`
- Fixed a `TypeError` in `LSWIII.setupFromParent()` where `Global.tracker` was assigned the raw `GalaxyLoader` instance instead of a proper `GalaxyTracker`, failing type coercion against `IGalaxyTracker`

### Player Identity
- Fixed `Galaxy.updateUser()` randomizing the player's displayed ID even when a real `player_id` of `0` was valid, causing the on-screen nametag to mismatch the HUD portrait
- Changed the offline fallback player ID from the original hardcoded `441482` to `0`, so single-player mode consistently shows "CLONE 0"

### Display / Rendering
- Fixed the game rendering at a fixed low internal resolution (960×660) and being CSS-scaled up, causing visible pixelation; `index.html` now lets Ruffle render at full native/device resolution (`scale: "showAll"`, `letterbox: "on"`) instead of a fixed-size canvas stretched via CSS `transform`

### Server Script
- Removed the hardcoded port 80 requirement from `server.py` — the game's `LSWIII.swf` had `http://localhost/config.xml` hardcoded internally (bypassing the relative path passed from `GalaxyLoader`), forcing port 80; fixed by patching `LSWIII.as` to load `xml/config.xml` as a relative path instead
- `server.py` now prompts on startup: "Use default port (80)? (y/n)" — if `n`, asks for a custom port instead, so the server no longer requires root/administrator privileges to run
- On startup, `server.py` now prints the server address and port, the serving directory, and the Python version

---

## What Was Fixed 1.1 (Non-Supported)

Notes 1.1:
- You can change resolution of web screen through enlarging window (CTRL + Scroll Up / Scroll Down).
- This version isn't more supported by this repository.
- The server was tested by firefox 153.0.1 (64 bits) on fedora linux.

### Server & Infrastructure
- Built a local Python HTTP server (`server.py`) with CORS headers to serve game files
- Fixed server working directory so files are served from the correct path
- Added `Cache-Control: no-store` headers to prevent stale file caching
- Restored `xml/config.xml` with all required fields including `<tracking>`, `<purchase>`, `<facebook>`, `<beta>` and `<planets>`

### Game Loading
- Restored `GalaxyLoader.swf` flow — the original loader that reads `xml/config.xml` and loads `LSWIII.swf`
- Fixed parameter name mismatch (`config` vs `configpath`) between the loader and the HTML
- Fixed XML parser crash caused by a newline inside `<intro>` tag

### Characters & Audio
- Added `audio` attribute to all entries in `characters.xml` (was missing, causing 404 on `media/characters/audio/.swf`)
- Set `audio="placeholder"` for all characters pointing to an existing placeholder SWF

### Map & Player
- Restored `com.lsw.maps.Map` class in `LSWIII.swf`:
  - Fixed `charHolder` not being added to the display hierarchy when no `view` MovieClip was passed
  - Fixed player spawn position using correct negative Y coordinates (Flash Y axis is inverted)
  - Fixed `updateCharacterZone()` fallback when no collision zones exist (`isSafe = true`, `floor = -370`)
- Fixed camera tracking — `GalaxyViewer.tick()` now correctly follows the player on both X and Y axes
- Fixed `map.y` being overwritten each frame by `(1 - scaleY) * height` — corrected the formula to account for player Y position

### Interface (UI)
- **Navigation bar**: Fixed `index.xml` structure — added proper `<title>` and `<link>` nodes instead of `<label>` and `<path>` so `Navigation` class renders correctly
- **Dropdown menus**: Added nested `<item>` elements to nav items so submenus slide out on hover
- **Footer**: Fixed `Footer` class to not block rendering when logo images (ESRB, LucasArts, TT Games) are missing — added `IOErrorEvent` fallback chain
- **Character panel**: Fixed `CharacterPanelContent.nextBadge()` crash when `view.parent` is null
- **Purchase message**: Fixed `PurchaseMessage` crash by adding `<purchase>` section to `config.xml`
- **Facebook message**: Fixed `FacebookMessage` crash by adding `<facebook><prompt>` and `<facebook><copy>` sections to `config.xml`
- **BETA badge**: Restored BETA badge on the logo by adding `<beta>true</beta>` to `config.xml`
- **Hologram sound**: Fixed hologram open sound — moved `playSound("hologramOpen")` from `onOverlayLoaded()` to `onAnimationComplete()` so it plays even when overlay SWF fails to load

### XML Configuration
- `config.xml` — restored all required sections
- `index.xml` — restored nav structure, footer, overlays
- `characters.xml` — added `audio` attribute to all characters
- `achievements.xml` — added placeholder achievement so the panel doesn't crash
- `stardestroyer.xml` — added planet definition with links

"1.0 version" it's just finded copy from [InternetArchive](https://archive.org/details/lswiii_202305) by Luna679.

---

## Tools Used

- [Ruffle](https://ruffle.rs/) — Flash emulator
- [JPEXS Free Flash Decompiler](https://github.com/jindrapetrik/jpexs-decompiler) — SWF decompilation and editing
- Python 3 — local HTTP server
- [WebSocket](https://github.com/websocket-client/websocket-client) - library servers and clients in python (optional if online)

---

## Credits

Original game by **TT Games** / **LucasArts**, published 2011.  
This is a fan preservation project with no commercial intent.

Need to talk? Discord: **nerart__** Or join server: [discord.gg/5fJbABgu7d](https://discord.gg/5fJbABgu7d)
