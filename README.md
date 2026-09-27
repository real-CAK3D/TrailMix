# Trail Mix

Maple and Herbie's monthly outdoors magazine for Lewiston and the rest of Maine: the cover story, real trail picks, the MapPI3 trip log, gear worth a look, what the season is doing, and Herbie's column. Salty, sweet, a little nutty.

Part of the Garden's papers, all read through **[The Corner Chronicle](https://github.com/real-CAK3D/NewsStand)** — one home-screen app that mounts every paper under one private (Tailscale-only) HTTPS address: [The Double Wide](https://github.com/real-CAK3D/TheDoubleWide) (daily), [The Re-Up](https://github.com/real-CAK3D/TheRe-Up) (want ads), [The Sunday Smoke](https://github.com/real-CAK3D/TheSundaySmoke) (Sundays), [Roach Clips](https://github.com/real-CAK3D/RoachClips) (Tuesdays), [The Green Thumb](https://github.com/real-CAK3D/TheGreenThumb) (the directory), [Dime Bags](https://github.com/real-CAK3D/DimeBags), [Trail Mix](https://github.com/real-CAK3D/TrailMix), [Dab Magazine](https://github.com/real-CAK3D/DabMagazine), [Hashish](https://github.com/real-CAK3D/Hashish), [The Perennial](https://github.com/real-CAK3D/ThePerennial), [Baked Goods](https://github.com/real-CAK3D/BakedGoods) and [Extra! Extra!](https://github.com/real-CAK3D/ExtraExtra). The papers are written by [Hermes](https://github.com/NousResearch/hermes-agent) agents running on a small Oracle VM called The Garden.

## Files

| File | What it does |
|---|---|
| `render_trail.py` | Prints an issue from Maple's JSON draft (or a preview before the first). |
| `prompts/trail_prompt.txt` | Maple's instructions and the issue schema. |
| `deliver.sh` | Prints the new issue and rings The Corner Chronicle's bell. |
| `gardenweb.py` | The small shared web-server kit every Garden paper carries its own copy of. |

## Running

Maple writes it on the 1st of every month at 08:00 Eastern; served at `/trail-mix/`. Each project is Linux-first (`%-d` date formatting) and expects a Hermes install on the same machine.
