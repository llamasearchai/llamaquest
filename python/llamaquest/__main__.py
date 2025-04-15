"""
Main entry point for LlamaQuest game
"""

import argparse
import os
import sys

from .game import GameEngine, run_game


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="LlamaQuest - A retro-style adventure game"
    )

    parser.add_argument(
        "--level",
        "-l",
        type=str,
        default="village",
        help="Starting level name (default: village)",
    )
    parser.add_argument(
        "--fullscreen", "-f", action="store_true", help="Start in fullscreen mode"
    )
    parser.add_argument(
        "--scale", "-s", type=int, default=4, help="Display scale factor (default: 4)"
    )
    parser.add_argument("--debug", "-d", action="store_true", help="Enable debug mode")

    return parser.parse_args()


def check_requirements():
    """Check if all requirements are met"""
    try:
        import numpy
        import pyxel
    except ImportError as e:
        print(f"Error: Missing required dependencies: {e}")
        print(
            "Please install all required packages with: pip install -r requirements.txt"
        )
        sys.exit(1)

    # Check for assets directory
    assets_dir = os.path.join(os.path.dirname(__file__), "..", "..", "assets")
    if not os.path.exists(assets_dir):
        print(f"Warning: Assets directory not found at {assets_dir}")
        print("Creating assets directory...")
        os.makedirs(os.path.join(assets_dir, "worlds"), exist_ok=True)
        os.makedirs(os.path.join(assets_dir, "sprites"), exist_ok=True)
        os.makedirs(os.path.join(assets_dir, "sounds"), exist_ok=True)

        # Create an empty resource file
        try:
            import pyxel

            pyxel.init(160, 120)
            pyxel.save(os.path.join(assets_dir, "resource.pyxres"))
        except Exception as e:
            print(f"Warning: Could not create empty resource file: {e}")


def main():
    """Main entry point"""
    print("Starting LlamaQuest...")

    # Parse command line arguments
    args = parse_args()

    # Check requirements
    check_requirements()

    # Configure game
    config = {
        "screen_width": 160,
        "screen_height": 120,
        "scale": args.scale,
        "fps": 60,
        "title": "LlamaQuest",
        "start_level": args.level,
        "fullscreen": args.fullscreen,
        "debug": args.debug,
    }

    # Start the game
    try:
        game = GameEngine(config)
        game.start()
    except Exception as e:
        print(f"Error: {e}")
        if args.debug:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
