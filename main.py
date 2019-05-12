#!/usr/bin/python3
import argparse

from utils.benchmark import benchmark

from animators import animators_dict
from audio_sources import audio_sources_dict
from screens import screens_dict


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='BeatDetectionArduinoEngine')
    parser.add_argument('--benchmark',
                        dest="benchmark",
                        action='store_true',
                        help='Benchmark an animator')
    parser.add_argument('--screen',
                        metavar="[ {} ]".format(" | ".join(screens_dict.keys())),
                        dest="screen", default="sdl", help='The screen')
    parser.add_argument('-n', '--nleds', dest="nleds",type=int, help="Number of leds", default=300)
    parser.add_argument('--animator', 
                        metavar="[ {} ]".format(" | ".join(animators_dict.keys())), 
                        dest="animator",
                        default="energy", help='Animator type')
    parser.add_argument(
        "--source",
        nargs=2,
        dest="source",
        required=True,
        metavar=(("[ {} ]".format(" | ".join(audio_sources_dict.keys())), "[ PARAM ]")),
        help="Audio input method"
    )

    args = parser.parse_args()
    screen = None
    animator = None
    audio_source = None

    try:
        screen_class = screens_dict[args.screen]
        screen = screen_class(args.nleds)
    except (KeyError, TypeError):
        print("\033[1;31;40mERROR:\033[0m Screen '{}' does not exist or failed to import".format(args.screen))
        parser.print_help()
        exit(1)
    
    try:
        animator = animators_dict[args.animator]
    except KeyError:
        print("\033[1;31;40mERROR:\033[0m Animator '{}' does not exist or failed to import".format(args.animator))
        parser.print_help()
        exit(1)
    
    try:
        # Retreive audio source configration
        # For Alsa, use "hw:CARD=Codec,DEV=0" as a second parameter
        source_name = args.source[0]
        source_config = args.source[1]
        audio_source = audio_sources_dict[source_name](source_config)
    except KeyError:
        print("\033[1;31;40mERROR:\033[0m Audio source '{}' does not exist or failed to import, or the given param {} is wrong".format(**args.source))
        parser.print_help()
        exit(1)
    
    if args.benchmark:
        benchmark(animator, 1000, nLeds = args.nleds)
        exit(0)
    else:
        a = animator(audio_source, screen)
        a.start()
    
