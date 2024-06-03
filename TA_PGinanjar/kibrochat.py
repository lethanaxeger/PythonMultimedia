from flet import *
import flet as ft
import socket
import threading


        
# Kelas untuk pesan
class Message:
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type

# Kelas untuk pesan chat
class ChatMessage(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment = "start"
        self.controls = [
            ft.CircleAvatar(
                content=ft.Text(self.get_initials(message.user_name)),
                color=ft.colors.WHITE,
                bgcolor=self.get_avatar_color(message.user_name),
            ),
            ft.Column(
                [
                    ft.Text(message.user_name, weight="bold"),
                    ft.Text(message.text, selectable=True),
                ],
                tight=True,
                spacing=5,
            ),
        ]

    def get_initials(self, user_name: str):
        return user_name[:1].capitalize() if user_name else "U"

    def get_avatar_color(self, user_name: str):
        colors_lookup = [
            ft.colors.AMBER, ft.colors.BLUE, ft.colors.BROWN, ft.colors.CYAN,
            ft.colors.GREEN, ft.colors.INDIGO, ft.colors.LIME, ft.colors.ORANGE,
            ft.colors.PINK, ft.colors.PURPLE, ft.colors.RED, ft.colors.TEAL,
            ft.colors.YELLOW,
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]

# Fungsi halaman chat
def chat_page(page):
    page.horizontal_alignment = "stretch"
    page.title = "Flet Chat"
    page.clean()  # Membersihkan konten halaman sebelum menambahkan yang baru

    def join_chat_click(e):
        if not join_user_name.value:
            join_user_name.error_text = "Name cannot be blank!"
            join_user_name.update()
        else:
            page.session.set("user_name", join_user_name.value)
            page.dialog.open = False
            new_message.prefix = ft.Text(f"{join_user_name.value}: ")
            page.pubsub.send_all(Message(user_name=join_user_name.value, text=f"{join_user_name.value} has joined the chat.", message_type="login_message"))
            page.update()

    def send_message_click(e):
        if new_message.value != "":
            page.pubsub.send_all(Message(page.session.get("user_name"), new_message.value, message_type="chat_message"))
            new_message.value = ""
            new_message.focus()
            page.update()

    def on_message(message: Message):
        if message.message_type == "chat_message":
            m = ChatMessage(message)
        elif message.message_type == "login_message":
            m = ft.Text(message.text, italic=True, color=ft.colors.BLACK45, size=12)
        chat.controls.append(m)
        page.update()

    page.pubsub.subscribe(on_message)

    # Dialog untuk memasukkan nama pengguna
    join_user_name = ft.TextField(
        label="Enter your name to join the chat",
        autofocus=True,
        on_submit=join_chat_click,
    )
    page.dialog = ft.AlertDialog(
        open=True,
        modal=True,
        title=ft.Text("Welcome!"),
        content=ft.Column([join_user_name], width=300, height=70, tight=True),
        actions=[ft.ElevatedButton(text="Join chat", on_click=join_chat_click)],
        actions_alignment="end",
    )

    # Daftar pesan chat
    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )

    # Formulir untuk pesan baru
    new_message = ft.TextField(
        hint_text="Write a message...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        on_submit=send_message_click,
    )

    # Menambahkan semua komponen ke halaman
    page.add(
        ft.Container(
            content=chat,
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=5,
            padding=10,
            expand=True,
        ),
        ft.Row(
            [
                new_message,
                ft.IconButton(
                    icon=ft.icons.SEND_ROUNDED,
                    tooltip="Send message",
                    on_click=send_message_click,
                ),
            ]
        ),
    )

# Fungsi halaman utama
def main_page(page):
    page.title = "Kita Ngobrol"
    page.bgcolor = ft.colors.LIGHT_BLUE_50
    page.padding = 50

    # Menambahkan logo di bagian atas halaman
    logo = ft.Image(
        src=f"/images/logobaru.png",  # Ganti dengan URL logo Anda
        width=600,
        height=600,
        fit=ft.ImageFit.CONTAIN,
    )

    # Membuat tombol untuk navigasi ke halaman chat
    button1 = ft.ElevatedButton("Yuk Ngobrol....", on_click=lambda e: chat_page(page))
    
    # Menambahkan logo dan tombol ke halaman
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Container(height=5),  # Spasi di atas logo untuk menggeser ke atas
                    logo,
                    ft.Container(height=2),  # Spasi antara logo dan tombol
                    ft.Row(
                        [button1],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            alignment=ft.alignment.center,
        )
    )

# Menjalankan aplikasi dari halaman utama
ft.app(target=main_page, view=ft.WEB_BROWSER)
