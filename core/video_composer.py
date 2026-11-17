"""
Video Composition Engine
Combines generated HD slides and synchronized audio narration tracks into a final
high-definition (1080p, H.264/AAC) MP4 explainer video using MoviePy.
"""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Optional, Callable
import moviepy.editor as mp


@dataclass
class VideoCompositionResult:
    video_path: str
    total_duration_secs: float
    file_size_mb: float
    slide_count: int


class VideoComposer:
    """
    Assembles slide visuals and voice narration tracks into an MP4 video.
    """

    def __init__(self, fps: int = 12, transition_duration: float = 0.3):
        self.fps = fps
        self.transition_duration = transition_duration

    def compose_explainer_video(
        self,
        slide_image_paths: List[str],
        audio_tracks: List[Tuple[str, float]],
        output_video_path: str = "output/videos/explainer_presentation.mp4",
        progress_callback: Optional[Callable[[str, float], None]] = None
    ) -> VideoCompositionResult:
        """
        Combines slides and audio into an MP4 video.

        Args:
            slide_image_paths: List of slide PNG paths.
            audio_tracks: List of (audio_wav_path, duration_secs) tuples.
            output_video_path: Target path for the generated MP4 file.
            progress_callback: Optional callback(stage_text, percent_float).
        """
        os.makedirs(os.path.dirname(output_video_path), exist_ok=True)
        if len(slide_image_paths) != len(audio_tracks):
            raise ValueError(
                f"Mismatch: {len(slide_image_paths)} slides vs {len(audio_tracks)} audio tracks."
            )

        if progress_callback:
            progress_callback("Loading slide media assets...", 0.1)

        clips = []
        opened_audios = []

        try:
            total_slides = len(slide_image_paths)
            for idx in range(total_slides):
                img_path = slide_image_paths[idx]
                wav_path, dur = audio_tracks[idx]

                # Load audio
                audio_clip = mp.AudioFileClip(wav_path)
                opened_audios.append(audio_clip)

                # Add a brief 0.4s pause after narration before next slide
                clip_duration = audio_clip.duration + 0.4

                # Create video clip from image
                img_clip = (
                    mp.ImageClip(img_path)
                    .set_duration(clip_duration)
                    .set_audio(audio_clip)
                )

                # Add subtle fadein if not the very first clip
                if idx > 0 and self.transition_duration > 0:
                    img_clip = img_clip.fadein(self.transition_duration)

                clips.append(img_clip)

            if progress_callback:
                progress_callback("Concatenating presentation timeline...", 0.4)

            # Concatenate all slide clips
            final_clip = mp.concatenate_videoclips(clips, method="compose")
            total_duration = final_clip.duration

            if progress_callback:
                progress_callback("Encoding full HD MP4 video with H.264/AAC...", 0.6)

            # Render to MP4
            final_clip.write_videofile(
                output_video_path,
                fps=self.fps,
                codec="libx264",
                audio_codec="aac",
                preset="ultrafast",
                threads=4,
                logger=None  # Suppress verbose terminal logs
            )

            # Measure final file size
            file_size_mb = round(os.path.getsize(output_video_path) / (1024.0 * 1024.0), 2)

            if progress_callback:
                progress_callback("Video generation completed!", 1.0)

            return VideoCompositionResult(
                video_path=output_video_path,
                total_duration_secs=round(total_duration, 1),
                file_size_mb=file_size_mb,
                slide_count=total_slides
            )

        finally:
            # Clean up open clip references to avoid Windows file locks
            for clip in clips:
                try:
                    clip.close()
                except Exception:
                    pass
            for audio in opened_audios:
                try:
                    audio.close()
                except Exception:
                    pass
            try:
                final_clip.close()
            except Exception:
                pass
