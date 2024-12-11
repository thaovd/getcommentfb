import tkinter as tk
import requests
from datetime import datetime, timezone
from tkinter import filedialog, simpledialog, messagebox
import os
import configparser
from get_token import get_access_token
import csv
import pytz
from get_name_profile import get_profile_data
import webbrowser

class FacebookCommentsApp:
    def __init__(self, master):
        self.master = master
        master.title("Get Comment FB - Tool Lỏ")
        master.geometry("1200x800")  # Set the window size to 1200x800

        # Set the application icon
        try:
            self.master.iconbitmap(os.path.join(os.path.dirname(__file__), 'icon.ico'))
        except:
            print("Failed to set application icon.")

        # Load config.ini
        self.config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
        self.config = configparser.ConfigParser()
        self.config.read(self.config_path)
        self.page_id = self.config.get('DEFAULT', 'PAGE_ID')
        self.limit = int(self.config.get('DEFAULT', 'LIMIT'))

        # Create the main frame
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create the left frame for function keys
        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

        # Create the right frame for comments display
        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create the status bar
        self.status_bar = tk.Label(self.master, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Create the comment count label
        self.comment_count_label = tk.Label(self.left_frame, text="")
        self.comment_count_label.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        # Fetch the user's profile name and display it on the status bar
        profile_data = get_profile_data()
        if profile_data:
            self.status_bar.config(text=f"Tải khoản đang sử dụng: {profile_data['name']}       Version 1.0.5 @ vuthao.id.vn")
        else:
            self.status_bar.config(text="Không thể lấy dữ liệu tài khoản.")

        # Create the input field and labels
        self.post_id_label = tk.Label(self.left_frame, text="ID Bài viết:")
        self.post_id_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.post_id_entry = tk.Entry(self.left_frame)
        self.post_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        # Create the buttons
        self.get_comments_button = tk.Button(self.left_frame, text="Lấy Comments", command=self.get_comments)
        self.get_comments_button.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        self.copy_comments_button = tk.Button(self.left_frame, text="Copy", command=self.copy_comments)
        self.copy_comments_button.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

        self.export_to_csv_button = tk.Button(self.left_frame, text="Lưu thành CSV", command=self.export_to_csv)
        self.export_to_csv_button.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)

        # Create the "Open CSV" button
        self.open_csv_button = tk.Button(self.left_frame, text="Open CSV", command=self.open_csv)
        self.open_csv_button.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)

        # Create the "Setting" button
        self.setting_button = tk.Button(self.left_frame, text="Setting", command=self.edit_config)
        self.setting_button.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)

        # Create the search input field and label
        self.search_label = tk.Label(self.left_frame, text="Search Comment:")
        self.search_label.grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
        self.search_entry = tk.Entry(self.left_frame)
        self.search_entry.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)
        self.search_entry.bind("<KeyRelease>", self.filter_comments)

        # Create the comments display with a scrollbar
        self.comments_text = tk.Text(self.right_frame, height=10, width=50, font=("Arial", 12))
        self.comments_text_scrollbar = tk.Scrollbar(self.right_frame, command=self.comments_text.yview)
        self.comments_text.config(yscrollcommand=self.comments_text_scrollbar.set)
        self.comments_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.comments_text_scrollbar.pack(side=tk.LEFT, fill=tk.BOTH)

        # Initialize the comments list
        self.comments = []

    def get_comments(self):
        post_id = self.post_id_entry.get()

        # Fetch the access token from the get-token.py script
        access_token = get_access_token()

        url = f"https://graph.facebook.com/v21.0/{self.page_id}_{post_id}/comments?fields=id,message,created_time&limit={self.limit}&access_token={access_token}"
        self.comments_text.delete("1.0", tk.END)
        self.comments_text.insert(tk.END, "Đang lấy dữ liệu từ Facebook. Xin vui lòng chờ...")
        self.master.update()  # Update the UI to display the "getting comments" message

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            self.comments = []
            for comment in data["data"]:
                # Convert the created_time to GMT+7 format
                created_time = datetime.strptime(comment["created_time"], "%Y-%m-%dT%H:%M:%S%z")
                created_time = created_time.astimezone(pytz.timezone("Asia/Jakarta")).strftime("%Y-%m-%d %H:%M:%S")
                comment_info = {
                    "created_time": created_time,
                    "message": comment["message"],
                    "id": comment["id"]
                }
                self.comments.append(comment_info)

            self.display_comments()
            self.search_label.grid()  # Show the search label after successful comments fetch

            # Update the comment count label
            self.comment_count_label.config(text=f"Lấy được: {len(self.comments)} Comments")
        else:
            self.comments_text.delete("1.0", tk.END)
            self.comments_text.insert(tk.END, "Lỗi không xác định! Vui lòng kiểm tra lại các thông số cài đặt như APIKey, PageID và PostID đảm bảo nó còn hoạt động...")
            messagebox.showerror("Lỗi!", "Lỗi không xác định!")

    def display_comments(self):
        self.comments_text.delete("1.0", tk.END)
        for comment in self.comments:
            # Create a link button for the comment ID
            comment_id_link = tk.Label(self.comments_text, text=f"ID: {comment['id']}", fg="blue", cursor="hand2")
            comment_id_link.bind("<Button-1>", lambda event, comment_id=comment['id']: self.open_comment_link(comment_id))
            self.comments_text.window_create(tk.END, window=comment_id_link)
            self.comments_text.insert(tk.END, f"\nCreated Time: {comment['created_time']}\nMessage: {comment['message']}\n\n")

    def open_comment_link(self, comment_id):
        webbrowser.open(f"https://www.facebook.com/{comment_id}")

    def filter_comments(self, event):
        search_term = self.search_entry.get().lower()
        filtered_comments = [comment for comment in self.comments if search_term in comment['message'].lower()]
        self.comments_text.delete("1.0", tk.END)
        for comment in filtered_comments:
            # Create a link button for the comment ID
            comment_id_link = tk.Label(self.comments_text, text=f"ID: {comment['id']}", fg="blue", cursor="hand2")
            comment_id_link.bind("<Button-1>", lambda event, comment_id=comment['id']: self.open_comment_link(comment_id))
            self.comments_text.window_create(tk.END, window=comment_id_link)
            self.comments_text.insert(tk.END, f"\nCreated Time: {comment['created_time']}\nMessage: {comment['message']}\n\n")

    def copy_comments(self):
        comments = self.comments_text.get("1.0", tk.END).strip()
        if comments:
            self.master.clipboard_clear()
            self.master.clipboard_append(comments)
            messagebox.showinfo("Đã copy Comments", "Comments đã được copy vào clipboard.")
        else:
            messagebox.showinfo("Không có comments nào!", "Không có comments nào để copy.")

    def export_to_csv(self):
        if self.comments:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
            if file_path:
                with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
                    fieldnames = ["created_time", "message", "id"]
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                    writer.writeheader()
                    for comment in self.comments:
                        writer.writerow(comment)

                messagebox.showinfo("Đã lưu CSV", f"File CSV đã được lưu tại {file_path}.")
        else:
            messagebox.showinfo("Không có comments nào!", "Không có comments nào để lưu.")

    def open_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.comments = []
            with open(file_path, "r", newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    self.comments.append(row)
            self.display_comments()
            self.comment_count_label.config(text=f"Lấy được: {len(self.comments)} Comments")
        else:
            messagebox.showinfo("Không có file CSV nào được chọn!", "Vui lòng chọn một file CSV để mở.")

    def edit_config(self):
        # Create a new window for the settings dialog
        settings_window = tk.Toplevel(self.master)
        settings_window.title("Settings")
        settings_window.geometry("350x260")

        # Create input fields for the config.ini data fields
        access_token_label = tk.Label(settings_window, text="Access Token Profile:")
        access_token_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.access_token_entry = tk.Entry(settings_window)
        self.access_token_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
        self.access_token_entry.insert(0, self.config.get('DEFAULT', 'ACCESS_TOKEN_PROFILE'))

        page_id_label = tk.Label(settings_window, text="Page ID:")
        page_id_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.page_id_entry = tk.Entry(settings_window)
        self.page_id_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
        self.page_id_entry.insert(0, self.config.get('DEFAULT', 'PAGE_ID'))

        limit_label = tk.Label(settings_window, text="Limit:")
        limit_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        self.limit_entry = tk.Entry(settings_window)
        self.limit_entry.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)
        self.limit_entry.insert(0, self.config.get('DEFAULT', 'LIMIT'))

        # Display the profile data in the settings window
        profile_data = get_profile_data()
        if profile_data:
            profile_name_label = tk.Label(settings_window, text=f"Profile Name: {profile_data['name']}")
            profile_name_label.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
            profile_id_label = tk.Label(settings_window, text=f"Profile ID: {profile_data['id']}")
            profile_id_label.grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
        else:
            profile_info_label = tk.Label(settings_window, text="Không thể lấy dữ liệu về tài khoản!.")
            profile_info_label.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)

        # Create a save button to update the config.ini file
        save_button = tk.Button(settings_window, text="Save", command=self.save_config)
        save_button.grid(row=5, column=0, columnspan=2, padx=150, pady=10, sticky=tk.W)

    def save_config(self):
        # Update the config.ini data fields
        self.config.set('DEFAULT', 'ACCESS_TOKEN_PROFILE', self.access_token_entry.get())
        self.config.set('DEFAULT', 'PAGE_ID', self.page_id_entry.get())
        self.config.set('DEFAULT', 'LIMIT', self.limit_entry.get())

        # Save the updated config.ini file
        with open(self.config_path, 'w') as config_file:
            self.config.write(config_file)

        # Display a message to the user that they need to restart the application
        messagebox.showinfo("Cài đặt mới đã được lưu!", "Bạn cần khởi động lại ứng dụng để cài đặt mới được áp dụng.")

        # Close the settings window
        self.master.destroy()
        
root = tk.Tk()
app = FacebookCommentsApp(root)
root.mainloop()
