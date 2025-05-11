import os
from gtts import gTTS
from pydub import AudioSegment

def markdown_to_mp3(markdown_path, mp3_output_path=None, lang='en'):
    """
    Convert a markdown file to an MP3 audio file using gTTS, splitting by sections and alternating voices.

    Args:
        markdown_path (str): Path to the markdown file to convert.
        mp3_output_path (str, optional): Path to save the MP3 file. If None, saves to outputs/podcast_audio/ with the same base name as the markdown file.
        lang (str, optional): Language code for TTS (default: 'en').

    Returns:
        str: Path to the generated MP3 file.

    The function splits the markdown into sections (by '##'), alternates between US and UK English voices for each section,
    combines the resulting audio, and saves the final MP3 file. Temporary files are cleaned up automatically.
    """
    if not os.path.exists(markdown_path):
        raise FileNotFoundError(f"Markdown file not found: {markdown_path}")

    with open(markdown_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Determine output path
    if not mp3_output_path:
        audio_dir = os.path.join('outputs', 'podcast_audio')
        os.makedirs(audio_dir, exist_ok=True)
        base_name = os.path.splitext(os.path.basename(markdown_path))[0]
        mp3_output_path = os.path.join(audio_dir, base_name + '.mp3')

    # Split text into sections that might represent different speakers
    sections = text.split('##')
    temp_dir = "temp_audio_sections"
    os.makedirs(temp_dir, exist_ok=True)
    temp_files = []

    for i, section in enumerate(sections):
        if not section.strip():
            continue
        # Alternate between different voice characteristics
        if i % 2 == 0:
            tts = gTTS(text=section, lang=lang, slow=False, tld='com')
        else:
            tts = gTTS(text=section, lang=lang, slow=False, tld='co.uk')
        temp_file = os.path.join(temp_dir, f"section_{i}.mp3")
        tts.save(temp_file)
        temp_files.append(temp_file)

    if temp_files:
        combined_audio = AudioSegment.from_mp3(temp_files[0])
        for temp_file in temp_files[1:]:
            next_segment = AudioSegment.from_mp3(temp_file)
            combined_audio += next_segment
        combined_audio.export(mp3_output_path, format="mp3")
        for temp_file in temp_files:
            os.remove(temp_file)
        os.rmdir(temp_dir)
        return mp3_output_path
    else:
        tts = gTTS(text=text, lang=lang, slow=False, tld='com')
        tts.save(mp3_output_path)
        return mp3_output_path