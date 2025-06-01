# 🎙️ Smart Voice Summarizer

**Live Demo:** [Try it on Hugging Face Spaces](https://huggingface.co/spaces/Talip7/smart_voice_Summarizer)  
**Author:** [Talip7](https://huggingface.co/Talip7)

---

## 🚀 Overview

**Smart Voice Summarizer** enables you to upload a short audio file and get, in seconds:

- 📝 **Full transcription** (OpenAI Whisper)
- ✂️ **Clean, short summary** (GPT-3.5)
- 📘 **Two multiple-choice quiz questions** (GPT-3.5, optional)
- 🌐 **Multilingual support** (auto-translation for summary/quiz)

It’s perfect for summarizing lectures, meetings, interviews, or podcasts in *any supported language*.

---

## 🧰 Features

- **Audio to Text:** Upload `.wav` or `.mp3`, get instant transcription
- **Multilingual:** Turkish, Arabic, Kurdish, Japanese, English
- **Summary & Quiz:** Summarize content, auto-generate two quiz questions
- **Auto-Translation:** Transcribes in the spoken language, summarizes in your preferred language
- **Modular Workflow:** Each step (transcribe, summarize, quiz) is separate for flexible use

---

## 📝 How To Use

1. **Upload an audio file** (`.wav` or `.mp3`)
2. **Select summary/quiz output language**
3. Click **Transcribe** to see the text
4. Click **Summarize** to get a short summary
5. Click **Generate Quiz** for two multiple-choice questions

---

## ⚙️ Technologies

- [OpenAI Whisper](https://github.com/openai/whisper) (speech-to-text)
- [OpenAI GPT-3.5](https://platform.openai.com/docs/guides/gpt)
- [Gradio](https://gradio.app/) (user interface)
- [langdetect](https://pypi.org/project/langdetect/)

---

## 🛠️ Installation

```bash
git clone https://github.com/7Talip/smart-voice-summarizer.git
cd smart-voice-summarizer
pip install -r requirements.txt
