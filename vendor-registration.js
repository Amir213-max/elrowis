(function () {
    'use strict';

    var companyName = document.getElementById('eoi-company-name');
    var counter = document.getElementById('eoi-company-counter');
    var yearInput = document.getElementById('eoi-year-establishment');
    var yearsDisplay = document.getElementById('eoi-years-display');
    var servicesTrigger = document.getElementById('eoi-services-trigger');
    var servicesPanel = document.getElementById('eoi-services-panel');
    var selectedTags = document.getElementById('eoi-selected-tags');
    var form = document.getElementById('eoi-form');

    function updateCounter() {
        if (!companyName || !counter) return;
        var len = companyName.value.length;
        counter.textContent = len + '/100';
    }

    function updateYears() {
        if (!yearInput || !yearsDisplay) return;
        var val = yearInput.value;
        if (!val) {
            yearsDisplay.textContent = 'N/A';
            return;
        }
        var year = new Date(val).getFullYear();
        if (isNaN(year)) {
            yearsDisplay.textContent = 'N/A';
            return;
        }
        var diff = new Date().getFullYear() - year;
        yearsDisplay.textContent = diff >= 0 ? String(diff) : 'N/A';
    }

    function bindUpload(btnId, inputId, dropId) {
        var btn = document.getElementById(btnId);
        var input = document.getElementById(inputId);
        var drop = document.getElementById(dropId);
        if (!btn || !input || !drop) return;

        function pick() { input.click(); }

        function showName() {
            if (input.files && input.files[0]) {
                drop.textContent = input.files[0].name;
                drop.classList.add('has-file');
            }
        }

        btn.addEventListener('click', pick);
        drop.addEventListener('click', pick);
        input.addEventListener('change', showName);
    }

    function getSelectedServices() {
        if (!servicesPanel) return [];
        return Array.prototype.slice.call(
            servicesPanel.querySelectorAll('input[type="checkbox"]:checked')
        ).map(function (cb) {
            return { value: cb.value, label: cb.dataset.label || cb.value };
        });
    }

    function renderTags() {
        if (!selectedTags || !servicesTrigger) return;
        var items = getSelectedServices();
        selectedTags.innerHTML = '';

        items.forEach(function (item) {
            var tag = document.createElement('span');
            tag.className = 'eoi-tag';
            tag.innerHTML = item.label + ' <button type="button" aria-label="Remove">&times;</button>';
            tag.querySelector('button').addEventListener('click', function () {
                var cb = servicesPanel.querySelector('input[value="' + item.value + '"]');
                if (cb) cb.checked = false;
                renderTags();
            });
            selectedTags.appendChild(tag);
        });

        if (items.length) {
            servicesTrigger.textContent = items.length + ' ' + (document.documentElement.lang === 'ar' ? 'خدمة محددة' : 'service(s) selected');
            servicesTrigger.classList.add('has-value');
        } else {
            servicesTrigger.textContent = servicesTrigger.dataset.placeholder || 'Select Service(s)';
            servicesTrigger.classList.remove('has-value');
        }
    }

    if (companyName) {
        companyName.addEventListener('input', updateCounter);
        updateCounter();
    }

    if (yearInput) {
        yearInput.addEventListener('change', updateYears);
        yearInput.addEventListener('input', updateYears);
    }

    bindUpload('eoi-upload-profile-btn', 'eoi-company-profile', 'eoi-profile-drop');
    bindUpload('eoi-upload-cr-btn', 'eoi-commercial-reg', 'eoi-cr-drop');

    if (servicesTrigger && servicesPanel) {
        servicesTrigger.addEventListener('click', function () {
            servicesPanel.classList.toggle('is-open');
        });

        servicesPanel.querySelectorAll('input[type="checkbox"]').forEach(function (cb) {
            cb.addEventListener('change', renderTags);
        });

        document.addEventListener('click', function (e) {
            if (!servicesTrigger.contains(e.target) && !servicesPanel.contains(e.target)) {
                servicesPanel.classList.remove('is-open');
            }
        });

        renderTags();
    }

    if (form) {
        var nextInput = document.getElementById('formsubmit-next');
        var successNotice = document.getElementById('eoi-success-notice');
        var submitBtn = document.getElementById('eoi-submit-btn');

        if (nextInput) {
            nextInput.value =
                window.location.origin +
                window.location.pathname +
                '?sent=1';
        }

        if (window.location.search.indexOf('sent=1') !== -1 && successNotice) {
            successNotice.classList.add('is-visible');
            if (window.history.replaceState) {
                window.history.replaceState(null, '', window.location.pathname);
            }
        }

        form.addEventListener('submit', function (e) {
            var existing = form.querySelector('input[name="الخدمات"]');
            if (existing) existing.remove();

            var services = getSelectedServices();
            if (!services.length) {
                e.preventDefault();
                alert(document.documentElement.lang === 'ar'
                    ? 'يرجى اختيار خدمة واحدة على الأقل.'
                    : 'Please select at least one service.');
                return;
            }

            var hidden = document.createElement('input');
            hidden.type = 'hidden';
            hidden.name = 'الخدمات';
            hidden.value = services.map(function (s) { return s.label; }).join('، ');
            form.appendChild(hidden);

            if (yearsDisplay && yearsDisplay.textContent !== 'N/A') {
                var yearsHidden = form.querySelector('input[name="سنوات التأسيس"]');
                if (!yearsHidden) {
                    yearsHidden = document.createElement('input');
                    yearsHidden.type = 'hidden';
                    yearsHidden.name = 'سنوات التأسيس';
                    form.appendChild(yearsHidden);
                }
                yearsHidden.value = yearsDisplay.textContent;
            }

            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = document.documentElement.lang === 'ar'
                    ? 'جاري الإرسال…'
                    : 'Sending…';
            }
        });
    }
})();
