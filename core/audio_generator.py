"""
Audio Narration Engine
Synthesizes voiceover narration for each slide using Windows SAPI5 (pywin32).
Runs 100% locally and offline without external AI services, network access, or API keys.
Includes thread-safe COM initialization for Streamlit worker threads.
"""

import os
import wave
from pathlib import Path
from typing import List, Tuple, Dict
import pythoncom
import win32com.client

from .rag_engine import SlideContent


def init_thread_com():
    """Initializes COM library on the active thread (required for Streamlit worker threads)."""
    try:
        pythoncom.CoInitialize()
    except Exception:
        pass


class AudioNarrationGenerator:
    """
    Local speech synthesis engine utilizing Windows SAPI.
    Generates high-clarity 22kHz/44kHz WAV audio files.
    """

    def __init__(self, voice_index: int = 0, speech_rate: int = 0, volume: int = 100):
        self.speech_rate = max(-10, min(10, speech_rate))
        self.volume = max(0, min(100, volume))
        self.voice_index = voice_index
        self._available_voices: List[Dict[str, str]] = self._get_installed_voices()

    def _get_installed_voices(self) -> List[Dict[str, str]]:
        """Enumerates available system voices installed in Windows."""
        voices = []
        init_thread_com()
        try:
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            sapi_voices = speaker.GetVoices()
            for i in range(sapi_voices.Count):
                voice_item = sapi_voices.Item(i)
                desc = voice_item.GetDescription()
                voices.append({"index": i, "name": desc})
        except Exception:
            voices.append({"index": 0, "name": "Default Windows Voice"})
        return voices

    def get_voice_options(self) -> List[str]:
        return [v["name"] for v in self._available_voices]

    def _measure_wav_duration(self, wav_path: str) -> float:
        """Computes audio duration in seconds using Python's standard wave library."""
        try:
            with wave.open(wav_path, "rb") as wf:
                frames = wf.getnframes()
                rate = wf.getframerate()
                if rate > 0:
                    return round(frames / float(rate), 2)
        except Exception:
            pass
        return 5.0

    def synthesize_script_to_wav(self, script_text: str, output_path: str) -> Tuple[str, float]:
        """
        Synthesizes a script string into a WAV file.
        Returns tuple of (wav_path, duration_seconds).
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        if os.path.exists(output_path):
            try:
                os.remove(output_path)
            except Exception:
                pass

        init_thread_com()
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        stream = win32com.client.Dispatch("SAPI.SpFileStream")

        sapi_voices = speaker.GetVoices()
        if 0 <= self.voice_index < sapi_voices.Count:
            speaker.Voice = sapi_voices.Item(self.voice_index)

        speaker.Rate = self.speech_rate
        speaker.Volume = self.volume

        # 3 = SSFMCreateForWrite
        stream.Open(output_path, 3)
        speaker.AudioOutputStream = stream

        clean_text = script_text.replace("\n", " ").strip()
        speaker.Speak(clean_text)

        stream.Close()

        duration = self._measure_wav_duration(output_path)
        return output_path, duration

    def generate_deck_narration(
        self,
        slides: List[SlideContent],
        output_dir: str = "output/audio"
    ) -> List[Tuple[str, float]]:
        """
        Generates individual narration WAV files for all slides in the deck.
        Returns list of (audio_path, duration_seconds).
        """
        os.makedirs(output_dir, exist_ok=True)
        results = []
        for s in slides:
            wav_path = os.path.join(output_dir, f"narration_slide_{s.slide_index:02d}.wav")
            path, dur = self.synthesize_script_to_wav(s.narration_script, wav_path)
            results.append((path, dur))
        return results
