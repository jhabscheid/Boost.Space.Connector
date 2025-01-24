import requests
import json

def publish_to_wordpress(
    worker_url: str,
    wordpress_api_key: str,
    wordpressurl: str,
    featuredimageurl: str,
    post_content: str,
    status: str = 'draft',
    title: str = "New WordPress Post",
    author_id: int = None,
    category_id: int = None
):
    """
    Publishes a post with featured image to WordPress via Cloudflare Worker.

    Args:
        worker_url (str): URL of the Cloudflare Worker
        wordpress_api_key (str): The WordPress API Key
        wordpressurl (str): The Website URL
        featuredimageurl (str): The URL to the featured Image
        post_content (str): The HTML Content for the Website
        title (str, optional): The title of the post. Defaults to "New WordPress Post"
        status (str, optional): Post status ('draft' or 'publish'). Defaults to 'draft'
        author_id (int, optional): WordPress user ID for post author
        category_id (int, optional): Category ID to assign to the post
    
    Returns:
        str: A message indicating success or failure of the operation
    """
    try:
        request_data = {
            'wordpress_api_key': wordpress_api_key,
            'wordpressurl': wordpressurl,
            'featuredimageurl': featuredimageurl,
            'post_content': post_content,
            'title': title,
            'status': status,
            'author_id': author_id,
            'category_id': category_id
        }
        # Remove sensitive data from logs
        log_data = request_data.copy()
        log_data['wordpress_api_key'] = '***'
        print("\nSending request to worker with data:", json.dumps(log_data, indent=2))
        
        response = requests.post(worker_url, json=request_data)
        print(f"\nResponse status code: {response.status_code}")
        
        try:
            response_text = response.text
            result = response.json()
            
            # Mask sensitive data in response logs
            if isinstance(result, dict):
                log_result = result.copy()
                if 'wordpress_api_key' in log_result:
                    log_result['wordpress_api_key'] = '***'
                print("\nParsed response:", json.dumps(log_result, indent=2))
            
            if response.status_code == 200 and result.get('success'):
                response_parts = [
                    f"Successfully created {result['message']}",
                    f"Post ID: {result['post_id']}",
                    f"URL (ID-based): {result['post_url']}",
                    f"URL (slug-based): {result.get('post_url_slug', 'Not available')}"
                ]
                if result.get('media_id'):
                    response_parts.append(f"Media ID: {result['media_id']}")
                if result.get('author_id'):
                    response_parts.append(f"Author ID: {result['author_id']}")
                return ". ".join(response_parts)
            else:
                error_msg = result.get('error', 'Unknown error')
                if result.get('response_data'):
                    error_msg += f"\nResponse data: {json.dumps(result['response_data'], indent=2)}"
                if result.get('response_text'):
                    error_msg += f"\nRaw response: {result['response_text']}"
                if result.get('details'):
                    error_msg += f"\nEndpoint: {result['details'].get('endpoint')}"
                return f"Request failed: {error_msg}"
        except ValueError as e:
            return f"Failed to parse response as JSON: {str(e)}\nRaw response: {response_text}"
            
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    # Example usage
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='Publish content to WordPress')
    parser.add_argument('worker_url', help='URL of the Cloudflare Worker')
    parser.add_argument('wordpress_api_key', help='WordPress API Key')
    parser.add_argument('wordpress_url', help='WordPress Site URL')
    parser.add_argument('featured_image_url', help='URL of the featured image')
    parser.add_argument('post_content', help='HTML content for the post')
    parser.add_argument('--status', default='draft', help='Post status (draft/publish)')
    parser.add_argument('--title', default='New WordPress Post', help='Post title')
    parser.add_argument('--author-id', type=int, help='WordPress user ID for post author')
    parser.add_argument('--category-id', type=int, help='Category ID to assign to the post')
    
    args = parser.parse_args()
    
    result = publish_to_wordpress(
        worker_url=args.worker_url,
        wordpress_api_key=args.wordpress_api_key,
        wordpressurl=args.wordpress_url,
        featuredimageurl=args.featured_image_url,
        post_content=args.post_content,
        status=args.status,
        title=args.title,
        author_id=args.author_id,
        category_id=args.category_id
    )
    print(result)
