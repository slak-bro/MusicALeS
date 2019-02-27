#!/usr/bin/python3

import argparse

from audio_sources.file_audio_source import FileAudioSource
from audio_sources.alsa_audio_source import ALSAAudioSource    
from screens.sdl_color_screen import SDLColorScreen
from animators.energy_animator import EnergyAnimator

screens = {
    "sdl": SDLColorScreen,
}
animators = {
    "energy": EnergyAnimator,
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='BeatDetectionArduinoEngine')
    parser.add_argument('--screen',
                        metavar="[ {} ]".format(" | ".join(screens.keys())),
                        dest="screen", default="sdl", help='The screen')
    parser.add_argument('-n', '--nleds', dest="nleds",type=int, help="Number of leds", default=50)
    parser.add_argument('--animator', 
                        metavar="[ {} ]".format(" | ".join(animators.keys())), 
                        dest="animator",
                        default="energy", help='Animator type')
    parser.add_argument('--alsa', default=False, dest="alsa", action="store_true", help='Alsa audio source')
    parser.add_argument(
        '-f',
        '--file',
        nargs=1,
        metavar='filepath',
        dest="filepath",
        help='Audio file as a source',
    )
    
    args = parser.parse_args()
    screen = None
    animator = None
    audio_source = None
    try:
        screen = screens[args.screen](args.nleds)
    except KeyError:
        parser.print_help()
        exit(1)
    try:
        animator = animators[args.animator]
    except KeyError:
        parser.print_help()
        exit(1)
    
    if args.alsa:
        audio_source = ALSAAudioSource()
    elif args.filepath:
        audio_source = FileAudioSource(args.filepath[0])
    else:
        parser.print_help()
        exit(1)
    
    a = animator(audio_source, screen)
    a.start()
    