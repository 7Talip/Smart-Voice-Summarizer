import gradio as gr
import whisper
from openai import OpenAI
from langdetect import detect
import os
import time

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
whisper_model = whisper.load_model("tiny")

LANGUAGES = ["Turkish", "Arabic", "Kurdish", "Japanese", "English"]
LANG_CODES = {
    "Turkish": "tr",
    "Arabic": "ar",
    "Kurdish": "ku",
    "Japanese": "ja",
    "English": "en"
}

SUMMARY_PROMPTS = {
    "Turkish": "Lütfen aşağıdaki metni açık ve öz bir şekilde özetle:\n\n{text}",
    "Arabic": "يرجى تلخيص النص التالي بطريقة واضحة وموجزة:\n\n{text}",
    "Kurdish": "Ji kerema xwe nivîsa jêr bi awayekê zelal û kurt re kurt bike:\n\n{text}",
    "Japanese": "以下の文章を簡潔に要約してください：\n\n{text}",
    "English": "Please summarize the following text clearly and briefly:\n\n{text}"
}
QUIZ_PROMPTS = {
    "Turkish": "Aşağıdaki özetten yola çıkarak 2 adet çoktan seçmeli soru üret (her biri 4 şıklı):\n\n{text}",
    "Arabic": "استنادًا إلى الملخص التالي، أنشئ سؤالين من نوع الاختيار من متعدد (لكل منهما 4 خيارات):\n\n{text}",
    "Kurdish": """Ji bo vê kurtkirinê, 2 pirsyarên bijartinê (her yek bi 4 vebijêrk) binivîse. Her pirsyar divê bi awayekê zelal were nivîsîn û vebijêrkên wê bi (a), (b), (c), (d) were nîşandan. Vebijêrkên rast û çewt li hev biguherînin.
Ev kurtkirinê:
{text}""",
    "Japanese": "以下の要約に基づいて、4つの選択肢を持つ選択式の質問を2つ作成してください：\n\n{text}",
    "English": "Based on the following summary, generate 2 multiple choice questions (each with 4 options):\n\n{text}"
}

def translate_text(text, target_lang):
    prompt = f"""Translate the following text into {target_lang}:\n\n{text}"""
    start = time.time()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )
    print(f"⏱️ Translate time: {time.time() - start:.2f}s")
    return response.choices[0].message.content.strip()

def transcribe_audio(audio):
    if audio is None:
        return "No audio uploaded", ""
    start = time.time()
    result = whisper_model.transcribe(audio)
    print(f"⏱️ Transcription time: {time.time() - start:.2f}s")
    return result["text"], result["text"]

def summarize_text(text, summary_lang):
    start = time.time()
    detected = detect(text)
    target_code = LANG_CODES[summary_lang]
    translated = translate_text(text, summary_lang) if detected != target_code else text
    prompt = SUMMARY_PROMPTS[summary_lang].format(text=translated)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    print(f"⏱️ Summarization time: {time.time() - start:.2f}s")
    return response.choices[0].message.content.strip()

def generate_quiz(summary, lang):
    start = time.time()
    prompt = QUIZ_PROMPTS[lang].format(text=summary)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    print(f"⏱️ Quiz generation time: {time.time() - start:.2f}s")
    return response.choices[0].message.content.strip()

custom_css = """
.audio-col {width: 320px !important;}
.lang-col {width: 200px !important; margin-left: 16px;}
.trans-box, .sum-box, .quiz-box {min-height: 60px; max-height: 210px; font-size: 1rem;}
#output_row .gr-box {margin-bottom: 10px;}
"""

with gr.Blocks(css=custom_css) as demo:
    gr.Markdown("# 🧠 Multilingual Audio Summarizer + Quiz Generator")

    with gr.Row():
        with gr.Column(elem_classes="audio-col"):
            audio_input = gr.Audio(type="filepath", label="🎙️ Upload audio")
        with gr.Column(elem_classes="lang-col"):
            summary_lang = gr.Dropdown(choices=LANGUAGES, value="Turkish", label="🌐 Output Language")
    with gr.Row(elem_id="output_row"):
        transcribed_text = gr.Textbox(label="📄 Transcription", lines=7, elem_classes="trans-box")
        summary_output = gr.Textbox(label="✂️ Summary", lines=7, elem_classes="sum-box")
        quiz_output = gr.Textbox(label="📘 Quiz", lines=7, elem_classes="quiz-box")

    with gr.Row():
        transcribe_btn = gr.Button("🎧 Transcribe")
        summarize_btn = gr.Button("✂️ Summarize")
        quiz_btn = gr.Button("📘 Generate Quiz")

    transcribe_btn.click(fn=transcribe_audio, inputs=[audio_input], outputs=[transcribed_text, transcribed_text])
    summarize_btn.click(fn=summarize_text, inputs=[transcribed_text, summary_lang], outputs=summary_output)
    quiz_btn.click(fn=generate_quiz, inputs=[summary_output, summary_lang], outputs=quiz_output)

demo.launch()