"""
Blog Posts Module - Stub implementation
Manages blog posts for the website
"""

from datetime import datetime

# Sample blog posts for demonstration
BLOG_POSTS = [
    {
        'slug': 'understanding-vo2max',
        'title': 'Understanding VO2max and Its Impact on Health',
        'excerpt': 'Learn what VO2max means and why it matters for your fitness and longevity.',
        'date': datetime(2024, 11, 1),
        'author': 'MetaboMax Pro Team',
        'content': '''
        <h2>What is VO2max?</h2>
        <p>VO2max is the maximum amount of oxygen your body can use during intense exercise...</p>
        '''
    },
    {
        'slug': 'metabolic-testing-101',
        'title': 'Metabolic Testing 101: What You Need to Know',
        'excerpt': 'A comprehensive guide to metabolic testing and how it can optimize your health.',
        'date': datetime(2024, 10, 15),
        'author': 'MetaboMax Pro Team',
        'content': '''
        <h2>Introduction to Metabolic Testing</h2>
        <p>Metabolic testing provides valuable insights into how your body processes energy...</p>
        '''
    }
]

def get_all_posts():
    """Get all blog posts"""
    return sorted(BLOG_POSTS, key=lambda x: x['date'], reverse=True)

def get_post_by_slug(slug):
    """Get a specific blog post by slug"""
    for post in BLOG_POSTS:
        if post['slug'] == slug:
            return post
    return None

def get_recent_posts(limit=3):
    """Get recent blog posts"""
    posts = get_all_posts()
    return posts[:limit]
