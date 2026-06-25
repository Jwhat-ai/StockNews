import feedparser as fd
import time
from datetime import datetime
from bs4 import BeautifulSoup
import re

RSS_FEEDS = {
    "stocks": "https://www.reddit.com/r/stocks/.rss",
    "wallstreetbets": "https://www.reddit.com/r/wallstreetbets/.rss",
    "SecurityAnalysis": "https://www.reddit.com/r/SecurityAnalysis/.rss",
    "investing": "https://www.reddit.com/r/investing/.rss",
}

def clean_html_content(html_text):
    """Clean HTML content and extract readable text"""
    if not html_text:
        return ""

    try:
        # Parse HTML and extract text
        soup = BeautifulSoup(html_text, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Get text and clean it up
        text = soup.gettext(separator=' ', strip=True)

        # Remove extra whitespace and clean up common patterns
        text = re.sub(r'\s+', ' ', text)  # Multiple spaces to single space
        text = re.sub(r'&nbsp;', ' ', text)  # HTML entities
        text = re.sub(r'&amp;', '&', text)
        text = re.sub(r'&lt;', '<', text)
        text = re.sub(r'&gt;', '>', text)

        # Remove Reddit-specific patterns
        text = re.sub(r'&#32; submitted by &#32; .*? <br />', '', text)
        text = re.sub(r'<span><a href=".*?">\[link\]</a></span> &#32; <span><a href=".*?">\[comments\]</a></span>', '', text)

        return text.strip()
    except Exception:
        # Fallback to simple text extraction
        # Remove HTML tags
        clean = re.sub(r'<.*?>', '', str(html_text))
        clean = re.sub(r'&[^;]+;', '', clean)
        return clean.strip()

def format_post_content(post_num, title, link, published, summary, author, tags):
    """Format a single post's content for better readability"""
    content = []
    content.append(f"\n{'='*50}")
    content.append(f"POST #{post_num}")
    content.append(f"{'='*50}")
    content.append(f"TITLE: {title}")
    content.append(f"URL: {link}")

    if published:
        content.append(f"PUBLISHED: {published}")

    if summary:
        content.append(f"\nSUMMARY:")
        content.append(f"{'-'*20}")
        # Wrap summary text to 80 characters
        lines = []
        for line in summary.split('\n'):
            while len(line) > 80:
                # Find a good break point
                break_point = line.rfind(' ', 0, 80)
                if break_point == -1:
                    break_point = 80
                lines.append(line[:break_point])
                line = line[break_point:].lstrip()
            if line:
                lines.append(line)
        content.extend(lines)

    if author:
        content.append(f"\nAUTHOR: {author}")

    if tags:
        content.append(f"\nTAGS: {tags}")

    content.append(f"{'='*50}\n")
    return '\n'.join(content)

def write_to_file(content, filename):
    """Write content to a text file with UTF-8 encoding"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

def scrape_reddit_feeds():
    """Scrape Reddit RSS feeds and save to text files"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    main_output = f"reddit_feeds_{timestamp}.txt"

    with open(main_output, 'w', encoding='utf-8') as f:
        f.write(f"Reddit RSS Feed Scraping Results\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")

        for subreddit, url in RSS_FEEDS.items():
            f.write(f"Subreddit: {subreddit}\n")
            f.write(f"URL: {url}\n")
            f.write("-" * 40 + "\n")

            try:
                # Try to parse the feed with retry logic
                feed = fd.parse(url)

                # Check if feed is well-formed
                if feed.bozo:
                    f.write(f"Warning: Feed might be malformed: {feed.bozo_exception}\n")

                # Get posts
                posts = feed.entries[:5]
                f.write(f"Total posts fetched: {len(posts)}\n\n")

                if len(posts) == 0:
                    f.write("No posts found. This might be due to:\n")
                    f.write("- Rate limiting from Reddit\n")
                    f.write("- Empty subreddit\n")
                    f.write("- RSS feed temporarily unavailable\n")
                    f.write("- Network issues\n\n")
                else:
                    for i, post in enumerate(posts):
                        # Extract post data
                        title = post.title if hasattr(post, 'title') else "No Title"
                        link = post.link if hasattr(post, 'link') else "No Link"
                        published = post.published if hasattr(post, 'published') else (post.updated if hasattr(post, 'updated') else None)

                        # Clean summary
                        summary_text = ""
                        if hasattr(post, 'summary'):
                            summary_text = clean_html_content(post.summary)
                        elif hasattr(post, 'description'):
                            summary_text = clean_html_content(post.description)

                        # Truncate long summaries
                        if summary_text and len(summary_text) > 1000:
                            summary_text = summary_text[:1000] + "..."

                        # Get author and tags
                        author = post.author if hasattr(post, 'author') else None
                        tags = None
                        if hasattr(post, 'tags') and post.tags:
                            tag_names = [tag.term for tag in post.tags if hasattr(tag, 'term')]
                            if tag_names:
                                tags = ', '.join(tag_names)

                        # Format and write
                        formatted_content = format_post_content(
                            i + 1, title, link, published, summary_text, author, tags
                        )
                        f.write(formatted_content)

                # Add delay between requests to be respectful
                f.write(f"Waiting 5 seconds before next request...\n\n")
                time.sleep(5)

            except Exception as e:
                f.write(f"Error fetching feed: {str(e)}\n")
                f.write(f"Attempted URL: {url}\n")
                f.write("Will retry in 10 seconds...\n\n")
                time.sleep(10)

            f.write("\n" + "=" * 60 + "\n\n")

        # Create individual files for each subreddit
        for subreddit, url in RSS_FEEDS.items():
            individual_file = f"{subreddit}_posts_{timestamp}.txt"
            with open(individual_file, 'w', encoding='utf-8') as ind_f:
                ind_f.write(f"r/{subreddit} Posts\n")
                ind_f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                ind_f.write(f"Source: {url}\n")
                ind_f.write("=" * 40 + "\n\n")

                try:
                    feed = fd.parse(url)
                    posts = feed.entries[:5]

                    if len(posts) == 0:
                        ind_f.write("No posts found for this subreddit.\n")
                        ind_f.write("This could be due to rate limiting or empty feed.\n")
                    else:
                        for i, post in enumerate(posts):
                            # Extract post data
                            title = post.title if hasattr(post, 'title') else "No Title"
                            link = post.link if hasattr(post, 'link') else "No Link"
                            published = post.published if hasattr(post, 'published') else None

                            # Clean summary
                            summary_text = ""
                            if hasattr(post, 'summary'):
                                summary_text = clean_html_content(post.summary)
                            elif hasattr(post, 'description'):
                                summary_text = clean_html_content(post.description)

                            # Truncate for individual files
                            if summary_text and len(summary_text) > 500:
                                summary_text = summary_text[:500] + "..."

                            # Get author
                            author = post.author if hasattr(post, 'author') else None

                            # Format and write for individual file (simpler format)
                            ind_f.write(f"\n{'='*40}")
                            ind_f.write(f"\nPOST #{i+1}")
                            ind_f.write(f"\n{'='*40}")
                            ind_f.write(f"\nTitle: {title}")
                            ind_f.write(f"\nLink: {link}")

                            if published:
                                ind_f.write(f"\nPublished: {published}")

                            if summary_text:
                                ind_f.write(f"\n\nSummary: {summary_text}")

                            if author:
                                ind_f.write(f"\n\nAuthor: {author}")

                            ind_f.write(f"\n{'='*40}\n")

                except Exception as e:
                    ind_f.write(f"Error fetching feed: {str(e)}\n")
                    ind_f.write(f"URL: {url}\n")

        f.write(f"All feeds scraped successfully!\n")
        f.write(f"Individual files saved:\n")
        for subreddit in RSS_FEEDS.keys():
            f.write(f"  - {subreddit}_posts_{timestamp}.txt\n")

if __name__ == "__main__":
    scrape_reddit_feeds()