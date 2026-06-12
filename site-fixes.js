(function () {
    'use strict';

    var REMOTE_BASE = 'https://nesmapartners.com/';

    // Resolve asset base from this script's location (works from root, en/, ar/, article/)
    (function setAssetBase() {
        var scripts = document.getElementsByTagName('script');
        for (var i = 0; i < scripts.length; i++) {
            var src = scripts[i].getAttribute('src') || '';
            if (src.indexOf('site-fixes.js') !== -1) {
                window.__ASSET_BASE__ = src.substring(0, src.lastIndexOf('/') + 1);
                return;
            }
        }
        window.__ASSET_BASE__ = '/';
    })();

    function resolveStorageUrl(src) {
        if (!src || src.startsWith('http://') || src.startsWith('https://') || src.startsWith('data:')) {
            return src;
        }
        var base = window.__ASSET_BASE__ || './';
        if (src.charAt(0) === '/') {
            src = src.replace(/^\//, '');
        }
        if (src.startsWith('storage/')) {
            return base + src;
        }
        return src;
    }

    function toRemoteUrl(src) {
        if (!src || src.startsWith('http://') || src.startsWith('https://') || src.startsWith('data:')) {
            return src;
        }
        if (src.includes('nesmapartners.com/') || src.includes('nesmacms.originmena.com/')) {
            return src;
        }
        var clean = src.replace(/^(\.\.\/)+/, '').replace(/^\//, '');
        if (clean.startsWith('storage/')) {
            return REMOTE_BASE + clean;
        }
        return src;
    }

    function fixStoragePaths() {
        document.querySelectorAll('[data-src]').forEach(function (el) {
            var src = el.getAttribute('data-src');
            if (!src || src.startsWith('http') || src.startsWith('data:')) {
                return;
            }
            el.setAttribute('data-src', resolveStorageUrl(src));
        });
        document.querySelectorAll('img[src^="/storage/"]').forEach(function (el) {
            el.setAttribute('src', resolveStorageUrl(el.getAttribute('src')));
        });
    }

    function loadLazyImages() {
        document.querySelectorAll('.load_img[data-src]').forEach(function (el) {
            var src = resolveStorageUrl(el.getAttribute('data-src'));
            if (!src) return;
            el.setAttribute('data-src', src);
            if (!el.getAttribute('src')) {
                el.setAttribute('src', src);
            }
        });
    }

    function patchGalleryImages() {
        document.querySelectorAll('#gallery img').forEach(function (img) {
            ['data-src', 'src'].forEach(function (attr) {
                var value = img.getAttribute(attr);
                if (!value || value.startsWith('http') || value.startsWith('data:')) {
                    return;
                }
                var fixed = resolveStorageUrl(value);
                if (fixed && fixed !== value) {
                    img.setAttribute(attr, fixed);
                }
            });
            var src = img.getAttribute('data-src') || img.getAttribute('src');
            if (src && !src.startsWith('http') && !src.startsWith('data:')) {
                img.setAttribute('src', resolveStorageUrl(src));
            }
        });
    }

    function resizeGalleryFlickity() {
        if (!window.Flickity) {
            return;
        }
        document.querySelectorAll('#gallery .gallery_slider').forEach(function (slider) {
            var flkty = window.Flickity.data(slider);
            if (flkty) {
                flkty.resize();
            }
        });
    }

    function initGallerySlider() {
        patchGalleryImages();

        document.querySelectorAll('#gallery .gallery_slider').forEach(function (slider) {
            var imgs = slider.querySelectorAll('img');
            var pending = imgs.length;

            function maybeResize() {
                pending -= 1;
                if (pending > 0) {
                    return;
                }
                resizeGalleryFlickity();
                setTimeout(resizeGalleryFlickity, 800);
            }

            if (!pending) {
                resizeGalleryFlickity();
                return;
            }

            imgs.forEach(function (img) {
                var src = resolveStorageUrl(img.getAttribute('data-src') || img.getAttribute('src'));
                if (src) {
                    img.setAttribute('src', src);
                }
                if (img.complete) {
                    maybeResize();
                } else {
                    img.addEventListener('load', maybeResize);
                    img.addEventListener('error', maybeResize);
                }
            });
        });
    }

    function scheduleGalleryFixes() {
        [0, 800, 2000, 4000, 6000].forEach(function (delay) {
            setTimeout(function () {
                patchGalleryImages();
                initGallerySlider();
                resizeGalleryFlickity();
            }, delay);
        });
    }

    function fallbackBrokenImages() {
        document.querySelectorAll('.load_bg').forEach(function (el) {
            var src = el.getAttribute('data-src') || el.dataset.src;
            var bg = el.style.backgroundImage || '';
            var match = bg.match(/url\(["']?([^"')]+)["']?\)/);
            var url = src || (match ? match[1] : '');
            if (!url || url.startsWith('data:')) return;

            var img = new Image();
            img.onerror = function () {
                var remote = toRemoteUrl(url);
                if (remote && remote !== url) {
                    el.style.backgroundImage = 'url(' + remote + ')';
                }
            };
            img.src = url;
        });

        document.querySelectorAll('.load_img, img[data-src]').forEach(function (el) {
            var src = el.getAttribute('data-src') || el.getAttribute('src');
            if (!src) return;
            el.addEventListener('error', function onErr() {
                var remote = toRemoteUrl(src);
                if (remote && remote !== el.src) {
                    el.src = remote;
                }
                el.removeEventListener('error', onErr);
            });
        });
    }

    function ensureVisibility() {
        var wrapper = document.getElementById('smooth-wrapper');
        if (wrapper) {
            wrapper.style.visibility = 'visible';
        }
    }

    function replaceBrandLogos() {
        document.querySelectorAll('.main_logo svg path').forEach(function (path) {
            path.setAttribute('fill', '#003d53');
        });
    }

    function updateBrandMeta() {
        var isAr = document.documentElement.lang === 'ar' || document.documentElement.dir === 'rtl';
        var brand = isAr ? 'الرويس' : 'Alruwais';
        var tagline = isAr ? 'معاً نبني التميز' : 'Together, We Build Excellence';
        var desc = isAr
            ? 'الرويس ملتزمة ببناء مستقبل أفضل من خلال التقدم المبتكر والمستدام للمجتمعات التي نخدمها.'
            : 'Alruwais is committed to shaping a better future through innovative, sustainable progress for the communities we serve.';
        var base = window.__ASSET_BASE__ || './';
        var ogImage = base + 'images/og-alruwais.png';

        function cleanBrand(text) {
            if (!text) return text;
            text = text
                .replace(/نسما[\s\u00a0]*(?:&|و)[\s\u00a0]*شرك[\s\u00a0]*(?:اهم|ائها|ائه)/gi, brand)
                .replace(/Nesma[\s\u00a0]*(?:&amp;|&)[\s\u00a0]*Partners/gi, brand)
                .replace(/Nesma[\s\u00a0]+and[\s\u00a0]+Partners/gi, brand);
            if (text === brand + ' - ' + brand) {
                return brand + ' - ' + tagline;
            }
            return text;
        }

        if (document.title) {
            document.title = cleanBrand(document.title);
        }

        document.querySelectorAll('meta[property="og:title"], meta[name="twitter:title"]').forEach(function (meta) {
            var content = meta.getAttribute('content');
            if (!content) return;
            meta.setAttribute('content', cleanBrand(content));
        });

        document.querySelectorAll('meta[name="description"], meta[property="og:description"], meta[name="twitter:description"]').forEach(function (meta) {
            meta.setAttribute('content', desc);
        });

        document.querySelectorAll('meta[property="og:image"], meta[name="twitter:image"]').forEach(function (meta) {
            meta.setAttribute('content', ogImage);
        });

        document.querySelectorAll('script[type="application/ld+json"]').forEach(function (node) {
            try {
                var data = JSON.parse(node.textContent);
                if (data.name) data.name = cleanBrand(data.name);
                if (data.headline) data.headline = cleanBrand(data.headline);
                data.description = desc;
                node.textContent = JSON.stringify(data);
            } catch (e) { /* ignore */ }
        });

        var iconUrl = base + 'images/favicon-alruwais-32x32.png?v=3';
        document.querySelectorAll('link[rel="icon"], link[rel="shortcut icon"], link[rel="apple-touch-icon"]').forEach(function (link) {
            link.setAttribute('href', iconUrl);
            link.setAttribute('type', 'image/png');
        });
    }

    function patchBackgroundImages() {
        document.querySelectorAll('.load_bg[data-src]').forEach(function (el) {
            var src = el.getAttribute('data-src') || el.dataset.src;
            if (!src) return;
            if (!el.style.backgroundImage || el.style.backgroundImage === 'url()') {
                el.style.backgroundImage = 'url(' + src + ')';
            }
        });
    }

    function setupFormFallbacks() {
        document.querySelectorAll('form[wire\\:submit]').forEach(function (form) {
            if (form.dataset.offlineHandled) return;
            form.dataset.offlineHandled = 'true';

            form.addEventListener('submit', function (e) {
                e.preventDefault();
                e.stopPropagation();

                var emailInput = form.querySelector('input[type="email"]');
                var email = emailInput ? emailInput.value : '';
                var isNewsletter = form.classList.contains('ft_form');
                var isContact = form.closest('.form_side') || form.id === 'contact-us-form';

                if (isNewsletter && email) {
                    window.location.href = 'mailto:info@nesmapartners.com?subject=Newsletter%20Subscription&body=Please%20subscribe%20me%20to%20the%20newsletter:%20' + encodeURIComponent(email);
                    return;
                }

                if (isContact) {
                    var name = (form.querySelector('[wire\\:model="name"]') || form.querySelector('input[name="name"]'));
                    var message = (form.querySelector('[wire\\:model="message"]') || form.querySelector('textarea'));
                    var subject = 'Contact Form - Nesma Partners';
                    var body = 'Name: ' + (name ? name.value : '') + '\nEmail: ' + email + '\n\n' + (message ? message.value : '');
                    window.location.href = 'mailto:info@nesmapartners.com?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
                    return;
                }

                alert(document.documentElement.lang === 'ar'
                    ? 'النموذج غير متصل بالخادم. يرجى التواصل عبر info@nesmapartners.com'
                    : 'Form is offline. Please contact us at info@nesmapartners.com');
            }, true);
        });
    }

    function addOfflineNotices() {
        var isAr = document.documentElement.lang === 'ar';
        var notice = isAr
            ? 'ملاحظة: سيتم فتح بريدك الإلكتروني لإرسال الرسالة.'
            : 'Note: Your email client will open to send this message.';

        document.querySelectorAll('form[wire\\:submit]').forEach(function (form) {
            if (form.nextElementSibling && form.nextElementSibling.classList.contains('form_offline_notice')) return;
            var span = document.createElement('span');
            span.className = 'form_offline_notice';
            span.textContent = notice;
            form.parentNode.insertBefore(span, form.nextSibling);
        });
    }

    fixStoragePaths();
    loadLazyImages();
    ensureVisibility();

    document.addEventListener('DOMContentLoaded', function () {
        fixStoragePaths();
        loadLazyImages();
        ensureVisibility();
        patchBackgroundImages();
        setupFormFallbacks();
        addOfflineNotices();
        updateBrandMeta();
    });

    replaceBrandLogos();
    updateBrandMeta();

    window.addEventListener('load', function () {
        fixStoragePaths();
        loadLazyImages();
        ensureVisibility();
        patchBackgroundImages();
        fallbackBrokenImages();
        replaceBrandLogos();
        updateBrandMeta();
        initGallerySlider();
        scheduleGalleryFixes();
    });

    setTimeout(function () {
        ensureVisibility();
        initGallerySlider();
        scheduleGalleryFixes();
    }, 3500);
})();
