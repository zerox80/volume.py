#!/usr/bin/env python3
import shutil
import subprocess
import sys

DEFAULT_SINK = "@DEFAULT_AUDIO_SINK@"
TARGET = "1.50"  # = 110 %

def main():
    if not shutil.which("wpctl"):
        print("Fehler: 'wpctl' nicht gefunden. Bitte PipeWire/WirePlumber-Tools installieren.", file=sys.stderr)
        sys.exit(1)

    # Entstummen (falls stumm)
    subprocess.run(["wpctl", "set-mute", DEFAULT_SINK, "0"], check=False)

    # Lautstärke auf 110 % setzen
    try:
        subprocess.run(["wpctl", "set-volume", DEFAULT_SINK, TARGET], check=True)
    except subprocess.CalledProcessError as e:
        print(f"wpctl-Fehler: {e}", file=sys.stderr)
        sys.exit(1)

    # Anzeige des aktuellen Werts
    try:
        out = subprocess.check_output(["wpctl", "get-volume", DEFAULT_SINK], text=True).strip()
        print("Lautstärke gesetzt auf 150% (wpctl).")
        print(out)
    except Exception:
        pass

if __name__ == "__main__":
    main()
