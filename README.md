# ⚡ Cloudflare R2 Tray Manager

A fast, lightweight, and user-friendly Windows System Tray utility built with **Python**, **CustomTkinter**, and **Boto3** to seamlessly manage, sync, and share assets across **Cloudflare R2** storage buckets.

Designed to live silently in your system tray with minimal RAM/CPU usage, giving you instant desktop control over your public CDNs and private cloud storage.

---

## ✨ Features

- ⚙️ **System Tray Native**: Runs quietly in the background without cluttering your taskbar.
- 🗂️ **Dual-Bucket Management**: Isolated environments for `public` assets and `private` secure files.
- 📁 **Local Mirroring & Transfers**: Automatically syncs with local folder structures (`C:\Users\<User>\Bucket\public` & `private`) and allows direct file moving/copying between local environments.
- 🖼️ **Remote Cloud Previews**: On-the-fly streaming thumbnail generation for images and videos directly from Cloudflare R2 without downloading full files.
- ⚡ **Batch Cloud Actions**: Bulk upload, download, delete, or migrate files between buckets with 1-click checkboxes.
- 🌐 **Multi-Domain CDN Router**: Switch between custom CDN domains (`cdn.noxe.es`, `cdn.capitansalami.es`, etc.) to instantly generate and copy public URLs.
- 🔒 **Presigned Private Links**: Generate temporary, secure S3 URLs for private files with 1-hour expiration.
- 🎨 **Modern Dark UI**: Powered by `CustomTkinter` for a clean desktop interface.

---

## ⚙️ Environment Configuration (`.env`)

To connect the application to your Cloudflare R2 storage, you need to set up an `.env` file in the root directory of the project.

### 1. Create the File
Create a file named strictly `.env` in the root folder:
```text
cloudflare_bucket_handler/
│
├── .env                  <-- Create here
├── main.py
├── r2_manager.py
├── local_watcher.py
└── thumbnail_helper.py

Windows Note: Ensure your file explorer does not append a .txt extension (it must be named .env, not .env.txt).


2. Environment Variables Template
Copy and paste the following template into your .env file and replace the placeholder values with your Cloudflare credentials:

# Cloudflare Account ID (Found in the Cloudflare R2 overview panel)
R2_ACCOUNT_ID=your_account_id_here

# R2 API Tokens (R2 > Manage R2 API Tokens)
R2_ACCESS_KEY_ID=your_access_key_id_here
R2_SECRET_ACCESS_KEY=your_secret_access_key_here

# Exact names of your Cloudflare R2 buckets
R2_BUCKET_PUBLIC=publico
R2_BUCKET_PRIVATE=privado

# Custom CDN domains attached to the public bucket (comma-separated)
PUBLIC_DOMAINS=cdn.noxe.es,cdn.capitansalami.es

3. How to Obtain Credentials from Cloudflare
Account ID:

Log into the Cloudflare Dashboard.

Navigate to R2 Object Storage.

Your Account ID is displayed in the right sidebar.

Access Key ID & Secret Access Key:

In the R2 Object Storage section, click on Manage R2 API Tokens on the right side.

Click Create API Token.

Set permissions to Admin Read & Write.

Once generated, save your Access Key ID and Secret Access Key immediately.

Buckets:

Ensure you have manually created the buckets in Cloudflare R2 matching the exact names set in R2_BUCKET_PUBLIC and R2_BUCKET_PRIVATE.

🚀 Getting Started

Install Dependencies:

pip install -r requirements.txt

Run the Application:

python main.py

Tech Stack
GUI: customtkinter

Tray Support: pystray + Pillow

Cloud Provider: boto3 (AWS S3 SDK configured for Cloudflare R2)

Environment Management: python-dotenv

Media Processing: opencv-python + Pillow