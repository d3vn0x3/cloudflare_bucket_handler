<div align="center">

# ⚡ Cloudflare R2 Sync Hub

### Manage your Cloudflare R2 buckets from the Windows system tray

*Upload, download, preview, and share files without opening the browser.*

<br/>

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![Cloudflare](https://img.shields.io/badge/Cloudflare_R2-F6821F?style=for-the-badge&logo=cloudflare&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

<br/>

[![Releases](https://img.shields.io/github/v/release/d3vn0x3/cloudflare_bucket_handler?style=for-the-badge&logo=github)](https://github.com/d3vn0x3/cloudflare_bucket_handler/releases)
[![Downloads](https://img.shields.io/github/downloads/d3vn0x3/cloudflare_bucket_handler/total?style=for-the-badge)](https://github.com/d3vn0x3/cloudflare_bucket_handler/releases)

<br/>

### [⬇️ Download the .exe for Windows](https://github.com/d3vn0x3/cloudflare_bucket_handler/releases/latest)

*No Python. No console. Double-click and done.*

</div>

---

## 🚀 2-minute setup (recommended)

> **You don't need to install Python or anything else.** Just grab the executable from [Releases](https://github.com/d3vn0x3/cloudflare_bucket_handler/releases/latest).

| Step | What to do |
|:----:|-----------|
| **1️⃣** | Go to **[Releases → Latest](https://github.com/d3vn0x3/cloudflare_bucket_handler/releases/latest)** and download `CloudflareR2Manager-vX.Y.Z.exe` |
| **2️⃣** | Create a folder, e.g. `C:\R2Manager\`, and move the `.exe` there |
| **3️⃣** | In that same folder, create a file named `.env` (see [configuration](#️-env-configuration) below) |
| **4️⃣** | Double-click the `.exe`. The app opens and stays minimized in the **system tray** (next to the clock) |
| **5️⃣** | Your local folders are created automatically at `C:\Users\<YourUser>\Bucket\public` and `\private` |

```text
C:\R2Manager\
├── CloudflareR2Manager-v1.0.0.exe  ← downloaded from the Release
└── .env                             ← you create this (one-time setup)
```

> ⚠️ **Important:** the `.exe` and the `.env` must be **in the same folder**.
> If Windows SmartScreen warns about an "unknown publisher" → click *More info → Run anyway* (expected, the binary is not code-signed).

---

## ✨ Features

| | Feature | Details |
|---|---|---|
| ⚙️ | **Lives in the tray** | No taskbar window. Right-click → *Open / Exit* |
| 🗂️ | **Dual bucket** | Separate tabs for `🌐 Public` and `🔒 Private` |
| 📁 | **Automatic local sync** | Anything you drop into `~/Bucket/public` or `~/Bucket/private` is **auto-uploaded** to R2 (background watcher) |
| 🖼️ | **Remote thumbnails** | Preview cloud images and videos **without downloading them** |
| 📦 ☁️ | **Batch actions** | Select with checkboxes → upload, download, delete, or move between buckets |
| 🌐 | **Multi-CDN router** | Dropdown with your domains (`cdn.yourdomain.com`, ...) → *🔗 Copy URL* button |
| 🔑 | **Temporary private links** | Generate 1-hour signed URLs for private files → *🔑 Share Private URL* |
| 🎨 | **Modern dark UI** | Built with `CustomTkinter`, lightweight and fast |

---

## 🖼️ Preview

> The app has 4 views: `🔒 Private → 📁 Local / ☁️ Cloud` and `🌐 Public → 📁 Local / ☁️ Cloud`.

```text
┌─────────────────────────────────────────────────┐
│ ⚡ Cloudflare R2 Sync Hub        ● Watcher Active │
├─────────────────────────────────────────────────┤
│ [🔒 Private Bucket] [🌐 Public Bucket]           │
│  ┌───────────────────────────────────────────┐  │
│  │ [📁 Local Files] [☁️ Cloud Files]          │  │
│  │ ☑ 🖼️ photo.png                            │  │
│  │ ☑ 🎬 video.mp4                            │  │
│  │ [📂 Move] [📋 Copy] [☁️ Upload to Cloud]   │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

---

## ⚙️ `.env` configuration

The app needs your Cloudflare R2 credentials. This is a **one-time setup**.

### 1. Create the file

Next to the `.exe` (or at the project root if you run from source), create a file named exactly `.env`:

```text
# If you use the .exe:
C:\R2Manager\.env

# If you run from source:
cloudflare_bucket_handler/.env
```

> 💡 On Windows, make sure it isn't saved as `.env.txt` (enable *View → File name extensions* in Explorer).

### 2. Paste this template and fill it in

```env
# Your account ID (R2 dashboard, right sidebar)
R2_ACCOUNT_ID=your_account_id_here

# API tokens (R2 → Manage R2 API Tokens → Create API Token)
R2_ACCESS_KEY_ID=your_access_key_here
R2_SECRET_ACCESS_KEY=your_secret_key_here

# Exact names of your R2 buckets
R2_BUCKET_PUBLIC=public
R2_BUCKET_PRIVATE=private

# Custom CDN domains attached to the public bucket (comma-separated)
PUBLIC_DOMAINS=cdn.yourdomain.com,cdn.otherdomain.com
```

| Variable | Where to get it |
|----------|-----------------|
| `R2_ACCOUNT_ID` | Cloudflare dashboard → **R2 Object Storage** → right sidebar |
| `R2_ACCESS_KEY_ID` / `R2_SECRET_ACCESS_KEY` | R2 → **Manage R2 API Tokens** → *Create API Token* → *Admin Read & Write* permission. Copy them immediately, they won't be shown again |
| `R2_BUCKET_PUBLIC` / `R2_BUCKET_PRIVATE` | Exact names of the buckets you **must have already created** in R2 |
| `PUBLIC_DOMAINS` | Custom domains attached to your public bucket (bucket's *Custom Domains* tab) |

<details>
<summary><b>📋 Full .env example</b></summary>

```env
R2_ACCOUNT_ID=a1b2c3d4e5f6g7h8i9j0
R2_ACCESS_KEY_ID=abc123def456
R2_SECRET_ACCESS_KEY=xyz789secretkey000111222
R2_BUCKET_PUBLIC=my-public-cdn
R2_BUCKET_PRIVATE=my-private-storage
PUBLIC_DOMAINS=cdn.mydomain.com
```

</details>

---

## 🧑‍💻 Run from source (developers)

```bash
# 1. Clone
git clone https://github.com/d3vn0x3/cloudflare_bucket_handler.git
cd cloudflare_bucket_handler

# 2. (Recommended) virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create the .env (see section above)

# 5. Run
python main.py
```

---

## 📁 Project structure

```text
cloudflare_bucket_handler/
├── main.py                  # Main app (GUI + system tray)
├── r2_manager.py            # boto3 client for Cloudflare R2
├── local_watcher.py         # Watcher: auto-uploads whatever lands in ~/Bucket/
├── thumbnail_helper.py      # Local and remote thumbnails (img + video)
├── requirements.txt
├── .env.example             # Configuration template
├── .github/workflows/
│   └── release.yml          # 🤖 Builds the .exe and publishes it to Releases
└── README.md
```

---

## 🤖 Automatic releases (how the .exe is built)

Every time a `v*` tag is created, GitHub Actions compiles the `.exe` on Windows and uploads it to the Release. **No manual building needed.**

```bash
# Publish a new version (maintainers):
git tag v1.0.1
git push origin v1.0.1
# → Actions builds → the Release with the .exe is created automatically
```

You can also trigger it manually from the **Actions → Build & Release .exe → Run workflow** tab.

The workflow does the following:

1. 🪟 Spins up a `windows-latest` runner
2. 🐍 Installs Python 3.11 + dependencies + PyInstaller
3. 📦 Runs `PyInstaller --onefile --windowed --name CloudflareR2Manager main.py`
4. 🚀 Publishes `CloudflareR2Manager-vX.Y.Z.exe` (+ `env.example.txt`) to the Releases page

### Build the .exe on your own PC (optional)

```bash
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed --name CloudflareR2Manager --collect-all customtkinter main.py
# The .exe lands in dist/ → place it next to your .env and run it
```

---

## 🛠️ Tech stack

| Layer | Library |
|------|----------|
| 🖥️ GUI | `customtkinter` |
| 📌 Tray | `pystray` + `Pillow` |
| ☁️ Cloud | `boto3` (S3 SDK pointed at R2) |
| 👀 Local watcher | `watchdog` |
| 🖼️ Thumbnails | `opencv-python` + `Pillow` |
| 🔐 Config | `python-dotenv` |
| 📦 Packaging | `PyInstaller` (CI only) |

---

## ❓ Troubleshooting

<details>
<summary><b>The app won't start / closes instantly</b></summary>

- Check that the `.env` sits **next to the `.exe`** and is named exactly `.env`.
- Open a terminal in that folder and run `CloudflareR2Manager-vX.Y.Z.exe` to see the error, or verify that all 5 variables are filled in.

</details>

<details>
<summary><b>Error <code>R2_ACCOUNT_ID could not be read</code></b></summary>

The `.env` wasn't found or is misnamed (`.env.txt`). Rename it and restart the app.

</details>

<details>
<summary><b>Windows says "Windows protected your PC" (SmartScreen)</b></summary>

That's expected: the `.exe` is not code-signed. Click *More info → Run anyway*.

</details>

<details>
<summary><b>Video thumbnails don't show up</b></summary>

Install the full bundle with `pip install -r requirements.txt` (you need `opencv-python`). The official `.exe` already includes it.

</details>

---

<div align="center">

Built with ⚡ to manage R2 without leaving your desktop.

**[⬇️ Download the latest version](https://github.com/d3vn0x3/cloudflare_bucket_handler/releases/latest)** · **[🐛 Report a bug](https://github.com/d3vn0x3/cloudflare_bucket_handler/issues)**

</div>
