#!/usr/bin/env python3
import shutil
import subprocess
import argparse
import sys

def run(cmd):
    try:
        subprocess.run(cmd, check=True)
        return True
    except FileNotFoundError:
        return False
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Ausführen: {' '.join(cmd)}\n{e}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description="Setze die Systemlautstärke (PulseAudio/PipeWire).")
    parser.add_argument(
        "--volume",
        required=True,
        help="Lautstärke (z. B. '90%%' oder '1.3' für 130%%)"
    )
    args = parser.parse_args()
    volume = args.volume

    # 1) Versuch: pactl
    if shutil.which("pactl"):
        run(["pactl", "set-sink-mute", "@DEFAULT_SINK@", "0"])
        if run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", volume]):
            print(f"Lautstärke ist jetzt auf {volume} (über pactl).")
            return

    # 2) Fallback: wpctl
    if shutil.which("wpctl"):
        run(["wpctl", "set-mute", "@DEFAULT_AUDIO_SINK@", "0"])
        # wpctl erwartet float (1.0 = 100%), darum ggf. Prozentzeichen konvertieren
        if volume.endswith("%"):
            try:
                vol_val = float(volume.strip("%")) / 100.0
            except ValueError:
                print("Ungültiger Wert für --volume", file=sys.stderr)
                sys.exit(1)
        else:
            try:
                vol_val = float(volume)
            except ValueError:
                print("Ungültiger Wert für --volume", file=sys.stderr)
                sys.exit(1)

        if run(["wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", str(vol_val)]):
            print(f"Lautstärke ist jetzt auf {volume} (über wpctl).")
            return

    print(
        "Konnte weder 'pactl' noch 'wpctl' ausführen.\n"
        "Bitte installiere ggf. 'pulseaudio-utils' (für pactl) oder 'wireplumber' (für wpctl).",
        file=sys.stderr
    )

if __name__ == "__main__":
    main()
