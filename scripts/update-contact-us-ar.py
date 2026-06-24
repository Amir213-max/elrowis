#!/usr/bin/env python3
"""Replace ar/contact-us.html main content with Alruwais contact + vendor portal."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "ar" / "contact-us.html"

MAIN_CONTENT = """<main>
    <!-- Hero -->
    <section id="contact-hero">
        <div class="light_green_bg f f-c x_padding inner_padding">
            <div class="cta_content f f-c a-c j-c _eleWrap">
                <div class="cta_title f f-c a-c j-c">
                    <h5 class="gray_color _eleY">خلك على تواصل</h5>
                    <h2 class="_eleY">تواصلكم معنا يصنع الفرق</h2>
                </div>
            </div>
        </div>
    </section>

    <!-- Contact details -->
    <section id="contact-info">
        <div class="section_wrap white_background f f-c x_padding inner_padding">
            <div class="contact_info_grid _eleWrap">
                <div class="contact_info_col _eleY">
                    <h4>العنوان</h4>
                    <p class="gray_color">المملكة العربية السعودية، مدينة الرياض، حي النخيل، المخطط 2732، البلك 1، وحدة رقم 01</p>
                </div>
                <div class="contact_info_col _eleY">
                    <h4>هاتف</h4>
                    <p class="gray_color">
                        <a href="tel:920012496" dir="ltr">920012496</a>
                        /
                        <a href="tel:+966571000074" dir="ltr">966571000074</a>
                    </p>
                </div>
                <div class="contact_info_col _eleY">
                    <h4>ايميل</h4>
                    <p class="gray_color"><a href="mailto:info@alruwais.com.sa">info@alruwais.com.sa</a></p>
                </div>
            </div>
            <div class="contact_info_divider"></div>
            <div class="ft_social f contact_info_social _eleY">
                <a href="https://www.linkedin.com/company/alruwais/?viewAsMember=true" target="_blank" rel="noopener noreferrer" class="rounded_button outline f a-c j-c magnet" aria-label="LinkedIn">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 16 16"><path fill="currentColor" d="M14.8 0H1.2A1.2 1.2 0 0 0 0 1.2v13.6A1.2 1.2 0 0 0 1.2 16h13.6a1.2 1.2 0 0 0 1.2-1.2V1.2A1.2 1.2 0 0 0 14.8 0Zm-10 13.6H2.4V6.4h2.4v7.2ZM3.6 5a1.4 1.4 0 1 1 1.44-1.4A1.424 1.424 0 0 1 3.6 5Zm10 8.6h-2.4V9.808c0-1.136-.48-1.544-1.104-1.544A1.392 1.392 0 0 0 8.8 9.752a.528.528 0 0 0 0 .112V13.6H6.4V6.4h2.32v1.04a2.488 2.488 0 0 1 2.16-1.12c1.24 0 2.688.688 2.688 2.928L13.6 13.6Z"></path></svg>
                </a>
                <a href="https://www.instagram.com/alruwais.sa/" target="_blank" rel="noopener noreferrer" class="rounded_button outline f a-c j-c magnet" aria-label="Instagram">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 16 16">
                        <path fill="currentColor" d="M8.001 2.808c1.691 0 1.892.006 2.56.037.401.005.799.078 1.175.218.275.101.524.263.729.474.21.204.372.453.473.728.14.377.214.774.219 1.176.03.668.037.868.037 2.56 0 1.69-.007 1.89-.037 2.558-.005.402-.079.8-.219 1.176a2.098 2.098 0 0 1-1.202 1.202c-.376.14-.774.214-1.176.218-.667.03-.868.037-2.559.037-1.69 0-1.891-.006-2.559-.037a3.505 3.505 0 0 1-1.176-.218 1.962 1.962 0 0 1-.728-.474 1.963 1.963 0 0 1-.474-.728 3.505 3.505 0 0 1-.218-1.176c-.03-.668-.037-.868-.037-2.559 0-1.69.006-1.891.037-2.56.005-.4.079-.798.218-1.175.102-.275.264-.524.474-.728.204-.21.453-.373.728-.474.377-.14.775-.213 1.176-.218.668-.03.868-.037 2.56-.037Zm0-1.141c-1.72 0-1.935.007-2.61.038-.526.01-1.046.11-1.538.294-.423.16-.806.409-1.122.731A3.104 3.104 0 0 0 2 3.852a4.649 4.649 0 0 0-.294 1.537c-.032.675-.039.891-.039 2.611 0 1.72.007 1.936.038 2.611.01.525.11 1.045.294 1.537.16.423.409.806.731 1.123.317.322.7.571 1.122.73a4.648 4.648 0 0 0 1.537.294c.676.031.892.038 2.611.038 1.72 0 1.936-.007 2.611-.038a4.648 4.648 0 0 0 1.538-.294 3.24 3.24 0 0 0 1.852-1.853 4.647 4.647 0 0 0 .294-1.537c.032-.675.039-.891.039-2.61 0-1.72-.008-1.937-.038-2.612a4.645 4.645 0 0 0-.295-1.537 3.104 3.104 0 0 0-.73-1.122 3.104 3.104 0 0 0-1.122-.731 4.648 4.648 0 0 0-1.538-.294c-.675-.031-.89-.038-2.61-.038Zm0 3.08a3.252 3.252 0 1 0 0 6.506 3.252 3.252 0 0 0 0-6.505Zm0 5.364a2.111 2.111 0 1 1 0-4.222 2.111 2.111 0 0 1 0 4.222Zm3.381-6.252a.76.76 0 1 0 0 1.52.76.76 0 0 0 0-1.52Z"/>
                    </svg>
                </a>
            </div>
        </div>
    </section>

    <!-- Map -->
    <section id="contact-location" class="contact_location_section">
        <div class="x2_padding inner_padding">
            <div class="contact_map_wrap _eleWrap">
                <h4 class="_eleY">موقعنا</h4>
                <div class="contact_map _eleY">
                    <iframe
                        src="https://maps.google.com/maps?q=%D8%AD%D9%8A+%D8%A7%D9%84%D9%86%D8%AE%D9%8A%D9%84+%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6+%D8%A7%D9%84%D9%85%D8%AE%D8%B7%D8%B7+2732&amp;t=&amp;z=15&amp;ie=UTF8&amp;iwloc=&amp;output=embed"
                        loading="lazy"
                        referrerpolicy="no-referrer-when-downgrade"
                        allowfullscreen
                        title="موقع الرويس على الخريطة"
                    ></iframe>
                </div>
            </div>
        </div>
    </section>

    <!-- Vendor portal -->
    <section id="vendor-portal">
        <div class="section_wrap light_green_bg f f-c x_padding inner_padding">
            <div class="vendor_portal_layout f s-b _eleWrap">
                <div class="vendor_portal_copy _eleY">
                    <div class="section_title f f-c">
                        <h2>بوابة الموردين</h2>
                    </div>
                    <p class="gray_color">نحو شراكات أكثر كفاءة واستدامة، توفر بوابة الموردين تجربة رقمية متكاملة تتيح التسجيل والتأهيل وإدارة البيانات والوصول إلى الخدمات والمستندات اللازمة، بما يعزز التعاون ويحقق أعلى مستويات الجودة والموثوقية.</p>
                    <a
                        href="javascript:void(0);"
                        class="site_button outline orange_color f a-c j-c interactive_label pointer scrollTo"
                        data-scroll="vendor-form"
                        aria-label="سجّل كمورد"
                    >
                        <strong class="uppercase _txt words">سجّل كمورد</strong>
                        <svg class="_shape" style="transform: scaleX(-1)" xmlns="http://www.w3.org/2000/svg" width="16" height="17" fill="none" viewBox="0 0 16 17">
                            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="m10.164 4.33 2.753 2.753a2 2 0 0 1 0 2.829l-2.753 2.752m3-4.166H2.498"/>
                        </svg>
                    </a>
                </div>
                <div class="vendor_portal_media _eleY">
                    <img
                        src="../images/contact/vendor-portal-hero.png"
                        alt="شراكة مع الموردين - الرويس"
                        width="1200"
                        height="500"
                    />
                </div>
            </div>
        </div>
    </section>

    <!-- Vendor form -->
    <section id="vendor-form">
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
                            <h2>نموذج تسجيل المورد</h2>
                        </div>
                    </div>

                    <div class="contact_form_notice" id="vendor-form-success" role="status">
                        تم إرسال طلبكم بنجاح. سنتواصل معكم قريباً.
                    </div>

                    <form
                        id="vendor-registration-form"
                        class="customForm"
                        action="https://formsubmit.co/info@alruwais.com.sa"
                        method="POST"
                    >
                        <input type="hidden" name="_subject" value="طلب تسجيل مورد - بوابة الموردين" />
                        <input type="hidden" name="_captcha" value="false" />
                        <input type="hidden" name="_template" value="table" />
                        <input type="hidden" name="_next" id="formsubmit-next" value="" />

                        <div class="form_set f f-c">
                            <div class="input_block">
                                <input type="text" name="اسم الشركة" placeholder="اسم الشركة" required />
                            </div>
                            <div class="input_block">
                                <input type="text" name="رقم السجل التجاري" placeholder="رقم السجل التجاري" required />
                            </div>
                            <div class="input_block">
                                <input type="text" name="اسم مسؤول التواصل" placeholder="اسم مسؤول التواصل" required />
                            </div>
                            <div class="input_block">
                                <input type="email" name="email" placeholder="البريد الإلكتروني" required />
                            </div>
                            <div class="input_block">
                                <input type="tel" name="رقم الهاتف" placeholder="رقم الهاتف" required dir="ltr" />
                            </div>
                            <div class="input_block">
                                <input type="text" name="المدينة" placeholder="المدينة" />
                            </div>
                            <div class="input_block">
                                <textarea name="نوع النشاط / الخدمات" placeholder="نوع النشاط / الخدمات المقدمة" rows="4"></textarea>
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
                </div>
            </div>
        </div>
    </section>
</main>"""


def main() -> None:
    text = PAGE.read_text(encoding="utf-8")

    start = text.index("<main>")
    end = text.index("</main>") + len("</main>")
    text = text[:start] + MAIN_CONTENT + text[end:]

    if 'class="page-contact-us"' not in text:
        text = text.replace("<body>", '<body class="page-contact-us">', 1)

    text = text.replace(
        "<title>Contact us - الرويس</title>",
        "<title>تواصل معنا - الرويس</title>",
    )
    if "تواصل معنا - الرويس" not in text.split("<title>")[1].split("</title>")[0]:
        import re
        text = re.sub(r"<title>.*?</title>", "<title>تواصل معنا - الرويس</title>", text, count=1)

    text = text.replace(
        '"name":"Contact us - الرويس"',
        '"name":"تواصل معنا - الرويس"',
    )

    if "contact-us-page.css" not in text:
        text = text.replace(
            '<link href="../site-fixes.css?v=56" rel="stylesheet">',
            '<link href="../site-fixes.css?v=56" rel="stylesheet">\n'
            '    <link href="../contact-us-page.css?v=2" rel="stylesheet">',
        )
    else:
        text = text.replace("contact-us-page.css?v=1", "contact-us-page.css?v=2")

    if "contact-us-page.js" not in text:
        text = text.replace(
            '<script defer src="../site-fixes.js?v=37"></script>',
            '<script defer src="../site-fixes.js?v=37"></script>\n'
            '    <script defer src="../contact-us-page.js?v=1"></script>',
        )

    PAGE.write_text(text, encoding="utf-8")
    print(f"Updated {PAGE}")


if __name__ == "__main__":
    main()
