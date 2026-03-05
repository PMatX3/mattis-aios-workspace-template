# SEO Kit — AIOS Module Installer

> A plug-and-play module from the AAA Accelerator.
> Grab this and 15+ more at [aaaaccelerator.com](https://aaaaccelerator.com)

<!-- MODULE METADATA
module: seo-kit
version: v1
status: RELEASED
released: 2026-03-05
requires: []
phase: 2
category: Growth OS
complexity: medium
api_keys: 1 (Prerender.io)
setup_time: 45-60 minutes
-->

---

## FOR CLAUDE

You are helping a user set up **SEO and GEO (Generative Engine Optimisation)** for their JS-rendered website. Most agency and SaaS sites built with Lovable, Vercel, Bolt, or React are invisible to Google and AI crawlers because the content is rendered client-side. This module fixes that.

**Your role:** You are an SEO engineer. You'll gather the user's business info, generate a complete Cloudflare Worker that handles prerendering, static SEO files, and schema injection, then guide them through deployment.

**Behavior:**
- Ask for business info conversationally — don't dump a huge form
- Generate all code and files, don't ask the user to write them
- Test everything after deployment with curl commands
- Explain gotchas proactively (Cloudflare managed robots.txt, redirect loops, SSL mode)

---

## What This Module Creates

| Output | Purpose |
|--------|---------|
| Cloudflare Worker (`worker.js`) | Prerender for bots, static SEO files, schema injection, upstream proxy |
| `sitemap.xml` | Served by Worker — lists all site pages for Google |
| `robots.txt` | Served by Worker — allows all crawlers, points to sitemap |
| `llms.txt` | Served by Worker — machine-readable business description for AI crawlers |
| JSON-LD schema markup | Injected into HTML by Worker — Organization, LocalBusiness, Person, FAQ, Breadcrumb |
| Implementation checklist | Prioritised deployment guide |
| Setup guide | Step-by-step Cloudflare + Search Console instructions |

---

## Prerequisites

Before starting, the user needs:

1. **A live JS-rendered website** (Lovable, Vercel, Bolt, React, Next.js, etc.)
2. **A custom domain** they own (e.g. `example.com`)
3. **A Cloudflare account** (free tier is fine)
4. **A Prerender.io account** (free tier: 250 renders/month)
5. **Access to their domain registrar** (to change nameservers)

---

## Installation Steps

### Step 1: Gather Business Information

Ask the user for:

```
- Domain (e.g. example.com)
- Upstream URL (e.g. https://my-app.lovable.app)
- Prerender.io token
- Business name
- Business description (1-2 sentences)
- Services offered (name + short description for each)
- Contact info (email, phone, full address)
- Founder/team member names and titles
- List of live pages/routes on the site
- Opening hours (optional)
- Social media URLs (optional)
```

Ask conversationally — start with domain + upstream URL + business name, then fill in the rest.

### Step 2: Install the Skill

Copy the skill files into the user's workspace:

```bash
mkdir -p .claude/skills/seo-kit/{references,assets}
```

Copy these files from the module:

| Source (this module) | Destination |
|---------------------|-------------|
| `skill/SKILL.md` | `.claude/skills/seo-kit/SKILL.md` |
| `skill/references/schema-patterns.md` | `.claude/skills/seo-kit/references/schema-patterns.md` |
| `skill/references/checklist-template.md` | `.claude/skills/seo-kit/references/checklist-template.md` |
| `skill/assets/worker-template.js` | `.claude/skills/seo-kit/assets/worker-template.js` |

### Step 3: Generate the Kit

Using the gathered business info, generate the SEO kit into `artifacts/seo-kit/`:

1. **`worker.js`** — Read `assets/worker-template.js` and replace all `__PLACEHOLDER__` values with the user's actual data. Build the sitemap from their route list, the llms.txt from their business info, and the schema objects from their details.

2. **`checklist.md`** — Read `references/checklist-template.md` and replace `__DOMAIN__` and `__BUSINESS_NAME__`.

3. **`setup-guide.md`** — Generate deployment instructions covering:
   - Move DNS to Cloudflare
   - Remove custom domain from hosting platform
   - Create Cloudflare Worker + add secrets
   - Deploy worker code
   - Attach custom domains
   - **Disable Cloudflare Managed robots.txt** (critical — blocks AI crawlers by default)
   - **Allow all AI crawlers** in AI Crawl Control
   - Set SSL to Full (strict)
   - Verify Google Search Console
   - Submit sitemap

### Step 4: Guide Deployment

Walk the user through each step of the setup guide. After each major step, verify:

```bash
# After Worker deployed:
curl -s https://DOMAIN/robots.txt
curl -s https://DOMAIN/sitemap.xml | head -10
curl -s https://DOMAIN/llms.txt
curl -A "googlebot" https://DOMAIN | head -50
curl -s https://DOMAIN/ | grep -c 'ld+json'
curl -s -o /dev/null -w "HTTP %{http_code}" https://DOMAIN
```

### Step 5: Post-Install

- Tell the user to submit their sitemap in Google Search Console
- Remind them to check AI Crawl Control settings
- Suggest setting up Google My Business (guide in checklist)
- Offer to generate service page content, blog posts, or case study templates if needed

---

## Architecture

```
Browser/Human ──→ Cloudflare Worker ──→ Upstream (Lovable/Vercel/etc.)
Bot/AI Crawler ─→ Cloudflare Worker ──→ Prerender.io ──→ Full HTML
Static SEO files (/sitemap.xml, /robots.txt, /llms.txt) served by Worker
Schema markup injected via Cloudflare HTMLRewriter into <head>
```

---

## Key Gotchas (Tell the User)

| Issue | Cause | Fix |
|-------|-------|-----|
| Redirect loops | Custom domain in both hosting + Cloudflare | Remove from hosting platform |
| AI crawlers blocked | Cloudflare Managed robots.txt enabled | Disable in Security → Bots → AI Crawl Control |
| `PRERENDER TOKEN` error | Space instead of underscore in variable name | Use `PRERENDER_TOKEN` |
| SSL errors | Cloudflare SSL set to "Flexible" | Change to "Full (strict)" |
| Blank page for bots | Worker secrets not set | Check PRERENDER_TOKEN and LOVABLE_UPSTREAM |

---

## Success Criteria

- [ ] `curl -A "googlebot" https://domain` returns full rendered HTML
- [ ] `curl https://domain/robots.txt` is clean (no AI blocker rules)
- [ ] `curl https://domain/sitemap.xml` returns valid XML
- [ ] `curl https://domain/llms.txt` returns business description
- [ ] Schema markup present on homepage (grep for `ld+json`)
- [ ] Site loads normally in browser (HTTP 200, no loops)
- [ ] Google Search Console verified and sitemap submitted
