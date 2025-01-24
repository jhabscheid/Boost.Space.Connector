// WordPress Post Publisher Worker

// Validation helper functions
function validateParams(params) {
  const required = ['wordpress_api_key', 'wordpressurl', 'featuredimageurl', 'post_content'];
  const missing = required.filter(param => !params[param]);
  
  if (missing.length > 0) {
    throw new Error(`Missing required parameters: ${missing.join(', ')}`);
  }
  
  if (params.status && !['draft', 'publish'].includes(params.status)) {
    throw new Error('Invalid status. Must be either "draft" or "publish"');
  }

  if (params.author_id && !Number.isInteger(Number(params.author_id))) {
    throw new Error('author_id must be a valid integer');
  }

  if (params.category_id && !Number.isInteger(Number(params.category_id))) {
    throw new Error('category_id must be a valid integer');
  }
}

function sanitizeUrl(url) {
  return url.replace(/\/$/, '');
}

addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  // Log request details
  console.log('Request details:', {
    method: request.method,
    headers: Object.fromEntries(request.headers.entries()),
    url: request.url
  });

  // Only allow POST requests
  if (request.method !== 'POST') {
    return new Response(JSON.stringify({
      success: false,
      error: 'Method not allowed'
    }), {
      status: 405,
      headers: { 'Content-Type': 'application/json' }
    });
  }

  try {
    // Try to parse request body
    let params;
    const contentType = request.headers.get('content-type') || '';
    const userAgent = request.headers.get('user-agent') || '';
    console.log('Content-Type:', contentType);
    console.log('User-Agent:', userAgent);

    try {
      // First try to parse as JSON
      const clonedRequest = request.clone();
      const text = await clonedRequest.text();
      console.log('Raw request body:', text);
      
      try {
        params = JSON.parse(text);
      } catch (jsonError) {
        console.log('Failed to parse as JSON, trying form data');
        // If JSON parsing fails, try form data
        const formData = new URLSearchParams(text);
        params = Object.fromEntries(formData.entries());
      }
    } catch (e) {
      console.error('Failed to parse request body:', e);
      return new Response(JSON.stringify({
        success: false,
        error: 'Failed to parse request body. Expected JSON or form data.',
        details: e.message
      }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    console.log('Parsed parameters:', params);
    console.log('Request headers:', Object.fromEntries(request.headers.entries()));
    
    let params;
    const requestContentType = request.headers.get('content-type');
    console.log('Content-Type:', requestContentType);
    
    if (requestContentType && requestContentType.includes('application/x-www-form-urlencoded')) {
      const formData = await request.formData();
      params = Object.fromEntries(formData.entries());
      console.log('Parsed form data:', params);
    } else {
      params = await request.json();
      console.log('Parsed JSON data:', params);
    }
    
    const { wordpress_api_key, wordpressurl, featuredimageurl, post_content, status = 'draft' } = params;

    // Validate parameters
    try {
      validateParams(params);
    } catch (validationError) {
      return new Response(JSON.stringify({
        success: false,
        error: validationError.message
      }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    // Fetch and validate image
    const imageResponse = await fetch(featuredimageurl);
    if (!imageResponse.ok) {
      return new Response(JSON.stringify({
        success: false,
        error: `Failed to fetch image: HTTP ${imageResponse.status}`
      }), {
        status: 502,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    const contentType = imageResponse.headers.get('content-type');
    if (!contentType || !contentType.startsWith('image/')) {
      return new Response(JSON.stringify({
        success: false,
        error: 'Invalid content type. URL must point to an image file.'
      }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    const imageBuffer = await imageResponse.arrayBuffer();
    const imageBlob = new Blob([imageBuffer], { type: contentType });

    // Upload image to WordPress
    const formData = new FormData();
    formData.append('file', imageBlob, 'featured-image' + (contentType === 'image/jpeg' ? '.jpg' : '.png'));

    const baseUrl = sanitizeUrl(wordpressurl);
    console.log('Uploading media to WordPress...');
    console.log('Request URL:', `${baseUrl}/wp-json/wp/v2/media`);
    console.log('Headers:', {
      'Accept': 'application/json',
      'IWC-API-KEY': wordpress_api_key
    });
    
    const uploadResponse = await fetch(`${baseUrl}/wp-json/wp/v2/media`, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'IWC-API-KEY': wordpress_api_key
      },
      body: formData
    });
    
    console.log('Media upload response status:', uploadResponse.status);
    console.log('Media upload response headers:', Object.fromEntries(uploadResponse.headers.entries()));

    if (!uploadResponse.ok) {
      let errorText;
      try {
        const errorJson = await uploadResponse.json();
        errorText = errorJson.message || errorJson.error || await uploadResponse.text();
      } catch {
        errorText = await uploadResponse.text();
      }
      return new Response(JSON.stringify({
        success: false,
        error: `WordPress media upload failed: ${errorText}`,
        status_code: uploadResponse.status,
        details: {
          endpoint: 'media',
          headers: Object.fromEntries(uploadResponse.headers.entries())
        }
      }), {
        status: uploadResponse.status,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    // Handle media upload response
    let uploadResult;
    try {
      const responseText = await uploadResponse.text();
      console.log('Raw media upload response:', responseText);
      
      try {
        uploadResult = JSON.parse(responseText);
        // Handle case where response might be double-encoded JSON
        if (typeof uploadResult === 'string') {
          uploadResult = JSON.parse(uploadResult);
        }
        console.log('Parsed media upload response:', JSON.stringify(uploadResult, null, 2));
      } catch (parseError) {
        console.error('Failed to parse response as JSON:', parseError);
        return new Response(JSON.stringify({
          success: false,
          error: 'Failed to parse media upload response as JSON',
          raw_response: responseText,
          parse_error: parseError.message
        }), {
          status: 502,
          headers: { 'Content-Type': 'application/json' }
        });
      }
    } catch (e) {
      console.error('Failed to read response:', e);
      return new Response(JSON.stringify({
        success: false,
        error: 'Failed to read media upload response',
        error_details: e.message
      }), {
        status: 502,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    // Check for media ID in various possible locations
    const mediaId = uploadResult.id || uploadResult.ID;
    console.log('Extracted media ID:', mediaId);
    console.log('Full response structure:', Object.keys(uploadResult));
    
    if (!mediaId) {
      return new Response(JSON.stringify({
        success: false,
        error: 'WordPress media upload succeeded but no media ID was returned',
        response_data: uploadResult
      }), {
        status: 502,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    // Create post with featured image
    const postResponse = await fetch(`${baseUrl}/wp-json/wp/v2/posts`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'IWC-API-KEY': wordpress_api_key
      },
      body: JSON.stringify({
        title: params.title || 'New WordPress Post',
        content: post_content,
        status: status,
        featured_media: mediaId,
        author: params.author_id ? Number(params.author_id) : undefined,
        categories: params.category_id ? [Number(params.category_id)] : undefined
      })
    });

    if (!postResponse.ok) {
      let errorText;
      try {
        const errorJson = await postResponse.json();
        errorText = errorJson.message || errorJson.error || await postResponse.text();
      } catch {
        errorText = await postResponse.text();
      }
      return new Response(JSON.stringify({
        success: false,
        error: `WordPress post creation failed: ${errorText}`,
        status_code: postResponse.status,
        details: {
          endpoint: 'posts',
          headers: Object.fromEntries(postResponse.headers.entries())
        }
      }), {
        status: postResponse.status,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    const postResult = await postResponse.json();
    console.log('Full post response:', JSON.stringify(postResult, null, 2));
    
    // Get the slug-based URL by combining site URL with post slug
    const siteRoot = sanitizeUrl(wordpressurl);
    const postTitle = params.title || 'New WordPress Post';
    const postSlug = postResult.slug || postTitle.toLowerCase().replace(/[^a-z0-9]+/g, '-');
    const slugUrl = `${siteRoot}/${postSlug}/`;
    
    return new Response(JSON.stringify({
      success: true,
      post_id: postResult.id,
      post_url: postResult.link,
      post_url_slug: slugUrl,
      media_id: mediaId,
      author_id: postResult.author,
      message: `Successfully created ${status} post`
    }), {
      headers: { 'Content-Type': 'application/json' }
    });

  } catch (error) {
    return new Response(JSON.stringify({
      success: false,
      error: `Internal server error: ${error.message}`
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}
