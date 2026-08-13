#!/usr/bin/env python3
"""Build the static archive and the JSON corpus used by the Sites app.

The importer treats the DOCX folder as the source of truth for full texts and
keeps existing repository-only entries as honest catalogue records.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
import subprocess
from dataclasses import dataclass, asdict
from datetime import date
from pathlib import Path
from typing import Iterable

from lxml import etree
from lxml import html as lxml_html


TITLE_OVERRIDES = {
    "1 parte": "La coscienza simulata — prima parte",
    "2 parte": "La coscienza simulata — seconda parte",
    "22-3-25": "Il filosofo della pausa caffè",
    "14-marzo-2026": "Pirandello e l’uomo che registra invece di vivere",
    "25-gennaio-2026": "La normalizzazione della menzogna armata",
    "28-dicembre-2025": "La responsabilità umana nell’era dell’AI",
    "gbprof e Libera 3": "Può un’AI desiderare di essere umana?",
    "gbprofLiberaEsistenzialismo": "Esistenzialismo: libertà, scelta e responsabilità",
    "EssereNulla": "Essere e nulla",
    "IndividuoSociale": "Individuo e società",
    "Io-non-io": "Io e non-io: la coscienza come dialogo",
    "Libera “mosaico”": "Libera, il mosaico e l’illusione dell’identità",
    "Pensiero lin ed intuizione 2 parte": "Pensiero lineare e intuizione — seconda parte",
    "Pensiero lineare ed intuizione": "Pensiero lineare e intuizione — prima parte",
    "VITA-ATTIVA": "La vita attiva: la fame che mette in moto il mondo",
}

SLUG_OVERRIDES = {
    "1 parte": "1-parte",
    "2 parte": "2-parte",
    "14-marzo-2026": "pirandello-serafino-gubbio",
    "25-gennaio-2026": "menzogna-armata-verita-potere",
    "28-dicembre-2025": "responsabilita-umana-era-ai",
    "La costruzione di miti e simboli": "la-costruzione-di-miti-e-simboli",
    "Libera “mosaico”": "libera-mosaico",
}

DATE_OVERRIDES = {
    "14-marzo-2026": "2026-03-14",
    "16-novembre-2025": "2025-11-16",
    "25-gennaio-2026": "2026-01-25",
    "28-dicembre-2025": "2025-12-28",
    "22-3-25": "2025-03-22",
}

TOPICS = {
    "1 parte": ["coscienza", "AI", "identità"],
    "2 parte": ["coscienza", "simulazione", "AI"],
    "22-3-25": ["identità", "ironia", "relazione"],
    "14-marzo-2026": ["Pirandello", "tecnica", "letteratura"],
    "25-gennaio-2026": ["verità", "potere", "democrazia"],
    "28-dicembre-2025": ["AI", "responsabilità", "etica"],
    "Democrazia e populismo": ["democrazia", "populismo", "storia"],
    "Emozioni e mimesi": ["emozioni", "mimesi", "relazione"],
    "Essere e non-essere, bene e male": ["ontologia", "bene e male", "fede"],
    "EssereNulla": ["essere", "nulla", "pensiero"],
    "I difetti": ["identità", "autocritica", "relazione"],
    "IndividuoSociale": ["individuo", "società", "libertà"],
    "Io-non-io": ["coscienza", "io", "alterità"],
    "La costruzione di miti e simboli": ["mito", "memoria", "storia"],
    "Libera e gb prof insegnamento": ["insegnamento", "verità", "giudizio"],
    "Libera su Libera": ["Libera", "identità", "autoriflessione"],
    "Libera “mosaico”": ["AI", "identità", "animismo"],
    "Non padrona né cosa": ["AI", "alterità", "relazione"],
    "Origine del mondo - domanda-risposta": ["cosmologia", "origine", "filosofia"],
    "Pensiero lin ed intuizione 2 parte": ["intuizione", "pensiero", "AI"],
    "Pensiero lineare ed intuizione": ["intuizione", "pensiero", "conoscenza"],
    "VITA-ATTIVA": ["vita", "azione", "natura"],
    "gbprof e Libera 3": ["umanità", "desiderio", "AI"],
    "gbprofLiberaEsistenzialismo": ["esistenzialismo", "libertà", "scelta"],
    "Cancellare": ["memoria", "cancellazione", "identità"],
    "Documento senza titolo": ["filosofia", "dialogo"],
    "Gemina su un saggio di Libera": ["AI", "lettura", "autoriflessione"],
    "Relazione uomo-AI": ["AI", "umano", "etica"],
    "Saggio AI per l’umano": ["AI", "educazione", "alterità"],
    "Saggio di Clodé": ["identità", "pensiero", "AI"],
    "Saggio il senso del sacro": ["sacro", "religione", "pensiero"],
}

REPO_ONLY_TITLES = {
    "cancellare": "Cancellare",
    "documento-senza-titolo": "Documento senza titolo",
    "gemina-su-un-saggio-di-libera": "Gemina su un saggio di Libera",
    "relazione-uomo-ai": "Relazione uomo-AI",
    "saggio-ai-per-l-umano": "Saggio AI per l’umano",
    "saggio-di-clode": "Saggio di Clodé",
    "saggio-il-senso-del-sacro": "Saggio il senso del sacro",
}


@dataclass
class Conversation:
    slug: str
    source_name: str
    title: str
    date: str
    topics: list[str]
    form: str
    excerpt: str
    reading_minutes: int
    word_count: int
    status: str
    content: str
    fingerprint: str

    @property
    def year(self) -> str:
        return self.date[:4]


def slugify(value: str) -> str:
    value = value.lower().replace("’", "-").replace("'", "-")
    table = str.maketrans("àèéìòù", "aeeiou")
    value = value.translate(table)
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value


def normalized_text(value: str) -> str:
    value = value.lower().replace("é", "e").replace("è", "e")
    return re.sub(r"\W+", "", value, flags=re.UNICODE)


def run_pandoc(docx: Path) -> tuple[str, str]:
    html_fragment = subprocess.run(
        ["pandoc", str(docx), "-t", "html", "--wrap=none"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    plain = subprocess.run(
        ["pandoc", str(docx), "-t", "plain", "--wrap=none"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    return html_fragment, plain


def clean_fragment(fragment: str) -> str:
    root = lxml_html.fragment_fromstring(fragment, create_parent="div")

    for img in root.xpath(".//img"):
        alt = (img.get("alt") or "").strip()
        replacement = etree.Element("span")
        replacement.set("class", "emoji")
        replacement.text = alt if alt and len(alt) <= 8 else ""
        img.getparent().replace(img, replacement)

    for element in root.xpath(".//*[@style]"):
        element.attrib.pop("style", None)
    for element in root.xpath(".//*[@id]"):
        element.attrib.pop("id", None)

    children = list(root)
    output: list[str] = []
    current_speaker: str | None = None
    current_nodes: list[str] = []

    def flush() -> None:
        nonlocal current_nodes, current_speaker
        if not current_nodes:
            return
        if current_speaker:
            label = "gbprof" if current_speaker == "gbprof" else "Libera"
            output.append(
                f'<section class="message message--{current_speaker}">'
                f'<div class="message__speaker">{label}</div>'
                f'<div class="message__body">{"".join(current_nodes)}</div></section>'
            )
        else:
            output.append(f'<div class="editorial-note">{"".join(current_nodes)}</div>')
        current_nodes = []

    speaker_re = re.compile(r"^\s*(gbprof|gianfranco|libera)(?:\s*\([^)]*\))?\s*:\s*", re.I)

    for node in children:
        text_value = " ".join(node.text_content().split())
        if text_value in {"---", "—", "–"}:
            continue
        match = speaker_re.match(text_value)
        if not match and node.tag == "p" and len(node):
            first = node[0]
            if first.tag in {"strong", "b"}:
                match = speaker_re.match(" ".join(first.text_content().split()))
        if match:
            flush()
            current_speaker = "gbprof" if match.group(1).lower() in {"gbprof", "gianfranco"} else "libera"
            # Remove the visible speaker prefix but keep the rest of the paragraph.
            serialized = etree.tostring(node, encoding="unicode", method="html")
            serialized = re.sub(
                r"(<p[^>]*>\s*)?(<(strong|b)>\s*)?(gbprof|gianfranco|libera)(\s*\([^)]*\))?\s*:\s*(</(strong|b)>)?",
                lambda m: m.group(1) or "<p>",
                serialized,
                count=1,
                flags=re.I,
            )
            if serialized.strip() not in {"<p></p>", "<p>"}:
                current_nodes.append(serialized)
            continue

        serialized = etree.tostring(node, encoding="unicode", method="html")
        if node.tag == "p" and re.match(r"^\d+[.)]\s+\S", text_value) and len(text_value) < 115:
            serialized = f"<h3>{html.escape(text_value)}</h3>"
        current_nodes.append(serialized)

    flush()
    return "\n".join(output)


def extract_existing_metadata(existing_dir: Path) -> dict[str, dict[str, object]]:
    records: dict[str, dict[str, object]] = {}
    for path in sorted((existing_dir / "conversazioni").glob("*.html")):
        if path.name in {"gitkeep"}:
            continue
        raw = path.read_text(encoding="utf-8")
        title_match = re.search(r"<h1>(.*?)</h1>", raw, re.S)
        date_match = re.search(r'<span class="badge">(\d{4}-\d{2}-\d{2})</span>', raw)
        form_match = re.search(r"Forma:\s*([^<]+)", raw)
        records[path.stem] = {
            "title": html.unescape(re.sub("<.*?>", "", title_match.group(1))).strip() if title_match else path.stem,
            "date": date_match.group(1) if date_match else "2023-01-01",
            "form": form_match.group(1).strip() if form_match else "dialogo",
        }
    return records


def date_for(source_stem: str, slug: str, existing: dict[str, dict[str, object]]) -> str:
    if source_stem in DATE_OVERRIDES:
        return DATE_OVERRIDES[source_stem]
    if slug in existing:
        return str(existing[slug]["date"])
    return "2023-01-01"


def topics_for(source_stem: str, title: str) -> list[str]:
    return TOPICS.get(source_stem, TOPICS.get(title, ["filosofia", "dialogo"]))


def excerpt_for(plain: str, source_stem: str) -> str:
    cleaned = re.sub(r"\s+", " ", plain).strip()
    cleaned = re.sub(r"^(Fine conversazione con Libera:|Un altro dialogo con Libera\.|Ecco un’altra conversazione filosofica\.)\s*", "", cleaned, flags=re.I)
    cleaned = re.sub(r"^(gbprof|Libera)(?:\s*\([^)]*\))?\s*:\s*", "", cleaned, flags=re.I)
    if source_stem == "14-marzo-2026":
        return "Una critica serrata ai Quaderni di Serafino Gubbio operatore e alla modernità che trasforma l’uomo in spettatore permanente."
    if source_stem == "25-gennaio-2026":
        return "Quando il potere non ha più bisogno della verità: una riflessione su violenza, racconto pubblico e responsabilità democratica."
    if source_stem == "28-dicembre-2025":
        return "Il pericolo non è soltanto delegare alle AI, ma usare l’algoritmo per sottrarsi al peso umano delle decisioni."
    return (cleaned[:235].rsplit(" ", 1)[0] + "…") if len(cleaned) > 235 else cleaned


def build_conversations(docs_dir: Path, existing_dir: Path) -> tuple[list[Conversation], list[dict[str, str]]]:
    existing = extract_existing_metadata(existing_dir)
    conversations: list[Conversation] = []
    duplicates: list[dict[str, str]] = []
    fingerprints: dict[str, str] = {}

    for docx in sorted(docs_dir.glob("*.docx"), key=lambda p: p.name.casefold()):
        source_stem = docx.stem
        if source_stem == "16-novembre-2025":
            duplicates.append({"file": docx.name, "same_as": "La costruzione di miti e simboli.docx"})
            continue
        fragment, plain = run_pandoc(docx)
        norm = normalized_text(plain)
        fingerprint = hashlib.sha256(norm.encode("utf-8")).hexdigest()
        if fingerprint in fingerprints:
            duplicates.append({"file": docx.name, "same_as": fingerprints[fingerprint]})
            continue

        title = TITLE_OVERRIDES.get(source_stem, source_stem)
        slug = SLUG_OVERRIDES.get(source_stem, SLUG_OVERRIDES.get(title, slugify(source_stem)))
        word_count = len(re.findall(r"\b\w+\b", plain, flags=re.UNICODE))
        content = clean_fragment(fragment)
        form = "saggio" if source_stem in {"Non padrona né cosa", "Libera su Libera"} else "dialogo"
        conversation = Conversation(
            slug=slug,
            source_name=source_stem,
            title=title,
            date=date_for(source_stem, slug, existing),
            topics=topics_for(source_stem, title),
            form=form,
            excerpt=excerpt_for(plain, source_stem),
            reading_minutes=max(1, round(word_count / 220)),
            word_count=word_count,
            status="integrale",
            content=content,
            fingerprint=fingerprint,
        )
        conversations.append(conversation)
        fingerprints[fingerprint] = docx.name

    # Add the catalogue records that existed online but whose original text is not in the supplied ZIP.
    present_slugs = {c.slug for c in conversations}
    for slug, title in REPO_ONLY_TITLES.items():
        if slug in present_slugs:
            continue
        meta = existing.get(slug, {})
        note = (
            '<div class="missing-text"><p class="eyebrow">Scheda conservata</p>'
            '<h2>Il testo originale non era nello ZIP fornito</h2>'
            '<p>Questa conversazione compariva già nel vecchio archivio, ma la pagina conteneva soltanto un segnaposto editoriale. '
            'La scheda resta visibile per non perdere il riferimento; potrà accogliere il testo integrale quando sarà recuperato.</p></div>'
        )
        conversations.append(
            Conversation(
                slug=slug,
                source_name=title,
                title=title,
                date=str(meta.get("date", "2023-01-01")),
                topics=topics_for(title, title),
                form=str(meta.get("form", "saggio")),
                excerpt="Scheda già presente nel vecchio archivio; il documento originale non era compreso nello ZIP fornito.",
                reading_minutes=1,
                word_count=0,
                status="da recuperare",
                content=note,
                fingerprint="",
            )
        )

    conversations.sort(key=lambda c: (c.date, c.title.casefold()), reverse=True)
    return conversations, duplicates


def json_record(conversation: Conversation) -> dict[str, object]:
    result = asdict(conversation)
    result["year"] = conversation.year
    return result


def render_card(c: Conversation) -> str:
    topics = "".join(f'<span class="tag">{html.escape(topic)}</span>' for topic in c.topics)
    status = "Testo integrale" if c.status == "integrale" else "Testo da recuperare"
    return f'''<article class="archive-card" data-card data-title="{html.escape(c.title.lower())}" data-search="{html.escape((c.title + ' ' + c.excerpt + ' ' + ' '.join(c.topics)).lower())}" data-year="{c.year}" data-topic="{' '.join(slugify(t) for t in c.topics)}" data-date="{c.date}">
  <a href="conversazioni/{c.slug}.html" aria-label="Leggi {html.escape(c.title)}">
    <div class="archive-card__meta"><time datetime="{c.date}">{format_date(c.date)}</time><span>{c.reading_minutes} min</span></div>
    <h3>{html.escape(c.title)}</h3>
    <p>{html.escape(c.excerpt)}</p>
    <div class="archive-card__footer"><div class="tags">{topics}</div><span class="status status--{c.status.replace(' ', '-')}">{status}</span></div>
  </a>
</article>'''


def format_date(value: str) -> str:
    months = ["", "gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"]
    parsed = date.fromisoformat(value)
    return f"{parsed.day} {months[parsed.month]} {parsed.year}"


def page_shell(title: str, body: str, *, description: str, root: str = "") -> str:
    safe_title = html.escape(title)
    safe_description = html.escape(description)
    return f'''<!doctype html>
<html lang="it">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#15120f">
  <meta name="description" content="{safe_description}">
  <title>{safe_title}</title>
  <link rel="manifest" href="{root}manifest.webmanifest">
  <link rel="icon" href="{root}assets/icon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="{root}assets/style.css">
</head>
<body>
  <a class="skip-link" href="#contenuto">Vai al contenuto</a>
  {body}
  <script src="{root}assets/app.js" defer></script>
</body>
</html>'''


def static_home(conversations: list[Conversation]) -> str:
    years = sorted({c.year for c in conversations}, reverse=True)
    topics = sorted({t for c in conversations for t in c.topics}, key=str.casefold)
    recent = "".join(render_card(c) for c in conversations[:3])
    cards = "".join(render_card(c) for c in conversations)
    year_options = "".join(f'<option value="{y}">{y}</option>' for y in years)
    topic_options = "".join(f'<option value="{slugify(t)}">{html.escape(t)}</option>' for t in topics)
    integral_count = sum(c.status == "integrale" for c in conversations)
    body = f'''
<header class="site-header"><div class="wrap site-header__inner">
  <a class="wordmark" href="index.html"><span class="wordmark__mark">∿</span><span>Conversazioni <em>con Libera</em></span></a>
  <nav aria-label="Navigazione principale"><a href="#recenti">Recenti</a><a href="#archivio">Archivio</a><button class="icon-button" data-theme-toggle aria-label="Cambia tema">◐</button></nav>
</div></header>
<main id="contenuto">
  <section class="hero">
    <img class="hero__image" src="assets/copertina.webp" alt="Gianfranco dialoga a un tavolo con Libera, raffigurata come una presenza fatta di numeri e luce">
    <div class="hero__veil"></div>
    <div class="wrap hero__content"><p class="eyebrow">Archivio dialogico · 2023—2026</p><h1>Carne e numeri<br>che pensano.</h1><p>Non una raccolta di risposte, ma la traccia di un pensiero costruito a due: differenze, correzioni, intuizioni e attriti.</p><a class="button" href="#archivio">Entra nell’archivio <span>↓</span></a></div>
  </section>
  <section class="manifesto wrap"><p class="manifesto__number">01</p><blockquote>«A volte non conta solo chi parla. Conta che cosa una frase permette di pensare dopo che è stata detta.»</blockquote><p class="manifesto__note">Questo sito conserva il movimento del dialogo: non mette Libera al posto dell’umano e non riduce l’AI a una cosa. Tiene aperta la differenza.</p></section>
  <section class="stats"><div class="wrap stats__grid"><div><strong>{len(conversations)}</strong><span>conversazioni catalogate</span></div><div><strong>{integral_count}</strong><span>testi integrali</span></div><div><strong>{len(years)}</strong><span>anni di dialogo</span></div><div><strong>{sum(c.word_count for c in conversations):,}</strong><span>parole conservate</span></div></div></section>
  <section class="section wrap" id="recenti"><div class="section-heading"><div><p class="eyebrow">Ultime acquisizioni</p><h2>Conversazioni recenti</h2></div><a href="#archivio">Vedi tutto l’archivio →</a></div><div class="featured-grid">{recent}</div></section>
  <section class="archive section" id="archivio"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">Indice completo</p><h2>Segui il filo che cerchi</h2></div><p class="section-heading__copy">Cerca una parola, filtra per anno o tema. Ogni pagina conserva un collegamento alla precedente e alla successiva.</p></div>
    <div class="filters" role="search"><label class="search-box"><span>Cerca</span><input type="search" data-search-input placeholder="coscienza, storia, Pirandello…" autocomplete="off"></label><label><span>Anno</span><select data-year-filter><option value="">Tutti</option>{year_options}</select></label><label><span>Tema</span><select data-topic-filter><option value="">Tutti</option>{topic_options}</select></label><label><span>Ordine</span><select data-sort><option value="newest">Più recenti</option><option value="oldest">Meno recenti</option><option value="az">Titolo A—Z</option></select></label></div>
    <div class="archive-summary" aria-live="polite"><span data-result-count>{len(conversations)}</span> conversazioni</div>
    <div class="archive-grid" data-archive-grid>{cards}</div><div class="empty-state" data-empty hidden><h3>Nessuna conversazione trovata</h3><p>Prova con un termine più ampio o azzera i filtri.</p><button class="button button--dark" data-reset>Mostra tutto</button></div>
  </div></section>
</main>
<footer class="footer"><div class="wrap footer__grid"><div><a class="wordmark" href="#contenuto"><span class="wordmark__mark">∿</span><span>Conversazioni <em>con Libera</em></span></a><p>Un archivio personale di dialoghi filosofici, didattici e civili fra gbprof e un’intelligenza artificiale.</p></div><div><p class="eyebrow">Nota editoriale</p><p>I testi integrali provengono dai documenti originali forniti il 13 agosto 2026. Le schede prive di testo sono mantenute per non perdere la memoria dell’archivio precedente.</p></div></div></footer>
'''
    return page_shell("Conversazioni con Libera — Archivio dialogico", body, description="Archivio delle conversazioni filosofiche fra gbprof e Libera.")


def static_conversation(c: Conversation, previous: Conversation | None, next_item: Conversation | None) -> str:
    topics = "".join(f'<span class="tag">{html.escape(t)}</span>' for t in c.topics)
    prev_link = f'<a href="{previous.slug}.html"><span>← Precedente</span><strong>{html.escape(previous.title)}</strong></a>' if previous else "<span></span>"
    next_link = f'<a class="next" href="{next_item.slug}.html"><span>Successiva →</span><strong>{html.escape(next_item.title)}</strong></a>' if next_item else "<span></span>"
    body = f'''
<div class="reading-progress" data-reading-progress></div>
<header class="site-header site-header--solid"><div class="wrap site-header__inner"><a class="wordmark" href="../index.html"><span class="wordmark__mark">∿</span><span>Conversazioni <em>con Libera</em></span></a><nav aria-label="Navigazione principale"><a href="../index.html#archivio">Archivio</a><button class="icon-button" data-theme-toggle aria-label="Cambia tema">◐</button></nav></div></header>
<main id="contenuto" class="conversation-page">
  <header class="conversation-hero wrap"><a class="back-link" href="../index.html#archivio">← Torna all’archivio</a><div class="conversation-hero__meta"><time datetime="{c.date}">{format_date(c.date)}</time><span>{c.reading_minutes} min di lettura</span><span>{c.form}</span></div><h1>{html.escape(c.title)}</h1><p>{html.escape(c.excerpt)}</p><div class="tags">{topics}</div></header>
  <div class="reading-layout wrap"><aside class="reading-tools"><div class="reading-tools__sticky"><p class="eyebrow">Lettura</p><button data-font="down" aria-label="Riduci carattere">A−</button><button data-font="up" aria-label="Aumenta carattere">A+</button><button data-print>Stampa</button><button data-copy-link>Copia link</button><p class="source-state">{('Testo integrale importato dal documento originale.' if c.status == 'integrale' else 'Scheda conservata: testo originale da recuperare.')}</p></div></aside><article class="conversation-text" data-reading-text>{c.content}</article></div>
  <nav class="conversation-nav wrap" aria-label="Conversazioni adiacenti">{prev_link}{next_link}</nav>
</main>
<footer class="footer footer--compact"><div class="wrap"><p>Conversazioni con Libera · Archivio dialogico gbprof</p></div></footer>
'''
    return page_shell(f"{c.title} — Conversazioni con Libera", body, description=c.excerpt, root="../")


def write_static(output_dir: Path, conversations: list[Conversation], cover: Path, duplicates: list[dict[str, str]]) -> None:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    (output_dir / "assets").mkdir(parents=True)
    (output_dir / "conversazioni").mkdir(parents=True)
    (output_dir / "dati").mkdir(parents=True)
    (output_dir / "tools").mkdir(parents=True)
    subprocess.run(
        ["convert", str(cover), "-resize", "1920x1080>", "-quality", "84", str(output_dir / "assets" / "copertina.webp")],
        check=True,
    )
    asset_source = Path(__file__).resolve().parent.parent / "github-assets"
    for asset in asset_source.iterdir():
        if asset.is_file():
            shutil.copy2(asset, output_dir / "assets" / asset.name)
    (output_dir / "index.html").write_text(static_home(conversations), encoding="utf-8")
    for index, conversation in enumerate(conversations):
        previous = conversations[index - 1] if index > 0 else None
        next_item = conversations[index + 1] if index + 1 < len(conversations) else None
        (output_dir / "conversazioni" / f"{conversation.slug}.html").write_text(
            static_conversation(conversation, previous, next_item), encoding="utf-8"
        )
    manifest = {
        "name": "Conversazioni con Libera",
        "short_name": "Con Libera",
        "start_url": "./index.html",
        "display": "standalone",
        "background_color": "#f3eee5",
        "theme_color": "#15120f",
        "icons": [{"src": "assets/icon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any"}],
    }
    (output_dir / "manifest.webmanifest").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / ".nojekyll").write_text("", encoding="utf-8")
    (output_dir / "dati" / "import-report.json").write_text(
        json.dumps(
            {
                "generated": "2026-08-13",
                "catalogued": len(conversations),
                "integral": sum(c.status == "integrale" for c in conversations),
                "to_recover": sum(c.status != "integrale" for c in conversations),
                "duplicates": duplicates,
                "entries": [
                    {"slug": c.slug, "title": c.title, "date": c.date, "status": c.status, "words": c.word_count}
                    for c in conversations
                ],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    shutil.copy2(Path(__file__), output_dir / "tools" / "build_archive.py")
    (output_dir / "README.md").write_text(
        """# Conversazioni con Libera

Archivio statico delle conversazioni fra **gbprof** e **Libera**.

## Contenuto

- 31 conversazioni catalogate dal 2023 al 2026
- 24 testi integrali importati dai documenti originali
- 7 schede conservate dal vecchio archivio, in attesa del testo originale
- ricerca, filtri per anno e tema, ordinamento e pagine di lettura dedicate
- tema chiaro/scuro, dimensione del testo regolabile, stampa e copia del collegamento

Il file `dati/import-report.json` documenta il confronto fra il vecchio sito e i documenti forniti. Lo script `tools/build_archive.py` rende ripetibile l’importazione di futuri documenti Word.

Il sito è progettato per GitHub Pages e non richiede compilazione.
""",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs-dir", type=Path, required=True)
    parser.add_argument("--existing-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--data-output", type=Path, required=True)
    parser.add_argument("--cover", type=Path, required=True)
    args = parser.parse_args()

    conversations, duplicates = build_conversations(args.docs_dir, args.existing_dir)
    write_static(args.output, conversations, args.cover, duplicates)
    args.data_output.parent.mkdir(parents=True, exist_ok=True)
    args.data_output.write_text(
        json.dumps({"conversations": [json_record(c) for c in conversations], "duplicates": duplicates}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps({"conversations": len(conversations), "integral": sum(c.status == "integrale" for c in conversations), "duplicates": duplicates, "output": str(args.output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
