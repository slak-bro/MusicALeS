if __name__ == "__main__":
    from audio_sources.file_audio_source import FileAudioSource
    from audio_sources.alsa_audio_source import ALSAAudioSource    
    from screens.sdl_color_screen import SDLColorScreen
    from animators.energy_animator import EnergyAnimator
    #audio_source = FileAudioSource("traindata/cvrl-subterfuge.mp3")
    audio_source = ALSAAudioSource()
    screen = SDLColorScreen(50)
    animator = EnergyAnimator(audio_source, screen)
    animator.start()