/**
 * Created by nicolasvodoz on 9/5/15.
 */
 $(document).ready(function() {
            $(".clickable-row").click(function() {
                window.document.location = $(this).data("href");
            });
        });