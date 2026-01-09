# 🎥 Video Compliance Bot

A lightweight **video content moderation prototype** that analyzes videos frame-by-frame to detect **NSFW (nudity/sexual) content**. This project is focused strictly on **current, working functionality** and is designed to run on **CPU-only, low-RAM machines**.

---

## ✅ Current Features

* Read video files using OpenCV
* Sample frames at regular intervals
* Classify frames as **NSFW or Normal** using a pretrained model
* Save NSFW frames as images
* Record timestamps where NSFW content appears
* Runs fully on **CPU (no GPU required)**

---

## 🛠️ Tech Stack

* **Python 3.10+**
* **OpenCV** – video decoding & frame extraction
* **PyTorch (CPU-only)** – model inference
* **Hugging Face Transformers** – model pipeline
* **Falconsai/nsfw_image_detection** – NSFW classification model
* **Pillow (PIL)** – image handling
* **FFmpeg** – video/audio processing (system dependency)

---

## ⚙️ Installation

### 1. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install dependencies (CPU only)

```bash
pip install torch torchvision transformers pillow opencv-python
```

### 3. Install FFmpeg

```bash
sudo apt install ffmpeg
```

---

## ▶️ Usage

1. Place a video file inside the `assets/` folder
2. Update the video path in `main.py`
3. Run:

```bash
python main.py
```

The script will:

* Sample frames from the video
* Detect NSFW content
* Save flagged frames in `generated-files/`
* Print timestamps of detected content

---

## ⚠️ Notes

* This project detects **only nudity/sexual content**
* Violence, blood, weapons, or audio-based moderation are **not included**
* Frame sampling may miss very short scenes
* Intended for **learning and experimentation**, not production use

---

**Author:** Long Khan
