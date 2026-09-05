import edge_tts
import asyncio
import os
from django.conf import settings
from django.core.files.base import ContentFile
import uuid

# Ja-JP: Nanami (Standard Japanese female) or Keita (Male)
# Uz-UZ: Madina (Standard Uzbek female)
VOICES = {
    "ja": "ja-JP-NanamiNeural",
    "uz": "uz-UZ-MadinaNeural",
}

async def _generate_audio_async(text, lang, output_path):
    voice = VOICES.get(lang)
    if not voice:
        raise ValueError(f"Unsupported language for audio generation: {lang}")

    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

def generate_vocabulary_audio(text, lang):
    """
    Generates audio file for given text and language.
    Returns the relative path within media directory.
    """
    # Create directory if not exists
    audio_dir = os.path.join(settings.MEDIA_ROOT, "vocabulary", "audio")
    os.makedirs(audio_dir, exist_ok=True)

    filename = f"{uuid.uuid4()}.mp3"
    full_path = os.path.join(audio_dir, filename)

    # Run async function in sync environment
    asyncio.run(_generate_audio_async(text, lang, full_path))

    return os.path.join("vocabulary", "audio", filename)
