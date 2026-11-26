# Bad Decisions · web

Static website for Bad Decisions (every Monday at Sala Apolo, Barcelona). English at `/`, Spanish at `/es/`.

## Structure
- `build.py`: generates every page into `public/`. Dates, prices, copy and FAQ live at the top of this file.
- `public/`: the site that gets published (Cloudflare Pages output directory).
- `public/assets/site.css`, `public/assets/site.js`: shared styles and script.
- `public/assets/fonts/`: Anton, M PLUS Rounded 1c and Permanent Marker (self-hosted, all SIL Open Font License). Permanent Marker is the accent font (class `.brush`).

## Change something
1. Edit `build.py` (dates, prices, texts).
2. Run `python3 build.py`.
3. Commit and push. Cloudflare Pages publishes `public/`.

The DICE link goes in `DICE_URL` at the top of `public/assets/site.js`.

`python3 build.py --local` builds a version you can open by double-clicking (do not publish that one).

## Coming soon mode
`COMING_SOON = True` at the top of `build.py` makes the live site (branch `main`) show only the spinning coin and "Coming soon" (`/` and `/es/`).
Set it to `False`, run `python3 build.py`, commit and push to launch the full site.

The full site is always built for: `python3 build.py --local`, `python3 build.py --full`, and Cloudflare preview builds of any branch other than `main`.

## Cloudflare (Workers with static assets)
The site is served by the Worker `bad-decisions-web`, configured in `wrangler.jsonc` (static files from `public/`).
Settings → Builds:
- Build command: `python3 build.py`
- Deploy command: `npx wrangler deploy`
- Non-production branch deploy command: `npx wrangler versions upload`
- Root directory: `/`
