#!/usr/bin/env python3
import shutil
import subprocess
import sys

# 1.50 = 150%  |  1.10 = 110%
TARGET_FACTOR = 1.50

def main():
    wpctl = shutil.which("wpctl")
    pactl = shutil.which("pactl")

    if wpctl:
        sink = "@DEFAULT_AUDIO_SINK@"
        # Entstummen
        subprocess.run([wpctl, "set-mute", sink, "0"], check=False)
        # Lautstärke setzen (Faktor)
        try:
            subprocess.run([wpctl, "set-volume", sink, f"{TARGET_FACTOR:.2f}"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"wpctl-Fehler: {e}", file=sys.stderr)
            sys.exit(1)
        try:
            out = subprocess.check_output([wpctl, "get-volume", sink], text=True).strip()
            print(f"Lautstärke gesetzt auf {int(TARGET_FACTOR*100)}% (wpctl).")
            print(out)
        except Exception:
            pass
        return

    if pactl:
        sink = "@DEFAULT_SINK@"
        percent = f"{int(round(TARGET_FACTOR * 100))}%"
        subprocess.run([pactl, "set-sink-mute", sink, "0"], check=False)
        try:
            subprocess.run([pactl, "set-sink-volume", sink, percent], check=True)
        except subprocess.CalledProcessError as e:
            print(f"pactl-Fehler: {e}", file=sys.stderr)
            sys.exit(1)
        try:
            vol = subprocess.check_output([pactl, "get-sink-volume", sink], text=True).strip()
            print(f"Lautstärke gesetzt auf {percent} (pactl).")
            print(vol)
        except Exception:
            pass
        return

    print("Weder 'wpctl' (PipeWire) noch 'pactl' (PulseAudio) gefunden. Bitte eins von beiden installieren.", file=sys.stderr)
    sys.exit(1)

if __name__ == "__main__":
    main()
