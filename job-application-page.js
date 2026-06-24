(function () {
    'use strict';

    var form = document.getElementById('job-application-form');
    var nextInput = document.getElementById('job-formsubmit-next');
    var successBanner = document.getElementById('job-form-success');

    if (nextInput) {
        nextInput.value =
            window.location.origin +
            window.location.pathname +
            '?sent=1#job-application-form';
    }

    if (window.location.search.indexOf('sent=1') !== -1 && successBanner) {
        successBanner.classList.add('is-visible');
        if (window.history.replaceState) {
            window.history.replaceState(null, '', window.location.pathname + '#job-application-form');
        }
    }

    if (form) {
        form.addEventListener('submit', function () {
            var btn = form.querySelector('button[type="submit"]');
            if (btn) {
                btn.disabled = true;
                var label = btn.querySelector('strong');
                if (label) {
                    label.textContent = document.documentElement.lang === 'ar'
                        ? 'جاري الإرسال…'
                        : 'Sending…';
                }
            }
        });
    }
})();
