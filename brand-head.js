(function () {
    'use strict';

    var docEl = document.documentElement;
    var isAr = docEl.lang === 'ar' || docEl.getAttribute('dir') === 'rtl';
    var brand = isAr ? 'الرويس' : 'Alruwais';
    var tagline = isAr ? 'معاً نبني التميز' : 'Together, We Build Excellence';

    function scriptBase() {
        var scripts = document.getElementsByTagName('script');
        for (var i = 0; i < scripts.length; i++) {
            var src = scripts[i].getAttribute('src') || '';
            if (src.indexOf('brand-head.js') !== -1) {
                return src.substring(0, src.lastIndexOf('/') + 1);
            }
        }
        return './';
    }

    function cleanBrand(text) {
        if (!text) return text;
        return text
            .replace(/نسما[\s\u00a0]*(?:&|و)[\s\u00a0]*شرك[\s\u00a0]*(?:اهم|ائها|ائه)/gi, brand)
            .replace(/Nesma[\s\u00a0]*(?:&amp;|&)[\s\u00a0]*Partners/gi, brand)
            .replace(/Nesma[\s\u00a0]+and[\s\u00a0]+Partners/gi, brand);
    }

    function setFavicon() {
        var iconUrl = scriptBase() + 'images/favicon-alruwais-32x32.png?v=1';
        var links = document.querySelectorAll('link[rel="icon"], link[rel="shortcut icon"], link[rel="apple-touch-icon"]');
        if (!links.length) {
            var link = document.createElement('link');
            link.rel = 'icon';
            link.type = 'image/png';
            link.href = iconUrl;
            document.head.appendChild(link);
            return;
        }
        links.forEach(function (el) {
            el.setAttribute('href', iconUrl);
            el.setAttribute('type', 'image/png');
        });
    }

    function updateTitles() {
        var titleEl = document.querySelector('title');
        if (titleEl) {
            titleEl.textContent = cleanBrand(titleEl.textContent);
        }

        document.querySelectorAll('meta[property="og:title"], meta[name="twitter:title"]').forEach(function (meta) {
            var content = meta.getAttribute('content');
            if (!content) return;
            if (/Nesma[\s\u00a0]*(?:&amp;|&)[\s\u00a0]*Partners[\s\u00a0]*-[\s\u00a0]*Together/i.test(content)) {
                meta.setAttribute('content', brand + ' - ' + tagline);
            } else {
                meta.setAttribute('content', cleanBrand(content));
            }
        });

        document.querySelectorAll('script[type="application/ld+json"]').forEach(function (node) {
            try {
                var data = JSON.parse(node.textContent);
                if (data.name) data.name = cleanBrand(data.name);
                if (data.headline) data.headline = cleanBrand(data.headline);
                node.textContent = JSON.stringify(data);
            } catch (e) { /* ignore */ }
        });
    }

    setFavicon();
    updateTitles();
})();
