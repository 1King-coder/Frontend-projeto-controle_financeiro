import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

def success_msg(title: str, text: str) -> None:
    CTkMessagebox(title=title, message=text, icon='check')

def error_msg(title: str, text: str) -> None:
    CTkMessagebox(title=title, message=text, icon='cancel')

def warning_msg(title: str, text: str) -> None:
    CTkMessagebox(title=title, message=text, icon='warning')