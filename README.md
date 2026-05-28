# 🦸‍♂️ River's Toy Room

A beautiful, mobile-first website showcasing educational video episodes starring Marvel action figures and toys. Built for fun, learning, and easy future growth.

**Live site:** Deployed via GitHub Pages (see below)

---

## ✅ Deployment Ready

The GitHub username has been pre-filled with **MojoMikeTaylor**.

After you push and enable GitHub Pages:

1. Test the live site on mobile + try the Episode Builder.
2. (Optional) Replace the fake hero stats ("48k kids", "214 adventures") with real numbers.
3. Share the link: `https://MojoMikeTaylor.github.io/RiverToyRoom/`

---

## ✨ Features

- **Stunning dark theme** with bright, joyful toy-inspired accent colors (hot pink, cyan, gold, purple)
- **Infinite-scroll gallery** — starts with 6 episodes and loads more as you scroll
- **Powerful filters** by super-skill (Teamwork, Creativity, Problem Solving, Leadership, Empathy, etc.)
- **Beautiful episode cards** featuring:
  - Custom Grok Imagine-generated thumbnails (real toy photography style)
  - Titles, short educational descriptions
  - Color-coded skill badges
  - Hero name + episode duration
  - One-click video playback
- **Full-screen YouTube video modal** with crisp embeds (real family-friendly Marvel toy learning videos)
- **"Add Your Episode" builder** — opens a form that instantly generates clean JSON ready to paste into `app.js`
- Fully responsive (mobile-first), keyboard accessible, fun micro-interactions
- Zero build step — pure static HTML + CSS + JS

## 🚀 Adding New Episodes (Super Easy)

1. Open `app.js`
2. Add a new object to the top of the `episodes` array:

```js
{
  id: 9,                              // increment
  title: "Your Awesome Episode Title",
  description: "Short, exciting description here...",
  hero: "Black Widow",
  skills: ["Empathy", "Communication"],
  thumbnail: "images/my-new-episode.jpg", // add image to /images
  videoId: "YOUTUBE_VIDEO_ID_HERE",
  duration: "4:55"
}
```

3. (Optional) Generate a thumbnail using any image tool or the built-in Episode Builder in the live site.
4. Refresh — the new episode appears instantly.

The site is intentionally **data-driven** so future episodes are trivial to add.

## 🖼️ Thumbnails

All current thumbnails were generated with Grok's Imagine model in realistic toy photography style. New episodes should use 16:9 images (ideally ~1200×675).

## 🛠️ Local Development

Just open `index.html` in any browser. No server, bundler, or install required.

For a nicer experience you can use any simple static server:

```bash
# Python
python -m http.server 8080

# Or with VS Code Live Server extension
```

## 📦 Deploy to GitHub Pages (Public & Free)

> **IMPORTANT**: After the site goes live, immediately complete the **Post-Deploy Checklist** at the very top of this README (OG image + URL fixes are required for nice social shares).

### One-time Setup (takes ~2 minutes)

1. Create a new GitHub repository named `RiverToyRoom` (recommended) or `riverstoyroom`

2. On your local machine (where Git is installed), simply run this script from the project folder:

```powershell
.\push-to-github.ps1
```

This will automatically initialize git, commit everything, set the correct remote, and push.

> (Remote is pre-configured for MojoMikeTaylor/RiverToyRoom)

3. Go to your repo on GitHub → **Settings → Pages**

4. Under "Build and deployment":
   - Source: **GitHub Actions** (or "Deploy from a branch")
   - If branch: select `main` and `/ (root)`

5. GitHub will publish the site at:
   `https://MojoMikeTaylor.github.io/RiverToyRoom/`

### Fast Alternative (root deployment)

Many people simply push the folder contents and choose the `main` branch + root folder in the Pages settings. Done.

> The site is 100% static and works perfectly on GitHub Pages with zero configuration.

## 🎨 Customization Tips

- **Colors:** Edit CSS variables in `styles.css` (or Tailwind classes)
- **New skills:** They auto-appear in filters as soon as used in an episode
- **Videos:** Any public YouTube ID works great. Use short educational clips.
- **Confetti Easter Egg:** Type the word `marvel` anywhere on the site

## 📜 Tech

- Tailwind CSS (via CDN — zero dependencies)
- Vanilla JavaScript (no frameworks)
- Pure HTML5 + CSS3
- YouTube iframe embeds

## ❤️ Credits & License

Created with imagination for curious kids (and the big kids who love them).

Not affiliated with Marvel or Disney. All characters and toys remain property of their respective owners.

---

**Ready to launch?** Push to GitHub and flip on GitHub Pages. The kids are waiting. 🌟
