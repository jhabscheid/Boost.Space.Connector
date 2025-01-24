<?php
/**
 * Uninstall hook for Make Connector plugin
 *
 * This file runs when the plugin is uninstalled to clean up plugin data.
 */

// If uninstall not called from WordPress, exit
if (!defined('WP_UNINSTALL_PLUGIN')) {
    exit;
}

// Clean up the API key from site options
delete_site_option('iwc_api_key');
