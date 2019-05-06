#!/usr/bin/python3
import argparse

from utils.benchmark import benchmark

from animators.energy_animator import EnergyAnimator
from animators.fft_animator import FFTAnimator

animators = {
    "energy": EnergyAnimator,
    "fft": FFTAnimator,
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='BeatDetectionArduinoEngine')
    parser.add_argument('--benchmark', 
                        metavar="[ {} ]".format(" | ".join(animators.keys())), 
                        dest="benchmark",
                        default=None,
                        help='Benchmark an animator')
    parser.add_argument('--screen',
                        metavar="[ sdl | serial ]",
                        dest="screen", default="sdl", help='The screen')
    parser.add_argument('-n', '--nleds', dest="nleds",type=int, help="Number of leds", default=300)
    parser.add_argument('--animator', 
                        metavar="[ {} ]".format(" | ".join(animators.keys())), 
                        dest="animator",
                        default="energy", help='Animator type')
    parser.add_argument(
        '--alsa', 
        nargs=1,
        metavar='device',
        dest="alsa",
        help='Alsa audio capture source (arecord -L can list capture devices)')
    parser.add_argument(
        '--sounddevice', 
        nargs=1,
        metavar='device',
        dest="sounddevice",
        help="""
        sounddevice capture source, to list capture devices :
        python3 -m sounddevice -c "sounddevice.query_devices(kind='input')" """)
    parser.add_argument(
        '-f',
        '--file',
        nargs=1,
        metavar='filepath',
        dest="filepath",
        help='Audio file as a source',
    )
    "hw:CARD=Codec,DEV=0"
    args = parser.parse_args()
    if args.benchmark is not None:
        if args.benchmark not in animators.keys():
            print("Unknown animator")
            parser.print_help()
            exit(1)
        benchmark(animators[args.benchmark], 1000, nLeds = args.nleds)
        exit(0)
    screen = None
    animator = None
    audio_source = None
    if args.screen == "sdl":
        from screens.sdl_color_screen import SDLColorScreen
        screen = SDLColorScreen(args.nleds)
    elif args.screen == "serial":
        from screens.serial_driver_screen import SerialDriverScreen
        screen = SerialDriverScreen(args.nleds)
    else:
        parser.print_help()
        exit(1)
    
    try:
        animator = animators[args.animator]
    except KeyError:
        parser.print_help()
        exit(1)
    
    if args.alsa:
        from audio_sources.alsa_audio_source import ALSAAudioSource
        audio_source = ALSAAudioSource(args.alsa[0])
    elif args.filepath:
        from audio_sources.file_audio_source import FileAudioSource
        audio_source = FileAudioSource(args.filepath[0])
    elif args.sounddevice:
        from audio_sources.sounddevice_audio_source import SoundDeviceAudioSource
        audio_source = SoundDeviceAudioSource(args.sounddevice[0])
    else:
        parser.print_help()
        exit(1)
    
    a = animator(audio_source, screen)
    a.start()
    
