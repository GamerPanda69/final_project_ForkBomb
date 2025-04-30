// static/js/script.js
$(document).ready(function() {
    console.log("Custom script loaded.");

    // --- Page Load Animation ---
    // The 'slide-in' class is now added directly in the templates.
    // You can add more complex entrance animations here if desired.

    // --- Tool Form Toggling (Using Bootstrap Collapse) ---
    // The accordion in tools.html now handles showing/hiding forms via Bootstrap's
    // Collapse plugin, triggered by the buttons. No extra JS needed for this basic toggle.

    // --- Optional: Smooth Scroll for internal links (if you add any) ---
    $('a[href^="#"]').on('click', function(event) {
        var target = $(this.getAttribute('href'));
        if( target.length ) {
            event.preventDefault();
            $('html, body').stop().animate({
                scrollTop: target.offset().top - 70 // Adjust offset for sticky navbar
            }, 800); // Duration in milliseconds
        }
    });

    // --- Optional: Auto-dismiss alerts (if not handled per-page) ---
    // Uncomment this if you want all alerts to fade out after a delay
    /*
    window.setTimeout(function() {
        $(".alert-dismissible").fadeTo(500, 0).slideUp(500, function(){
            $(this).remove();
        });
    }, 7000); // 7 seconds delay
    */

    // --- Form Submission Indicator (Example) ---
    // Show a simple loading state on buttons when forms are submitted
    $('form').on('submit', function() {
        var $btn = $(this).find('button[type="submit"]');
        // Disable button and show spinner (using Font Awesome)
        if ($btn.length) {
            $btn.prop('disabled', true);
            // Append spinner icon - ensure Font Awesome is loaded
            $btn.html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...');
        }
        // Note: If the submission fails and the page re-renders with errors,
        // the button state will reset automatically. If using AJAX, you'd need
        // to re-enable the button manually on success/error.
    });


    console.log("jQuery version:", $.fn.jquery); // Verify jQuery is loaded
});