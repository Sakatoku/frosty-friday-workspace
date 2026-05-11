from __future__ import annotations

import argparse
import csv
import io
from pathlib import Path

from PIL import Image


def convert_webp_to_png_csv(
    input_dir: Path,
    output_dir: Path,
    output_csv: Path,
    resize: tuple[int, int] | None = None,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    webp_files = sorted(input_dir.rglob("*.webp"))

    with output_csv.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["FILE_NAME", "IMAGE_BYTES"])

        for webp_path in webp_files:
            png_name = f"{webp_path.stem}.png"
            png_path = output_dir / png_name

            with Image.open(webp_path) as image:
                if resize is not None:
                    image = image.resize(resize)
                buffer = io.BytesIO()
                image.save(buffer, format="PNG")
                png_bytes = buffer.getvalue()

            png_path.write_bytes(png_bytes)
            writer.writerow([png_name, png_bytes.hex()])


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert all WEBP files under a directory to PNG and export a CSV."
    )
    parser.add_argument(
        "input_dir", type=Path, help="Directory that contains WEBP files"
    )
    parser.add_argument(
        "output_dir",
        type=Path,
        nargs="?",
        default=Path("png_output"),
        help="Directory to save PNG files (default: png_output)",
    )
    parser.add_argument(
        "output_csv",
        type=Path,
        nargs="?",
        default=Path("images.csv"),
        help="CSV file path (default: images.csv)",
    )
    parser.add_argument(
        "--resize",
        type=int,
        nargs=2,
        metavar=("WIDTH", "HEIGHT"),
        help="Resize output PNG to WIDTH HEIGHT before saving",
    )
    args = parser.parse_args()

    resize = tuple(args.resize) if args.resize else None
    convert_webp_to_png_csv(
        args.input_dir, args.output_dir, args.output_csv, resize=resize
    )


if __name__ == "__main__":
    main()
