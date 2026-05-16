# LEGO Star Wars III: The Clone Wars — Beta Restoration Project

A community-driven effort to restore and run the 2011 promotional beta of **LEGO Star Wars III: The Clone Wars**, originally hosted on LucasArts.com. The game runs in the browser via [Ruffle](https://ruffle.rs/), a Flash emulator written in Rust/WebAssembly.

---

## Background

The beta was a browser-based Flash game available on the LucasArts website prior to the game's retail release in 2011. It featured a multiplayer hub world set aboard a Star Destroyer, where players could walk around, interact, and unlock characters. The original server infrastructure has long since been shut down.

This project restores as much of the original functionality as possible using a local Python server and Ruffle.

---

## What Was Fixed

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

---

## File Structure

```
Server/
├── index.html              # Main HTML page (uses Ruffle)
├── index.jsp               # Original JavaServer page
├── server.py               # Local Python HTTP server
├── GalaxyLoader.swf        # Original loader SWF
├── LSWIII.swf              # Main game SWF (modified)
├── config.xml              # Variables configuration
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
    ├── stardestroyer.xml
    └── smartfox.json
```

---

## How to Run

**Requirements:** Python 3

```bash
cd Server/
sudo python3 server.py
```

Then open your browser and go to: `http://127.0.0.1`

> The server must run on port 80 (root) because the game hardcodes `http://localhost/config.xml`.

---

## Known Issues / Not Yet Restored

- Character SWF files are missing — characters load as Clone Troopers only
- Character audio SWFs are missing — audio uses a silent placeholder
- Star Destroyer map textures are incomplete
- Collision zones not defined — player uses hardcoded floor position
- SmartFox multiplayer server not running — game runs in single-player offline mode
- Overlay SWFs (`Achievements.swf`, `Characters.swf`) are missing

---

## Tools Used

- [Ruffle](https://ruffle.rs/) — Flash emulator
- [JPEXS Free Flash Decompiler](https://github.com/jindrapetrik/jpexs-ffdec) — SWF decompilation and editing
- Python 3 — local HTTP server

---

## Credits

Original game by **TT Games** / **LucasArts**, published 2011.  
This is a fan preservation project with no commercial intent.

Need to talk? Email: devkacper80@gmail.com Discord: **nerart__**
