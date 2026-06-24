(function () {
    'use strict';

    var form = document.getElementById('vendor-registration-form');
    var nextInput = document.getElementById('formsubmit-next');
    var successBanner = document.getElementById('vendor-form-success');

    if (nextInput) {
        nextInput.value =
            window.location.origin +
            window.location.pathname +
            '?sent=1#vendor-form';
    }

    if (window.location.search.indexOf('sent=1') !== -1 && successBanner) {
        successBanner.classList.add('is-visible');
        if (window.history.replaceState) {
            window.history.replaceState(null, '', window.location.pathname + '#vendor-form');
        }
    }

    if (form) {
        form.addEventListener('submit', function () {
            var btn = form.querySelector('button[type="submit"]');
            if (btn) {
                btn.disabled = true;
                var label = btn.querySelector('strong');
                if (label) {
                    label.textContent = 'جاري الإرسال…';
                }
            }
        });
    }
})();
