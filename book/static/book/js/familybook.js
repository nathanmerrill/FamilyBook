new WOW().init();
(function ($) {
    $(document).ready(function () {
        var $post = $('#new-post');
        $post.on('keydown', 'textarea', function (e) {
            if (e.ctrlKey && e.keyCode === 13) {
                $($post, 'button[type="submit"]').trigger('submit');
            }
        });
        $post.on('change', 'input[type="file"]', function () {
            var $btn = $(this).parent();
            var fileCount = this.files.length;
            if (fileCount >= 1) {
                $btn.removeClass('btn-secondary');
                $btn.addClass('btn-secondary-outline');
                $btn.find('span').html('+' + fileCount + ' files');
            } else {
                $btn.removeClass('btn-secondary-outline');
                $btn.addClass('btn-secondary');
                $btn.find('span').html('Add files');
            }
        });
        toastr.options.closeButton = true;
        toastr.options.timeout = 0;
        $.each(errors, function (i, error) {
            toastr.error(error);
        });
         $('.mdb-select').material_select();
    });
})(jQuery);
