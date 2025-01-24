<?php
namespace Integromat;

if (!defined('ABSPATH')) {
    exit;
}
?>
<div class="key-regeneration-section">
    <h2>API Key Management</h2>
    <form method="POST" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" class="key-regeneration-form">
        <?php wp_nonce_field('regenerate_key_nonce'); ?>
        <input type="hidden" name="action" value="regenerate_key" />
        <button type="submit" class="button button-secondary">Regenerate Key</button>
    </form>
</div>
