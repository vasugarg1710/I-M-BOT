from tkinter import *
from playsound import playsound
import yfinance as YF
root = Tk()
root.title("Chat Bot")
root.maxsize(844, 744)
root.minsize(844, 744)

# Some predefined things
num = 0
userMessages = 0
# Dictionary for chatBot
dictQA = {'How are u': 'I am fine',
          'How old are u': 'I am 16',
          'Who are u': 'I am your assistant',
          'Hi':'Hello'}

def changeTheme(themeColor):
    global messageFrame
    global userFrame
    if themeColor=="dark":
        messageFrame.configure(bg="black")
        userFrame.configure(bg="black")
        displayBotMessage("Theme changed to dark mode")
    elif themeColor=="light":
        messageFrame.configure(bg="light grey")
        userFrame.configure(bg="light grey")
        displayBotMessage("Theme changed to light mode")
    else:
        displayBotMessage("Theme not found")

def playBeep():
    path = "audio/beep.wav"
    playsound(path)

def displayUserMessage(t):
    global messageFrame
    display = Label(messageFrame, text=t, font=("calibri", 15, "bold"),
                    foreground="black", background="pink", padx='5', pady='5')
    display.pack(anchor="e", pady="10", padx="10")
    playBeep()


def displayBotMessage(t):
    global messageFrame
    display = Label(messageFrame, text=t, font=("calibri", 15),
                    foreground="black", background="light green", padx='5', pady='5')
    display.pack(anchor="w", pady="10", padx="10")

def fetchStockPrice(ticker):
    try:
        cmp = round(YF.Ticker(ticker.upper()).info['regularMarketPrice'],2)
        displayBotMessage(f"The stock price of {ticker.upper()} is {cmp}.")
    except Exception as e:
        displayBotMessage("Invalid stock ticker entered or there is some problem with ur internet connection")

def enter_key(event):
    answer()

# creating a bot answer function
def answer():
    global userMessages
    global qText
    global display
    if chat_entry.get().strip() != "":
        matchFound = False
        displayUserMessage(chat_entry.get().strip())
        if userMessages == 0:
            displayBotMessage(f"Hi {chat_entry.get().strip().capitalize()}")
            displayBotMessage('Try asking me some questions like "What is the stock price of <ticker>"')
            chat_entry.delete(0, END)
            userMessages = 1
        else:
            #Some Custom Functions
            if "stock price" in chat_entry.get().lower().strip():
                words = chat_entry.get().lower().strip().split()
                fetchStockPrice(words[len(words)-1])
                matchFound = True
            if "theme" in chat_entry.get().lower().strip():
                themeColor = chat_entry.get().lower().strip().split()[-1]
                changeTheme(themeColor)
                matchFound=True
            for i in dictQA.keys():
                if chat_entry.get().lower().strip() == i.lower():
                    displayBotMessage(dictQA[i].capitalize())
                    matchFound = True

            if matchFound == False:
                displayBotMessage("Try asking something different ")
            chat_entry.delete(0, END)

    # when messages are filled up
        if userMessages >= 4:
            clear_frame()
            displayBotMessage("Screen cleared up!")
            userMessages = 0
    userMessages += 1
    # print(userMessages)

def clear_frame():
    global messageFrame
    for widgets in messageFrame.winfo_children():
        # print(widgets.winfo_name())
        if (widgets.winfo_name() != "!label"):
            widgets.destroy()


# creating message frame
messageFrame = Frame(root, bg="light grey")
messageFrame.pack(fill=BOTH, expand=True)
# place header
img = PhotoImage(file="img/header.png")
photoimage = img.subsample(3, 3)
Label(messageFrame, image=photoimage).pack(
    side=TOP, anchor="w", padx=10, pady=10)

# display first question
displayBotMessage("What is your name?")

# USER FRAME
userFrame = Frame(root, bg="light grey")
userFrame.pack(side=BOTTOM, fill="x")

# Displaying the button
button = Button(userFrame, text="SEND", font=("calibri", 13, "bold"),
                foreground="black", background="yellow", command=answer)
button.pack(side="bottom", pady=(0, 10))

# creating a user input entry
chat_var = StringVar()
chat_entry = Entry(userFrame, textvariable=chat_var, font=(
    'calibri', 15, 'italic'), highlightthickness=1)
chat_entry.config(highlightbackground="red", highlightcolor="red")
chat_entry.pack(side="bottom", fill="x", pady=5, padx=5)

# binding enter key with a function
root.bind('<Return>', enter_key)

root.mainloop()
