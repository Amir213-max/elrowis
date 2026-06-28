#!/usr/bin/env python3
"""Generate job application page from careers.html template."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EMAIL = "jobs@alruwais.com.sa"


def form_main(lang: str) -> str:
    if lang == "ar":
        return f'''<main>
    <section id="job-application-intro">
        <div class="light_green_bg f f-c x_padding inner_padding">
            <div class="cta_content f f-c a-c j-c _eleWrap">
                <div class="cta_title f f-c a-c j-c">
                    <h5 class="gray_color _eleY">الوظائف</h5>
                    <h2 class="_eleY">تقديم طلب توظيف</h2>
                </div>
                <p class="job_form_intro _eleY">املأ النموذج أدناه وسيقوم فريق الموارد البشرية بمراجعة طلبك والتواصل معك في حال توفر فرصة مناسبة.</p>
            </div>
        </div>
    </section>

    <section id="job-application-form">
        <div class="x2_padding inner_padding white_background">
            <div class="contact_sides f s-b">
                <div class="form_side f f-c">
                    <div class="section_head f a-c s-b">
                        <div class="section_shape">
                            <svg xmlns="http://www.w3.org/2000/svg" width="100" height="97" fill="none" viewBox="0 0 100 97" aria-hidden="true">
                                <path fill="#003d53" d="M8.5 90.5L33.5 90.5L96.5 71.5Q96.5 69.5 96.5 67.5L96.5 10.5Q96.5 8.5 94.5 8.5L53.5 20L53.5 56L8.5 90.5Z"/>
                            </svg>
                        </div>
                        <div class="section_title f f-c">
                            <h2>نموذج التقديم</h2>
                        </div>
                    </div>

                    <div class="contact_form_notice" id="job-form-success" role="status">
                        تم إرسال طلبكم بنجاح. سنتواصل معكم قريباً.
                    </div>

                    <form
                        id="job-application-form-el"
                        action="https://formsubmit.co/{EMAIL}"
                        method="POST"
                        enctype="multipart/form-data"
                    >
                        <input type="hidden" name="_subject" value="طلب توظيف - الرويس" />
                        <input type="hidden" name="_captcha" value="false" />
                        <input type="hidden" name="_template" value="table" />
                        <input type="hidden" name="_next" id="job-formsubmit-next" value="" />

                        <div class="form_set f f-c">
                            <div class="input_block">
                                <input type="text" name="الاسم الكامل" placeholder="الاسم الكامل" required />
                            </div>
                            <div class="input_block">
                                <input type="email" name="email" placeholder="البريد الإلكتروني" required />
                            </div>
                            <div class="input_block">
                                <input type="tel" name="رقم الجوال" placeholder="رقم الجوال" required dir="ltr" />
                            </div>
                            <div class="input_block">
                                <input type="text" name="المدينة" placeholder="المدينة" required />
                            </div>
                            <div class="input_block">
                                <input type="text" name="المسمى الوظيفي" placeholder="المسمى الوظيفي المطلوب" required />
                            </div>
                            <div class="input_block">
                                <label for="job-cv">السيرة الذاتية (PDF)</label>
                                <input type="file" id="job-cv" name="السيرة الذاتية" accept=".pdf,application/pdf" required />
                            </div>
                            <div class="input_block f f-c a-s static">
                                <button type="submit" class="site_button orange_bg f a-c j-c interactive_label pointer">
                                    <strong class="uppercase _txt words">إرسال الطلب</strong>
                                    <svg class="_shape" style="transform: scaleX(-1)" xmlns="http://www.w3.org/2000/svg" width="16" height="17" fill="none" viewBox="0 0 16 17">
                                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="m10.164 4.33 2.753 2.753a2 2 0 0 1 0 2.829l-2.753 2.752m3-4.166H2.498"/>
                                    </svg>
                                </button>
                            </div>
                        </div>
                    </form>
                    <p class="job_form_footer">للاستفسارات: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
                </div>
            </div>
        </div>
    </section>
</main>'''

    return f'''<main>
    <section id="job-application-intro">
        <div class="light_green_bg f f-c x_padding inner_padding">
            <div class="cta_content f f-c a-c j-c _eleWrap">
                <div class="cta_title f f-c a-c j-c">
                    <h5 class="gray_color _eleY">Careers</h5>
                    <h2 class="_eleY">Job Application</h2>
                </div>
                <p class="job_form_intro _eleY">Complete the form below and our HR team will review your application and contact you if a suitable opportunity is available.</p>
            </div>
        </div>
    </section>

    <section id="job-application-form">
        <div class="x2_padding inner_padding white_background">
            <div class="contact_sides f s-b">
                <div class="form_side f f-c">
                    <div class="section_head f a-c s-b">
                        <div class="section_shape">
                            <svg xmlns="http://www.w3.org/2000/svg" width="100" height="97" fill="none" viewBox="0 0 100 97" aria-hidden="true">
                                <path fill="#003d53" d="M8.5 90.5L33.5 90.5L96.5 71.5Q96.5 69.5 96.5 67.5L96.5 10.5Q96.5 8.5 94.5 8.5L53.5 20L53.5 56L8.5 90.5Z"/>
                            </svg>
                        </div>
                        <div class="section_title f f-c">
                            <h2>Application Form</h2>
                        </div>
                    </div>

                    <div class="contact_form_notice" id="job-form-success" role="status">
                        Your application has been submitted successfully. We will contact you soon.
                    </div>

                    <form
                        id="job-application-form-el"
                        action="https://formsubmit.co/{EMAIL}"
                        method="POST"
                        enctype="multipart/form-data"
                    >
                        <input type="hidden" name="_subject" value="Job application - Alruwais" />
                        <input type="hidden" name="_captcha" value="false" />
                        <input type="hidden" name="_template" value="table" />
                        <input type="hidden" name="_next" id="job-formsubmit-next" value="" />

                        <div class="form_set f f-c">
                            <div class="input_block">
                                <input type="text" name="Full name" placeholder="Full name" required />
                            </div>
                            <div class="input_block">
                                <input type="email" name="email" placeholder="Email address" required />
                            </div>
                            <div class="input_block">
                                <input type="tel" name="Mobile number" placeholder="Mobile number" required />
                            </div>
                            <div class="input_block">
                                <input type="text" name="City" placeholder="City" required />
                            </div>
                            <div class="input_block">
                                <input type="text" name="Job title" placeholder="Desired job title" required />
                            </div>
                            <div class="input_block">
                                <label for="job-cv">CV (PDF)</label>
                                <input type="file" id="job-cv" name="CV" accept=".pdf,application/pdf" required />
                            </div>
                            <div class="input_block f f-c a-s static">
                                <button type="submit" class="site_button orange_bg f a-c j-c interactive_label pointer">
                                    <strong class="uppercase _txt words">Submit Application</strong>
                                    <svg class="_shape" style="transform: scaleX(-1)" xmlns="http://www.w3.org/2000/svg" width="16" height="17" fill="none" viewBox="0 0 16 17">
                                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="m10.164 4.33 2.753 2.753a2 2 0 0 1 0 2.829l-2.753 2.752m3-4.166H2.498"/>
                                    </svg>
                                </button>
                            </div>
                        </div>
                    </form>
                    <p class="job_form_footer">For inquiries: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
                </div>
            </div>
        </div>
    </section>
</main>'''


def build_page(lang: str) -> None:
    src = ROOT / lang / "careers.html"
    text = src.read_text(encoding="utf-8")
    start = text.index("<main>")
    end = text.index("</main>") + len("</main>")

    head_end = text.index("</head>")
    head = text[:head_end]

    if lang == "ar":
        head = head.replace(
            "<title>الوظائف والتدريب المهني - الرويس</title>",
            "<title>تقديم طلب توظيف - الرويس</title>",
        )
        lang_href = "../en/job-application.html"
    else:
        head = head.replace(
            "<title>Careers - Alruwais</title>",
            "<title>Job Application - Alruwais</title>",
        )
        if "Job Application -" not in head:
            head = head.replace(
                "<title>Careers and Vocational Training - Nesma & Partners</title>",
                "<title>Job Application - Alruwais</title>",
            )
        lang_href = "../ar/job-application.html"

    if "job-application-page.css" not in head:
        head = head.replace(
            '<link href="../site-fixes.css?v=55" rel="stylesheet">',
            '<link href="../site-fixes.css?v=55" rel="stylesheet">\n    <link href="../job-application-page.css?v=1" rel="stylesheet">',
        )
    if "job-application-page.js" not in head:
        head = head.replace(
            '<script defer src="../site-fixes.js?v=37"></script>',
            '<script defer src="../site-fixes.js?v=37"></script>\n    <script defer src="../job-application-page.js?v=1"></script>',
        )

    body_start = text.index("<body")
    body_tag_end = text.index(">", body_start) + 1
    body_open = text[body_start:body_tag_end].replace(
        'class="page-careers"', 'class="page-job-application"'
    )
    after_body = text[body_tag_end:start]
    rest_after_main = text[end:]

    # Language switcher on job application page
    after_body = after_body.replace(
        f'href="../{"en" if lang == "ar" else "ar"}/careers.html"',
        f'href="{lang_href}"',
    )

    out = head + "\n</head>\n" + body_open + after_body + form_main(lang) + rest_after_main
    dest = ROOT / lang / "job-application.html"
    dest.write_text(out, encoding="utf-8")
    print(f"Wrote {dest}")


def update_careers_button(lang: str) -> None:
    path = ROOT / lang / "careers.html"
    text = path.read_text(encoding="utf-8")
    old = 'href="https://careers.nesmapartners.com/"'
    new = 'href="job-application.html"'
    if old not in text:
        print(f"No external careers link in {path}")
        return
    updated = text.replace(old, new)
    updated = updated.replace('target="_blank"\n                        ', "")
    updated = updated.replace("target=\"_blank\"\n                    ", "")
    path.write_text(updated, encoding="utf-8")
    print(f"Updated careers button in {path}")


if __name__ == "__main__":
    build_page("ar")
    build_page("en")
    update_careers_button("ar")
    update_careers_button("en")
