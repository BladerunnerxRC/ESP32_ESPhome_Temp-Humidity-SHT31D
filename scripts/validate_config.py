"""Validate an isolated config using dummy secrets; never upload firmware."""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--generate-only', action='store_true')
    parser.add_argument('--config', type=Path,
                        default=Path(__file__).resolve().parents[1] / 'enviro-a1.yaml')
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='enviro-a1-') as directory:
        target = Path(directory)
        shutil.copy2(args.config, target / 'enviro-a1.yaml')
        (target / 'secrets.yaml').write_text('''wifi_ssid: validation-network
wifi_password: validation-password
enviro_a1_api_key: AQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQE=
enviro_a1_ap_sid: validation-recovery
enviro_a1_ap_pwd: validation-password
''', encoding='utf-8')
        command = [sys.executable, '-m', 'esphome', 'compile',
                   str(target / 'enviro-a1.yaml')]
        if args.generate_only:
            command.append('--only-generate')
        subprocess.run(command, check=True)


if __name__ == '__main__':
    main()
