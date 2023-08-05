import os
import webbrowser
from concurrent.futures import ThreadPoolExecutor

import torch
import whisper
from whisper.utils import get_writer

import customtkinter as ctk
from customtkinter import filedialog as fd

from PIL import Image

app_logo = "./icons/logo.ico"
clear_icon = ctk.CTkImage(Image.open("./icons/delete.png"), size=(20, 20))
github_icon = ctk.CTkImage(Image.open("./icons/github.png"), size=(20, 20))
close_icon = ctk.CTkImage(Image.open("./icons/close-white.png"), size=(20, 20))


class Notification(ctk.CTkFrame):
    def __init__(self, master, width=350, height=50, text=""):
        super().__init__(
            master,
            width=width,
            height=height,
            border_color="#36719f",
            border_width=2,
            corner_radius=5,
        )
        self.pack_propagate(0)

        self.master = master

        message = ctk.CTkLabel(self, text=text)
        message.pack(side="left", padx=10)

        close_btn = ctk.CTkButton(
            self,
            text="",
            image=close_icon,
            command=self.hide_message,
            width=30,
            corner_radius=2,
        )
        close_btn.pack(side="right", padx=10)

    def show_message(self):
        self.place(relx=0.98, x=10, y=10, anchor="ne")

    def hide_message(self):
        self.place_forget()


class TopFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        title = ctk.CTkLabel(
            self, text="Audio Transcriber & Translator", font=("", 20, "bold")
        )
        title.pack(side="left", padx=10, pady=15)

        values = ["System", "Dark", "Light"]
        theme_option = ctk.CTkOptionMenu(
            self, values=values, command=self.change_theme, corner_radius=5
        )
        theme_option.set("System")
        theme_option.pack(side="right", padx=10, pady=15)

        theme_label = ctk.CTkLabel(self, text="Theme", font=("", 12, "bold"))
        theme_label.pack(side="right", padx=10, pady=15)

    def change_theme(self, new_theme):
        ctk.set_appearance_mode(new_theme)


class LeftFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master
        self.create_widgets()

        self.file_path = None

    def create_widgets(self):
        self.grid_rowconfigure(5, weight=1)

        title = ctk.CTkLabel(self, text="Settings", font=("", 18))
        title.grid(row=0, column=0, padx=10, pady=10)

        model_label = ctk.CTkLabel(self, text="Model Size")
        model_label.grid(row=1, column=0, padx=10, pady=10)

        model_values = ["tiny", "base", "small", "medium", "large"]
        self.model_option = ctk.CTkOptionMenu(
            self, values=model_values, corner_radius=5
        )
        self.model_option.set("medium")
        self.model_option.grid(row=1, column=1, padx=10, pady=10)

        language_label = ctk.CTkLabel(self, text="Language")
        language_label.grid(row=2, column=0, padx=10, pady=10)

        language_values = [
            "Auto Detection",
            "afrikaans",
            "albanian",
            "amharic",
            "arabic",
            "armenian",
            "assamese",
            "azerbaijani",
            "basque",
            "belarusian",
            "bengali",
            "bosnian",
            "breton",
            "bulgarian",
            "catalan",
            "croatian",
            "czech",
            "danish",
            "dutch",
            "english",
            "estonian",
            "faroese",
            "finnish",
            "french",
            "galician",
            "georgian",
            "german",
            "greek",
            "gujarati",
            "haitian creole",
            "hausa",
            "hebrew",
            "hindi",
            "hungarian",
            "icelandic",
            "indonesian",
            "italian",
            "japanese",
            "javanese",
            "kannada",
            "kazakh",
            "khmer",
            "korean",
            "kurdish",
            "kyrgyz",
            "lao",
            "latin",
            "latvian",
            "lingala",
            "lithuanian",
            "luxembourgish",
            "macedonian",
            "malagasy",
            "malay",
            "malayalam",
            "maltese",
            "maori",
            "marathi",
            "mongolian",
            "myanmar",
            "nepali",
            "norwegian",
            "nynorsk",
            "occitan",
            "pashto",
            "persian",
            "polish",
            "portuguese",
            "punjabi",
            "romanian",
            "russian",
            "sanskrit",
            "sindhi",
            "sinhala",
            "slovak",
            "slovenian",
            "somali",
            "spanish",
            "swahili",
            "swedish",
            "tagalog",
            "tajik",
            "tamil",
            "tatar",
            "telugu",
            "thai",
            "tibetan",
            "turkish",
            "turkmen",
            "ukrainian",
            "uzbek",
            "vietnamese",
            "welsh",
            "xhosa",
            "yoruba",
            "zulu",
        ]
        self.language_option = ctk.CTkOptionMenu(
            self, values=language_values, corner_radius=5
        )
        self.language_option.set("Auto Detection")
        self.language_option.grid(row=2, column=1, padx=10, pady=10)

        task_label = ctk.CTkLabel(self, text="Task")
        task_label.grid(row=3, column=0, padx=10, pady=10)

        task_values = ["Transcribe", "Translate"]
        self.task_option = ctk.CTkOptionMenu(self, values=task_values, corner_radius=5)
        self.task_option.set("Translate")
        self.task_option.grid(row=3, column=1, padx=10, pady=10)

        self.upload_button = ctk.CTkButton(
            self,
            text="Upload Audio/Video",
            command=self.select_file,
            border_spacing=5,
            corner_radius=5,
        )
        self.upload_button.grid(
            row=5, column=0, padx=10, pady=10, rowspan=5, columnspan=2
        )

    def select_file(self):
        file_path = fd.askopenfilename(
            parent=self,
            title="Select Audio/Video File",
            filetypes=(
                (('All files', '*.*'),
                 ('Videofile', '*.mp4 *.avi *.mkv *.mov *.wmv *.webm *.flv'),
                 ('Audiofile', '*.mp3 *.wav *.flac *.aac *.ogg *.wma *.m4a')
                 )
            ),
        )
        if file_path:
            file_name = os.path.basename(file_path)
            notification = Notification(
                master=self.master, text=f"Selected file name: {file_name}"
            )
            notification.show_message()
            self.after(5000, notification.hide_message)
            self.file_path = file_path
        else:
            notification = Notification(
                master=self.master, text="Warning: No file is selected."
            )
            notification.show_message()
            self.after(50000, notification.hide_message)
            self.file_path = None

    def return_data(self):
        if self.file_path:
            model = self.model_option.get().lower()
            language = self.language_option.get().lower()
            task = self.task_option.get().lower()

            if language == "english" and model != "large":
                model += ".en"

            if language == "english":
                task = "transcribe"

            return self.file_path, model, language, task
        notification = Notification(
            master=self.master,
            text="Please upload an audio file to begin the task!",
        )
        notification.show_message()
        self.after(5000, notification.hide_message)
        return None


class RightFrame(ctk.CTkFrame):
    def __init__(self, master, left_frame_ref):
        super().__init__(master)

        self.left_frame_ref = left_frame_ref

        self.master = master

        self.thread_pool = ThreadPoolExecutor(max_workers=5)

        self.result = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.textbox = ctk.CTkTextbox(self, wrap="word")
        self.textbox.insert("0.0", "Configure settings and than click start button!")
        self.textbox.configure(state="disabled")
        self.textbox.grid(
            row=0, column=0, columnspan=5, padx=10, pady=10, sticky="nsew"
        )

        self.subtitle_button = ctk.CTkButton(
            self,text="Add Subtitle to Video", command=self.start_subtask, corner_radius=5
        )
        self.subtitle_button.grid(row=1, column=3, padx=10, pady=10)

        self.start_button = ctk.CTkButton(
            self, text="Start", command=self.start_task, corner_radius=5
        )
        self.start_button.grid(row=1, column=1, padx=10, pady=10)

        self.save_button = ctk.CTkButton(
            self, text="Save", command=self.save_text, corner_radius=5
        )
        self.save_button.grid(row=1, column=2, padx=10, pady=10)

        self.clear_button = ctk.CTkButton(
            self,
            text="",
            command=self.clear_output,
            image=clear_icon,
            compound="right",
            width=50,
            border_spacing=2,
            corner_radius=5,
        )
        self.clear_button.grid(row=1, column=4, padx=10, pady=10)

    #add subtitle to video
    def start_subtask(self):
        if self.result is not None:
            ogfile_name = os.path.basename(self.file_path)
            sep = "."
            ogfile_name = ogfile_name.split(sep,1)[0]
            file_path = fd.asksaveasfilename(
                parent=self,
                initialfile= ogfile_name+"-sub",
                defaultextension=".srt",
                title="Export subtitle",
                filetypes=[("MPEG-4", "*.mp4"),("MKV","*.mkv"), ("All", "*.*")],)
            
            file_name = os.path.basename(file_path)
            dir_name = os.path.dirname(file_path)
            file_extension = os.path.splitext(file_path)

            tempfile_name = "tempsrt.srt"
            writer = get_writer("srt", ".")
            writer(self.result, tempfile_name)
            #add the subtitle
            if file_extension[1] == ".mkv":
                os.system("ffmpeg -i {} -i {} -map 0 -map 1 -c copy -disposition:s:0 default -metadata:s:s:0 language={} {} -y".format('"'+self.file_path+'"',tempfile_name,self.lang, os.path.join('"'+dir_name,file_name+'"')))
            else:
                os.system("ffmpeg -i {} -c:v h264_nvenc -vf subtitles={} {} -y".format('"'+self.file_path+'"',tempfile_name, os.path.join('"'+dir_name,file_name+'"')))
            
            os.remove(os.path.join(".", tempfile_name))
        else:
            notification = Notification(
                master=self.master, text="Warning: No file is transcribed."
            )
            notification.show_message()
            self.after(50000, notification.hide_message)

    def start_task(self):
        self.clear_output()
        if self.left_frame_ref.return_data():
            file_path, model, language, task = self.left_frame_ref.return_data()

            self.thread_pool.submit(
                self.run_transcribe, file_path, model, language, task
            )

    def run_transcribe(self, file_path, model, language, task):
        notification = Notification(
            master=self.master, text="Task has started. Please wait!"
        )
        notification.show_message()
        self.after(5000, notification.destroy)

        self.start_button.configure(state="disabled")
        self.file_path = file_path

        load_model = whisper.load_model(model)

        if language == "auto detection":
            # load audio and pad/trim it to fit 30 seconds
            audio = whisper.load_audio(file_path)
            audio = whisper.pad_or_trim(audio)

            # make log-Mel spectrogram and move to the same device as the model
            mel = whisper.log_mel_spectrogram(audio).to(load_model.device)

            # detect the spoken language
            _, probs = load_model.detect_language(mel)
            lang = (f"Detected language: {max(probs, key=probs.get)}")
            self.lang = max(probs, key=probs.get)

            #Notification about the detected language
            notification = Notification(master=self.master, text=lang)
            notification.show_message()

            #transcribe the audio
            result = load_model.transcribe(file_path, beam_size=5, best_of=2, temperature=(0.0, 0.2, 0.4, 0.6, 0.8, 1.0), verbose=False, task=task)
            
            #textbox output
            for segment in result["segments"]:
                segment = "[%s --> %s]%s" % (round(segment["start"],2),round(segment["end"],2), segment["text"])
                self.textbox.configure(state="normal")
                self.textbox.insert("end", segment+"\n")
                self.textbox.configure(state="disabled")

        else:
            #transcribe the audio
            result = load_model.transcribe(file_path, beam_size=5, best_of=2, temperature=(0.0, 0.2, 0.4, 0.6, 0.8, 1.0), language=language, verbose=False, task=task)
            #textbox output
            for segment in result["segments"]:
                segment = "[%s --> %s]%s" % (round(segment["start"],2),round(segment["end"],2), segment["text"])
                self.textbox.configure(state="normal")
                self.textbox.insert("end", segment+"\n")
                self.textbox.configure(state="disabled")

        self.result = result      
        self.start_button.configure(state="normal")
        notification.destroy()
        notification = Notification(master=self.master, text="Task complete!")
        notification.show_message()


    def save_text(self):
        #get original filename
        ogfile_name = os.path.basename(self.file_path)
        sep = "."
        ogfile_name = ogfile_name.split(sep,1)[0]
        #ask for save as filename
        file_path = fd.asksaveasfilename(
            parent=self,
            initialfile= ogfile_name,
            defaultextension=".srt",
            title="Export subtitle",
            filetypes=[("SubRip Subtitle file", "*.srt"), ("text file", "*.txt"),("Web Video Text Tracks", "*.vtt"),
                       ("Tab-separated values", "*.tsv"),("JSON", "*.json"), ("Save all extensions", "*.all")],)
        #get file name and file path
        file_name = os.path.basename(file_path)
        file_extension = os.path.splitext(file_path)
        dir_name = os.path.dirname(file_path)
        #output subtitle
        if file_path and (file_extension[1]==".srt"):
            #save as SRT file
            writer = get_writer("srt", dir_name)
            writer(self.result, file_name)
            self.save_notification()
        elif file_path and (file_extension[1]==".txt"):
            #save as TXT file
            txt_writer = get_writer("txt", dir_name)
            txt_writer(self.result, file_name)
            self.save_notification()
        elif file_path and (file_extension[1]==".vtt"):
            # Save as an VTT file
            vtt_writer = get_writer("vtt", dir_name)
            vtt_writer(self.result, file_name)
            self.save_notification()
        elif file_path and (file_extension[1]==".tsv"):
            # Save as a TSV file
            tsv_writer = get_writer("tsv", dir_name)
            tsv_writer(self.result, file_name)
            self.save_notification()
        elif file_path and (file_extension[1]==".json"):
            # Save as a JSON file
            json_writer = get_writer("json", dir_name)
            json_writer(self.result, file_name)
            self.save_notification()
        elif file_path and (file_extension[1]==".all"):
            all_writer = get_writer("all", dir_name)
            all_writer(self.result, file_name)
            self.save_notification()

    def clear_output(self):
        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", "end")
        self.textbox.configure(state="disabled")

    def save_notification(self):
        notification = Notification(master=self.master, text="Saving Successfully!")
        notification.show_message()
        self.after(5000, notification.hide_message)


class BottomFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(1, weight=1)

        version_label = ctk.CTkLabel(self, text="Version 1.1", font=("", 12, "italic"))
        version_label.grid(row=0, column=0, padx=10, pady=10)

        github_button = ctk.CTkButton(
            self,
            text="Github",
            command=self.open_github,
            image=github_icon,
            compound="right",
            width=100,
            border_spacing=4,
            corner_radius=5,
        )
        github_button.grid(row=0, column=2, padx=10, pady=10)

    def open_github(self):
        webbrowser.open("https://github.com/meeksqueal")


class WhisperGui(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x500")
        self.title("Whisper GUI - ASR")
        self.iconbitmap(app_logo)
        self.minsize(1000, 500)
        window_height = 500
        window_width = 1000

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))

        self.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

        self.create_widgets()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        top_frame = TopFrame(self)
        top_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        left_frame = LeftFrame(self)
        left_frame.grid(row=1, column=0, sticky="ns", padx=10, pady=(0, 10))

        self.right_frame = RightFrame(self, left_frame)
        self.right_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=(0, 10))

        bottom_frame = BottomFrame(self)
        bottom_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

    def on_close(self):
        self.right_frame.thread_pool.shutdown(wait=False)
        self.destroy()


if __name__ == "__main__":
    app = WhisperGui()
    app.mainloop()
