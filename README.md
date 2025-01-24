# Make Connector WordPress Plugin

A WordPress plugin that safely connects your site to make.com and allows working with custom meta fields through the REST API.

## Recent Changes (v1.5.9)

### API Key Management Improvements
- Added "Regenerate Key" button in the WordPress admin interface
- Implemented secure key regeneration with proper permissions and nonce verification
- Added automatic key cleanup on plugin uninstall
- Fixed form submission to use admin-post.php for better security
- Separated key regeneration form from main settings for improved UX

### User Interface Updates
- Renamed menu from "Make" to "Make-Boost"
- Updated menu icon to use Bandit Logo
- Improved form layout and user experience
- Added success messages after key regeneration

### Plugin Metadata Updates
- Updated author to Joe Habscheid
- Updated website to https://habscheid.com
- Incremented version number to 1.5.9
- Directory renamed from boost-space-connector to integromat-connector

## Installation

1. Upload the "integromat-connector" folder to the "/wp-content/plugins/" directory
2. Activate the plugin through the "Plugins" menu in WordPress
3. Find the "Make-Boost" menu item in your admin panel to:
   - View your API key for connecting to Make.com
   - Regenerate your API key if needed
   - Configure custom fields visibility in REST API responses

## Features

- Secure API key generation and management
- Custom meta fields support in REST API
- Safe connection to Make.com
- Custom taxonomies support
- API calls logging capability

## Security

- API keys are stored securely in WordPress site options
- Key regeneration protected by WordPress nonce verification
- Admin-level permissions required for key management
- Automatic cleanup of sensitive data on uninstall

## Requirements

- WordPress 5.0 or higher
- PHP 7.2 or higher

## License

GPLv2 or later

## Credits

Originally developed by Celonis s.r.o., now maintained by Joe Habscheid.
