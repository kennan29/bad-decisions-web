# Bad Decisions · web

Static website for Bad Decisions (every Monday at Sala Apolo, Barcelona). English at `/`, Spanish at `/es/`.

## Structure
- `build.py`: generates every page into `public/`. Dates, prices, copy and FAQ live at the top of this file.
- `public/`: the site that gets published (Cloudflare Pages output directory).
- `public/assets/site.css`, `public/assets/site.js`: shared styles and script.
- `public/assets/fonts/`: Anton and M PLUS Rounded 1c (self-hosted). Add `silent-brush.woff2` here.

## Change something
1. Edit `build.py` (dates, prices, texts).
2. Run `python3 build.py`.
3. Commit and push. Cloudflare Pages publishes `public/`.

The DICE link goes in `DICE_URL` at the top of `public/assets/site.js`.

`python3 build.py --local` builds a version you can open by double-clicking (do not publish that one).
