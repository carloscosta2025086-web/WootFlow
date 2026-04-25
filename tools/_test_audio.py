"""Test AudioReactive module with system audio capture."""
import sys, time
sys.path.insert(0, r"c:\Users\bl4z3\Documents\VSC\RGB_Key")
from audio_reactive import AudioReactive

ar = AudioReactive()
print(f"Available: {AudioReactive.available()}")

if ar.start():
    print(f"Started - capturing: {ar.device_name}")
    for i in range(10):
        time.sleep(0.1)
        bands = ar.get_bands()
        vol = ar.get_volume()
        bar = "".join(["█" if b > 0.1 else "░" for b in bands])
        print(f"  Vol={vol:.3f}  [{bar}]")
    ar.stop()
    print("Stopped OK")
else:
    print("FAILED to start")
