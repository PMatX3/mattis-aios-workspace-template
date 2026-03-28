# [Your Company] Design System

> Portable, agent-readable design system for all creative tools.
> Used by: HTML/CSS outputs, lead magnets, PDFs, social graphics, video tools.
> Keep this file at the project root so every tool finds it automatically.
>
> **Instructions:** Replace all placeholder values below with your brand specifics.
> Delete these instruction comments once you have filled in your details.

## Brand Identity

<!-- Replace with your company name, tagline, and brand personality -->
**Company:** [Your Company]
**Tagline:** [Your one-line value proposition]
**Personality:** [3-4 adjectives describing your brand voice, e.g. "Professional, direct, trustworthy"]
**Logo:** `reference/brand/logo.png`

## Color Palette

<!-- Replace hex values with your brand colours. Keep the token names for consistency. -->

| Token | Hex | Usage |
|-------|-----|-------|
| `--primary` | #2563EB | Brand primary. Headers, table headers, accent borders, CTA buttons |
| `--primary-light` | #93C5FD | Lighter variant. Blockquote borders, secondary accents, hover states |
| `--bg` | #FFFFFF | Page/slide background |
| `--bg-alt` | #F8FAFC | Card surfaces, alternating rows, blockquote backgrounds |
| `--bg-dark` | #1A1A1A | Dark mode background, video backgrounds |
| `--ink` | #1A1A1A | Primary text |
| `--ink-muted` | #444444 | Secondary text, captions |
| `--ink-light` | #FFFFFF | Text on dark backgrounds |
| `--border` | #D0D0D0 | Default borders |
| `--border-light` | #CCCCCC | Horizontal rules, subtle dividers |
| `--green` | #22C55E | Success, positive metrics, "live" status |
| `--red` | #EF4444 | Error, negative metrics, "broken" status |
| `--amber` | #F59E0B | Warning, "at risk" status |

### Dark mode (video, social content)

For videos and social graphics, invert the palette:
- Background: `--bg-dark` (#1A1A1A) or near-black (#0A0B12)
- Text: `--ink-light` (#FFFFFF)
- Accent: `--primary-light` or `--primary`
- Avoid pure black (#000000). Use #1A1A1A or #0A0B12 for depth.

## Typography

<!-- Replace with your preferred fonts. Inter and JetBrains Mono are good defaults. -->

| Role | Family | Weight | Fallback |
|------|--------|--------|----------|
| Display / Headings | Inter | 700 (Bold) | Arial, sans-serif |
| Body | Inter | 400 (Regular) | Arial, sans-serif |
| Mono / Code | JetBrains Mono | 400 | Courier New, monospace |
| PDF / Documents | Calibri | 400/700 | Arial, sans-serif |

**Google Fonts CDN:**
```
https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap
```

### Type Scale

| Token | Size | Usage |
|-------|------|-------|
| `--text-xs` | 10px | Timestamps, fine print |
| `--text-sm` | 12px | Captions, labels |
| `--text-base` | 14px | Body text |
| `--text-md` | 16px | Large body, card text |
| `--text-lg` | 20px | Section headings |
| `--text-xl` | 24px | Page headings |
| `--text-2xl` | 32px | Hero headings |
| `--text-3xl` | 48px | Video title cards |
| `--text-4xl` | 64px | Impact numbers (stats, scores) |

## Spacing

Base unit: 4px. Scale: 4, 8, 12, 16, 20, 24, 32, 48, 64.

Use multiples of 8px for major layout spacing. Use 4px for tight internal padding.

## Video

<!-- Remove this section if you don't produce video content -->

### Defaults
- **Aspect ratio:** 16:9 (1920x1080) for LinkedIn/YouTube. 9:16 (1080x1920) for Reels/Shorts.
- **Duration:** 15-30 seconds for social clips. 45-90 seconds for explainers.
- **FPS:** 30
- **Background:** #1A1A1A with subtle grain or gradient (never pure black)
- **Text colour:** #FFFFFF for headlines, use `--primary-light` for labels/accents
- **Animation style:** Clean and snappy. Use spring easing for text entrances, ease-out for exits. No bounce.

### Text animation patterns
- Headlines: Fade up + slight scale (0.95 to 1.0), 0.4s spring
- Stats/numbers: Count up from 0 to final value, 0.8s
- Labels: Fade in, 0.3s ease
- Scene transitions: Cross-fade or slide-left, 0.5s

## Graphics (Social / Carousels)

- Clean, minimal layouts. White space is a feature, not a bug.
- One idea per slide. No visual clutter.
- Max 3 visual elements per graphic.
- Text: large, legible at mobile size (minimum 16px equivalent)
- Brand mark (logo or company wordmark) in bottom corner, small

## Documents (PDFs / Proposals)

<!-- Update font and colour references to match your palette above -->
- Use Calibri as primary font (or your chosen PDF font)
- Table headers: `--primary` background, white text
- Blockquotes: left border in `--primary-light`, light background
- Code blocks: left border in `--primary`, light grey background
- Clean, professional aesthetic. Readable, not "designed."

## Design Rules

### DO
- Use the colour palette consistently across all outputs
- Prioritise readability and clarity over visual flair
- Keep layouts clean and spacious
- Use numbers and specifics (not vague claims)
- Let white space do the work

### DON'T
- Use gradients (except subtle dark-to-darker in video backgrounds)
- Use rounded corners larger than 8px
- Use drop shadows heavier than `0 2px 8px rgba(0,0,0,0.1)`
- Use emoji in professional outputs
- Use more than 2 font weights on a single screen/slide
- Mix warm and cool accent colours

## CTA Defaults

<!-- Replace with your own URLs and preferred CTA language -->

| Context | CTA Text | URL |
|---------|----------|-----|
| LinkedIn post | "Comment [KEYWORD] and I'll send you..." | n/a |
| Video end card | "[yourwebsite.com]" | https://yourwebsite.com |
| Lead magnet | "Book a free discovery call" | https://yourwebsite.com/book |
| Email | you@yourcompany.com | mailto:you@yourcompany.com |
