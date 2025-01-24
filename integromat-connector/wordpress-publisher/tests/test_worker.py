import pytest
from unittest.mock import Mock, MagicMock
import sys
import os
import json

# Add parent directory to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wordpress_publisher import publish_to_wordpress

def create_mock_response(status_code, json_data):
    """Helper function to create properly configured mock responses"""
    mock_response = MagicMock()
    mock_response.status_code = status_code
    mock_response.json.return_value = json_data
    mock_response.text = json.dumps(json_data)
    mock_response.headers = {'Content-Type': 'application/json'}
    return mock_response

def test_publish_to_wordpress_success_with_title(mocker):
    # Mock successful response
    mock_response = create_mock_response(200, {
        'success': True,
        'post_id': 123,
        'post_url': 'https://example.com/post/123',
        'post_url_slug': 'https://example.com/custom-title',
        'media_id': 456,
        'message': 'Successfully created publish post'
    })
    mocker.patch('requests.post', return_value=mock_response)

    result = publish_to_wordpress(
        worker_url='https://test-worker.example.com',
        wordpress_api_key='test_key',
        wordpressurl='https://example.com',
        featuredimageurl='https://example.com/image.jpg',
        post_content='<h1>Test</h1>',
        title='Custom Title',
        status='publish'
    )
    
    assert 'Successfully created' in result
    assert '123' in result
    assert 'https://example.com/post/123' in result

def test_publish_to_wordpress_with_defaults(mocker):
    # Mock successful response with defaults
    mock_response = create_mock_response(200, {
        'success': True,
        'post_id': 123,
        'post_url': 'https://example.com/post/123',
        'post_url_slug': 'https://example.com/new-wordpress-post',
        'media_id': 456,
        'message': 'Successfully created draft post'
    })
    mocker.patch('requests.post', return_value=mock_response)

    result = publish_to_wordpress(
        worker_url='https://test-worker.example.com',
        wordpress_api_key='test_key',
        wordpressurl='https://example.com',
        featuredimageurl='https://example.com/image.jpg',
        post_content='<h1>Test</h1>'
    )
    
    assert 'Successfully created' in result
    assert 'draft post' in result

def test_publish_to_wordpress_error(mocker):
    # Mock error response
    mock_response = create_mock_response(500, {
        'success': False,
        'error': 'Internal server error'
    })
    mocker.patch('requests.post', return_value=mock_response)

    result = publish_to_wordpress(
        worker_url='https://test-worker.example.com',
        wordpress_api_key='test_key',
        wordpressurl='https://example.com',
        featuredimageurl='https://example.com/image.jpg',
        post_content='<h1>Test</h1>'
    )
    
    assert 'Request failed' in result

def test_publish_to_wordpress_success_with_all_params(mocker):
    # Mock successful response with all parameters
    mock_response = create_mock_response(200, {
        'success': True,
        'post_id': 123,
        'post_url': 'https://example.com/post/123',
        'post_url_slug': 'https://example.com/custom-title',
        'media_id': 456,
        'author_id': 789,
        'message': 'Successfully created publish post'
    })
    mocker.patch('requests.post', return_value=mock_response)

    result = publish_to_wordpress(
        worker_url='https://test-worker.example.com',
        wordpress_api_key='test_key',
        wordpressurl='https://example.com',
        featuredimageurl='https://example.com/image.jpg',
        post_content='<h1>Test</h1>',
        title='Custom Title',
        status='publish',
        author_id=789,
        category_id=101
    )
    
    assert 'Successfully created' in result
    assert '123' in result
    assert 'https://example.com/post/123' in result

def test_publish_to_wordpress_network_error(mocker):
    # Mock network error
    mocker.patch('requests.post', side_effect=Exception('Network error'))

    result = publish_to_wordpress(
        worker_url='https://test-worker.example.com',
        wordpress_api_key='test_key',
        wordpressurl='https://example.com',
        featuredimageurl='https://example.com/image.jpg',
        post_content='<h1>Test</h1>'
    )
    
    assert 'An error occurred' in result
    assert 'Network error' in result

def test_publish_to_wordpress_invalid_author_id(mocker):
    # Mock validation error response for invalid author_id
    mock_response = create_mock_response(400, {
        'success': False,
        'error': 'author_id must be a valid integer'
    })
    mocker.patch('requests.post', return_value=mock_response)

    result = publish_to_wordpress(
        worker_url='https://test-worker.example.com',
        wordpress_api_key='test_key',
        wordpressurl='https://example.com',
        featuredimageurl='https://example.com/image.jpg',
        post_content='<h1>Test</h1>',
        author_id='invalid'  # Invalid author_id to trigger validation error
    )
    
    assert 'Request failed' in result
    assert 'author_id must be a valid integer' in result

def test_publish_to_wordpress_without_protocol(mocker):
    """Test handling of URLs without http(s):// protocol"""
    mock_response = create_mock_response(200, {
        'success': True,
        'post_id': 123,
        'post_url': 'https://example.com/post/123',
        'post_url_slug': 'https://example.com/protocol-test',
        'media_id': 456,
        'message': 'Successfully created draft post'
    })
    mocker.patch('requests.post', return_value=mock_response)

    result = publish_to_wordpress(
        worker_url='test-worker.example.com',  # No protocol
        wordpress_api_key='test_key',
        wordpressurl='example.com',  # No protocol
        featuredimageurl='storage.googleapis.com/image.jpg',  # No protocol
        post_content='<h1>Protocol Test</h1>',
        title='Protocol Test'
    )
    
    assert 'Successfully created' in result
    assert '123' in result
    assert 'https://example.com/post/123' in result

def test_publish_to_wordpress_validation_error(mocker):
    # Mock validation error response for invalid status
    mock_response = create_mock_response(400, {
        'success': False,
        'error': 'Invalid status. Must be either "draft" or "publish"'
    })
    mocker.patch('requests.post', return_value=mock_response)

    result = publish_to_wordpress(
        worker_url='https://test-worker.example.com',
        wordpress_api_key='test_key',
        wordpressurl='https://example.com',
        featuredimageurl='https://example.com/image.jpg',
        post_content='<h1>Test</h1>',
        status='invalid'  # Invalid status to trigger validation error
    )
    
    assert 'Request failed' in result
    assert 'Invalid status' in result

if __name__ == '__main__':
    pytest.main([__file__])
