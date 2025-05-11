import argparse
from gitlab_api import fetch_gitlab_issues
from markdown_gen import generate_podcast_markdown
from audio_gen import markdown_to_mp3

def main():
    parser = argparse.ArgumentParser(description="Generate podcast audio from GitLab issues.")
    parser.add_argument('--days', type=int, default=1, help='Number of days to backtrack for issues/comments (default: 1)')
    args = parser.parse_args()

    days_to_backtrack = args.days
    issues = fetch_gitlab_issues(days_to_backtrack=days_to_backtrack)
    if issues:
        md_path = generate_podcast_markdown(issues, days_to_backtrack=days_to_backtrack)
        if md_path:
            print("\nConverting markdown to audio (MP3) using gTTS...")
            mp3_path = markdown_to_mp3(md_path)
            print(f"MP3 file generated: {mp3_path}")

if __name__ == "__main__":
    main()
