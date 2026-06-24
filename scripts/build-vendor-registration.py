#!/usr/bin/env python3
"""Generate vendor registration pages from vendors.html template."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DIAL_CODES = [
    ("+966", "Saudi Arabia", "المملكة العربية السعودية"),
    ("+971", "United Arab Emirates", "الإمارات العربية المتحدة"),
    ("+973", "Bahrain", "البحرين"),
    ("+974", "Qatar", "قطر"),
    ("+965", "Kuwait", "الكويت"),
    ("+968", "Oman", "عُمان"),
    ("+962", "Jordan", "الأردن"),
    ("+961", "Lebanon", "لبنان"),
    ("+20", "Egypt", "مصر"),
    ("+1", "United States", "الولايات المتحدة"),
    ("+44", "United Kingdom", "المملكة المتحدة"),
    ("+91", "India", "الهند"),
    ("+92", "Pakistan", "باكستان"),
    ("+63", "Philippines", "الفلبين"),
]

COUNTRIES = [
    ("SA", "Saudi Arabia", "المملكة العربية السعودية"),
    ("AE", "United Arab Emirates", "الإمارات العربية المتحدة"),
    ("BH", "Bahrain", "البحرين"),
    ("QA", "Qatar", "قطر"),
    ("KW", "Kuwait", "الكويت"),
    ("OM", "Oman", "عُمان"),
    ("JO", "Jordan", "الأردن"),
    ("LB", "Lebanon", "لبنان"),
    ("EG", "Egypt", "مصر"),
    ("US", "United States", "الولايات المتحدة"),
    ("GB", "United Kingdom", "المملكة المتحدة"),
    ("IN", "India", "الهند"),
    ("PK", "Pakistan", "باكستان"),
    ("PH", "Philippines", "الفلبين"),
]

TITLES = [
    ("CEO", "CEO", "الرئيس التنفيذي"),
    ("MD", "Managing Director", "المدير العام"),
    ("GM", "General Manager", "مدير عام"),
    ("BDM", "Business Development Manager", "مدير تطوير الأعمال"),
    ("PM", "Project Manager", "مدير مشروع"),
    ("OTHER", "Other", "أخرى"),
]

SERVICES = [
    ("civil", "Civil Works", "الأعمال المدنية"),
    ("mechanical", "Mechanical", "ميكانيك"),
    ("electrical", "Electrical", "كهرباء"),
    ("piping", "Piping", "أنابيب"),
    ("hvac", "HVAC", "تكييف وتهوية"),
    ("instrumentation", "Instrumentation", "أجهزة قياس"),
    ("it", "IT Services", "خدمات تقنية"),
    ("logistics", "Logistics", "لوجستيات"),
    ("manpower", "Manpower Supply", "توريد عمالة"),
    ("consulting", "Consulting", "استشارات"),
    ("materials", "Materials Supply", "توريد مواد"),
    ("equipment", "Equipment Rental", "تأجير معدات"),
]

ICON_BUILDING = '<svg class="eoi-section__icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 21h18M5 21V7l7-4 7 4v14M9 21v-4h6v4M9 9h.01M15 9h.01M9 13h.01M15 13h.01" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>'
ICON_USER = '<svg class="eoi-section__icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M20 21a8 8 0 0 0-16 0M12 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>'
ICON_GEAR = '<svg class="eoi-section__icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z" stroke="currentColor" stroke-width="1.5"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09a1.65 1.65 0 0 0-1-1.51 1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.6 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9c.7 0 1.34.37 1.51 1H21a2 2 0 1 1 0 4h-.09c-.7 0-1.34.37-1.51 1Z" stroke="currentColor" stroke-width="1.5"/></svg>'
ICON_PDF = '<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6Z" stroke="currentColor" stroke-width="1.5"/><path d="M14 2v6h6M9 13h6M9 17h6M9 9h1" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>'


def options(items, lang, placeholder=None, selected=None):
    lines = []
    if placeholder:
        lines.append(f'<option value="">{placeholder}</option>')
    for code, en, ar in items:
        label = ar if lang == "ar" else en
        if len(items[0]) == 3 and code.startswith("+"):
            text = f"{code} - {label}"
            val = code
        else:
            text = label
            val = code
        sel = ' selected' if selected and val == selected else ''
        lines.append(f'<option value="{val}"{sel}>{text}</option>')
    return "\n".join(lines)


def dial_options(lang):
    ph = "اختر رمز الاتصال" if lang == "ar" else "Select dial code"
    lines = [f'<option value="">{ph}</option>']
    for code, en, ar in DIAL_CODES:
        label = ar if lang == "ar" else en
        sel = ' selected' if code == "+966" else ''
        lines.append(f'<option value="{code}"{sel}>{code} - {label}</option>')
    return "\n".join(lines)


def country_options(lang):
    ph = "اختر الدولة" if lang == "ar" else "Select Country"
    lines = [f'<option value="">{ph}</option>']
    for code, en, ar in COUNTRIES:
        label = ar if lang == "ar" else en
        sel = ' selected' if code == "SA" else ''
        lines.append(f'<option value="{code}"{sel}>{label}</option>')
    return "\n".join(lines)


def title_options(lang):
    ph = "اختر المنصب" if lang == "ar" else "Select Position"
    lines = [f'<option value="">{ph}</option>']
    for code, en, ar in TITLES:
        label = ar if lang == "ar" else en
        lines.append(f'<option value="{code}">{label}</option>')
    return "\n".join(lines)


def services_checkboxes(lang):
    lines = []
    for code, en, ar in SERVICES:
        label = ar if lang == "ar" else en
        lines.append(
            f'<label><input type="checkbox" value="{code}" data-label="{label}"> {label}</label>'
        )
    return "\n".join(lines)


def form_main(lang):
    if lang == "ar":
        t = {
            "banner_tagline": "قيمة راسخة",
            "banner_title": "الرويس",
            "lang_en": "ENGLISH",
            "lang_ar": "العربية",
            "login": "تسجيل الدخول إلى V360",
            "guide": "دليل تسجيل الموردين",
            "company": "تفاصيل الشركة",
            "company_name": "اسم الشركة",
            "company_hint": "يجب أن يكون اسم الشركة بالإنجليزية",
            "country": "الدولة",
            "cr": "السجل التجاري أو ما يعادله",
            "year": "سنة التأسيس",
            "years_calc": "سنوات التأسيس المحسوبة",
            "contact": "تفاصيل الاتصال",
            "first": "الاسم الأول لجهة الاتصال",
            "last": "اسم العائلة لجهة الاتصال",
            "title": "منصب جهة الاتصال",
            "email": "البريد الإلكتروني لجهة الاتصال",
            "dial1": "رمز الاتصال 1",
            "mobile1": "رقم الجوال 1",
            "website": "الموقع الإلكتروني",
            "dial2": "رمز الاتصال 2",
            "mobile2": "رقم الجوال 2",
            "linkedin": "LinkedIn",
            "service": "تفاصيل الخدمات",
            "profile": "ملف الشركة",
            "commercial": "السجل التجاري",
            "upload": "رفع",
            "drop": "اسحب الملف أو الصقه هنا",
            "pdf_note": "ارفع ملف بصيغة .pdf حتى 20 ميجابايت",
            "services": "الخدمة/الخدمات",
            "services_ph": "اختر الخدمة/الخدمات",
            "selected": "الخدمات المحددة",
            "details": "تفاصيل إضافية",
            "footer": 'في حال وجود أي مشكلة أثناء التسجيل، يرجى التواصل على <a href="mailto:info@alruwais.com.sa">info@alruwais.com.sa</a>',
            "success": "تم إرسال طلبكم بنجاح. سنتواصل معكم قريباً.",
            "form_subject": "طلب تسجيل مورد - نموذج التعبير عن الاهتمام",
            "submit": "إرسال",
            "copyright": "حقوق النشر © 2026، نسما وشركاهم. جميع الحقوق محفوظة.",
            "email_ph": "username@companyname.com",
            "web_ph": "companyname.com",
            "required": "مطلوب",
        }
        other_lang = "../en/vendor-registration.html"
        self_lang = "vendor-registration.html"
    else:
        t = {
            "banner_tagline": '<em>Together, We Build Excellence</em>',
            "banner_title": "Expression of Interest Form",
            "lang_en": "ENGLISH",
            "lang_ar": "العربية",
            "login": "Login to V360",
            "guide": "Vendor Registration User Guide",
            "company": "Company Details",
            "company_name": "Company Name",
            "company_hint": "Company name should be in English",
            "country": "Country",
            "cr": "Commercial Registration # or Equivalent",
            "year": "Year of Establishment",
            "years_calc": "Calculated Years of Establishment",
            "contact": "Contact Details",
            "first": "Contact First Name",
            "last": "Contact Last Name",
            "title": "Title of Contact Person",
            "email": "Contact Email Address",
            "dial1": "Dial Code 1",
            "mobile1": "Mobile Number 1",
            "website": "Website",
            "dial2": "Dial Code 2",
            "mobile2": "Mobile Number 2",
            "linkedin": "LinkedIn",
            "service": "Service Details",
            "profile": "Company Profile",
            "commercial": "Commercial Registration",
            "upload": "UPLOAD",
            "drop": "Drop or paste file here",
            "pdf_note": "Upload a .pdf format file up 20MB",
            "services": "Service(s)",
            "services_ph": "Select Service(s)",
            "selected": "Selected Service(s)",
            "details": "Further Details",
            "footer": 'In case of any issues during registration, please contact <a href="mailto:info@alruwais.com.sa">info@alruwais.com.sa</a>',
            "success": "Your submission has been received. We will contact you shortly.",
            "form_subject": "Vendor registration - Expression of Interest",
            "submit": "Submit",
            "copyright": "Copyright © 2026, Nesma & Partners. All Rights Reserved.",
            "email_ph": "username@companyname.com",
            "web_ph": "companyname.com",
            "required": "Required",
        }
        other_lang = "../ar/vendor-registration.html"
        self_lang = "vendor-registration.html"

    req = '<span class="req">*</span>'

    return f'''<main>
    <div class="eoi-page">
        <div class="eoi-banner">
            <div class="eoi-banner__logo-wrap">
                <img class="eoi-banner__logo" src="../images/alruwais-logo-transparent.png" alt="{t['banner_title']}">
            </div>
            <h1 class="eoi-banner__title">{t["banner_title"]}</h1>
            <p class="eoi-banner__tagline">{t["banner_tagline"]}</p>
        </div>

        <div class="eoi-toolbar">
            <div class="eoi-lang">
                <a href="{other_lang if lang == 'ar' else self_lang}" class="{"is-active" if lang == "en" else ""}">{t["lang_en"]}</a>
                <a href="{self_lang if lang == "ar" else other_lang}" class="{"is-active" if lang == "ar" else ""}">{t["lang_ar"]}</a>
            </div>
            <div class="eoi-actions">
                <a href="https://my.apps.nesma-partners.com/suite/sites/np-360" class="eoi-login-btn" target="_blank" rel="noopener">{t["login"]}</a>
                <a href="https://my.appianportals.com/expressionofinterest" class="eoi-guide-link" target="_blank" rel="noopener">{ICON_PDF} {t["guide"]}</a>
            </div>
        </div>

        <div class="eoi-card">
            <form id="eoi-form" action="https://formsubmit.co/info@alruwais.com.sa" method="POST" enctype="multipart/form-data">
                <input type="hidden" name="_subject" value="{t["form_subject"]}" />
                <input type="hidden" name="_captcha" value="false" />
                <input type="hidden" name="_template" value="table" />
                <input type="hidden" name="_next" id="formsubmit-next" value="" />
                <section class="eoi-section">
                    <div class="eoi-section__head">{ICON_BUILDING}<h2 class="eoi-section__title">{t["company"]}</h2></div>
                    <div class="eoi-grid eoi-grid--2">
                        <div class="eoi-field eoi-field--full">
                            <label class="eoi-label" for="eoi-company-name">{t["company_name"]} {req}</label>
                            <div class="eoi-input--counter-wrap">
                                <input class="eoi-input" id="eoi-company-name" name="company_name" maxlength="100" required>
                                <span class="eoi-counter" id="eoi-company-counter">0/100</span>
                            </div>
                            <span class="eoi-hint">{t["company_hint"]}</span>
                        </div>
                        <div class="eoi-field">
                            <label class="eoi-label" for="eoi-country">{t["country"]} {req}</label>
                            <select class="eoi-select" id="eoi-country" name="country" required>{country_options(lang)}</select>
                        </div>
                        <div class="eoi-field">
                            <label class="eoi-label" for="eoi-cr">{t["cr"]} {req}</label>
                            <input class="eoi-input" id="eoi-cr" name="commercial_registration" required>
                        </div>
                        <div class="eoi-field">
                            <label class="eoi-label" for="eoi-year-establishment">{t["year"]}</label>
                            <input class="eoi-input" type="date" id="eoi-year-establishment" name="year_establishment">
                        </div>
                        <div class="eoi-field">
                            <span class="eoi-label">{t["years_calc"]}</span>
                            <div class="eoi-readonly"><strong id="eoi-years-display">N/A</strong></div>
                        </div>
                    </div>
                </section>

                <section class="eoi-section">
                    <div class="eoi-section__head">{ICON_USER}<h2 class="eoi-section__title">{t["contact"]}</h2></div>
                    <div class="eoi-grid eoi-grid--3">
                        <div class="eoi-field"><label class="eoi-label" for="eoi-first">{t["first"]} {req}</label><input class="eoi-input" id="eoi-first" name="first_name" required></div>
                        <div class="eoi-field"><label class="eoi-label" for="eoi-last">{t["last"]} {req}</label><input class="eoi-input" id="eoi-last" name="last_name" required></div>
                        <div class="eoi-field"><label class="eoi-label" for="eoi-title">{t["title"]}</label><select class="eoi-select" id="eoi-title" name="title">{title_options(lang)}</select></div>
                        <div class="eoi-field"><label class="eoi-label" for="eoi-email">{t["email"]} {req}</label><input class="eoi-input" type="email" id="eoi-email" name="email" placeholder="{t["email_ph"]}" required></div>
                        <div class="eoi-field"><label class="eoi-label" for="eoi-dial1">{t["dial1"]} {req}</label><select class="eoi-select" id="eoi-dial1" name="dial1" required>{dial_options(lang)}</select></div>
                        <div class="eoi-field"><label class="eoi-label" for="eoi-mobile1">{t["mobile1"]} {req}</label><input class="eoi-input" type="tel" id="eoi-mobile1" name="mobile1" required></div>
                        <div class="eoi-field"><label class="eoi-label" for="eoi-website">{t["website"]}</label><input class="eoi-input" id="eoi-website" name="website" placeholder="{t["web_ph"]}"></div>
                        <div class="eoi-field"><label class="eoi-label" for="eoi-dial2">{t["dial2"]}</label><select class="eoi-select" id="eoi-dial2" name="dial2">{dial_options(lang)}</select></div>
                        <div class="eoi-field"><label class="eoi-label" for="eoi-mobile2">{t["mobile2"]}</label><input class="eoi-input" type="tel" id="eoi-mobile2" name="mobile2"></div>
                        <div class="eoi-field eoi-field--full"><label class="eoi-label" for="eoi-linkedin">{t["linkedin"]}</label><input class="eoi-input" id="eoi-linkedin" name="linkedin"></div>
                    </div>
                </section>

                <section class="eoi-section">
                    <div class="eoi-section__head">{ICON_GEAR}<h2 class="eoi-section__title">{t["service"]}</h2></div>
                    <div class="eoi-upload-row">
                        <div class="eoi-upload">
                            <label class="eoi-label">{t["profile"]} {req}</label>
                            <div class="eoi-upload__zone">
                                <button type="button" class="eoi-upload__btn" id="eoi-upload-profile-btn">{t["upload"]}</button>
                                <div class="eoi-upload__drop" id="eoi-profile-drop">{t["drop"]}</div>
                                <input type="file" id="eoi-company-profile" name="company_profile" accept=".pdf,application/pdf" required>
                            </div>
                            <span class="eoi-upload__note">{t["pdf_note"]}</span>
                        </div>
                        <div class="eoi-upload">
                            <label class="eoi-label">{t["commercial"]} {req}</label>
                            <div class="eoi-upload__zone">
                                <button type="button" class="eoi-upload__btn" id="eoi-upload-cr-btn">{t["upload"]}</button>
                                <div class="eoi-upload__drop" id="eoi-cr-drop">{t["drop"]}</div>
                                <input type="file" id="eoi-commercial-reg" name="commercial_registration_file" accept=".pdf,application/pdf" required>
                            </div>
                            <span class="eoi-upload__note">{t["pdf_note"]}</span>
                        </div>
                    </div>
                    <div class="eoi-grid" style="margin-top:1.25em">
                        <div class="eoi-field">
                            <label class="eoi-label">{t["services"]} {req}</label>
                            <div class="eoi-services-wrap">
                                <button type="button" class="eoi-services-trigger" id="eoi-services-trigger" data-placeholder="{t["services_ph"]}">{t["services_ph"]}</button>
                                <div class="eoi-services-panel" id="eoi-services-panel">{services_checkboxes(lang)}</div>
                            </div>
                        </div>
                        <div class="eoi-field">
                            <span class="eoi-label">{t["selected"]}</span>
                            <div class="eoi-selected-tags" id="eoi-selected-tags"></div>
                        </div>
                        <div class="eoi-field eoi-field--full">
                            <label class="eoi-label" for="eoi-details">{t["details"]}</label>
                            <textarea class="eoi-textarea" id="eoi-details" name="details" rows="4"></textarea>
                        </div>
                    </div>
                </section>

                <p class="eoi-footer-note">{t["footer"]}</p>
                <div class="eoi-submit-wrap"><button type="submit" class="eoi-submit" id="eoi-submit-btn">{t["submit"]}</button></div>
                <p class="eoi-success-notice" id="eoi-success-notice" role="status">{t["success"]}</p>
            </form>
        </div>
        <p class="eoi-copyright">{t["copyright"]}</p>
    </div>
</main>'''


def build_page(lang):
    src = ROOT / lang / "vendors.html"
    text = src.read_text(encoding="utf-8")
    start = text.index("<main>")
    end = text.index("</main>") + len("</main>")

    head_end = text.index("</head>")
    head = text[:head_end]
    head = head.replace(
        "<title>الموردون - نسما و شركاهم</title>" if lang == "ar" else "<title>Vendors - Nesma & Partners</title>",
        "<title>نموذج التعبير عن الاهتمام - نسما و شركاهم</title>" if lang == "ar" else "<title>Expression of Interest - Nesma & Partners</title>",
    )
    if "vendor-registration.css" not in head:
        head = head.replace(
            '<link href="../site-fixes.css?v=17" rel="stylesheet">',
            '<link href="../site-fixes.css?v=18" rel="stylesheet">\n    <link href="../vendor-registration.css?v=1" rel="stylesheet">',
        )
    if "vendor-registration.js" not in head:
        head = head.replace(
            '<script defer src="../site-fixes.js?v=6"></script>',
            '<script defer src="../site-fixes.js?v=6"></script>\n    <script defer src="../vendor-registration.js?v=1"></script>',
        )

    body_start = text.index("<body")
    body_tag_end = text.index(">", body_start) + 1
    body_open = text[body_start:body_tag_end]
    body_open = body_open.replace('class="page-vendors"', 'class="page-vendor-registration"')
    after_body = text[body_tag_end:start]
    rest_after_main = text[end:]

    out = head + "\n</head>\n" + body_open + after_body + form_main(lang) + rest_after_main
    dest = ROOT / lang / "vendor-registration.html"
    dest.write_text(out, encoding="utf-8")
    print(f"Wrote {dest}")


if __name__ == "__main__":
    build_page("ar")
    build_page("en")
