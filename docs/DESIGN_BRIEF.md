# Aegis design brief

The visual design exists to make a regulatory tool feel trustworthy, not to look like a typical AI app. The reference points are official legal and government documents, not consumer software.

## Principles

Institutional over playful. The user is an SME owner or compliance officer making decisions with legal weight. The interface should read like a serious reference document, calm, precise, text-led.

Readable over decorative. Generous line height, a single narrow column (820px) so lines do not run too wide, clear hierarchy through type rather than colour or boxes.

Citations are first-class. Every page reference and Article number is set in a monospace face so it reads as a verifiable reference, not body prose.

## Type

- Headings: Lora (serif). Chosen for a documentary, legal-text feel.
- Body: Source Sans 3. A clean humanist sans that stays readable at length.
- Citations and code: IBM Plex Mono.

All three are Google Fonts, chosen deliberately to avoid the Inter/Roboto/system-sans default that signals "another LLM wrapper."

## Colour

- Background: #FBFAF7, a warm off-white, paper rather than screen-white.
- Text: #1A1A1A, near-black for contrast without harshness.
- Accent: #1B3A5C, a deep institutional blue for headings and the active tab.
- Border: #D8D4CC, a soft warm grey.

Risk-tier colours are muted and legal rather than traffic-light bright:
- prohibited: #8B2635 (deep red)
- high: #9A6A1E (ochre)
- limited: #3A6B8C (slate blue)
- minimal: #2D5A3D (forest green)

Light theme only for now. A dark mode is a possible Week 9 stretch item.

## Layout

Single centred column, 820px. Four tabs: Inventory, Classification, Obligations, Ask. A disclaimer banner sits under the header on every screen. A privacy warning sits next to every input. A footer states the tool is independent and unaffiliated with any authority.