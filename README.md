# Podcast Marker

[![GitHub](https://img.shields.io/badge/GitHub-encoreshao%2Fpodcast--marker-blue?logo=github)](https://github.com/encoreshao/podcast-marker)

Generate podcast-ready markdown summaries and audio (MP3) from GitLab issues and comments, with support for multi-speaker TTS.

---

## Repository

Project home: [https://github.com/encoreshao/podcast-marker](https://github.com/encoreshao/podcast-marker)

---

## Features

- Fetches recent issues and comments from a GitLab project.
- Generates a well-structured markdown summary.
- Converts the markdown to an MP3 audio file using Google Text-to-Speech (gTTS), with alternating voices for sections.
- Modular codebase for easy reuse and extension.

---

## Requirements

- Python 3.8+
- [ffmpeg](https://ffmpeg.org/) (required for MP3 audio processing with `pydub`)

### Python dependencies

Install all dependencies with:

```bash
pip install -r requirements.txt
```

### FFmpeg installation

- **macOS:**
  `brew install ffmpeg`
- **Ubuntu:**
  `sudo apt-get install ffmpeg`
- **Windows:**
  Download from [ffmpeg.org/download.html](https://ffmpeg.org/download.html) and add the `bin` folder to your system PATH.

---

## Setup

1. **Clone the repository** and navigate to the project root:

   ```bash
   git clone git@github.com:encoreshao/podcast-marker.git
   cd podcast-marker
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your `.env` file** in the project root with the following variables:
   ```
   GITLAB_TOKEN=your_gitlab_token
   GITLAB_PROJECT_ID=your_project_id
   GITLAB_URL=https://gitlab.example.com
   ```

---

## Usage

### Command Line

Run the main script to fetch issues, generate markdown, and produce an MP3 audio file:

```bash
python src/podcast-marker/main.py --days 7
```

- `--days` (optional): Number of days to backtrack for issues/comments (default: 1).

The script will print the path to the generated markdown and MP3 files, which are saved in `outputs/podcast_markdowns/` and `outputs/podcast_audio/` respectively.

---

### As a Python Library

You can import and use any part of the workflow in your own scripts:

```python
from podcast_marker import fetch_gitlab_issues, generate_podcast_markdown, markdown_to_mp3

issues = fetch_gitlab_issues(days_to_backtrack=3)
md_path = generate_podcast_markdown(issues, days_to_backtrack=3)
mp3_path = markdown_to_mp3(md_path)
```

---

## Project Structure

```
src/podcast-marker/
  ├── __init__.py
  ├── main.py
  ├── gitlab_api.py
  ├── markdown_gen.py
  └── audio_gen.py
outputs/
  ├── podcast_markdowns/
  └── podcast_audio/
```

---

## Notes

- The TTS step uses gTTS and requires an internet connection.
- The audio generator alternates between US and UK English voices for different sections.
- For large markdown files, the script splits the text into sections for more natural audio.
- All outputs are saved in the `outputs/` directory for easy access.

---

## Contributors

- [Encore Shao](https://github.com/encoreshao/)

---

## License

MIT
