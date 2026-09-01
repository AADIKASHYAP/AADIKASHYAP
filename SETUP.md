# Adarsh Kashyap — Complete GitHub Profile

Target repository: `AADIKASHYAP/AADIKASHYAP`

This version is intentionally self-contained for the visual assets, so the README does not depend on missing local images. It contains a cinematic hero, terminal identity card, stack, current-work panel, contribution heatmap, real repository cards, activity section, socials, and daily GitHub Actions automation.

## First run

```bash
python -m venv .venv
```

Windows:

```bash
.venv\\Scripts\\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

```bash
pip install -r scripts/requirements.txt
python scripts/update_profile.py
python scripts/fetch_contributions.py
python scripts/render_heatmap.py
git add .
git commit -m "feat: build complete GitHub profile"
git push origin main
```

The workflow runs daily at 06:17 UTC and can be manually triggered from GitHub Actions.

No fake projects, achievements, follower counts, portfolio URLs, Instagram URLs, or Facebook URLs are invented.
