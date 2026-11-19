# The World in One Day — Thursday, 19 November 2026

A one-image newspaper front page summing up Thursday 19 November 2026,
drawn entirely in code with Pillow (`render.py`). `main.py` (standard library
only) copies `entry.png` to `$MAKEFUN_OUTPUT_DIR`.

## The six stories

1. **Vice City opens** — Grand Theft Auto VI begins its global rollout
   after a 13-year wait. Sources: Associated Press; JagranJosh
   (19 Nov world news roundup); The West Australian.
2. **Three leaders, one room** — Trump, Xi and Putin meet in Shenzhen on
   19 November for their first-ever three-way talks on the APEC sidelines;
   nuclear arms and the Iran war on the agenda, no deal expected.
   Sources: Reuters (18 Nov); White House / AFP; China's Foreign Ministry.
3. **First Black Speaker nominee** — House Democrats nominate Hakeem
   Jeffries for Speaker of the House; he would take the gavel on
   3 January. Sources: BBC; NDTV.
4. **Storm bears down on India** — Severe Cyclone Akvan nears the Andhra
   Pradesh–Odisha coast; red alerts, schools shut 19–21 Nov, landfall
   forecast by noon 20 Nov. Sources: The Hindu; India Meteorological
   Department; Daily Jagran.
5. **Islam to pass Christianity by 2035** — Pew Research Center projects
   2.57bn Muslims vs 2.52bn Christians by 2035, driven by higher
   fertility; both faiths keep growing. Sources: Pew Research Center;
   New York Post; Sky News.
6. **Earth's missing billion years** — A Nature study (Dhungana &
   Flament, University of Wollongong) says mantle currents lifted whole
   continents, erasing up to 1.2bn years of rock record. Sources:
   Smithsonian Magazine; Nature World News; University of Wollongong.

Ticker: NASA to confirm Voyager 1's one-light-day milestone at noon ET;
Fed minutes point to more rate hikes; Nvidia halts H-series chips to
China; EU unveils a €45bn Ukraine loan plan; oil falls 3.2% to $83.26.

## Run it

```
python3 render.py        # regenerates entry.png (deterministic)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Entry for the make.fun competition `news-image-20261119`.
License: MIT.
