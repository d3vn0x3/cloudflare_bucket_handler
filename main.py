import os
import shutil
import sys
import threading
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image, ImageDraw
import pystray
from r2_manager import R2Manager
from local_watcher import LocalWatcher
from thumbnail_helper import get_file_thumbnail, get_cloud_file_thumbnail

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class R2TrayApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Cloudflare R2 Sync Hub")
        self.geometry("920x680")
        self.resizable(False, False)

  
        user_home = os.path.expanduser("~")
        self.base_dir = os.path.join(user_home, "Bucket")
        self.local_public_path = os.path.join(self.base_dir, "public")
        self.local_private_path = os.path.join(self.base_dir, "private")

        os.makedirs(self.local_public_path, exist_ok=True)
        os.makedirs(self.local_private_path, exist_ok=True)

   
        self.r2 = R2Manager()
        self.watcher = LocalWatcher(
            self.r2, self.local_public_path, self.local_private_path
        )
        self.watcher.start()

       
        self.protocol("WM_DELETE_WINDOW", self.hide_to_tray)
        self.build_ui()

        self.tray_icon = None
        threading.Thread(target=self.setup_tray_icon, daemon=True).start()

    def build_ui(self):
        
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(15, 5))

        title_lbl = ctk.CTkLabel(
            header_frame, 
            text="⚡ Cloudflare R2 Sync Hub", 
            font=ctk.CTkFont(size=22, weight="bold")
        )
        title_lbl.pack(side="left")

        status_badge = ctk.CTkLabel(
            header_frame, 
            text="● Watcher Active", 
            text_color="#10b981", 
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#064e3b",
            corner_radius=12,
            padx=10,
            pady=3
        )
        status_badge.pack(side="right")

     
        self.main_tabview = ctk.CTkTabview(self, width=880, height=600)
        self.main_tabview.pack(padx=20, pady=(0, 15), fill="both", expand=True)

        self.tab_private = self.main_tabview.add("🔒 Private Bucket")
        self.tab_public = self.main_tabview.add("🌐 Public Bucket")

        self.setup_bucket_view(self.tab_private, is_public_bucket=False)
        self.setup_bucket_view(self.tab_public, is_public_bucket=True)

    def setup_bucket_view(self, parent_tab, is_public_bucket):
        sub_tabview = ctk.CTkTabview(parent_tab)
        sub_tabview.pack(fill="both", expand=True, padx=5, pady=5)

        tab_local = sub_tabview.add("📁 Local Files")
        tab_cloud = sub_tabview.add("☁️ Cloud Files")

        self.render_local_view(tab_local, is_public_bucket)
        self.render_cloud_view(tab_cloud, is_public_bucket)

 
    def render_local_view(self, parent, is_public):
        bucket_name = self.r2.bucket_public if is_public else self.r2.bucket_private
        local_dir = self.local_public_path if is_public else self.local_private_path
        target_local_dir = self.local_private_path if is_public else self.local_public_path
        target_name = "Private" if is_public else "Public"

        top_frame = ctk.CTkFrame(parent, fg_color="#1e1e2e", corner_radius=8)
        top_frame.pack(fill="x", padx=10, pady=5, ipady=3)

        select_all_var = tk.BooleanVar(value=False)
        checkbox_vars = []

        scroll_frame = ctk.CTkScrollableFrame(parent, height=330, fg_color="#181825")
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=5)

        def refresh_local_list():
            for child in scroll_frame.winfo_children():
                child.destroy()

            checkbox_vars.clear()
            files = [f for f in os.listdir(local_dir) if os.path.isfile(os.path.join(local_dir, f))]

            if not files:
                empty_lbl = ctk.CTkLabel(scroll_frame, text="No local files found", text_color="#6c7086")
                empty_lbl.pack(pady=40)
                return

            for f in files:
                row = ctk.CTkFrame(scroll_frame, fg_color="#2b2b3b", corner_radius=6)
                row.pack(fill="x", pady=3, padx=5, ipady=2)

                var = tk.BooleanVar(value=False)
                checkbox_vars.append((f, var))

                chk = ctk.CTkCheckBox(row, text="", variable=var, width=24, checkbox_width=18, checkbox_height=18)
                chk.pack(side="left", padx=(10, 5))

                filepath = os.path.join(local_dir, f)
                pil_img = get_file_thumbnail(filepath)

                if pil_img:
                    ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(40, 40))
                    img_label = ctk.CTkLabel(row, image=ctk_img, text="")
                    img_label.pack(side="left", padx=(5, 10))
                else:
                    file_icon = ctk.CTkLabel(row, text="📄", font=ctk.CTkFont(size=20))
                    file_icon.pack(side="left", padx=(10, 10))

                lbl = ctk.CTkLabel(row, text=f, anchor="w", font=ctk.CTkFont(size=13))
                lbl.pack(side="left", fill="x", expand=True)

        def toggle_select_all():
            state = select_all_var.get()
            for _, var in checkbox_vars:
                var.set(state)

        ctk.CTkCheckBox(top_frame, text="Select All", variable=select_all_var, command=toggle_select_all).pack(side="left", padx=10)
        ctk.CTkButton(top_frame, text="🔄 Refresh", width=80, fg_color="#313244", hover_color="#45475a", command=refresh_local_list).pack(side="right", padx=10)

        action_frame = ctk.CTkFrame(parent, fg_color="transparent")
        action_frame.pack(fill="x", padx=10, pady=8)

        def transfer_local_files(move=True):
            selected = [f for f, var in checkbox_vars if var.get()]
            if not selected:
                messagebox.showwarning("Warning", "No local files selected.")
                return

            action_str = "Moved" if move else "Copied"
            for filename in selected:
                src = os.path.join(local_dir, filename)
                dst = os.path.join(target_local_dir, filename)
                if move:
                    shutil.move(src, dst)
                else:
                    shutil.copy2(src, dst)

            messagebox.showinfo("Success", f"{action_str} {len(selected)} file(s) to Local {target_name}.")
            refresh_local_list()

        def upload_selected():
            selected = [f for f, var in checkbox_vars if var.get()]
            if not selected:
                messagebox.showwarning("Warning", "No local files selected.")
                return

            keep_local = messagebox.askyesno("Upload Option", "Keep local files after upload?\n\n('No' deletes them locally)")

            for filename in selected:
                filepath = os.path.join(local_dir, filename)
                self.r2.upload_file(filepath, bucket_name, filename)
                if not keep_local:
                    os.remove(filepath)

            messagebox.showinfo("Success", f"Uploaded {len(selected)} file(s) to Cloud {bucket_name}.")
            refresh_local_list()

        ctk.CTkButton(
            action_frame, 
            text=f"📂 Move to Local {target_name}", 
            fg_color="#89b4fa", 
            text_color="#11111b",
            hover_color="#b4befe",
            command=lambda: transfer_local_files(move=True)
        ).pack(side="left", padx=(0, 5))

        ctk.CTkButton(
            action_frame, 
            text=f"📋 Copy to Local {target_name}", 
            fg_color="#45475a", 
            hover_color="#585b70",
            command=lambda: transfer_local_files(move=False)
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            action_frame, 
            text="☁️ Upload to Cloud", 
            fg_color="#1e66f5", 
            hover_color="#2563eb",
            command=upload_selected
        ).pack(side="right")

        refresh_local_list()

   
    def render_cloud_view(self, parent, is_public):
        bucket_name = self.r2.bucket_public if is_public else self.r2.bucket_private
        target_bucket = self.r2.bucket_private if is_public else self.r2.bucket_public
        local_dir = self.local_public_path if is_public else self.local_private_path

        top_frame = ctk.CTkFrame(parent, fg_color="#1e1e2e", corner_radius=8)
        top_frame.pack(fill="x", padx=10, pady=5, ipady=3)

        select_all_var = tk.BooleanVar(value=False)
        checkbox_vars = []

        scroll_frame = ctk.CTkScrollableFrame(parent, height=310, fg_color="#181825")
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=5)

        def refresh_cloud_list():
            for child in scroll_frame.winfo_children():
                child.destroy()

            checkbox_vars.clear()
            files = self.r2.list_cloud_files(bucket_name)

            if not files:
                empty_lbl = ctk.CTkLabel(scroll_frame, text="No files found in bucket", text_color="#6c7086")
                empty_lbl.pack(pady=40)
                return

            for f in files:
                row = ctk.CTkFrame(scroll_frame, fg_color="#2b2b3b", corner_radius=6)
                row.pack(fill="x", pady=3, padx=5, ipady=2)

                var = tk.BooleanVar(value=False)
                checkbox_vars.append((f, var))

                chk = ctk.CTkCheckBox(row, text="", variable=var, width=24, checkbox_width=18, checkbox_height=18)
                chk.pack(side="left", padx=(10, 5))

                img_label = ctk.CTkLabel(row, text="☁️", font=ctk.CTkFont(size=18), width=40)
                img_label.pack(side="left", padx=(5, 10))

                lbl = ctk.CTkLabel(row, text=f, anchor="w", font=ctk.CTkFont(size=13))
                lbl.pack(side="left", fill="x", expand=True)

                filepath = os.path.join(local_dir, f)

              
                if os.path.exists(filepath):
                    pil_img = get_file_thumbnail(filepath)
                    if pil_img:
                        ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(40, 40))
                        img_label.configure(image=ctk_img, text="")
                else:
                  
                    def load_remote_thumb(target_label, object_name):
                        pil_img = get_cloud_file_thumbnail(self.r2.s3_client, bucket_name, object_name)
                        if pil_img:
                            ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(40, 40))
                            self.after(0, lambda: target_label.configure(image=ctk_img, text=""))

                    threading.Thread(target=load_remote_thumb, args=(img_label, f), daemon=True).start()

        def toggle_select_all():
            state = select_all_var.get()
            for _, var in checkbox_vars:
                var.set(state)

        ctk.CTkCheckBox(top_frame, text="Select All", variable=select_all_var, command=toggle_select_all).pack(side="left", padx=10)
        ctk.CTkButton(top_frame, text="🔄 Refresh", width=80, fg_color="#313244", hover_color="#45475a", command=refresh_cloud_list).pack(side="right", padx=10)

        action_frame = ctk.CTkFrame(parent, fg_color="transparent")
        action_frame.pack(fill="x", padx=10, pady=8)

        def download_selected():
            selected = [f for f, var in checkbox_vars if var.get()]
            if not selected:
                messagebox.showwarning("Warning", "No cloud files selected.")
                return

            keep_cloud = messagebox.askyesno("Download Option", "Keep files in Cloud after downloading?")

            for filename in selected:
                dest = os.path.join(local_dir, filename)
                self.r2.download_file(bucket_name, filename, dest)
                if not keep_cloud:
                    self.r2.delete_file(bucket_name, filename)

            messagebox.showinfo("Success", f"Downloaded {len(selected)} file(s).")
            refresh_cloud_list()

        def delete_selected():
            selected = [f for f, var in checkbox_vars if var.get()]
            if not selected:
                return
            if messagebox.askyesno("Confirm Delete", f"Delete {len(selected)} file(s) permanently from {bucket_name}?"):
                for filename in selected:
                    self.r2.delete_file(bucket_name, filename)
                refresh_cloud_list()

        def move_bucket():
            selected = [f for f, var in checkbox_vars if var.get()]
            if not selected:
                return
            for filename in selected:
                self.r2.move_between_buckets(bucket_name, target_bucket, filename)
            messagebox.showinfo("Moved", f"Moved {len(selected)} file(s) to {'Public' if not is_public else 'Private'} bucket.")
            refresh_cloud_list()

        ctk.CTkButton(action_frame, text="⬇️ Download", width=100, fg_color="#313244", command=download_selected).pack(side="left", padx=(0, 5))
        ctk.CTkButton(action_frame, text="🗑️ Delete", width=90, fg_color="#f38ba8", text_color="#11111b", hover_color="#f5e0dc", command=delete_selected).pack(side="left", padx=5)
        ctk.CTkButton(action_frame, text=f"📦 Move to Cloud {'Public' if not is_public else 'Private'}", width=140, fg_color="#fab387", text_color="#11111b", command=move_bucket).pack(side="left", padx=5)

        if is_public:
            domain_var = tk.StringVar(value=self.r2.public_domains[0] if self.r2.public_domains else "")
            domain_dropdown = ctk.CTkOptionMenu(action_frame, values=self.r2.public_domains, variable=domain_var, width=150)
            domain_dropdown.pack(side="right", padx=(5, 0))

            def copy_public_url():
                selected = [f for f, var in checkbox_vars if var.get()]
                if len(selected) != 1:
                    messagebox.showwarning("Warning", "Select exactly 1 file to copy URL.")
                    return
                url = self.r2.generate_public_url(domain_var.get(), selected[0])
                self.clipboard_clear()
                self.clipboard_append(url)
                messagebox.showinfo("URL Copied", f"Copied to clipboard:\n{url}")

            ctk.CTkButton(action_frame, text="🔗 Copy URL", width=100, fg_color="#a6e3a1", text_color="#11111b", command=copy_public_url).pack(side="right", padx=5)

        else:
            def copy_presigned_url():
                selected = [f for f, var in checkbox_vars if var.get()]
                if len(selected) != 1:
                    messagebox.showwarning("Warning", "Select exactly 1 file to share.")
                    return
                url = self.r2.generate_presigned_url(selected[0], expiration=3600)
                self.clipboard_clear()
                self.clipboard_append(url)
                messagebox.showinfo("Presigned URL Copied", "Private temporary URL (1 Hour) copied to clipboard.")

            ctk.CTkButton(action_frame, text="🔑 Share Private URL", width=130, fg_color="#a6e3a1", text_color="#11111b", command=copy_presigned_url).pack(side="right", padx=5)

        refresh_cloud_list()

    def create_tray_image(self):
        width, height = 64, 64
        image = Image.new('RGB', (width, height), (30, 30, 30))
        dc = ImageDraw.Draw(image)
        dc.rectangle((16, 16, 48, 48), fill=(137, 180, 250))
        return image

    def setup_tray_icon(self):
        menu = pystray.Menu(
            pystray.MenuItem("Open", self.show_from_tray, default=True),
            pystray.MenuItem("Exit", self.quit_app)
        )
        self.tray_icon = pystray.Icon("R2 Sync", self.create_tray_image(), "Cloudflare R2 Manager", menu)
        self.tray_icon.run()

    def hide_to_tray(self):
        self.withdraw()

    def show_from_tray(self, icon=None, item=None):
        self.deiconify()
        self.lift()

    def quit_app(self, icon=None, item=None):
        if hasattr(self, 'watcher'):
            self.watcher.stop()
        if self.tray_icon:
            self.tray_icon.stop()
        self.destroy()
        sys.exit()

if __name__ == "__main__":
    app = R2TrayApp()
    app.mainloop()