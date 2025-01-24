import os
from wordpress_publisher import publish_to_wordpress

# Test configuration
WORKER_URL = os.getenv('WORDPRESS_WORKER_URL', 'https://your-worker.workers.dev')
WORDPRESS_API_KEY = os.getenv('WORDPRESS_API_KEY', 'your-api-key')
WORDPRESS_URL = os.getenv('WORDPRESS_URL', 'https://your-wordpress-site.com')
FEATURED_IMAGE_URL = os.getenv('FEATURED_IMAGE_URL', 'https://example.com/test-image.jpg')

def test_basic_post():
    """Test basic post creation with featured image"""
    try:
        result = publish_to_wordpress(
            worker_url=WORKER_URL,
            wordpress_api_key=WORDPRESS_API_KEY,
            wordpressurl=WORDPRESS_URL,
            featuredimageurl=FEATURED_IMAGE_URL,
            post_content="<h1>Test Post</h1><p>Basic post test</p>",
            title="Basic Post Test",
            status="draft"
        )
        print("\nBasic Post Test:", result)
    except Exception as e:
        print("\nBasic Post Test Error:", str(e))
        import traceback
        traceback.print_exc()

def test_with_author():
    """Test post creation with author ID"""
    try:
        result = publish_to_wordpress(
            worker_url=WORKER_URL,
            wordpress_api_key=WORDPRESS_API_KEY,
            wordpressurl=WORDPRESS_URL,
            featuredimageurl=FEATURED_IMAGE_URL,
            post_content="<h1>Author Test</h1><p>Post with author test</p>",
            title="Author Post Test",
            status="draft",
            author_id=1  # Usually 1 is the admin user
        )
        print("\nAuthor Test:", result)
    except Exception as e:
        print("\nAuthor Test Error:", str(e))
        import traceback
        traceback.print_exc()

def test_with_category():
    """Test post creation with category"""
    try:
        result = publish_to_wordpress(
            worker_url=WORKER_URL,
            wordpress_api_key=WORDPRESS_API_KEY,
            wordpressurl=WORDPRESS_URL,
            featuredimageurl=FEATURED_IMAGE_URL,
            post_content="<h1>Category Test</h1><p>Post with category test</p>",
            title="Category Post Test",
            status="draft",
            category_id=1  # Usually 1 is the default "Uncategorized" category
        )
        print("\nCategory Test:", result)
    except Exception as e:
        print("\nCategory Test Error:", str(e))
        import traceback
        traceback.print_exc()

def test_invalid_author():
    """Test error handling with invalid author ID"""
    try:
        result = publish_to_wordpress(
            worker_url=WORKER_URL,
            wordpress_api_key=WORDPRESS_API_KEY,
            wordpressurl=WORDPRESS_URL,
            featuredimageurl=FEATURED_IMAGE_URL,
            post_content="<h1>Invalid Author Test</h1>",
            title="Invalid Author Test",
            author_id="invalid"  # Should trigger validation error
        )
        print("\nInvalid Author Test:", result)
    except Exception as e:
        print("\nInvalid Author Test Error:", str(e))
        import traceback
        traceback.print_exc()

def test_invalid_status():
    """Test error handling with invalid status"""
    try:
        result = publish_to_wordpress(
            worker_url=WORKER_URL,
            wordpress_api_key=WORDPRESS_API_KEY,
            wordpressurl=WORDPRESS_URL,
            featuredimageurl=FEATURED_IMAGE_URL,
            post_content="<h1>Invalid Status Test</h1>",
            title="Invalid Status Test",
            status="invalid"  # Should trigger validation error
        )
        print("\nInvalid Status Test:", result)
    except Exception as e:
        print("\nInvalid Status Test Error:", str(e))
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Running integration tests...")
    print("\nRunning all tests to verify parameters...")
    test_basic_post()
    test_with_author()
    test_with_category()
    test_invalid_author()
    test_invalid_status()
