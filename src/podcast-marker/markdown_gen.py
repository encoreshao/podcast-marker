from datetime import datetime, timedelta
import os


def generate_podcast_markdown(issues, days_to_backtrack=1):
    """
    Generate a markdown file summarizing GitLab issues and comments for podcast content creation.

    Args:
        issues (list): List of issue dicts, each with recent comments and label names.
        days_to_backtrack (int): Number of days to look back for the summary window (default: 1).

    Returns:
        str: Path to the generated markdown file, or None if no issues provided.

    The markdown file is saved in outputs/podcast_markdowns/ with a date-based filename.
    """
    if not issues:
        return

    today = datetime.now()
    output_dir = os.path.join('outputs', 'podcast_markdowns')
    os.makedirs(output_dir, exist_ok=True)
    filename = f"podcast_material_{today.strftime('%Y%m%d')}.md"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        # Write header
        f.write(f"# Business Development Update - Week of {today.strftime('%B %d, %Y')}\n\n")
        f.write("## Overview\n")
        f.write(f"This update covers business development activities and discussions from {(today - timedelta(days=days_to_backtrack)).strftime('%B %d')} to {today.strftime('%B %d')}.\n\n")

        # Categorize issues
        open_issues = [i for i in issues if i['state'] == 'opened']
        closed_issues = [i for i in issues if i['state'] == 'closed']

        # Recent Discussions by Status
        f.write("## Recent Updates and Discussions\n\n")

        # Active Projects (Open Issues)
        if open_issues:
            f.write("### Active Projects\n")
            for issue in open_issues:
                f.write(f"#### {issue['title']}\n")
                if issue['description']:
                    f.write(f"{issue['description']}\n\n")
                if issue.get('label_names'):
                    f.write("**Labels:** " + ", ".join(issue['label_names']) + "\n")
                if issue.get('due_date'):
                    f.write(f"**Due Date:** {issue['due_date']}\n")
                f.write("\n**Recent Updates:**\n")
                sorted_comments = sorted(issue['recent_comments'], key=lambda x: x['created_at'], reverse=True)
                for comment in sorted_comments:
                    f.write(f"- [{comment['created_at'][:10]}] {comment['body']}\n")
                f.write("\n")

        # Completed Projects (Closed Issues)
        if closed_issues:
            f.write("### Recently Completed\n")
            for issue in closed_issues:
                f.write(f"#### {issue['title']}\n")
                if issue['description']:
                    f.write(f"{issue['description']}\n\n")
                f.write(f"**Completed:** {issue['closed_at'][:10]}\n\n")
                f.write("**Final Updates:**\n")
                sorted_comments = sorted(issue['recent_comments'], key=lambda x: x['created_at'], reverse=True)
                for comment in sorted_comments:
                    f.write(f"- [{comment['created_at'][:10]}] {comment['body']}\n")
                f.write("\n")

        # Looking Forward section
        f.write("## Looking Forward\n")
        f.write("*Key initiatives and upcoming milestones:*\n\n")
        for issue in open_issues:
            if issue.get('due_date'):
                f.write(f"- {issue['title']} (Due: {issue['due_date']})\n")
            else:
                f.write(f"- {issue['title']} (Ongoing)\n")

    print(f"\nMarkdown file generated: {filepath}")
    return filepath