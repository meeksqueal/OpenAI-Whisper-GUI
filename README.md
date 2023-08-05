# OpenAI Whisper GUI
A modern GUI application that transcribes and translates audio and video files, offering the option to save the subtitles as separate files, embed the subtitles in a .mkv format, or hardcode them into the video using OpenAI Whisper and ffmpeg.

Tested on Windows with an Nvidia GPU.


## Preview
![WhiserGUI](https://github.com/meeksqueal/OpenAI-Whisper-GUI/assets/141447225/ce1dfbe4-394d-4763-975b-63a67593011a)



## Setup

### Requirements
* Python version 3.9 or newer
* Torch with Cuda
* ffmpeg
* customtkinter 

> For more information please visit OpenAI Wishper github: https://github.com/openai/whisper

1. Install the required dependencies by running the following command:

```
pip install customtkinter Pillow torch -f https://download.pytorch.org/whl/torch_stable.html openai-whisper
```

2. Install fffmpeg:
```
# on Ubuntu or Debian
sudo apt update && sudo apt install ffmpeg

# on Arch Linux
sudo pacman -S ffmpeg

# on Windows using Chocolatey (https://chocolatey.org/)
choco install ffmpeg

# on Windows using Scoop (https://scoop.sh/)
scoop install ffmpeg
```

3. Run the application by executing the following command:

```
python main.py 
```
