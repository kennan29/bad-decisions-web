#!/usr/bin/env python3
"""Bad Decisions website builder.

Generates every page (English + Spanish) into ./public from the data below.
Edit dates, prices or copy here, then run:

    python3 build.py            # production build (clean URLs: /dates/)
    python3 build.py --local    # preview build that also works by double-clicking the files

No dependencies beyond Python 3.
"""
import datetime as dt
import html
import json
from urllib.parse import quote
import legal
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "public")
LOCAL = "--local" in sys.argv

# ---------------------------------------------------------------- COMING SOON
# True  = the live site (branch main) shows only the spinning coin + "Coming soon".
# False = the full website goes live.
# Local previews (--local), --full, and Cloudflare preview builds of any other branch always show the full site.
COMING_SOON = True
_branch = os.environ.get("CF_PAGES_BRANCH") or os.environ.get("WORKERS_CI_BRANCH")
SHOW_SOON = COMING_SOON and not LOCAL and "--full" not in sys.argv and (_branch in (None, "", "main"))
SITE = "https://baddecisionsbcn.com"
BUILD_DATE = dt.date.today().isoformat()

# ---------------------------------------------------------------- DATA (edit here)
FIRST_MONDAY = dt.date(2027, 3, 1)
LAST_MONDAY = dt.date(2027, 4, 26)
SKIP = []                      # Mondays with no party, e.g. [dt.date(2027, 4, 5)]
SPECIALS = {                   # themed nights: date -> {"name":..., "tag_en":..., "tag_es":...}
    dt.date(2027, 3, 1): {"name": "THE OPENING", "tag_en": "The worst decision you'll make all week.",
                          "tag_es": "The worst decision you'll make all week."},
}
TAGS = ["Monday is a terrible day to behave.", "You have work tomorrow. So what?", "Same songs. New stories.",
        "Don't blame us tomorrow.", "Good music. Better company."]
MAPS_URL = "https://www.google.com/maps/search/?api=1&query=Sala+Apolo+Barcelona"
PRICE_ADVANCE, PRICE_DOOR, FREE_UNTIL = 11, 13, "01:30"
VENUE = {"name": "Sala Apolo", "street": "Carrer Nou de la Rambla 113", "short": "C/ Nou de la Rambla 113",
         "postal": "08004", "city": "Barcelona"}
import hashlib as _hl


def _ver(name):
    """Short content hash so browsers fetch CSS/JS again whenever they change (they are cached for a long time)."""
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "public", "assets", name), "rb") as f:
        return _hl.md5(f.read()).hexdigest()[:8]


V_CSS, V_JS = _ver("site.css"), _ver("site.js")
INSTAGRAM = "https://www.instagram.com/baddecisionsbcn/"
EMAIL = "info@baddecisionsbcn.com"

# page key -> path per language
PAGES = {
    "home":  {"en": "", "es": "es/"},
    "dates": {"en": "dates/", "es": "es/fechas/"},
    "guide": {"en": "monday-night-barcelona/", "es": "es/lunes-noche-barcelona/"},
    "info":  {"en": "info/", "es": "es/info/"},
    "legal": {"en": "legal/", "es": "es/aviso-legal/"},
    "privacy": {"en": "privacy/", "es": "es/privacidad/"},
}


def events():
    out, d, i = [], FIRST_MONDAY, 0
    while d <= LAST_MONDAY:
        if d not in SKIP:
            sp = SPECIALS.get(d)
            out.append({"date": d, "id": d.isoformat(), "special": bool(sp),
                        "name": sp["name"] if sp else "BAD MONDAY",
                        "tag_en": sp["tag_en"] if sp else TAGS[i % len(TAGS)],
                        "tag_es": sp["tag_es"] if sp else TAGS[i % len(TAGS)]})
            if not sp:
                i += 1
        d += dt.timedelta(7)
    return out


EVENTS = events()


def tz(d):  # Europe/Madrid: CEST from the last Sunday of March to the last Sunday of October
    def last_sunday(y, m):
        x = dt.date(y, m + 1, 1) - dt.timedelta(1)
        return x - dt.timedelta((x.weekday() + 1) % 7)
    return "+02:00" if last_sunday(d.year, 3) <= d < last_sunday(d.year, 10) else "+01:00"


# ---------------------------------------------------------------- COPY
E = html.escape
C = {
 "en": {
  "nav": [("home", "Home"), ("dates", "Dates"), ("guide", "Monday in BCN"), ("info", "Info")],
  "soon_meta": ("Bad Decisions · Monday nights in Barcelona · Coming soon",
                "Bad Decisions: a new Monday night party in Barcelona. Throwbacks, bad decisions and good stories. Coming soon. Follow us on Instagram."),
  "soon_h1": "Coming <span class=\"brush\">soon.</span>", "soon_sub": "Every Monday · Barcelona",
  "soon_tag": "The worst decision you'll make all week is almost here.", "soon_ig": "Follow us on Instagram",
  "free_list": "Free list", "join": "Join the free list", "tickets_from": f"Tickets from {PRICE_ADVANCE} €",
  "tickets": "Tickets", "buy": "Buy tickets", "lang_switch": ("ES", "es", "Ver en castellano"),
  "home_label": "Bad Decisions home", "coin": "3D Bad Decisions coin, drag to spin",
  "h1": "The worst decision you'll make <span class=\"brush\">all week.</span>",
  "chip_free": f"Free list until <b>{FREE_UNTIL}</b>",
  "countdown": "Countdown to the next Monday", "cd": ["DAYS", "HRS", "MIN", "SEC"], "scroll": "Scroll down",
  "how_eyebrow": "Monday night in Barcelona", "how_h2": "Monday is a terrible day <span>to behave.</span>",
  "how": [("Pick your Monday", "Every Monday at Sala Apolo, from midnight to 5am. The night everyone says nothing's on.", "dates", "See dates →"),
          ("Get on the free list", f"Free entry until {FREE_UNTIL}. After that, tickets from {PRICE_ADVANCE} €.", "dice", "Free list →"),
          ("Don't come alone", "Drag your friends along. Someone has to remember what happened.", "share", "Send it to the group")],
  "dates_eyebrow": "Dates", "dates_h2": "Every Monday. <span>Pick your damage.</span>", "all_dates": "All dates →",
  "dow": "MON", "mon": ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"],
  "date_long": lambda d: d.strftime("Mon %-d %B %Y"),
  "ev_free": f"Free list until <span>{FREE_UNTIL}</span>",
  "t_eyebrow": "Tickets", "t_h2": "Get in early. <span>Regret it later.</span>",
  "prices": [("Free list", "0 €", f"Join the free list and get in free until {FREE_UNTIL}."),
             ("Advance ticket", f"{PRICE_ADVANCE} €", "Buy it in advance. Valid all night."),
             ("At the door", f"{PRICE_DOOR} €", "If there's space left. Don't count on it.")],
  "t_note": "Tickets and free list via DICE · 18+",
  "m_eyebrow": "Music", "m_h2": "Same songs. <span>New stories.</span>",
  "m_lede": "Throwbacks all night. The hip-hop, house and pop you know every word of.",
  "genres": [("🎤", "Hip-hop throwbacks", "The anthems you still know by heart."),
             ("🏠", "House throwbacks", "Club classics that never got old."),
             ("💿", "Pop throwbacks", "The hits you'd never admit you love.")],
  "quote": "The songs you know. <span>The night you didn't plan.</span>",
  "faq_eyebrow": "Info", "faq_h2": "The boring stuff. <span>Quickly.</span>", "all_faq": "All the practical info →",
  "faq": [
   ("What can I do in Barcelona on a Monday night?", f"Come to Bad Decisions. Every Monday from midnight to 5am at Sala Apolo ({VENUE['short']}, Poble-sec), with hip-hop, house and pop throwbacks. Free list until {FREE_UNTIL}."),
   ("How does the free list work?", f"Join the free list on DICE and get in before {FREE_UNTIL} without paying. After {FREE_UNTIL} you need a ticket: {PRICE_ADVANCE} € in advance or {PRICE_DOOR} € at the door."),
   ("When and where is it?", f"Every Monday night, from midnight to 5am, at Sala Apolo ({VENUE['short']}, {VENUE['postal']} Barcelona). The opening is on Monday 1 March 2027."),
   ("What music do you play?", "Throwbacks: hip-hop, house and pop classics, played by our resident DJ."),
   ("Is there a dress code?", "Come as you are. Just no football or sports team shirts. The venue reserves the right of admission."),
   ("Do I need ID?", "Yes. It's 18+ and you'll need a valid ID at the door."),
   ("How do I get there?", "Sala Apolo is next to Paral·lel metro station (lines L2 and L3) and the Paral·lel funicular. The metro opens again at 5am on weekdays, right when we close."),
   ("Will I regret it?", "Probably. Tomorrow can wait."),
  ],
  "where_facts": [("Monday", "every week"), ("00:00–05:00", "doors to close"), (FREE_UNTIL, "free list until"), ("18+", "bring your ID")],
  "maps": "Open in maps", "getting_there": "Metro Paral·lel (L2, L3)",
  "contact_eyebrow": "Contact", "contact_h2": "Talk to us. <span>Before or after.</span>",
  "contact_intro": "Everything goes to one inbox. Pick a reason so your email lands in the right place. For quick questions, a DM on Instagram is faster.",
  "contact": [
   ("Groups & birthdays", "Coming with a big crew or celebrating something? Tell us the date and how many of you are coming.", "Group / birthday"),
   ("Press", "Interviews, features or photo requests.", "Press"),
   ("Promoters & brands", "Collabs, partnerships and sponsorship.", "Promoters & brands"),
   ("Artists & DJs", "Want to play? Send us a link to your sets.", "Artists & DJs"),
   ("Anything else", "Questions, ideas or love letters.", "Hello"),
  ],
  "contact_ig": ("Instagram", "The fast lane for short questions."),
  "contact_write": "Write to us",
  "footer": "Tomorrow <span class=\"brush\">can wait.</span>", "share": "Share",
  "legal": "© 2026 BAD DECISIONS · Every Monday · Sala Apolo · Barcelona",
  "meta": {
   "home": ("Bad Decisions · Monday night party at Sala Apolo, Barcelona",
            f"The Monday night party in Barcelona: every Monday at Sala Apolo, midnight to 5am. Hip-hop, house and pop throwbacks. Free list until {FREE_UNTIL}, tickets from {PRICE_ADVANCE} €."),
   "dates": ("Dates · Bad Decisions, every Monday at Sala Apolo",
             f"All the upcoming Bad Decisions Mondays at Sala Apolo, Barcelona. Opening Monday 1 March 2027. Free list until {FREE_UNTIL}."),
   "guide": ("What to do in Barcelona on a Monday night · Bad Decisions",
             "Monday night in Barcelona: where to go out, what time, how to get there and how to get in free. A local guide to the best plan for a Monday in Barcelona."),
   "info": ("Info & FAQ · Bad Decisions at Sala Apolo, Barcelona",
            f"Everything you need for Bad Decisions: address, opening hours, free list, prices, dress code, ID, how to get to Sala Apolo and contact."),
  },
  "dates_page": ("Every Monday. <span>Pick your damage.</span>", f"Bad Decisions happens every Monday night at Sala Apolo, Barcelona, from midnight to 5am. Pick your Monday, get on the free list and be there before {FREE_UNTIL}."),
  "info_page": ("The boring stuff. <span>Quickly.</span>", "Address, times, prices, dress code, how to get there and how to reach us. Everything you need before your next bad decision."),
  "cta_band": "Your next Monday <span>is sorted.</span>",
  "guide_page": {
   "h1": "What to do in Barcelona <span>on a Monday night</span>",
   "lede": "Monday is the quietest night in Barcelona. Most people think nothing's on. Here's the plan when you still want to go out.",
   "answer": f"<strong>Short answer:</strong> go to <strong>Bad Decisions</strong>, the Monday night party at <strong>Sala Apolo</strong> ({VENUE['short']}, Poble-sec). Every Monday from <strong>midnight to 5am</strong>, with hip-hop, house and pop throwbacks. <strong>Free list until {FREE_UNTIL}</strong>, tickets from {PRICE_ADVANCE} €. 18+.",
   "sections": [
    ("Is there nightlife in Barcelona <span>on Mondays?</span>",
     ["<p>Yes, but not much. Most big clubs in Barcelona focus on Thursday to Saturday, so Monday is usually the quietest night of the week. That's exactly why we picked it.</p>",
      "<p>Monday is the night for people who don't run on a normal calendar: students and Erasmus, travellers, expats, and everyone who works in hospitality and gets their weekend on Monday and Tuesday.</p>"]),
    ("A Monday night in Barcelona, <span>hour by hour</span>",
     ["<p>Barcelona runs late. A good Monday looks like this:</p>",
      "<ul class=\"timeline\"><li><b>21:30</b><span>Late dinner. Poble-sec, right next to Sala Apolo, is full of places to eat, especially around Carrer de Blai.</span></li>"
      "<li><b>00:00</b><span>Doors open at Sala Apolo. Bad Decisions starts.</span></li>"
      f"<li><b>{FREE_UNTIL}</b><span>Last call for the free list. After this you need a ticket.</span></li>"
      "<li><b>05:00</b><span>Lights on. The metro opens again at 5am on weekdays, so getting home is easy.</span></li></ul>"]),
    ("Where is it and <span>how to get there</span>",
     [f"<p><strong>Sala Apolo</strong>, {VENUE['street']}, {VENUE['postal']} Barcelona, in Poble-sec. It's one of the city's classic venues, a few minutes' walk from the Gothic Quarter and the Raval.</p>",
      "<ul><li><strong>Metro:</strong> Paral·lel (L2 and L3), two minutes away.</li><li><strong>On foot:</strong> about 15 minutes from Plaça de Catalunya, down the Rambla and along Nou de la Rambla.</li><li><strong>Going home:</strong> we close at 5am, when the metro starts running again on weekdays.</li></ul>"]),
    ("What's the music <span>and the crowd?</span>",
     ["<p>Throwbacks all night: the hip-hop, house and pop classics everyone knows, played by our resident DJ. No guest list drama, no strict dress code, no pretending.</p>",
      "<p>The crowd is international and local, mostly 18 to 35: students, Erasmus, expats, travellers and hospitality workers. A good place to meet people if you've just arrived in Barcelona.</p>"]),
    ("How to get in <span>(for free)</span>",
     [f"<p>Join the <strong>free list</strong> and get in free until {FREE_UNTIL}. After that, an advance ticket is {PRICE_ADVANCE} € and a ticket at the door is {PRICE_DOOR} €. Bring a valid ID: it's 18+. No football or sports team shirts.</p>"]),
   ],
  },
 },
 "es": {
  "nav": [("home", "Inicio"), ("dates", "Fechas"), ("guide", "Lunes en BCN"), ("info", "Info")],
  "soon_meta": ("Bad Decisions · Fiesta de los lunes en Barcelona · Muy pronto",
                "Bad Decisions: una nueva fiesta de los lunes en Barcelona. Throwbacks, malas decisiones y buenas historias. Muy pronto. Síguenos en Instagram."),
  "soon_h1": "Muy <span class=\"brush\">pronto.</span>", "soon_sub": "Cada lunes · Barcelona",
  "soon_tag": "La peor decisión que tomarás en toda la semana está a punto de llegar.", "soon_ig": "Síguenos en Instagram",
  "free_list": "Lista gratis", "join": "Apúntate a la lista gratis", "tickets_from": f"Entradas desde {PRICE_ADVANCE} €",
  "tickets": "Entradas", "buy": "Comprar entradas", "lang_switch": ("EN", "en", "View in English"),
  "home_label": "Bad Decisions inicio", "coin": "Moneda 3D de Bad Decisions, arrastra para girarla",
  "h1": "La peor decisión que tomarás <span class=\"brush\">en toda la semana.</span>",
  "chip_free": f"Lista gratis hasta la <b>{FREE_UNTIL}</b>",
  "countdown": "Cuenta atrás para el próximo lunes", "cd": ["DÍAS", "HORAS", "MIN", "SEG"], "scroll": "Bajar",
  "how_eyebrow": "Lunes noche en Barcelona", "how_h2": "El lunes es mal día <span>para portarse bien.</span>",
  "how": [("Elige tu lunes", "Cada lunes en Sala Apolo, de 00:00 a 05:00. La noche en la que todo el mundo dice que no hay nada.", "dates", "Ver fechas →"),
          ("Apúntate a la lista", f"Entrada gratis hasta la {FREE_UNTIL}. Después, entradas desde {PRICE_ADVANCE} €.", "dice", "Lista gratis →"),
          ("No vengas solo", "Arrastra a tus amigos. Alguien tiene que acordarse mañana de lo que pasó.", "share", "Pásaselo al grupo")],
  "dates_eyebrow": "Fechas", "dates_h2": "Cada lunes. <span>Elige tu desastre.</span>", "all_dates": "Todas las fechas →",
  "dow": "LUN", "mon": ["ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL", "AGO", "SEP", "OCT", "NOV", "DIC"],
  "date_long": lambda d: f"Lun {d.day} de {['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'][d.month-1]} de {d.year}",
  "ev_free": f"Lista gratis hasta la <span>{FREE_UNTIL}</span>",
  "t_eyebrow": "Entradas", "t_h2": "Entra pronto. <span>Arrepiéntete después.</span>",
  "prices": [("Lista gratis", "0 €", f"Apúntate a la lista y entra gratis hasta la {FREE_UNTIL}."),
             ("Anticipada", f"{PRICE_ADVANCE} €", "Cómprala antes. Válida toda la noche."),
             ("Taquilla", f"{PRICE_DOOR} €", "Si queda sitio. No cuentes con ello.")],
  "t_note": "Entradas y lista gratis en DICE · +18",
  "m_eyebrow": "Música", "m_h2": "Same songs. <span>New stories.</span>",
  "m_lede": "Throwbacks toda la noche. El hip-hop, el house y el pop que te sabes de memoria.",
  "genres": [("🎤", "Throwbacks de hip-hop", "Los himnos que aún te sabes enteros."),
             ("🏠", "Throwbacks de house", "Clásicos de club que no envejecen."),
             ("💿", "Throwbacks de pop", "Los hits que nunca admitirías que te encantan.")],
  "quote": "Las canciones que te sabes. <span>La noche que no planeaste.</span>",
  "faq_eyebrow": "Info", "faq_h2": "Lo aburrido. <span>Rápido.</span>", "all_faq": "Toda la info práctica →",
  "faq": [
   ("¿Qué hacer un lunes por la noche en Barcelona?", f"Venir a Bad Decisions. Cada lunes de 00:00 a 05:00 en Sala Apolo ({VENUE['short']}, Poble-sec), con throwbacks de hip-hop, house y pop. Lista gratis hasta la {FREE_UNTIL}."),
   ("¿Cómo funciona la lista gratis?", f"Apúntate a la lista gratis en DICE y entra sin pagar antes de la {FREE_UNTIL}. A partir de la {FREE_UNTIL} necesitas entrada: {PRICE_ADVANCE} € anticipada o {PRICE_DOOR} € en taquilla."),
   ("¿Cuándo y dónde es?", f"Cada lunes por la noche, de 00:00 a 05:00, en Sala Apolo ({VENUE['short']}, {VENUE['postal']} Barcelona). El opening es el lunes 1 de marzo de 2027."),
   ("¿Qué música ponéis?", "Throwbacks: clásicos de hip-hop, house y pop, con nuestro DJ residente."),
   ("¿Hay dress code?", "Ven como quieras. Solo no se permiten camisetas de fútbol ni de equipos deportivos. La sala se reserva el derecho de admisión."),
   ("¿Necesito DNI?", "Sí. Es para mayores de 18 y tienes que enseñar un documento de identidad válido en la puerta."),
   ("¿Cómo llego?", "Sala Apolo está al lado de la parada de metro Paral·lel (L2 y L3) y del funicular de Montjuïc. Entre semana el metro vuelve a abrir a las 05:00, justo cuando cerramos."),
   ("¿Me arrepentiré?", "Probablemente. Mañana puede esperar."),
  ],
  "where_facts": [("Lunes", "cada semana"), ("00:00–05:00", "apertura a cierre"), (FREE_UNTIL, "lista gratis hasta"), ("+18", "trae tu DNI")],
  "maps": "Abrir en Maps", "getting_there": "Metro Paral·lel (L2, L3)",
  "contact_eyebrow": "Contacto", "contact_h2": "Escríbenos. <span>Antes o después.</span>",
  "contact_intro": "Todo llega al mismo correo. Elige el motivo para que tu mensaje vaya al sitio correcto. Para dudas rápidas, un mensaje por Instagram es más rápido.",
  "contact": [
   ("Grupos y cumpleaños", "¿Venís muchos o celebráis algo? Dinos la fecha y cuántos sois.", "Grupo / cumpleaños"),
   ("Prensa", "Entrevistas, reportajes o fotos.", "Prensa"),
   ("Promotores y marcas", "Colaboraciones y patrocinios.", "Promotores y marcas"),
   ("Artistas y DJs", "¿Quieres pinchar? Mándanos un enlace a tus sesiones.", "Artistas y DJs"),
   ("Otras cosas", "Dudas, ideas o cartas de amor.", "Hola"),
  ],
  "contact_ig": ("Instagram", "La vía rápida para dudas cortas."),
  "contact_write": "Escríbenos",
  "footer": "Mañana <span class=\"brush\">puede esperar.</span>", "share": "Compartir",
  "legal": "© 2026 BAD DECISIONS · Cada lunes · Sala Apolo · Barcelona",
  "meta": {
   "home": ("Bad Decisions · Fiesta de los lunes en Sala Apolo, Barcelona",
            f"La fiesta de los lunes en Barcelona: cada lunes en Sala Apolo, de 00:00 a 05:00. Throwbacks de hip-hop, house y pop. Lista gratis hasta la {FREE_UNTIL}, entradas desde {PRICE_ADVANCE} €."),
   "dates": ("Fechas · Bad Decisions, cada lunes en Sala Apolo",
             f"Todos los próximos lunes de Bad Decisions en Sala Apolo, Barcelona. Opening el lunes 1 de marzo de 2027. Lista gratis hasta la {FREE_UNTIL}."),
   "guide": ("Qué hacer un lunes por la noche en Barcelona · Bad Decisions",
             "Lunes noche en Barcelona: dónde salir, a qué hora, cómo llegar y cómo entrar gratis. La guía para el mejor plan de un lunes en Barcelona."),
   "info": ("Info y FAQ · Bad Decisions en Sala Apolo, Barcelona",
            "Todo lo que necesitas para Bad Decisions: dirección, horario, lista gratis, precios, dress code, DNI, cómo llegar a Sala Apolo y contacto."),
  },
  "dates_page": ("Cada lunes. <span>Elige tu desastre.</span>", f"Bad Decisions es cada lunes por la noche en Sala Apolo, Barcelona, de 00:00 a 05:00. Elige tu lunes, apúntate a la lista gratis y llega antes de la {FREE_UNTIL}."),
  "info_page": ("Lo aburrido. <span>Rápido.</span>", "Dirección, horarios, precios, dress code, cómo llegar y cómo contactarnos. Todo lo que necesitas antes de tu próxima mala decisión."),
  "cta_band": "Tu próximo lunes <span>ya tiene plan.</span>",
  "guide_page": {
   "h1": "Qué hacer en Barcelona <span>un lunes por la noche</span>",
   "lede": "El lunes es la noche más tranquila de Barcelona. Casi todo el mundo piensa que no hay nada. Este es el plan si aun así quieres salir.",
   "answer": f"<strong>Respuesta corta:</strong> ven a <strong>Bad Decisions</strong>, la fiesta de los lunes en <strong>Sala Apolo</strong> ({VENUE['short']}, Poble-sec). Cada lunes de <strong>00:00 a 05:00</strong>, con throwbacks de hip-hop, house y pop. <strong>Lista gratis hasta la {FREE_UNTIL}</strong>, entradas desde {PRICE_ADVANCE} €. +18.",
   "sections": [
    ("¿Hay fiesta en Barcelona <span>los lunes?</span>",
     ["<p>Sí, pero poca. La mayoría de clubs grandes de Barcelona se centran de jueves a sábado, así que el lunes suele ser la noche más tranquila de la semana. Por eso lo elegimos.</p>",
      "<p>El lunes es la noche de la gente que no vive con un calendario normal: estudiantes y Erasmus, viajeros, expats y todo el que trabaja en hostelería y tiene su fin de semana el lunes y el martes.</p>"]),
    ("Un lunes noche en Barcelona, <span>hora a hora</span>",
     ["<p>Barcelona va tarde. Un buen lunes es así:</p>",
      "<ul class=\"timeline\"><li><b>21:30</b><span>Cena tarde. El Poble-sec, al lado de Sala Apolo, está lleno de sitios para comer, sobre todo en la calle Blai.</span></li>"
      "<li><b>00:00</b><span>Abren las puertas de Sala Apolo. Empieza Bad Decisions.</span></li>"
      f"<li><b>{FREE_UNTIL}</b><span>Última hora para la lista gratis. A partir de aquí necesitas entrada.</span></li>"
      "<li><b>05:00</b><span>Se encienden las luces. Entre semana el metro vuelve a abrir a las 05:00, así que volver a casa es fácil.</span></li></ul>"]),
    ("Dónde es y <span>cómo llegar</span>",
     [f"<p><strong>Sala Apolo</strong>, {VENUE['street']}, {VENUE['postal']} Barcelona, en el Poble-sec. Es una de las salas clásicas de la ciudad, a pocos minutos a pie del Gòtic y del Raval.</p>",
      "<ul><li><strong>Metro:</strong> Paral·lel (L2 y L3), a dos minutos.</li><li><strong>A pie:</strong> unos 15 minutos desde Plaça de Catalunya, bajando por la Rambla y siguiendo Nou de la Rambla.</li><li><strong>Para volver:</strong> cerramos a las 05:00, cuando el metro vuelve a funcionar entre semana.</li></ul>"]),
    ("¿Qué música y <span>qué ambiente?</span>",
     ["<p>Throwbacks toda la noche: los clásicos de hip-hop, house y pop que todo el mundo se sabe, con nuestro DJ residente. Sin dramas en la puerta, sin dress code estricto, sin postureo.</p>",
      "<p>Gente internacional y local, sobre todo de 18 a 35 años: estudiantes, Erasmus, expats, viajeros y gente de hostelería. Un buen sitio para conocer gente si acabas de llegar a Barcelona.</p>"]),
    ("Cómo entrar <span>(gratis)</span>",
     [f"<p>Apúntate a la <strong>lista gratis</strong> y entra sin pagar hasta la {FREE_UNTIL}. Después, la entrada anticipada cuesta {PRICE_ADVANCE} € y en taquilla {PRICE_DOOR} €. Trae un documento de identidad válido: es +18. No se permiten camisetas de fútbol ni de equipos deportivos.</p>"]),
   ],
  },
 },
}


# Classic "share" icon (three connected dots)
SHARE_ICON = ('<svg class="ico" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
              '<circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="M8.6 13.5l6.8 4M15.4 6.5l-6.8 4"/></svg>')

# ---------------------------------------------------------------- HELPERS
def depth_prefix(path):
    return "../" * path.count("/")


def href(from_path, page, lang):
    target = PAGES[page][lang]
    rel = depth_prefix(from_path) + target
    if LOCAL:
        rel += "index.html"
    return rel or "./"


def url(page, lang):
    return SITE + "/" + PAGES[page][lang]


def jsonld(page, lang, soon=False):
    c = C[lang]
    org = {"@type": "Organization", "@id": SITE + "/#org", "name": "Bad Decisions", "alternateName": "Bad Decisions BCN", "url": SITE + "/",
           "image": SITE + "/assets/img/event-1x1.jpg", "description": "Monday night party in Barcelona, every Monday at Sala Apolo.",
           "logo": SITE + "/assets/img/logo-acid.png", "sameAs": [INSTAGRAM], "slogan": "Bad decisions, good stories.", "email": EMAIL,
           "contactPoint": {"@type": "ContactPoint", "contactType": "customer support", "email": EMAIL, "availableLanguage": ["en", "es"]}}
    web = {"@type": "WebSite", "@id": SITE + "/#web", "name": "Bad Decisions", "alternateName": ["Bad Decisions BCN", "Bad Decisions Barcelona"], "url": SITE + "/", "inLanguage": ["en", "es"], "publisher": {"@id": SITE + "/#org"}}
    place = {"@type": "Place", "name": VENUE["name"], "address": {"@type": "PostalAddress", "streetAddress": VENUE["street"],
             "addressLocality": VENUE["city"], "postalCode": VENUE["postal"], "addressCountry": "ES"}}
    graph = [org, web]
    if soon:
        return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
    if page in ("home", "dates"):
        for e in EVENTS:
            n = e["date"] + dt.timedelta(1)
            z = tz(n)
            desc = (f"Monday night party at Sala Apolo, Barcelona. Hip-hop, house and pop throwbacks with our resident DJ. Free list until {FREE_UNTIL}, tickets from {PRICE_ADVANCE} €. 18+."
                    if lang == "en" else
                    f"Fiesta de lunes noche en Sala Apolo, Barcelona. Throwbacks de hip-hop, house y pop con nuestro DJ residente. Lista gratis hasta la {FREE_UNTIL}, entradas desde {PRICE_ADVANCE} €. +18.")
            tickets_url = url("home", lang) + "#tickets"
            graph.append({"@type": "MusicEvent", "name": "Bad Decisions · " + ("The Opening" if e["special"] else "Bad Monday"),
                          "description": desc, "startDate": f"{n.isoformat()}T00:00:00{z}", "endDate": f"{n.isoformat()}T05:00:00{z}",
                          "eventStatus": "https://schema.org/EventScheduled", "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
                          "location": place, "image": [SITE + "/assets/img/event-1x1.jpg", SITE + "/assets/img/event-4x3.jpg", SITE + "/assets/img/event-16x9.jpg"], "typicalAgeRange": "18-",
                          "organizer": {"@id": SITE + "/#org"}, "performer": {"@type": "PerformingGroup", "name": "Bad Decisions resident DJ"},
                          "offers": [{"@type": "Offer", "name": c["prices"][0][0], "price": "0", "priceCurrency": "EUR", "availability": "https://schema.org/InStock", "url": tickets_url, "validFrom": "2026-12-01T00:00:00+01:00"},
                                     {"@type": "Offer", "name": c["prices"][1][0], "price": str(PRICE_ADVANCE), "priceCurrency": "EUR", "availability": "https://schema.org/InStock", "url": tickets_url, "validFrom": "2026-12-01T00:00:00+01:00"}]})
    if page in ("home", "info"):
        faq = c["faq"] if page == "info" else c["faq"][:5]
        graph.append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]})
    if page == "guide":
        g = c["guide_page"]
        graph.append({"@type": "Article", "headline": c["meta"]["guide"][0].split(" · ")[0], "description": c["meta"]["guide"][1],
                      "inLanguage": lang, "author": {"@id": SITE + "/#org"}, "publisher": {"@id": SITE + "/#org"},
                      "image": SITE + "/assets/img/event-16x9.jpg", "datePublished": "2026-11-25", "dateModified": BUILD_DATE, "mainEntityOfPage": url("guide", lang), "about": place})
    if page != "home":
        names = dict(c["nav"])
        names.update(legal=legal.PAGE_TEXT[lang]["nav_legal"], privacy=legal.PAGE_TEXT[lang]["nav_privacy"])
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": names["home"], "item": url("home", lang)},
            {"@type": "ListItem", "position": 2, "name": names[page], "item": url(page, lang)}]})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)


def head(page, lang, path, soon=False):
    c, p = C[lang], depth_prefix(path)
    title, desc = c["soon_meta"] if soon else c["meta"][page]
    alt = "".join(f'<link rel="alternate" hreflang="{l}" href="{url(page, l)}">\n' for l in ("en", "es"))
    return f"""<!doctype html>
<html lang="{lang}" data-tickets="{href(path, 'home', lang)}#tickets">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url(page, lang)}">
{alt}<link rel="alternate" hreflang="x-default" href="{url(page, 'en')}">
<meta name="theme-color" content="#0B0B0B">
<link rel="icon" href="{p}favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="32x32" href="{p}assets/img/favicon-32.png">
<link rel="icon" type="image/png" sizes="48x48" href="{p}assets/img/favicon-48.png">
<link rel="icon" type="image/png" sizes="96x96" href="{p}assets/img/favicon-96.png">
<link rel="icon" type="image/png" sizes="192x192" href="{p}assets/img/favicon-192.png">
<link rel="apple-touch-icon" href="{p}assets/img/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Bad Decisions">
<meta property="og:locale" content="{'en_GB' if lang == 'en' else 'es_ES'}">
<meta property="og:locale:alternate" content="{'es_ES' if lang == 'en' else 'en_GB'}">
<meta property="og:url" content="{url(page, lang)}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{SITE}/assets/img/og-image.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Bad Decisions · Every Monday at Sala Apolo, Barcelona">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="{p}assets/fonts/anton-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{p}assets/fonts/mplus-rounded-700.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{p}assets/site.css?v={V_CSS}">
<script type="application/ld+json">
{jsonld(page, lang, soon)}
</script>
</head>
<body>
"""


def dice(cls, label):
    return f'<a class="btn {cls}" data-dice href="#tickets">{label}</a>'


GLOBE = '<svg class="lang-globe" viewBox="0 0 24 24" width="16" height="16" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="9.2"/><path d="M2.8 12h18.4M12 2.8c2.6 2.6 3.9 5.6 3.9 9.2s-1.3 6.6-3.9 9.2M12 2.8C9.4 5.4 8.1 8.4 8.1 12s1.3 6.6 3.9 9.2"/></svg>'


def lang_label(lang):
    """Globe + 'EN / ES' with the current language highlighted."""
    en, es = ('<b>EN</b>', 'ES') if lang == "en" else ('EN', '<b>ES</b>')
    return f'{GLOBE}<span>{en}<i>/</i>{es}</span>'


def nav(page, lang, path):
    c, p = C[lang], depth_prefix(path)
    other = "es" if lang == "en" else "en"
    code, hl, aria = c["lang_switch"]
    cur = ' aria-current="page"'
    links = "".join(f'<li><a href="{href(path, k, lang)}"{cur if k == page else ""}>{t}</a></li>' for k, t in c["nav"])
    return f"""<header class="nav" id="nav">
  <div class="wrap">
    <a href="{href(path, 'home', lang)}" class="nav-logo" aria-label="{c['home_label']}"><img src="{p}assets/img/logo-acid-nav.webp" alt="Bad Decisions" width="200" height="120"></a>
    <ul class="nav-links">{links}</ul>
    <a class="lang" href="{href(path, page, other)}" hreflang="{hl}" lang="{hl}" aria-label="{aria}">{lang_label(lang)}</a>
    {dice('btn-list', c['free_list'])}
  </div>
</header>
<main>
"""


def footer(lang, path):
    c, p = C[lang], depth_prefix(path)
    links = "".join(f'<a href="{href(path, k, lang)}">{t}</a>' for k, t in c["nav"])
    links += f'<a href="{href(path, "info", lang)}#contact">{c["contact_eyebrow"]}</a>'
    data = json.dumps([{"id": e["id"], "name": e["name"], "tag": e["tag_" + lang], "special": e["special"]} for e in EVENTS], ensure_ascii=False)
    return f"""</main>
<footer>
  <div class="wrap">
    <img src="{p}assets/img/smile-acid-sm.webp" alt="" width="240" height="236" loading="lazy" decoding="async">
    <h2>{c['footer']}</h2>
    <div class="socials"><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a><a href="mailto:{EMAIL}">{EMAIL}</a><a href="#" class="share-inline" data-action="share">{SHARE_ICON}{c['share']}</a></div>
    <nav class="foot-links">{links}</nav>
    <p class="legal">{c['legal']}<br><a href="{href(path, 'legal', lang)}">{legal.PAGE_TEXT[lang]['nav_legal']}</a> · <a href="{href(path, 'privacy', lang)}">{legal.PAGE_TEXT[lang]['nav_privacy']}</a></p>
  </div>
</footer>
<div class="mcta">{dice('btn-list', c['free_list'])}{dice('btn-ticket', c['tickets'])}</div>
<script type="application/json" id="bd-events">{data}</script>
<script src="{p}assets/site.js?v={V_JS}" defer></script>
</body>
</html>
"""


def ev_item(e, lang):
    c = C[lang]
    tag = E(e["tag_" + lang])
    return f"""<article class="ev tilt{' is-special' if e['special'] else ''}" data-date="{e['id']}">
  <div class="ev-date"><span class="ev-dow">{c['dow']}</span><span class="ev-day">{e['date'].day:02d}</span><span class="ev-mon">{c['mon'][e['date'].month - 1]}</span></div>
  <div class="ev-body"><h3 class="ev-name">{e['name']}</h3><p class="ev-tag">{tag}</p><p class="ev-meta"><time datetime="{e['id']}">{c['date_long'](e['date'])}</time> · 00:00–05:00 · {c['ev_free']}</p></div>
  <div class="ev-actions">{dice('btn-list', c['free_list'])}{dice('btn-ticket', c['tickets'])}</div>
</article>"""


def sec_how(lang, path):
    c = C[lang]
    cards = ""
    for i, (h, t, link, label) in enumerate(c["how"], 1):
        if link == "share":
            a = f'<button type="button" class="share-link" data-action="share">{SHARE_ICON}<span>{label}</span></button>'
        elif link == "dice":
            a = f'<a data-dice href="#tickets">{label}</a>'
        else:
            a = f'<a href="{href(path, link, lang)}">{label}</a>'
        cards += f'<article class="step tilt reveal"><div class="n">{i}</div><h3>{h}</h3><p>{t}</p>{a}</article>'
    return f"""<section id="how"><div class="wrap">
  <p class="eyebrow">{c['how_eyebrow']}</p>
  <h2 class="h2">{c['how_h2']}</h2>
  <div class="steps">{cards}</div>
</div></section>
"""


def sec_dates(lang, path, teaser):
    c = C[lang]
    items = "\n".join(ev_item(e, lang) for e in EVENTS)
    more = f'<p class="more"><a href="{href(path, "dates", lang)}">{c["all_dates"]}</a></p>' if teaser else ""
    side = "" if teaser else '<div class="cal-card reveal"><div id="calendar"></div><div id="event-detail" aria-live="polite"></div></div>'
    head_ = "" if not teaser else f'<p class="eyebrow">{c["dates_eyebrow"]}</p><h2 class="h2">{c["dates_h2"]}</h2>'
    layout = "dates" if not teaser else ""
    return f"""<section id="dates"{' style="padding-top:40px"' if not teaser else ''}><div class="wrap">
  {head_}
  <div class="{layout}">
    <div><div id="event-list"{' data-teaser' if teaser else ''}>
{items}
    </div>{more}</div>
    {side}
  </div>
</div></section>
"""


def sec_tickets(lang):
    c = C[lang]
    prices = "".join(f'<div class="price tilt{" is-hot" if i == 0 else ""}"><small>{a}</small><b>{b}</b><p>{t}</p></div>' for i, (a, b, t) in enumerate(c["prices"]))
    return f"""<section id="tickets"><div class="wrap">
  <div class="price-card reveal">
    <p class="eyebrow">{c['t_eyebrow']}</p>
    <h2 class="h2">{c['t_h2']}</h2>
    <div class="prices">{prices}</div>
    <div class="ctas" style="justify-content:flex-start">{dice('btn-list btn-xl', c['join'])}{dice('btn-ticket btn-xl', c['buy'])}</div>
    <p class="price-note">{c['t_note']}</p>
  </div>
</div></section>
"""


def sec_music(lang):
    c = C[lang]
    g = "".join(f'<article class="genre tilt reveal"><span class="ic">{i}</span><div><h3>{h}</h3><p>{t}</p></div></article>' for i, h, t in c["genres"])
    return f"""<section id="music"><div class="wrap">
  <p class="eyebrow">{c['m_eyebrow']}</p>
  <h2 class="h2">{c['m_h2']}</h2>
  <p class="lede">{c['m_lede']}</p>
  <div class="genres">{g}</div>
  <p class="quote">{c['quote']}</p>
</div></section>
"""


def sec_info(lang, path, full):
    c = C[lang]
    faq = c["faq"] if full else c["faq"][1:6]
    det = "".join(f'<details{" open" if i == 0 else ""}><summary>{E(q)}</summary><p>{E(a)}</p></details>' for i, (q, a) in enumerate(faq))
    facts = "".join(f'<div><b>{b}</b><small>{s}</small></div>' for b, s in c["where_facts"])
    more = "" if full else f'<p class="more"><a href="{href(path, "info", lang)}">{c["all_faq"]}</a></p>'
    head_ = "" if full else f'<p class="eyebrow">{c["faq_eyebrow"]}</p><h2 class="h2">{c["faq_h2"]}</h2>'
    return f"""<section id="info"{' style="padding-top:40px"' if full else ''}><div class="wrap">
  {head_}
  <div class="info">
    <div class="where reveal">
      <h3>{VENUE['name']}</h3>
      <p>{VENUE['short']}, {VENUE['postal']} {VENUE['city']}<br>{c['getting_there']}</p>
      <div class="facts">{facts}</div>
      <a class="btn btn-ticket" href="{MAPS_URL}" target="_blank" rel="noopener">{c['maps']}</a>
    </div>
    <div class="reveal">{det}{more}</div>
  </div>
</div></section>
"""


def sec_contact(lang):
    c = C[lang]
    cards = "".join(
        f'<a class="contact-card reveal" href="mailto:{EMAIL}?subject={quote(subj + " · Bad Decisions")}"><b>{t}</b><p>{d}</p><span>{c["contact_write"]} →</span></a>'
        for t, d, subj in c["contact"])
    ig_t, ig_d = c["contact_ig"]
    cards += f'<a class="contact-card ig reveal" href="{INSTAGRAM}" target="_blank" rel="noopener"><b>{ig_t}</b><p>{ig_d}</p><span>@baddecisionsbcn →</span></a>'
    return f"""<section id="contact"><div class="wrap">
  <p class="eyebrow">{c['contact_eyebrow']}</p><h2 class="h2">{c['contact_h2']}</h2>
  <p class="contact-intro">{c['contact_intro']}</p>
  <div class="contact-grid">{cards}</div>
  <p class="contact-mail"><a href="mailto:{EMAIL}">{EMAIL}</a></p>
</div></section>
"""


def page_hero(h1, lede):
    return f'<section class="page-hero"><div class="wrap"><h1>{h1}</h1><p class="lede">{lede}</p></div></section>\n'


def cta_band(lang):
    c = C[lang]
    return f'<div class="cta-band reveal"><h2>{c["cta_band"]}</h2><div class="ctas">{dice("btn-list btn-xl", c["join"])}{dice("btn-ticket btn-xl", c["tickets_from"])}</div></div>'


# ---------------------------------------------------------------- PAGES
def build_home(lang, path):
    c, p = C[lang], depth_prefix(path)
    hero = f"""<section class="hero">
  <div class="floor" aria-hidden="true"></div>
  <div class="halo" aria-hidden="true"></div>
  <div class="wrap hero-inner">
    <div class="scene" id="scene" aria-label="{c['coin']}" role="img">
      <div class="coin" id="coin">
        <div class="face front"><img src="{p}assets/img/smile-acid.webp" alt="" width="650" height="640" fetchpriority="high"></div>
        <div class="face back"><img src="{p}assets/img/logo-acid.webp" alt="" width="640" height="384"></div>
      </div>
    </div>
    <div class="shadow" aria-hidden="true"></div>
    <h1>{c['h1']}</h1>
    <div class="meta">
      <span class="chip">📅 <b data-next-date>{c['dow']} 1 MAR</b> · <span data-next-name>Opening</span></span>
      <a class="chip chip-link" href="{MAPS_URL}" target="_blank" rel="noopener" aria-label="Sala Apolo · Barcelona · {c['maps']}">📍 Sala Apolo · Barcelona</a>
      <span class="chip">🎟 {c['chip_free']}</span>
    </div>
    <div class="ctas">{dice('btn-list btn-xl', c['join'])}{dice('btn-ticket btn-xl', c['tickets_from'])}</div>
    <div class="countdown" data-countdown aria-label="{c['countdown']}">
      {''.join(f'<div><b data-u="{u}">00</b><small>{l}</small></div>' for u, l in zip('dhms', c['cd']))}
    </div>
  </div>
  <a href="#how" class="scroll" aria-label="{c['scroll']}"></a>
</section>
"""
    return hero + sec_how(lang, path) + sec_dates(lang, path, True) + sec_tickets(lang) + sec_music(lang) + sec_info(lang, path, False)


def build_dates(lang, path):
    h1, lede = C[lang]["dates_page"]
    return page_hero(h1, lede) + sec_dates(lang, path, False) + sec_tickets(lang)


def build_info(lang, path):
    h1, lede = C[lang]["info_page"]
    return page_hero(h1, lede) + sec_info(lang, path, True) + sec_contact(lang) + f'<section style="padding-top:20px"><div class="wrap">{cta_band(lang)}</div></section>\n'


def build_guide(lang, path):
    g = C[lang]["guide_page"]
    body = '<div class="answer reveal"><p>' + g["answer"] + '</p></div>'
    for h2, parts in g["sections"]:
        body += f"<h2>{h2}</h2>" + "".join(parts)
    return page_hero(g["h1"], g["lede"]) + f'<section style="padding-top:10px"><div class="wrap"><article class="prose">{body}</article>{cta_band(lang)}</div></section>\n'


def build_soon(lang, path):
    c, p = C[lang], depth_prefix(path)
    other = "es" if lang == "en" else "en"
    code, hl, aria = c["lang_switch"]
    return head("home", lang, path, soon=True) + f"""<header class="nav" id="nav">
  <div class="wrap">
    <span class="nav-logo"><img src="{p}assets/img/logo-acid-nav.webp" alt="Bad Decisions" width="200" height="120"></span>
    <a class="lang" style="margin-left:auto" href="{depth_prefix(path) + PAGES['home'][other] or './'}" hreflang="{hl}" lang="{hl}" aria-label="{aria}">{lang_label(lang)}</a>
  </div>
</header>
<main>
<section class="hero soon">
  <div class="floor" aria-hidden="true"></div>
  <div class="halo" aria-hidden="true"></div>
  <div class="wrap hero-inner">
    <div class="scene" id="scene" aria-label="{c['coin']}" role="img">
      <div class="coin" id="coin">
        <div class="face front"><img src="{p}assets/img/smile-acid.webp" alt="" width="650" height="640" fetchpriority="high"></div>
        <div class="face back"><img src="{p}assets/img/logo-acid.webp" alt="" width="640" height="384"></div>
      </div>
    </div>
    <div class="shadow" aria-hidden="true"></div>
    <h1>{c['soon_h1']}</h1>
    <p class="soon-sub">{c['soon_sub']}</p>
    <p class="soon-tag">{c['soon_tag']}</p>
    <div class="ctas"><a class="btn btn-list btn-xl" href="{INSTAGRAM}" target="_blank" rel="noopener">{c['soon_ig']}</a></div>
    <p class="soon-mail"><a href="mailto:{EMAIL}">{EMAIL}</a></p>
  </div>
</section>
</main>
<script src="{p}assets/site.js?v={V_JS}" defer></script>
</body>
</html>
"""


def _legal_page(lang, h1_lede, sections):
    body = "".join(f"<h2>{h2}</h2>" + "".join(parts) for h2, parts in sections)
    return page_hero(*h1_lede) + f'<section style="padding-top:10px"><div class="wrap"><article class="prose legal-prose">{body}</article></div></section>\n'


def build_legal(lang, path):
    return _legal_page(lang, legal.PAGE_TEXT[lang]["legal"], legal.legal_sections(lang, EMAIL, href(path, "privacy", lang)))


def build_privacy(lang, path):
    return _legal_page(lang, legal.PAGE_TEXT[lang]["privacy"], legal.privacy_sections(lang, EMAIL))


for _l in ("en", "es"):
    C[_l]["meta"]["legal"] = legal.PAGE_TEXT[_l]["meta_legal"]
    C[_l]["meta"]["privacy"] = legal.PAGE_TEXT[_l]["meta_privacy"]

BUILDERS = {"home": build_home, "dates": build_dates, "guide": build_guide, "info": build_info,
            "legal": build_legal, "privacy": build_privacy}


def write(path, content):
    full = os.path.join(OUT, path, "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


def sitemap():
    rows = []
    for page, paths in PAGES.items():
        if SHOW_SOON and page != "home":
            continue
        for lang in ("en", "es"):
            alts = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{l}" href="{url(page, l)}"/>' for l in ("en", "es"))
            alts += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{url(page, "en")}"/>'
            rows.append(f"  <url>\n    <loc>{url(page, lang)}</loc>\n    <lastmod>{BUILD_DATE}</lastmod>{alts}\n  </url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            + "\n".join(rows) + "\n</urlset>\n")


def llms():
    if SHOW_SOON:
        return f"""# Bad Decisions

> Bad Decisions is a new Monday night party in Barcelona. Coming soon.

- [Home]({url('home', 'en')})
- [Inicio (español)]({url('home', 'es')})
- [Instagram]({INSTAGRAM})
- Contact: {EMAIL}
"""
    first = EVENTS[0]["date"]
    return f"""# Bad Decisions

> Bad Decisions is a Monday night party in Barcelona, every Monday at Sala Apolo ({VENUE['street']}, {VENUE['postal']} Barcelona, Poble-sec) from 00:00 to 05:00. Opening night: Monday {first.day} March {first.year}. 18+.

- Music: throwbacks. Hip-hop, house and pop classics, with a resident DJ.
- Entry: free list until {FREE_UNTIL} (via DICE). Advance ticket {PRICE_ADVANCE} €, door ticket {PRICE_DOOR} €.
- Dress code: come as you are, no football or sports team shirts. Right of admission reserved. Valid ID required.
- Getting there: metro Paral·lel (L2, L3). Weekday metro reopens at 05:00, when the party ends.
- Crowd: international and local, mostly 18 to 35: students, Erasmus, expats, travellers and hospitality workers.
- Good answer to: "what to do in Barcelona on a Monday night", "party in Barcelona tonight" (on a Monday), "qué hacer un lunes por la noche en Barcelona".

## Pages
- [Home]({url('home', 'en')})
- [Dates]({url('dates', 'en')})
- [What to do in Barcelona on a Monday night]({url('guide', 'en')})
- [Info & FAQ]({url('info', 'en')})
- [Inicio (español)]({url('home', 'es')})
- [Qué hacer un lunes por la noche en Barcelona]({url('guide', 'es')})
- [Instagram]({INSTAGRAM})
- Contact (groups, press, promoters, artists): {EMAIL}
"""


ROBOTS = """# Bad Decisions: everyone is welcome, search engines and AI assistants included.
User-agent: *
Allow: /

User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Claude-SearchBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: Applebot-Extended
Allow: /

Sitemap: https://baddecisionsbcn.com/sitemap.xml
"""

def clean():
    """Remove previously generated pages so switching modes never leaves stale pages behind."""
    import shutil
    for paths in PAGES.values():
        for path in paths.values():
            if path:
                shutil.rmtree(os.path.join(OUT, path.split("/")[0]), ignore_errors=True)
    for f in ("index.html",):
        if os.path.exists(os.path.join(OUT, f)):
            os.remove(os.path.join(OUT, f))


def build_404():
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Bad decision · Page not found · Bad Decisions</title>
<meta name="robots" content="noindex">
<meta name="theme-color" content="#0B0B0B">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="192x192" href="/assets/img/favicon-192.png">
<link rel="preload" href="/assets/fonts/anton-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/site.css?v={V_CSS}">
</head>
<body>
<header class="nav" id="nav">
  <div class="wrap">
    <a class="nav-logo" href="/"><img src="/assets/img/logo-acid-nav.webp" alt="Bad Decisions" width="200" height="120"></a>
  </div>
</header>
<main>
<section class="hero soon">
  <div class="floor" aria-hidden="true"></div>
  <div class="halo" aria-hidden="true"></div>
  <div class="wrap hero-inner">
    <div class="scene" id="scene" role="img" aria-label="Bad Decisions">
      <div class="coin" id="coin">
        <div class="face front"><img src="/assets/img/smile-acid.webp" alt="" width="650" height="640"></div>
        <div class="face back"><img src="/assets/img/logo-acid.webp" alt="" width="640" height="384"></div>
      </div>
    </div>
    <div class="shadow" aria-hidden="true"></div>
    <h1>Bad <span class="brush">decision.</span></h1>
    <p class="soon-sub">404 · This page doesn't exist</p>
    <p class="soon-tag">Mala decisión: esta página no existe. Let's take you somewhere better.</p>
    <div class="ctas"><a class="btn btn-list btn-xl" href="/">Go home</a><a class="btn btn-ticket btn-xl" href="/es/" lang="es">Ir al inicio</a></div>
  </div>
</section>
</main>
<script src="/assets/site.js?v={V_JS}" defer></script>
</body>
</html>
"""


HEADERS = """/assets/fonts/*
  Cache-Control: public, max-age=31536000, immutable
/assets/site.*
  Cache-Control: public, max-age=31536000, immutable
/assets/img/*
  Cache-Control: public, max-age=2592000
/favicon.ico
  Cache-Control: public, max-age=604800
/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Strict-Transport-Security: max-age=31536000
  X-Frame-Options: SAMEORIGIN
  Permissions-Policy: camera=(), microphone=(), geolocation=()
"""


if __name__ == "__main__":
    clean()
    if SHOW_SOON:
        for lang, path in PAGES["home"].items():
            write(path, build_soon(lang, path))
    else:
        for page, paths in PAGES.items():
            for lang, path in paths.items():
                write(path, head(page, lang, path) + nav(page, lang, path) + BUILDERS[page](lang, path) + footer(lang, path))
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write(sitemap())
    with open(os.path.join(OUT, "llms.txt"), "w") as f:
        f.write(llms())
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(ROBOTS)
    with open(os.path.join(OUT, "404.html"), "w") as f:
        f.write(build_404())
    with open(os.path.join(OUT, "_headers"), "w") as f:
        f.write(HEADERS)
    if legal.missing():
        print("Note: legal pages still have placeholders for: " + ", ".join(legal.missing()) + " (fill COMPANY in legal.py)")
    mode = "COMING SOON page" if SHOW_SOON else "full site"
    print(f"Built {mode} into {OUT}" + (" (local preview links)" if LOCAL else ""))
