import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
import os

def create_cipher(password: str, iv: bytes) -> AES:
    key = SHA256.new(password.encode("utf-8")).digest()
    return AES.new(key, AES.MODE_CFB, iv=iv)

def encrypt(data: bytes, password: str) -> bytes:
    iv = get_random_bytes(AES.block_size)
    cipher = create_cipher(password, iv)
    return iv + cipher.encrypt(data)

def decrypt(data: bytes, password: str) -> bytes:
    iv = data[: AES.block_size]
    cipher = create_cipher(password, iv)
    return cipher.decrypt(data[AES.block_size :])

class AESFileTool:
    def __init__(self, root):
        self.root = root
        self.root.title("AES-256 ファイル暗号化・復号ツール")
        self.root.geometry("570x430")
        self.root.resizable(False, False)
        self.input_file = ""
        self.mode = "encrypt"  # or "decrypt"

        self.setup_ui()

    def setup_ui(self):
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.title_label = ttk.Label(
            self.main_frame, text="ファイル暗号化・復号ツール", font=("Helvetica", 14, "bold")
        )
        self.title_label.pack(pady=10)

        # モード切替
        mode_frame = ttk.Frame(self.main_frame)
        mode_frame.pack(pady=3)
        self.encrypt_btn = ttk.Button(mode_frame, text="暗号化モード", command=self.set_encrypt_mode)
        self.encrypt_btn.grid(row=0, column=0, padx=5)
        self.decrypt_btn = ttk.Button(mode_frame, text="復号モード", command=self.set_decrypt_mode)
        self.decrypt_btn.grid(row=0, column=1, padx=5)

        # パスワード設定フレーム
        self.pw_frame = ttk.LabelFrame(self.main_frame, text="パスワード設定", padding=10)
        self.pw_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(self.pw_frame, text="パスワード:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(self.pw_frame, textvariable=self.password_var, show="*", width=30)
        self.password_entry.grid(row=0, column=1, padx=5, pady=5)

        # 暗号化時のみ確認用パスワード
        self.confirm_label = ttk.Label(self.pw_frame, text="確認用:")
        self.confirm_var = tk.StringVar()
        self.confirm_entry = ttk.Entry(self.pw_frame, textvariable=self.confirm_var, show="*", width=30)
        self.confirm_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        self.confirm_entry.grid(row=1, column=1, padx=5, pady=5)

        self.show_password = tk.BooleanVar()
        ttk.Checkbutton(
            self.pw_frame, text="パスワードを表示", variable=self.show_password, command=self.toggle_password
        ).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)

        # ファイル選択フレーム
        file_frame = ttk.LabelFrame(self.main_frame, text="ファイル選択", padding=10)
        file_frame.pack(fill=tk.X, padx=10, pady=10)

        self.file_select_btn = ttk.Button(file_frame, text="ファイルを選択", command=self.select_input_file)
        self.file_select_btn.grid(row=0, column=0, padx=5, pady=5)
        self.input_file_label = ttk.Label(file_frame, text="ファイルが選択されていません", width=35)
        self.input_file_label.grid(row=0, column=1, padx=5, pady=5)

        # 操作ボタン
        self.action_btn = ttk.Button(self.main_frame, text="暗号化", width=20, command=self.handle_action)
        self.action_btn.pack(pady=14)

        # ステータスバー
        self.status_var = tk.StringVar(value="準備完了")
        ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W).pack(
            side=tk.BOTTOM, fill=tk.X
        )

        self.set_encrypt_mode()

    def set_encrypt_mode(self):
        self.mode = "encrypt"
        self.action_btn.config(text="暗号化")
        self.confirm_label.grid()
        self.confirm_entry.grid()
        self.title_label.config(text="AES-256 ファイル暗号化ツール")
        self.status_var.set("暗号化モードです")
        self.clear_password_fields()

    def set_decrypt_mode(self):
        self.mode = "decrypt"
        self.action_btn.config(text="復号")
        self.confirm_label.grid_remove()
        self.confirm_entry.grid_remove()
        self.title_label.config(text="AES-256 ファイル復号ツール")
        self.status_var.set("復号モードです")
        self.clear_password_fields()

    def toggle_password(self):
        show = "" if self.show_password.get() else "*"
        self.password_entry.config(show=show)
        self.confirm_entry.config(show=show)

    def select_input_file(self):
        if self.mode == "encrypt":
            filetypes = [("すべてのファイル", "*.*")]
            title = "暗号化するファイルを選択"
        else:
            filetypes = [("暗号化ファイル", "*.enc"), ("すべてのファイル", "*.*")]
            title = "復号するファイルを選択"

        filename = filedialog.askopenfilename(title=title, filetypes=filetypes)
        if filename:
            self.input_file = filename
            self.input_file_label.config(text=os.path.basename(filename))
            self.status_var.set(f"ファイルを選択しました: {os.path.basename(filename)}")

    def clear_password_fields(self):
        self.password_var.set("")
        self.confirm_var.set("")

    def validate_password(self):
        pwd = self.password_var.get()
        if not pwd:
            messagebox.showerror("エラー", "パスワードを入力してください")
            return False
        if self.mode == "encrypt":
            conf = self.confirm_var.get()
            if pwd != conf:
                messagebox.showerror("エラー", "パスワードが一致しません")
                return False
        return True

    def handle_action(self):
        if self.mode == "encrypt":
            self.encrypt_file()
        else:
            self.decrypt_file()

    def encrypt_file(self):
        if not self.input_file:
            messagebox.showerror("エラー", "入力ファイルを選択してください")
            return
        if not self.validate_password():
            return

        try:
            base = os.path.basename(self.input_file)
            outfile = filedialog.asksaveasfilename(
                initialfile=base + ".enc",
                defaultextension=".enc",
                filetypes=[("暗号化ファイル", "*.enc"), ("すべてのファイル", "*.*")]
            )

            if not outfile:
                return

            with open(self.input_file, "rb") as f:
                data = f.read()

            ext = os.path.splitext(self.input_file)[1].encode()
            ext_len = len(ext).to_bytes(1, "big")
            password = self.password_var.get()
            encrypted_data = encrypt(ext_len + ext + data, password)

            with open(outfile, "wb") as f:
                f.write(encrypted_data)

            self.status_var.set("暗号化が完了しました")
            messagebox.showinfo("成功", "ファイルの暗号化が完了しました")
        except Exception as e:
            self.status_var.set(f"エラーが発生しました: {str(e)}")
            messagebox.showerror("エラー", f"暗号化中にエラーが発生しました:\n{str(e)}")

    def decrypt_file(self):
        if not self.input_file:
            messagebox.showerror("エラー", "入力ファイルを選択してください")
            return
        if not self.validate_password():
            return
        try:
            with open(self.input_file, "rb") as f:
                encrypted_data = f.read()
            password = self.password_var.get()
            try:
                decrypted_data = decrypt(encrypted_data, password)
            except ValueError:
                messagebox.showerror(
                    "エラー", "復号に失敗しました。パスワードが正しいか確認してください。"
                )
                return

            ext_len = decrypted_data[0]
            ext = decrypted_data[1 : 1 + ext_len].decode()
            content = decrypted_data[1 + ext_len :]

            # 元ファイル名から .enc を除去
            default_name = os.path.basename(self.input_file)
            if default_name.endswith(".enc"):
                default_name = default_name[:-4]
            outfile = filedialog.asksaveasfilename(
                initialfile=default_name,
                defaultextension=ext,
                filetypes=[("元のファイル", f"*{ext}"), ("すべてのファイル", "*.*")]
            )

            if not outfile:
                return
            with open(outfile, "wb") as f:
                f.write(content)

            self.status_var.set("復号が完了しました")
            messagebox.showinfo("成功", f"ファイルの復号が完了しました\n拡張子: {ext}")
        except Exception as e:
            self.status_var.set(f"エラーが発生しました: {str(e)}")
            messagebox.showerror("エラー", f"復号中にエラーが発生しました:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AESFileTool(root)
    root.mainloop()