import base64
import hashlib
import sqlite3
import uuid
from functools import partial
import os
import pyperclip
from tkinter import *
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from customtkinter import *
from PIL import Image, ImageTk

script_dir = os.path.dirname(__file__)
backend = default_backend()
salt = b"2444"
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=backend
)
color = {
    "black1": "#1E1E1E",
    "black2": "#3C3C3C",
    "red1": "#FF1E1E",
    "red2": "#FF7878",
    "yellow": "#FFFF1E",
    "green": "#64FF64",
    "blue1": "#00FFFF",
    "blue2": "#5082FF",
    "purple1": "#783CFF",
    "purple2": "#9678FF",
    "orange1": "#FF6400",
    "orange2": "#FFB450",
    "white": "#F0F0F0",
}

encryptionKey = 0


def encrypt(message: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(message)


def decrypt(message: bytes, token: bytes) -> bytes:

    return Fernet(token).decrypt(message)


with sqlite3.connect(script_dir + "/Keyperpasswords.db") as db:
    cursor = db.cursor()
    cursor.execute(
        """
CREATE TABLE IF NOT EXISTS masterpassword(
id INTEGER PRIMARY KEY,
password TEXT NOT NULL,
recoveryKey TEXT NOT NULL);
"""
    )

    cursor.execute(
        """
CREATE TABLE IF NOT EXISTS vault(
id INTEGER PRIMARY KEY,
website TEXT NOT NULL,
username TEXT NOT NULL,
password TEXT NOT NULL);
"""
    )
btn_font = "Inter 18"
frame_width = 560
frame_height = 360
window = Tk()
window.title("Keyper")
window.update()
window.option_add("*font", "Inter 18")
window["bg"] = color["black1"]
w_window = 600
h_window = 400
pos_right = round(window.winfo_screenwidth() / 2 - w_window / 2)
pos_down = round(window.winfo_screenheight() / 2 - h_window / 2)
window.geometry("{}x{}+{}+{}".format(w_window, h_window, pos_right, pos_down))
window.resizable(False, False)
fade = True
logo_img = ImageTk.PhotoImage(
    Image.open(script_dir + "/assets/logo.png").resize(size=(140, 75))
)
search_img = ImageTk.PhotoImage(
    Image.open(script_dir + "/assets/search_dark.png").resize(size=(20, 20))
)
add_img = ImageTk.PhotoImage(
    Image.open(script_dir + "/assets/add_dark.png").resize(size=(20, 20))
)
close_img = ImageTk.PhotoImage(
    Image.open(script_dir + "/assets/close_dark.png").resize(size=(20, 20))
)
window.iconphoto(False, logo_img)


def exiting():
    if fade:
        alpha = window.attributes("-alpha")
        if alpha > 0:
            alpha -= 0.05
            window.attributes("-alpha", alpha)
            window.after(5, exiting)
        else:
            quit()
    else:
        quit()


def startup():
    alpha = window.attributes("-alpha")
    if alpha < 1:
        alpha += 0.05
        window.attributes("-alpha", alpha)
        window.after(5, startup)
    else:
        return


if fade:
    window.attributes("-alpha", 0.0)
    startup()


def hashPassword(input):
    hash1 = hashlib.sha256(input)
    hash1 = hash1.hexdigest()

    return hash1


def messageScreen(msg):
    messagebox_window = Tk()
    messagebox_window.update()
    messagebox_window.option_add("*font", "Inter  18")
    messagebox_window.title(msg)
    w_window = 400
    h_window = 200
    pos_right = round(window.winfo_screenwidth() / 2 - w_window / 2)
    pos_down = round(window.winfo_screenheight() / 2 - h_window / 2)
    messagebox_window.geometry(
        "{}x{}+{}+{}".format(w_window, h_window, pos_right, pos_down)
    )
    messagebox_window["background"] = color["black1"]
    messagebox_window.resizable(False, False)
    frame2 = CTkFrame(
        master=messagebox_window,
        corner_radius=5,
        fg_color=color["black2"],
        width=360,
        height=160,
    )
    frame2.place(x=20, y=20)
    lbl = Label(frame2, text=msg, fg=color["white"], bg=color["black2"])
    lbl.place(x=180 - lbl.winfo_reqwidth() / 2, y=40)

    def close():
        messagebox_window.destroy()

    btn = CTkButton(
        text="Close",
        command=close,
        corner_radius=4,
        text_color=color["white"],
        fg_color=color["red2"],
        hover_color=color["purple1"],
        text_font=btn_font,
        bg_color=color["black2"],
        height=45,
        master=frame2,
    )
    btn.place(x=120, y=100)
    messagebox_window.mainloop()


def newUser():
    for widget in window.winfo_children():
        widget.destroy()

    frame = CTkFrame(
        master=window, corner_radius=5, fg_color=color["black2"], width=560, height=360
    )
    frame.place(x=20, y=20)
    lbl = Label(
        frame,
        text="No existing vault file\ncould be found.",
        fg=color["red2"],
        bg=color["black2"],
    )
    lbl.place(x=160, y=60)

    def close():
        os.remove(script_dir + "/Keyperpasswords.db")
        quit()

    def create():
        firstTimeScreen()

    btn = CTkButton(
        text="Exit",
        command=close,
        corner_radius=4,
        text_color=color["white"],
        fg_color=color["red1"],
        hover_color=color["yellow"],
        text_font=btn_font,
        bg_color=color["black2"],
        height=45,
    )
    btn.place(x=170, y=235)
    btn2 = CTkButton(
        text="Create",
        command=create,
        corner_radius=4,
        text_color=color["black1"],
        fg_color=color["green"],
        hover_color=color["orange1"],
        text_font=btn_font,
        bg_color=color["black2"],
        height=45,
    )
    btn2.place(x=335, y=235)


def firstTimeScreen():
    for widget in window.winfo_children():
        widget.destroy()

    frame = CTkFrame(
        master=window, corner_radius=5, fg_color=color["black2"], width=560, height=360
    )
    frame.place(x=20, y=20)
    lbl = Label(
        frame, text="Choose a Master Password", fg=color["red2"], bg=color["black2"]
    )
    lbl.place(x=125, y=45)

    txt = CTkEntry(
        frame,
        width=200,
        show="●",
        justify="center",
        corner_radius=4,
        text_color=color["red1"],
    )
    txt.place(x=200, y=85)
    txt.focus()

    lbl1 = Label(
        frame, text="Re-enter password", fg=color["purple2"], bg=color["black2"]
    )
    lbl1.place(x=175, y=135)

    txt1 = CTkEntry(
        frame,
        width=200,
        show="●",
        justify="center",
        corner_radius=4,
        text_color=color["red1"],
    )
    txt1.place(x=200, y=185)

    def savePassword():
        if txt.get() == txt1.get():
            sql = "DELETE FROM masterpassword WHERE id = 1"

            cursor.execute(sql)

            hashedPassword = hashPassword(txt.get().encode("utf-8"))
            key = str(uuid.uuid4().hex)
            recoveryKey = hashPassword(key.encode("utf-8"))

            global encryptionKey
            encryptionKey = base64.urlsafe_b64encode(
                kdf.derive(txt.get().encode("utf-8"))
            )

            insert_password = """INSERT INTO masterpassword(password, recoveryKey)
            VALUES(?, ?) """
            cursor.execute(insert_password, ((hashedPassword), (recoveryKey)))
            db.commit()

            recoveryScreen(key)
        else:
            lbl.config(text="Passwords do not match")
            lbl.place(x=140, y=45)

    btn = CTkButton(
        text="Save",
        command=savePassword,
        corner_radius=4,
        text_color=color["black1"],
        fg_color=color["green"],
        hover_color=color["orange1"],
        text_font=btn_font,
        bg_color=color["black2"],
        height=45,
    )
    btn.place(x=250, y=255)


def recoveryScreen(key):
    for widget in window.winfo_children():
        widget.destroy()

    frame = CTkFrame(
        master=window, corner_radius=5, fg_color=color["black2"], width=560, height=360
    )
    frame.place(x=20, y=20)

    lbl = Label(
        frame,
        text="Save this key to be able to recover account",
        fg=color["red2"],
        bg=color["black2"],
        font=("Inter 16"),
    )
    lbl.place(x=55, y=45)

    lbl1 = Label(frame, text=key, bg=color["black2"], fg=color["green"])
    lbl1.place(x=50, y=125)

    def copyKey():
        pyperclip.copy(lbl1.cget("text"))
        homeScreen()

    btn = CTkButton(
        text="Copy and Continue",
        command=copyKey,
        corner_radius=4,
        bg_color=color["black2"],
        fg_color=color["yellow"],
        hover_color=color["green"],
        text_font=btn_font,
        text_color=color["black2"],
    )
    btn.place(x=180, y=205)


def resetScreen():
    for widget in window.winfo_children():
        widget.destroy()

    frame = CTkFrame(
        master=window, corner_radius=5, fg_color=color["black2"], width=560, height=360
    )
    frame.place(x=20, y=20)
    lbl = Label(
        frame, fg=color["orange2"], bg=color["black2"], text="Enter Recovery Key"
    )
    lbl.place(x=170, y=85)

    txt = CTkEntry(
        frame, width=460, justify="center", corner_radius=4, text_color=color["green"]
    )
    txt.place(x=50, y=155)
    txt.focus()

    def getRecoveryKey():
        recoveryKeyCheck = hashPassword(str(txt.get()).encode("utf-8"))
        cursor.execute(
            "SELECT * FROM masterpassword WHERE id = 1 AND recoveryKey = ?",
            [(recoveryKeyCheck)],
        )
        return cursor.fetchall()

    def checkRecoveryKey():
        checked = getRecoveryKey()

        if checked:
            firstTimeScreen()
        else:
            txt.delete(0, "end")

    btn = CTkButton(
        text="Check Key",
        command=checkRecoveryKey,
        corner_radius=4,
        bg_color=color["black2"],
        fg_color=color["blue1"],
        hover_color=color["green"],
        text_font=btn_font,
        text_color=color["black2"],
    )
    btn.place(x=225, y=230)


def loginScreen():
    for widget in window.winfo_children():
        widget.destroy()

    frame = CTkFrame(
        master=window, corner_radius=5, fg_color=color["black2"], width=560, height=360
    )
    frame.place(x=20, y=20)

    lbl = Label(
        frame, fg=color["blue1"], bg=color["black2"], text="Enter  Master Password"
    )
    lbl.place(x=150, y=60)

    txt = CTkEntry(
        frame,
        width=200,
        show="●",
        justify="center",
        corner_radius=4,
        text_color=color["red1"],
    )
    txt.place(x=190, y=125)
    txt.focus()

    def getMasterPassword():
        checkHashedPassword = hashPassword(txt.get().encode("utf-8"))
        global encryptionKey
        encryptionKey = base64.urlsafe_b64encode(kdf.derive(txt.get().encode("utf-8")))
        cursor.execute(
            "SELECT * FROM masterpassword WHERE id = 1 AND password = ?",
            [(checkHashedPassword)],
        )
        return cursor.fetchall()

    def restart():
        os.execl(sys.executable, sys.executable, *sys.argv)

    def checkPassword():
        password = getMasterPassword()

        if password:
            homeScreen()
        else:
            txt.delete(0, "end")
            lbl.config(text="Incorrect Password")
            lbl.place(x=175, y=60)
            btn = CTkButton(
                text="Try Again",
                command=restart,
                corner_radius=4,
                bg_color=color["black2"],
                fg_color=color["green"],
                hover_color=color["yellow"],
                text_font=btn_font,
                text_color=color["black2"],
            )
            btn.place(x=250, y=220)
            txt.place_forget()

    def resetPassword():
        resetScreen()

    btn = CTkButton(
        text="Login",
        command=checkPassword,
        corner_radius=4,
        bg_color=color["black2"],
        fg_color=color["green"],
        hover_color=color["yellow"],
        text_font=btn_font,
        text_color=color["black2"],
    )
    btn.place(x=250, y=220)

    btn = CTkButton(
        text="Forgot Password",
        command=resetPassword,
        corner_radius=4,
        bg_color=color["black2"],
        fg_color=color["red1"],
        hover_color=color["purple1"],
        text_font=btn_font,
        text_color=color["white"],
    )
    btn.place(x=210, y=270)


def homeScreen():
    for widget in window.winfo_children():
        widget.destroy()

    frame = CTkFrame(
        master=window, corner_radius=5, fg_color=color["black2"], width=560, height=360
    )
    frame.place(x=20, y=20)

    def addEntry():
        entry_window = Tk()
        entry_window.update()
        entry_window.title("Add Entry")
        entry_window.option_add("*font", "Inter  18")
        w_window = 600
        h_window = 400
        pos_right = round(window.winfo_screenwidth() / 2 - w_window / 2)
        pos_down = round(window.winfo_screenheight() / 2 - h_window / 2)
        entry_window.geometry(
            "{}x{}+{}+{}".format(w_window, h_window, pos_right, pos_down)
        )
        entry_window["background"] = color["black1"]
        entry_window.resizable(False, False)
        frame2 = CTkFrame(
            master=entry_window,
            corner_radius=5,
            fg_color=color["black2"],
            width=560,
            height=360,
        )
        frame2.place(x=20, y=20)
        lbl = Label(frame2, text="Enter website", fg=color["blue1"], bg=color["black2"])
        lbl.place(x=40, y=40)
        txt = CTkEntry(
            frame2,
            width=220,
            justify="center",
            corner_radius=4,
            text_color=color["blue1"],
        )
        txt.place(x=40, y=85)
        txt.focus()

        lbl2 = Label(
            frame2, text="Enter user id", fg=color["purple2"], bg=color["black2"]
        )
        lbl2.place(x=40, y=125)
        txt2 = CTkEntry(
            frame2,
            width=220,
            justify="center",
            corner_radius=4,
            text_color=color["purple2"],
        )
        txt2.place(x=40, y=170)

        lbl3 = Label(
            frame2, text="Enter password", fg=color["orange2"], bg=color["black2"]
        )
        lbl3.place(x=40, y=215)
        txt3 = CTkEntry(
            frame2,
            width=220,
            justify="center",
            corner_radius=4,
            text_color=color["orange2"],
            show="●",
        )
        txt3.place(x=40, y=255)

        def savePassword():
            global website, username, password
            website = txt.get()
            uid = txt2.get()
            pwd = txt3.get()
            username = encrypt(uid.encode("utf-8"), encryptionKey)
            password = encrypt(pwd.encode("utf-8"), encryptionKey)  # type: ignore
            insert_fields = """INSERT INTO vault(website, username, password) 
        VALUES(?, ?, ?) """
            cursor.execute(insert_fields, (website, username, password))
            db.commit()
            entry_window.destroy()
            homeScreen()

        def cancel():
            entry_window.destroy()
            homeScreen()

        btn = CTkButton(
            text="Save",
            command=savePassword,
            corner_radius=4,
            text_color=color["black1"],
            fg_color=color["green"],
            hover_color=color["orange1"],
            text_font=btn_font,
            bg_color=color["black2"],
            height=45,
            master=frame2,
        )
        btn.place(x=365, y=130)
        btn2 = CTkButton(
            text="Cancel",
            command=cancel,
            corner_radius=4,
            text_color=color["white"],
            fg_color=color["red1"],
            hover_color=color["purple1"],
            text_font=btn_font,
            bg_color=color["black2"],
            height=45,
            master=frame2,
        )
        btn2.place(x=365, y=225)

    def removeEntry(input):
        cursor.execute("DELETE FROM vault WHERE id = ?", (input,))
        db.commit()
        homeScreen()

    logo = Label(window, image=logo_img, bg=color["black2"])
    logo.place(x=235, y=40)
    lbl2 = Label(
        frame, text="Search for website", fg=color["yellow"], bg=color["black2"]
    )
    lbl2.place(x=175, y=120)
    searchbox = CTkEntry(
        frame, width=220, justify="center", corner_radius=4, text_color=color["orange2"]
    )
    searchbox.place(x=180, y=165)
    searchbox.focus()
    btn = CTkButton(
        text="Add new",
        command=addEntry,
        corner_radius=4,
        text_color=color["black1"],
        fg_color=color["green"],
        hover_color=color["yellow"],
        text_font=("Inter Bold", 14),
        bg_color=color["black2"],
        width=95,
        master=frame,
        image=add_img,
    )
    btn.place(x=230, y=250)

    def search():
        txt = searchbox.get()
        txt = txt.lower()
        searchbox.delete(0, END)
        cursor.execute("SELECT * FROM vault WHERE website = ?", (txt,))
        entry = cursor.fetchall()
        if len(entry) == 0:
            messageScreen("No entry found")
        else:

            def exit_view():
                frame2.destroy()

            i = 0
            frame2 = CTkFrame(
                master=window,
                corner_radius=5,
                fg_color=color["black2"],
                width=560,
                height=360,
            )
            frame2.place(x=20, y=20)
            lbl = Label(
                frame2,
                text="Website",
                bg=color["black2"],
                fg=color["blue1"],
                font=("Inter Bold", 12),
            )
            lbl.place(x=50, y=25)
            lbl = Label(
                frame2,
                text="Username",
                bg=color["black2"],
                fg=color["purple2"],
                font=("Inter Bold", 12),
            )
            lbl.place(x=205, y=25)
            lbl = Label(
                frame2,
                text="Password",
                bg=color["black2"],
                fg=color["orange2"],
                font=("Inter Bold", 12),
            )
            for i in range(len(entry)):
                lbl = Label(
                    frame2,
                    text=entry[i][1],
                    font=("Inter Bold", 12),
                    bg=color["black2"],
                    fg=color["blue1"],
                )
                lbl.place(x=50, y=65 + (i * 40))
                lbl.configure(anchor=CENTER)
                lbl2 = Label(
                    frame2,
                    text=(decrypt(entry[i][2], encryptionKey)),
                    font=("Inter Bold", 12),
                    bg=color["black2"],
                    fg=color["purple2"],
                )
                lbl2.place(x=205, y=65 + (i * 40))
                lbl2.configure(anchor=CENTER)
                lbl3 = Label(
                    frame2,
                    text=(decrypt(entry[i][3], encryptionKey)),
                    font=("Inter Bold", 12),
                    bg=color["black2"],
                    fg=color["orange2"],
                )
                lbl3.place(x=360, y=65 + (i * 40))
                lbl3.configure(anchor=CENTER)
                btn = CTkButton(
                    text="Remove",
                    command=lambda i=i: removeEntry(entry[i][0]),
                    corner_radius=4,
                    text_color=color["black1"],
                    fg_color=color["red1"],
                    hover_color=color["purple1"],
                    text_font=("Inter Bold", 12),
                    bg_color=color["black2"],
                    width=95,
                    master=frame2,
                )
                btn.place(x=450, y=65 + (i * 40))
            btn2 = CTkButton(
                text="Exit",
                command=exit_view,
                corner_radius=4,
                text_color=color["black1"],
                fg_color=color["orange1"],
                bg_color=color["black2"],
                width=65,
                hover_color=color["blue1"],
                master=frame2,
                text_font=("Inter", 25),
            )
            btn2.place(x=35, y=290)

    searchicon = CTkButton(
        master=frame,
        bg=color["black2"],
        command=search,
        hover=None,
        image=search_img,
        text="",
        width=20,
        height=20,
        fg_color=color["black2"],
        corner_radius=25,
    )
    searchicon.place(x=410, y=167)


cursor.execute("SELECT * FROM masterpassword")
if cursor.fetchall():
    loginScreen()
else:
    newUser()
window.mainloop()
