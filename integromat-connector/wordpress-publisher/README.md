# WordPress Publisher Cloudflare Worker

A Cloudflare Worker that facilitates publishing posts to WordPress with featured images, custom authors, and categories.

## Setup Instructions

1. Install Wrangler CLI:
```bash
npm install -g wrangler
```

2. Login to Cloudflare:
```bash
wrangler login
```

3. Create a `wrangler.toml` file in your project directory:
```toml
name = "wordpress-publisher"
main = "worker.js"
compatibility_date = "2024-01-24"
```

4. Deploy the worker:
```bash
wrangler deploy
```

## API Reference

### Endpoint
POST request to your worker URL

### Headers
- `Content-Type: application/json`

### Request Body Parameters

#### Required Parameters
- `wordpress_api_key` (string): Your WordPress API key
- `wordpressurl` (string): Your WordPress site URL
- `featuredimageurl` (string): URL of the featured image
- `post_content` (string): HTML content for the post

#### Optional Parameters
- `title` (string): Post title (default: "New WordPress Post")
- `status` (string): Post status ("draft" or "publish", default: "draft")
- `author_id` (integer): WordPress user ID for post author
- `category_id` (integer): Category ID to assign to the post

### Response Format
```json
{
  "success": true,
  "post_id": 123,
  "post_url": "https://example.com/post/123",
  "media_id": 456,
  "author_id": 789,
  "message": "Successfully created draft post"
}
```

### Error Responses
The worker returns detailed error messages for:
- Missing required parameters
- Invalid parameter types
- Network errors
- WordPress API errors
- Image upload failures

## Python Client Usage

```python
from wordpress_publisher import publish_to_wordpress

result = publish_to_wordpress(
    worker_url="YOUR_WORKER_URL",
    wordpress_api_key="your_api_key",
    wordpressurl="https://your-site.com",
    featuredimageurl="https://path-to-image.jpg",
    post_content="<h1>Test Post</h1>",
    title="Custom Title",
    status="draft",
    author_id=789,
    category_id=101
)
print(result)
```

## Authentication

The worker uses the WordPress plugin's custom authentication method with the `IWC-API-KEY` header. Make sure your WordPress site has the Make Connector plugin installed and configured.

## Error Handling

The worker includes comprehensive error handling:
- Validates all input parameters
- Verifies image content type
- Handles network errors gracefully
- Provides detailed error messages
- Returns appropriate HTTP status codes

## Testing

Run the test suite:
```bash
python -m pytest tests/
```

The test suite includes:
- Success cases with all parameters
- Default parameter handling
- Error scenarios
- Parameter validation
- Network error handling
