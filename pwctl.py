#!/usr/bin/env python3
import argparse
import subprocess
import sys
import shutil

DEFAULT_SINK = "@DEFAULT_AUDIO_SINK@"

def parse_volume(v: str) -> str:
    """Konvertiert '150%' -> '1.5' oder gibt Float-String unverändert zurück."""
    v = v.strip()
    if v.endswith("%"):
        try:
            return str(float(v[:-1]) / 100.0)
        except ValueError:
            print("Ungültiger Prozentwert für --volume", file=sys.stderr)
            sys.exit(1)
    try:
        float(v)  # Validierung
        return v
    except ValueError:
        print("Ungültiger Wert für --volume (verwende z. B. '150%%' oder '1.5')", file=sys.stderr)
        sys.exit(1)

def main():
    if not shutil.which("wpctl"):
        print("Fehler: 'wpctl' nicht gefunden. Bitte WirePlumber/PipeWire-Tools installieren.", file=sys.stderr)
        sys.exit(1)

    ap = argparse.ArgumentParser(description="Setzt die Systemlautstärke mit wpctl (PipeWire/WirePlumber).")
    ap.add_argument("--volume", required=True, help="z. B. '90%%' oder '1.3' (=130%%)")
    args = ap.parse_args()

    vol = parse_volume(args.volume)

    # Entstummen (ignoriert Fehler, falls schon unmute)
    try:
        subprocess.run(["wpctl", "set-mute", DEFAULT_SINK, "0"], check=False)
        # Lautstärke setzen (1.0 = 100 %, >1.0 = Überverstärkung)
        subprocess.run(["wpctl", "set-volume", DEFAULT_SINK, vol], check=True)
    except subprocess.CalledProcessError as e:
        print(f"wpctl-Fehler: {e}", file=sys.stderr)
        sys.exit(1)

    # Aktuellen Wert anzeigen
    try:
        out = subprocess.check_output(["wpctl", "get-volume", DEFAULT_SINK], text=True).strip()
        print(f"Lautstärke gesetzt auf {args.volume} (wpctl).")
        print(out)
    except Exception:
        pass

if __name__ == "__main__":
    main()
