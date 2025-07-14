from socket import *
from threading import *
import ssl, sys, time, signal, re
import customtkinter as ctk

# --- Style Constants (Hacksor Aesthetic) ---
THEME_COLOR_PRIMARY = "#00ff00"
THEME_COLOR_SECONDARY = "#008080"
TEXT_COLOR = "#00ff00"
ERROR_COLOR = "#ff0000"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

FONT_FAMILY = "Consolas"
FONT_SIZE_NORMAL = 12
FONT_SIZE_LARGE = 14


# Ctrl + c Signal Handler
def def_handler(sif, frame):
    print("\nQUITTING ...\n")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

# SSL Configuration
context = ssl.create_default_context()
context.load_verify_locations("./server-cert.pem")
context.check_hostname = False

# Socket Initialization
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
host = "127.0.0.1"
port = 4488
ssl_socket = context.wrap_socket(client_socket, server_hostname='127.0.0.1')

try:
    ssl_socket.connect((host, port))
except Exception as e:
    print(f"Error connecting to server: {e}")
    sys.exit(1)

# User and Email Setup
print("\nPlace this oneline if you are in a bspwm (bspc rule -a Tk state=floating)" )
time.sleep(1)
print("Press ctrl +c to exit")
time.sleep(1.2)

username = ""
while True: # Loop for valid username
    username = input("\nEnter your username: ")
    if not username.strip():
        print("Username cannot be empty. Please try again.")
        continue
    
    ssl_socket.send(username.encode("utf-8"))
    server_response = ssl_socket.recv(1024).decode("utf-8")
    
    if server_response == "USERNAME_ACCEPTED":
        print(f"Username '{username}' accepted.")
        break
    elif server_response == "ERROR_USERNAME_TAKEN":
        print("This username is already in use. Please choose another.")
    else:
        print(f"Unexpected server error: {server_response}")
        ssl_socket.close()
        sys.exit(1)

noti = input("\nDo you want notifications? (yes or no): ").lower()
email = ""
if noti == "si":
    while True: # Loop for valid email
        email = input("\nEnter your email for notifications: ")
        test_email_regex = r"\b[A-Za-z-0-9._+-]+@[A-Za-z0-9]+\.[A-Za-z]{2,}\b"

        if email and re.findall(test_email_regex, email):
            print("Entering notification mode")
            print("To use notification mode, press the \"NOTIFY A\" button or Ctrl + e")
            print("Want everyone to know you're here? Type GENERAL and notify them")
            time.sleep(5)
            ssl_socket.send(email.encode("utf-8"))
            break
        else:
            print("Please enter a valid email. Try again.")
elif noti == "no":
    print("Entering incognito mode ...")
    print("To use notification mode, place the user in the message field and press the \"NOTIFICAR A\" button")
    time.sleep(5)
    ssl_socket.send(" ".encode("utf-8"))
else:
    print("Enter a valid option (yes or no)")
    ssl_socket.close()
    sys.exit(1)
   
# Chat UI (CustomTkinter)
window = ctk.CTk()
window.attributes("-topmost", True)
window.title(f"// AnonChat_Terminal - {username} //")
window.geometry("500x700")
window.resizable(False, False)
window.configure(fg_color=("#1a1a1a"))

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

# Message Display Area
msg_txt = ctk.CTkTextbox(window, width=50, height=20, font=(FONT_FAMILY, FONT_SIZE_NORMAL),
                         state="disabled", wrap="word",
                         fg_color="#1a1a1a", text_color=TEXT_COLOR,
                         scrollbar_button_color=THEME_COLOR_SECONDARY, scrollbar_button_hover_color=THEME_COLOR_PRIMARY,
                         border_color=THEME_COLOR_SECONDARY, border_width=2, corner_radius=10)
msg_txt.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Color Tag Configuration
msg_txt.tag_config('green', foreground=TEXT_COLOR)
msg_txt.tag_config('accent', foreground=THEME_COLOR_PRIMARY)
msg_txt.tag_config('error', foreground=ERROR_COLOR)
msg_txt.tag_config('normal', foreground=TEXT_COLOR)

# Message Input Field
you_msg_txt = ctk.CTkEntry(window, width=50, font=(FONT_FAMILY, FONT_SIZE_NORMAL),
                           placeholder_text=f"// Connected as {username} //",
                           fg_color="#333333", text_color=TEXT_COLOR,
                           border_color=THEME_COLOR_SECONDARY, border_width=1, corner_radius=10)
you_msg_txt.grid(row=1, column=0, padx=10, pady=(0, 5), sticky="ew")

# Notification Input Field
you_noti_txt = ctk.CTkEntry(window, width=50, font=(FONT_FAMILY, FONT_SIZE_NORMAL),
                            placeholder_text=f"// Target User or GENERAL for Notification //",
                            fg_color="#333333", text_color=TEXT_COLOR,
                            border_color=THEME_COLOR_SECONDARY, border_width=1, corner_radius=10)
you_noti_txt.grid(row=3, column=0, padx=10, pady=(5, 0), sticky="ew")

# --- Send Functions ---
def send_msg_button():
    client_msg = you_msg_txt.get().strip()
    if client_msg:
        msg_txt.configure(state="normal")
        msg_txt.insert("end", f"\n[{time.strftime('%H:%M:%S')}] > {username} Says: {client_msg}", 'green')
        msg_txt.see("end")
        msg_txt.configure(state="disabled")
        ssl_socket.send((f"Says: {client_msg}").encode("utf-8"))
        you_msg_txt.delete(0, "end")

def send_msg_event(event):
    send_msg_button()

def send_email_button_click():
    target = you_noti_txt.get().strip()
    if not target:
        msg_txt.configure(state="normal")
        msg_txt.insert("end", f"\n[{time.strftime('%H:%M:%S')}] ERROR: Target for notification cannot be empty!", 'error')
        msg_txt.see("end")
        msg_txt.configure(state="disabled")
        return

    msg_txt.configure(state="normal")
    if target.upper() == "GENERAL":
        msg_txt.insert("end", f"\n[{time.strftime('%H:%M:%S')}] // Initiating GENERAL notification...", 'accent')
    else:
        msg_txt.insert("end", f"\n[{time.strftime('%H:%M:%S')}] // Initiating notification to: {target}...", 'accent')
    msg_txt.see("end")
    ssl_socket.send((f"NOTIFY:{target}").encode("utf-8"))
    msg_txt.configure(state="disabled")
    you_noti_txt.delete(0, "end")

def send_email_event(event):
    send_email_button_click()

# Send Button
button_msg = ctk.CTkButton(window, text="SEND_MSG", command=send_msg_button,
                           font=(FONT_FAMILY, FONT_SIZE_LARGE, "bold"),
                           fg_color=THEME_COLOR_PRIMARY, text_color="black",
                           hover_color=THEME_COLOR_SECONDARY,
                           corner_radius=10, border_width=2, border_color=THEME_COLOR_SECONDARY)
button_msg.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
window.bind('<Return>', send_msg_event)

# Notify Button
button_enviar_a = ctk.CTkButton(window, text="NOTIFY_USER", command=send_email_button_click,
                                font=(FONT_FAMILY, FONT_SIZE_LARGE, "bold"),
                                fg_color=THEME_COLOR_PRIMARY, text_color="black",
                                hover_color=THEME_COLOR_SECONDARY,
                                corner_radius=10, border_width=2, border_color=THEME_COLOR_SECONDARY)
button_enviar_a.grid(row=4, column=0, padx=10, pady=(0, 10), sticky="ew")
window.bind('<Control-e>', send_email_event)

# Receive Message Function
def recv_msg():
    while True:
        try:
            server_msg = ssl_socket.recv(2048).decode("utf-8")
            if server_msg:
                msg_txt.configure(state="normal")
                timestamp = time.strftime('%H:%M:%S')

                if server_msg.startswith("---"):
                    msg_txt.insert("end", f"\n[{timestamp}] {server_msg}", 'accent')
                elif server_msg.startswith("ERROR:"):
                    msg_txt.insert("end", f"\n[{timestamp}] {server_msg}", 'error')
                elif server_msg.startswith("Usuarios conectados:"):
                    msg_txt.insert("end", f"\n[{timestamp}] {server_msg}", 'green')
                elif server_msg.startswith("Notificación enviada"):
                     msg_txt.insert("end", f"\n[{timestamp}] {server_msg}", 'accent')
                else:
                    msg_txt.insert("end", f"\n[{timestamp}] {server_msg}", 'normal')
                
                msg_txt.see("end")
                msg_txt.configure(state="disabled")
            else: # Server disconnected
                msg_txt.configure(state="normal")
                msg_txt.insert("end", f"\n[{time.strftime('%H:%M:%S')}] --- Server disconnected. Exiting... ---", 'error')
                msg_txt.see("end")
                msg_txt.configure(state="disabled")
                time.sleep(2)
                sys.exit(0)
        except Exception as e: # Connection error
            msg_txt.configure(state="normal")
            msg_txt.insert("end", f"\n[{time.strftime('%H:%M:%S')}] Connection error: {e}. Exiting...", 'error')
            msg_txt.see("end")
            msg_txt.configure(state="disabled")
            time.sleep(2)
            sys.exit(1)

recv_thread = Thread(target=recv_msg)
recv_thread.daemon = True
recv_thread.start()

window.mainloop()
