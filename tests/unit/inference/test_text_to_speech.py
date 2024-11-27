from pathlib import Path

from opennotebookllm.inference.text_to_speech import text_to_speech

from opennotebookllm.podcast_maker.config import PodcastConfig
from opennotebookllm.podcast_maker.script_to_audio import save_waveform_as_file


def test_text_to_speech_parler(
    tmp_path: Path, tts_prompt: str, podcast_config: PodcastConfig
):
    speaker_cfg = list(podcast_config.speakers.values())[0]

    waveform = text_to_speech(
        tts_prompt,
        speaker_cfg.model,
        speaker_cfg.tokenizer,
        speaker_cfg.speaker_description,
    )

    save_waveform_as_file(
        waveform=waveform,
        sampling_rate=podcast_config.sampling_rate,
        filename=tmp_path / "test_parler_tts.wav",
    )
