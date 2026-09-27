<div align="center">

# ⚡ Cloudflare R2 Sync Hub

### Gestiona tus buckets de Cloudflare R2 desde la bandeja de Windows

*Sube, descarga, previsualiza y comparte archivos sin abrir el navegador.*

<br/>

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![Cloudflare](https://img.shields.io/badge/Cloudflare_R2-F6821F?style=for-the-badge&logo=cloudflare&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

<br/>

[![Releases](https://img.shields.io/github/v/release/d3vn0x3/cloudflare_bucket_handler?style=for-the-badge&logo=github)](https://github.com/d3vn0x3/cloudflare_bucket_handler/releases)
[![Downloads](https://img.shields.io/github/downloads/d3vn0x3/cloudflare_bucket_handler/total?style=for-the-badge)](https://github.com/d3vn0x3/cloudflare_bucket_handler/releases)

<br/>

### [⬇️ Descargar .exe para Windows](https://github.com/d3vn0x3/cloudflare_bucket_handler/releases/latest)

*Sin Python. Sin consola. Doble clic y listo.*

</div>

---

## 🚀 Instalación en 2 minutos (recomendado)

> **No necesitas instalar Python ni nada más.** Solo descarga el ejecutable de la sección [Releases](https://github.com/d3vn0x3/cloudflare_bucket_handler/releases/latest).

| Paso | Qué hacer |
|:----:|-----------|
| **1️⃣** | Ve a **[Releases → Latest](https://github.com/d3vn0x3/cloudflare_bucket_handler/releases/latest)** y descarga el archivo `CloudflareR2Manager-vX.Y.Z.exe` |
| **2️⃣** | Crea una carpeta, por ejemplo `C:\R2Manager\`, y mueve allí el `.exe` |
| **3️⃣** | En esa misma carpeta crea un archivo llamado `.env` (ver [configuración](#️-configuración-env) abajo) |
| **4️⃣** | Doble clic en el `.exe`. Se abrirá la app y quedará minimizada en la **bandeja del sistema** (junto al reloj) |
| **5️⃣** | Tus carpetas locales se crean solas en `C:\Users\<TuUsuario>\Bucket\public` y `\private` |

```text
C:\R2Manager\
├── CloudflareR2Manager-v1.0.0.exe  ← descargado del Release
└── .env                             ← lo creas tú (una sola vez)
```

> ⚠️ **Importante:** el `.exe` y el `.env` deben estar **en la misma carpeta**.
> Si Windows SmartScreen avisa de "origen desconocido" → clic en *Más información → Ejecutar de todas formas* (normal al no tener firma de pago).

---

## ✨ Características

| | Funcionalidad | Detalle |
|---|---|---|
| ⚙️ | **Vive en la bandeja** | Sin ventana en la barra de tareas. Clic derecho → *Abrir / Salir* |
| 🗂️ | **Doble bucket** | Pestañas separadas para `🌐 Public` y `🔒 Private` |
| 📁 | **Sync local automático** | Todo lo que copies a `~/Bucket/public` o `~/Bucket/private` se **sube solo** a R2 (watcher en segundo plano) |
| 🖼️ | **Miniaturas remotas** | Previsualiza imágenes y vídeos de la nube **sin descargarlos** |
| � ☁️ | **Acciones en lote** | Selecciona con checkboxes → subir, descargar, borrar o mover entre buckets |
| 🌐 | **Router multi-CDN** | Desplegable con tus dominios (`cdn.tudominio.es`, ...) → botón *🔗 Copy URL* |
| 🔑 | **Enlaces privados temporales** | Genera URLs firmadas de 1 hora para archivos privados → *🔑 Share Private URL* |
| 🎨 | **UI oscura moderna** | Hecha con `CustomTkinter`, ligera y rápida |

---

## 🖼️ Vista previa

> La app tiene 4 vistas: `🔒 Private → 📁 Local / ☁️ Cloud` y `🌐 Public → 📁 Local / ☁️ Cloud`.

```text
┌─────────────────────────────────────────────────┐
│ ⚡ Cloudflare R2 Sync Hub        ● Watcher Active │
├─────────────────────────────────────────────────┤
│ [🔒 Private Bucket] [🌐 Public Bucket]           │
│  ┌───────────────────────────────────────────┐  │
│  │ [📁 Local Files] [☁️ Cloud Files]          │  │
│  │ ☑ 🖼️ foto.png                             │  │
│  │ ☑ 🎬 video.mp4                            │  │
│  │ [📂 Move] [📋 Copy] [☁️ Upload to Cloud]   │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

---

## ⚙️ Configuración `.env`

La app necesita tus credenciales de Cloudflare R2. Solo se hace **una vez**.

### 1. Crea el archivo

Junto al `.exe` (o en la raíz del proyecto si ejecutas desde código), crea un archivo llamado exactamente `.env`:

```text
# Si usas el .exe:
C:\R2Manager\.env

# Si usas el código fuente:
cloudflare_bucket_handler/.env
```

> 💡 En Windows, asegúrate de que no se guarde como `.env.txt` (activa *Ver → Extensiones de nombre de archivo* en el Explorador).

### 2. Pega esta plantilla y rellénala

```env
# ID de tu cuenta (panel de R2, barra lateral derecha)
R2_ACCOUNT_ID=tu_account_id_aqui

# Tokens de API (R2 → Manage R2 API Tokens → Create API Token)
R2_ACCESS_KEY_ID=tu_access_key_aqui
R2_SECRET_ACCESS_KEY=tu_secret_key_aqui

# Nombres exactos de tus buckets en R2
R2_BUCKET_PUBLIC=publico
R2_BUCKET_PRIVATE=privado

# Dominios CDN conectados al bucket público (separados por comas)
PUBLIC_DOMAINS=cdn.tudominio.es,cdn.otrodominio.es
```

| Variable | Dónde conseguirla |
|----------|-------------------|
| `R2_ACCOUNT_ID` | Dashboard Cloudflare → **R2 Object Storage** → barra lateral derecha |
| `R2_ACCESS_KEY_ID` / `R2_SECRET_ACCESS_KEY` | R2 → **Manage R2 API Tokens** → *Create API Token* → permiso *Admin Read & Write*. Cópialas al momento, no se vuelven a mostrar |
| `R2_BUCKET_PUBLIC` / `R2_BUCKET_PRIVATE` | Nombres exactos de los buckets que **ya debes tener creados** en R2 |
| `PUBLIC_DOMAINS` | Dominios personalizados conectados a tu bucket público (pestaña *Custom Domains* del bucket) |

<details>
<summary><b>📋 Ejemplo de .env completo</b></summary>

```env
R2_ACCOUNT_ID=a1b2c3d4e5f6g7h8i9j0
R2_ACCESS_KEY_ID=abc123def456
R2_SECRET_ACCESS_KEY=xyz789secretkey000111222
R2_BUCKET_PUBLIC=mi-cdn-publico
R2_BUCKET_PRIVATE=mi-archivo-privado
PUBLIC_DOMAINS=cdn.midominio.es
```

</details>

---

## 🧑‍💻 Ejecutar desde código fuente (desarrolladores)

```bash
# 1. Clonar
git clone https://github.com/d3vn0x3/cloudflare_bucket_handler.git
cd cloudflare_bucket_handler

# 2. (Recomendado) entorno virtual
python -m venv venv
venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Crear el .env (ver sección anterior)

# 5. Ejecutar
python main.py
```

---

## 📁 Estructura del proyecto

```text
cloudflare_bucket_handler/
├── main.py                  # App principal (GUI + bandeja del sistema)
├── r2_manager.py            # Cliente boto3 para Cloudflare R2
├── local_watcher.py         # Watcher: auto-sube lo que cae en ~/Bucket/
├── thumbnail_helper.py      # Miniaturas locales y remotas (img + vídeo)
├── requirements.txt
├── .env.example             # Plantilla de configuración
├── .github/workflows/
│   └── release.yml          # 🤖 Compila el .exe y lo publica en Releases
└── README.md
```

---

## 🤖 Releases automáticos (cómo se genera el .exe)

Cada vez que se crea un tag `v*`, GitHub Actions compila el `.exe` en Windows y lo sube al Release. **No hay que compilar a mano.**

```bash
# Publicar una nueva versión (mantenedores):
git tag v1.0.1
git push origin v1.0.1
# → Actions compila → se crea el Release con el .exe automáticamente
```

También puedes lanzarlo manualmente desde la pestaña **Actions → Build & Release .exe → Run workflow**.

El workflow hace:

1. 🪟 Arranca un `windows-latest`
2. 🐍 Instala Python 3.11 + dependencias + PyInstaller
3. 📦 Ejecuta `PyInstaller --onefile --windowed --name CloudflareR2Manager main.py`
4. 🚀 Publica `CloudflareR2Manager-vX.Y.Z.exe` (+ `.env.example`) en la página de Releases

### Compilar el .exe en tu PC (opcional)

```bash
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed --name CloudflareR2Manager --collect-all customtkinter main.py
# El .exe queda en dist/ → ponlo junto a tu .env y ejecútalo
```

---

## 🛠️ Stack tecnológico

| Capa | Librería |
|------|----------|
| 🖥️ GUI | `customtkinter` |
| 📌 Bandeja | `pystray` + `Pillow` |
| ☁️ Cloud | `boto3` (SDK S3 apuntando a R2) |
| 👀 Watcher local | `watchdog` |
| 🖼️ Miniaturas | `opencv-python` + `Pillow` |
| 🔐 Config | `python-dotenv` |
| 📦 Empaquetado | `PyInstaller` (solo en CI) |

---

## ❓ Solución de problemas

<details>
<summary><b>La app no arranca / se cierra al instante</b></summary>

- Revisa que el `.env` esté **junto al `.exe`** y se llame exactamente `.env`.
- Abre una terminal en esa carpeta y ejecuta `CloudflareR2Manager-vX.Y.Z.exe` para ver el error, o revisa que las 5 variables estén rellenas.

</details>

<details>
<summary><b>Error <code>R2_ACCOUNT_ID no se ha podido leer</code></b></summary>

El `.env` no se encuentra o tiene nombre incorrecto (`.env.txt`). Renómbralo y reinicia la app.

</details>

<details>
<summary><b>Windows dice "Windows protegió su PC" (SmartScreen)</b></summary>

Es normal: el `.exe` no tiene firma de pago. Clic en *Más información → Ejecutar de todas formas*.

</details>

<details>
<summary><b>Las miniaturas de vídeo no se ven</b></summary>

Instala el paquete completo con `pip install -r requirements.txt` (necesitas `opencv-python`). En el `.exe` oficial ya va incluido.

</details>

---

<div align="center">

Hecho con ⚡ para gestionar R2 sin salir del escritorio.

**[⬇️ Descargar última versión](https://github.com/d3vn0x3/cloudflare_bucket_handler/releases/latest)** · **[🐛 Reportar un bug](https://github.com/d3vn0x3/cloudflare_bucket_handler/issues)**

</div>
