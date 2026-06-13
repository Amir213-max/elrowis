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

    function updateMapPath(index) {
        var cards = document.querySelectorAll('#map .map_card');
        var paths = document.querySelectorAll('#map .map_vector path');
        if (!cards[index]) return;
        var locationID = cards[index].dataset.location;
        var pathTarget = document.getElementById(locationID);
        paths.forEach(function (path) {
            path.classList.remove('active');
        });
        if (pathTarget) {
            pathTarget.classList.add('active');
        }
    }

    function forceVisible(el) {
        if (!el) return;
        el.style.setProperty('visibility', 'visible', 'important');
        el.style.setProperty('opacity', '1', 'important');
        el.style.setProperty('transform', 'none', 'important');
    }

    function revealMapProjects(slider) {
        if (!slider) return;
        slider.classList.add('inview');
        forceVisible(slider);
        slider.querySelectorAll('.map_project, .map_card, .map_card_cover, .map_card_head, ._eleY, .load_bg').forEach(forceVisible);
    }

    function destroyMapFlickity(slider) {
        if (!slider) return;
        if (window.Flickity) {
            var flkty = window.Flickity.data(slider);
            if (flkty) flkty.destroy();
        }
        slider.classList.remove('flickity-enabled', 'flickity-rtl', 'map-mobile-native', 'map-scroll-native', 'map-slide-native');
        slider.removeAttribute('style');
        slider.querySelectorAll('.map_project').forEach(function (p) {
            p.removeAttribute('style');
            p.classList.remove('is-active');
        });
        delete slider.dataset.mapFixed;
        delete slider.dataset.mapMode;
    }

    function isMapCarouselViewport() {
        return window.innerWidth <= 1200;
    }

    function restoreMapProjectsDom(slider) {
        if (!slider) return;
        var viewport = slider.querySelector('.flickity-viewport');
        if (viewport) {
            var track = viewport.querySelector('.flickity-slider');
            if (track) {
                Array.prototype.slice.call(track.children).forEach(function (child) {
                    slider.appendChild(child);
                });
            }
            viewport.remove();
        }
        slider.querySelectorAll('.map_project').forEach(function (project) {
            if (project.parentElement !== slider) {
                slider.appendChild(project);
            }
        });
    }

    function getMapProjectCells(slider) {
        restoreMapProjectsDom(slider);
        var cells = slider.querySelectorAll('.map_project');
        return Array.prototype.slice.call(cells);
    }

    function reorderMapSection() {
        if (!isMapCarouselViewport()) return;
        var hero = document.querySelector('#map .map_hero');
        var head = document.querySelector('#map .map_head_set');
        var vector = document.querySelector('#map .map_vector');
        var projects = document.querySelector('#map .map_projects_set');
        if (!hero || !head || !vector || !projects) return;
        if (head.nextElementSibling !== vector) {
            hero.insertBefore(head, vector);
        }
        if (vector.nextElementSibling !== projects) {
            hero.insertBefore(projects, null);
        }
    }

    function initMobileNativeSlider(slider, projectsSet) {
        destroyMapFlickity(slider);
        restoreMapProjectsDom(slider);
        reorderMapSection();
        patchBackgroundImages();
        revealMapProjects(slider);
        revealMapProjects(projectsSet);

        var projects = getMapProjectCells(slider);
        if (!projects.length) return null;

        var state = {
            index: typeof projectsSet.__mobileIdx === 'number' ? projectsSet.__mobileIdx : 0
        };

        slider.classList.remove('map-mobile-native', 'map-scroll-native');
        slider.classList.add('map-slide-native');
        slider.dataset.mapMode = 'slide-native';
        slider.dataset.mapFixed = '1';
        slider.scrollLeft = 0;

        function show(index) {
            state.index = Math.max(0, Math.min(index, projects.length - 1));
            projectsSet.__mobileIdx = state.index;
            projects.forEach(function (project, i) {
                var active = i === state.index;
                project.classList.toggle('is-active', active);
                project.style.setProperty('display', active ? 'block' : 'none', 'important');
                forceVisible(project);
                project.querySelectorAll('.map_card, ._eleY, .load_bg').forEach(forceVisible);
            });
            updateMapPath(state.index);
            updateMapDots(projectsSet, api, state.index);
            ensureMapNav(projectsSet, api);
        }

        var api = {
            cells: projects,
            get selectedIndex() { return state.index; },
            select: function (index) { show(index); },
            previous: function () { show(state.index - 1); },
            next: function () { show(state.index + 1); }
        };

        projectsSet.__mapFlkty = api;
        show(state.index);
        return api;
    }

    function isMapMobile() {
        return window.innerWidth <= 600;
    }

    function syncMapCarouselCells(flkty, slider) {
        var viewport = slider.querySelector('.flickity-viewport');
        var viewportWidth = viewport ? viewport.clientWidth : slider.offsetWidth;
        if (!viewportWidth) viewportWidth = slider.offsetWidth;

        var isTablet = viewportWidth > 600;
        var cellWidth;

        if (isTablet) {
            var pad = 48;
            var gap = 12;
            var available = Math.max(0, viewportWidth - pad);
            cellWidth = Math.max(180, Math.floor((available - gap) / 2));
        } else {
            cellWidth = viewportWidth;
        }

        flkty.options.rightToLeft = false;
        flkty.options.percentPosition = false;
        flkty.options.adaptiveHeight = true;
        flkty.options.contain = true;
        flkty.options.cellAlign = isTablet ? 'left' : 'center';
        slider.classList.remove('flickity-rtl');

        flkty.cells.forEach(function (cell) {
            cell.size.width = cellWidth;
            if (cell.element) {
                cell.element.style.width = cellWidth + 'px';
                cell.element.style.margin = '0';
            }
        });
    }

    function resizeMapFlickityViewport(flkty) {
        if (!flkty.viewport || !flkty.selectedElement) return;
        var height = flkty.selectedElement.offsetHeight;
        if (height > 0) {
            flkty.viewport.style.height = (height + 4) + 'px';
        }
        if (typeof flkty.reposition === 'function') {
            flkty.reposition();
        }
    }

    function ensureMapNav() {
        /* arrows removed on mobile — dots only */
    }

    function initMapCarousel(slider, projectsSet) {
        var FlickityCtor = window.Flickity;
        if (!FlickityCtor) return null;

        revealMapProjects(slider);
        var existing = FlickityCtor.data(slider);
        var idx = existing ? existing.selectedIndex : 0;
        if (existing) existing.destroy();

        slider.classList.remove('flickity-rtl');
        slider.querySelectorAll('.map_project').forEach(function (p) {
            p.removeAttribute('style');
        });

        var flkty = new FlickityCtor(slider, {
            prevNextButtons: false,
            pageDots: false,
            draggable: true,
            percentPosition: false,
            cellAlign: isMapMobile() ? 'center' : 'left',
            rightToLeft: false,
            adaptiveHeight: true,
            contain: true,
            watchCSS: false,
            friction: 0.8,
            selectedAttraction: 0.2
        });

        syncMapCarouselCells(flkty, slider);
        flkty.resize();
        if (typeof flkty.reposition === 'function') flkty.reposition();

        var safe = Math.min(Math.max(0, idx), Math.max(0, flkty.cells.length - 1));
        flkty.select(safe, false, true);
        resizeMapFlickityViewport(flkty);
        revealMapProjects(slider);
        updateMapPath(safe);

        flkty.off('change');
        flkty.on('change', function (i) {
            updateMapPath(i);
            resizeMapFlickityViewport(flkty);
            ensureMapNav(projectsSet, flkty);
            updateMapDots(projectsSet, flkty, i);
            revealMapProjects(slider);
        });

        slider.dataset.mapFixed = '1';
        return flkty;
    }

    function refreshMapCarouselAfterImages(slider, projectsSet) {
        var flkty = window.Flickity && window.Flickity.data(slider);
        if (!flkty) return;
        syncMapCarouselCells(flkty, slider);
        flkty.resize();
        resizeMapFlickityViewport(flkty);
        ensureMapNav(projectsSet, flkty);
    }

    function updateMapDots() {
        /* dots removed — swipe between projects */
    }

    function needsMapFix(slider) {
        if (!slider.classList.contains('flickity-enabled')) return true;
        if (slider.classList.contains('flickity-rtl')) return true;
        if (slider.dataset.mapFixed !== '1') return true;
        var flkty = window.Flickity && window.Flickity.data(slider);
        return !flkty || flkty.options.rightToLeft;
    }

    function fixMapProjectsCarousel(attempt) {
        attempt = attempt || 0;
        if (!isMapCarouselViewport()) return;

        var projectsSet = document.querySelector('#map .map_projects_set');
        var slider = document.querySelector('#map .map_projects');
        if (!projectsSet || !slider) return;

        revealMapProjects(slider);
        revealMapProjects(projectsSet);
        patchBackgroundImages();
        reorderMapSection();

        var existingDots = projectsSet.querySelector('.map_projects_dots');
        if (existingDots) existingDots.remove();
        var existingNav = projectsSet.querySelector('.map_projects_nav');
        if (existingNav) existingNav.remove();

        if (slider.dataset.mapMode === 'slide-native' && !slider.classList.contains('flickity-enabled')) {
            var activeApi = projectsSet.__mapFlkty;
            if (activeApi) {
                updateMapDots(projectsSet, activeApi, activeApi.selectedIndex);
                ensureMapNav(projectsSet, activeApi);
            }
            revealMapProjects(slider);
            return;
        }

        initMobileNativeSlider(slider, projectsSet);
    }

    function watchMapSlider() {
        var slider = document.querySelector('#map .map_projects');
        if (!slider || slider.dataset.mapWatch) return;
        slider.dataset.mapWatch = '1';
        var observer = new MutationObserver(function () {
            if (isMapCarouselViewport() && slider.classList.contains('flickity-enabled')) {
                fixMapProjectsCarousel();
            }
        });
        observer.observe(slider, { attributes: true, attributeFilter: ['class'] });
    }

    function scheduleMapCarouselFixes() {
        fixMapProjectsCarousel();
        setTimeout(fixMapProjectsCarousel, 300);
        setTimeout(fixMapProjectsCarousel, 800);
        setTimeout(fixMapProjectsCarousel, 1500);
        setTimeout(fixMapProjectsCarousel, 3000);
        setTimeout(fixMapProjectsCarousel, 5000);
        setTimeout(fixMapProjectsCarousel, 8000);

        var ticks = 0;
        var guard = setInterval(function () {
            if (!isMapCarouselViewport()) {
                clearInterval(guard);
                return;
            }
            revealMapProjects(document.querySelector('#map .map_projects'));
            fixMapProjectsCarousel();
            ticks += 1;
            if (ticks >= 12) clearInterval(guard);
        }, 1000);
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
        watchMapSlider();
        reorderMapSection();
        if (isMapCarouselViewport()) {
            fixMapProjectsCarousel();
        }
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
        scheduleMapCarouselFixes();
        watchMapSlider();
    });

    window.addEventListener('resize', function () {
        clearTimeout(window.__mapCarouselResize);
        window.__mapCarouselResize = setTimeout(function () {
            var slider = document.querySelector('#map .map_projects');
            if (slider) {
                delete slider.dataset.mapFixed;
                delete slider.dataset.mapMode;
            }
            fixMapProjectsCarousel();
        }, 200);
    });

    scheduleMapCarouselFixes();

    setTimeout(function () {
        ensureVisibility();
        initGallerySlider();
        scheduleGalleryFixes();
    }, 3500);
})();
