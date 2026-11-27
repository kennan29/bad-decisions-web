"""Legal notice and privacy policy (EN/ES), used by build.py.

When the company is set up, fill in COMPANY below and rebuild: every placeholder
on both pages is taken from here. Until then the missing data shows highlighted.
Last reviewed: see UPDATED. Have a gestoría/lawyer check the final text.

RULE: any change to the site that affects data, cookies, analytics/pixels, forms,
providers, embeds, ticketing or the company must update these texts (EN and ES)
and UPDATED in the same change.
"""

COMPANY = {
    "name": None,      # razón social, e.g. "Bad Decisions Events, S.L."
    "cif": None,       # NIF/CIF, e.g. "B12345678"
    "address": None,   # domicilio social, e.g. "C/ Ejemplo 1, 08001 Barcelona"
    "registry": None,  # datos registrales, e.g. "Registro Mercantil de Barcelona, tomo X, folio Y, hoja B-Z"
}
UPDATED = {"en": "27 November 2026", "es": "27 de noviembre de 2026"}

_TODO = {
    "en": {"name": "[COMPANY NAME]", "cif": "[TAX ID]", "address": "[REGISTERED ADDRESS]", "registry": "[COMMERCIAL REGISTRY DETAILS]"},
    "es": {"name": "[RAZÓN SOCIAL]", "cif": "[CIF]", "address": "[DOMICILIO SOCIAL]", "registry": "[DATOS DEL REGISTRO MERCANTIL]"},
}


def missing():
    return [k for k, v in COMPANY.items() if not v]


def _f(key, lang):
    v = COMPANY[key]
    return v if v else f'<mark class="todo">{_TODO[lang][key]}</mark>'


def _owner(lang, email):
    lab = {"en": ("Owner", "Tax ID", "Registered address", "Registry", "Email"),
           "es": ("Titular", "CIF", "Domicilio", "Registro", "Correo")}[lang]
    vals = [_f("name", lang), _f("cif", lang), _f("address", lang), _f("registry", lang), f'<a href="mailto:{email}">{email}</a>']
    return "<ul>" + "".join(f"<li><strong>{l}:</strong> {v}</li>" for l, v in zip(lab, vals)) + "</ul>"


def legal_sections(lang, email, privacy_href):
    if lang == "es":
        return [
            ("Quién está <span>detrás</span>", [
                "<p>En cumplimiento de la Ley 34/2002, de Servicios de la Sociedad de la Información y de Comercio Electrónico (LSSI-CE), estos son los datos del titular de baddecisionsbcn.com:</p>",
                _owner(lang, email)]),
            ("Qué es esta <span>web</span>", [
                "<p>Esta web informa sobre Bad Decisions, una fiesta que se celebra los lunes en Sala Apolo (Barcelona): fechas, horarios, precios, normas de acceso y contacto.</p>",
                "<p>Las entradas y la lista gratuita se gestionan a través de <strong>DICE</strong>, con sus propias condiciones de venta y su propia política de privacidad. En esta web no se vende nada ni se recogen datos mediante formularios.</p>"]),
            ("Condiciones de <span>uso</span>", [
                "<p>Al usar esta web aceptas este aviso legal. Te comprometes a hacer un uso correcto de la web y de sus contenidos, sin dañarla ni usarla con fines ilícitos.</p>",
                "<p>Hacemos lo posible para que la información (fechas, horarios, precios, artistas) esté al día, pero puede cambiar sin previo aviso. La información válida para cada fiesta es la que figura en DICE en el momento de la compra.</p>",
                "<p>Para entrar es necesario ser mayor de 18 años y presentar un documento de identidad válido. La organización y la sala se reservan el derecho de admisión.</p>"]),
            ("Propiedad <span>intelectual</span>", [
                "<p>El nombre Bad Decisions, los logotipos, el diseño, los textos y las imágenes de esta web pertenecen a su titular o se usan con permiso. No se pueden copiar, modificar ni usar con fines comerciales sin autorización por escrito.</p>"]),
            ("Enlaces a otras <span>webs</span>", [
                "<p>Esta web enlaza a servicios de terceros (DICE, Instagram, Google Maps, Sala Apolo). No controlamos su contenido ni somos responsables de él; cada uno tiene sus propias condiciones.</p>"]),
            ("Datos <span>personales</span>", [
                f'<p>Cómo tratamos tus datos está explicado en la <a href="{privacy_href}">política de privacidad</a>.</p>']),
            ("Ley <span>aplicable</span>", [
                "<p>Este aviso legal se rige por la ley española. Para cualquier conflicto, y salvo que la ley establezca otra cosa (por ejemplo, si eres consumidor), las partes se someten a los juzgados y tribunales de Barcelona.</p>",
                f"<p><em>Última actualización: {UPDATED[lang]}.</em></p>"]),
        ]
    return [
        ("Who is <span>behind it</span>", [
            "<p>In line with Spanish Law 34/2002 on Information Society Services and E-commerce (LSSI-CE), these are the details of the owner of baddecisionsbcn.com:</p>",
            _owner(lang, email)]),
        ("What this site <span>is</span>", [
            "<p>This website gives information about Bad Decisions, a party held on Mondays at Sala Apolo (Barcelona): dates, times, prices, entry rules and contact.</p>",
            "<p>Tickets and the free guest list are handled by <strong>DICE</strong>, under its own terms of sale and privacy policy. Nothing is sold on this site and no data is collected through forms.</p>"]),
        ("Terms of <span>use</span>", [
            "<p>By using this website you accept this legal notice. You agree to use the site and its content properly, without damaging it or using it for unlawful purposes.</p>",
            "<p>We do our best to keep the information (dates, times, prices, artists) up to date, but it may change without notice. The information that applies to each party is the one shown on DICE at the time of purchase.</p>",
            "<p>Entry is for over-18s only, with a valid ID. The organisers and the venue reserve the right of admission.</p>"]),
        ("Intellectual <span>property</span>", [
            "<p>The Bad Decisions name, logos, design, texts and images on this website belong to their owner or are used with permission. They may not be copied, modified or used commercially without written permission.</p>"]),
        ("Links to other <span>sites</span>", [
            "<p>This website links to third-party services (DICE, Instagram, Google Maps, Sala Apolo). We don't control their content and are not responsible for it; each has its own terms.</p>"]),
        ("Personal <span>data</span>", [
            f'<p>How we handle your data is explained in the <a href="{privacy_href}">privacy policy</a>.</p>']),
        ("Governing <span>law</span>", [
            "<p>This legal notice is governed by Spanish law. Any dispute will be handled by the courts of Barcelona, unless the law says otherwise (for example, if you are a consumer).</p>",
            f"<p><em>Last updated: {UPDATED[lang]}.</em></p>"]),
    ]


def privacy_sections(lang, email):
    if lang == "es":
        return [
            ("La versión <span>corta</span>", [
                "<p>Esta web no tiene formularios, ni cuentas de usuario, ni cookies. Solo tratamos tus datos si nos escribes un correo, y únicamente para contestarte.</p>"]),
            ("Responsable del <span>tratamiento</span>", [_owner(lang, email)]),
            ("Qué datos tratamos y <span>para qué</span>", [
                "<ul>"
                "<li><strong>Si nos escribes</strong> a info@ o por Instagram: tu nombre, tu correo o usuario y lo que nos cuentes. Lo usamos solo para responderte y gestionar lo que nos pidas (por ejemplo, una reserva de grupo o una colaboración). Base legal: tu consentimiento al escribirnos y nuestro interés legítimo en atenderte.</li>"
                "<li><strong>Estadísticas de visitas:</strong> usamos Cloudflare Web Analytics, que cuenta visitas de forma agregada, sin cookies y sin identificarte.</li>"
                "<li><strong>Datos técnicos:</strong> como cualquier web, nuestro proveedor de alojamiento procesa tu dirección IP para servirte la página y protegerla de ataques. No la usamos para identificarte.</li>"
                "</ul>"]),
            ("Cuánto tiempo los <span>guardamos</span>", [
                "<p>Los correos, el tiempo necesario para atender tu consulta y, después, como máximo un año, salvo que la ley nos obligue a conservarlos más tiempo.</p>"]),
            ("Con quién los <span>compartimos</span>", [
                "<p>No vendemos ni cedemos tus datos. Solo intervienen proveedores que nos dan servicio: <strong>Cloudflare</strong> (alojamiento y estadísticas) y <strong>Google Workspace</strong> (correo). Algunos pueden tratar datos fuera de la UE, siempre con las garantías del RGPD (cláusulas contractuales tipo o el Marco de Privacidad de Datos UE-EE. UU.).</p>",
                "<p>Cuando te apuntas a la lista o compras entradas en <strong>DICE</strong>, o nos escribes por <strong>Instagram</strong>, esas plataformas son responsables de los datos que les das, según sus propias políticas de privacidad.</p>"]),
            ("<span>Cookies</span>", [
                "<p>Ahora mismo esta web no usa cookies propias ni de terceros. Si en el futuro añadimos alguna que no sea imprescindible (por ejemplo, para medir campañas), te pediremos permiso antes y actualizaremos esta política.</p>"]),
            ("Tus <span>derechos</span>", [
                f'<p>Puedes pedirnos acceder a tus datos, corregirlos, borrarlos, limitar u oponerte a su uso, o llevártelos, escribiendo a <a href="mailto:{email}">{email}</a>. Si crees que no los hemos tratado bien, puedes reclamar ante la Agencia Española de Protección de Datos (<a href="https://www.aepd.es" target="_blank" rel="noopener">aepd.es</a>).</p>',
                f"<p><em>Última actualización: {UPDATED[lang]}.</em></p>"]),
        ]
    return [
        ("The short <span>version</span>", [
            "<p>This website has no forms, no user accounts and no cookies. We only handle your data if you email us, and only to reply to you.</p>"]),
        ("Data <span>controller</span>", [_owner(lang, email)]),
        ("What data we use and <span>why</span>", [
            "<ul>"
            "<li><strong>If you write to us</strong> at info@ or on Instagram: your name, your email or username and whatever you tell us. We use it only to reply and handle your request (for example, a group booking or a collaboration). Legal basis: your consent when you write to us and our legitimate interest in answering you.</li>"
            "<li><strong>Visit statistics:</strong> we use Cloudflare Web Analytics, which counts visits in aggregate, without cookies and without identifying you.</li>"
            "<li><strong>Technical data:</strong> like any website, our hosting provider processes your IP address to serve the page and protect it from attacks. We don't use it to identify you.</li>"
            "</ul>"]),
        ("How long we <span>keep it</span>", [
            "<p>Emails are kept for as long as needed to handle your request and then for one year at most, unless the law requires us to keep them longer.</p>"]),
        ("Who we <span>share it with</span>", [
            "<p>We don't sell or give away your data. Only the providers that run our services are involved: <strong>Cloudflare</strong> (hosting and statistics) and <strong>Google Workspace</strong> (email). Some may process data outside the EU, always with GDPR safeguards (standard contractual clauses or the EU-US Data Privacy Framework).</p>",
            "<p>When you join the guest list or buy tickets on <strong>DICE</strong>, or message us on <strong>Instagram</strong>, those platforms are responsible for the data you give them, under their own privacy policies.</p>"]),
        ("<span>Cookies</span>", [
            "<p>Right now this website uses no first-party or third-party cookies. If we ever add one that isn't strictly necessary (for example, to measure campaigns), we'll ask for your permission first and update this policy.</p>"]),
        ("Your <span>rights</span>", [
            f'<p>You can ask us to access, correct or delete your data, restrict or object to its use, or take a copy, by writing to <a href="mailto:{email}">{email}</a>. If you think we haven\'t handled it properly, you can complain to the Spanish Data Protection Agency (<a href="https://www.aepd.es/en" target="_blank" rel="noopener">aepd.es</a>).</p>',
            f"<p><em>Last updated: {UPDATED[lang]}.</em></p>"]),
    ]


PAGE_TEXT = {
    "en": {"legal": ("Legal <span>notice</span>", "Who runs this website and the rules for using it. Short and in plain English."),
           "privacy": ("Privacy <span>policy</span>", "What we do with your data. Spoiler: very little."),
           "meta_legal": ("Legal notice · Bad Decisions", "Legal notice of baddecisionsbcn.com: owner, terms of use, intellectual property and governing law."),
           "meta_privacy": ("Privacy policy · Bad Decisions", "Privacy policy of baddecisionsbcn.com: no forms, no cookies. What data we handle when you contact us and your rights."),
           "nav_legal": "Legal notice", "nav_privacy": "Privacy"},
    "es": {"legal": ("Aviso <span>legal</span>", "Quién está detrás de esta web y las normas para usarla. Corto y sin letra pequeña."),
           "privacy": ("Política de <span>privacidad</span>", "Qué hacemos con tus datos. Spoiler: muy poco."),
           "meta_legal": ("Aviso legal · Bad Decisions", "Aviso legal de baddecisionsbcn.com: titular, condiciones de uso, propiedad intelectual y ley aplicable."),
           "meta_privacy": ("Política de privacidad · Bad Decisions", "Política de privacidad de baddecisionsbcn.com: sin formularios ni cookies. Qué datos tratamos si nos escribes y tus derechos."),
           "nav_legal": "Aviso legal", "nav_privacy": "Privacidad"},
}
