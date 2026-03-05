# SEO Kit

**Make your JS-rendered site visible to Google and AI search engines.**

Most sites built with Lovable, Bolt, Vercel, or React are invisible to search engines because the content is rendered client-side with JavaScript. Google sees a blank page. AI crawlers (ChatGPT, Perplexity, Claude) see nothing.

This module fixes that in one session.

## What It Does

- Deploys a **Cloudflare Worker** that serves pre-rendered HTML to search bots via Prerender.io
- Generates **sitemap.xml**, **robots.txt**, and **llms.txt** served directly by the Worker
- Injects **JSON-LD schema markup** (Organization, LocalBusiness, Person, FAQ, Breadcrumbs) into every page
- Walks you through **Google Search Console** verification and sitemap submission
- Disables Cloudflare's default **AI crawler blocking** so ChatGPT, Perplexity, and Claude can index your site

## What You Need

- A live website on Lovable, Vercel, Bolt, or any JS-rendered platform
- A custom domain you own
- A free Cloudflare account
- A free Prerender.io account (250 renders/month free)
- ~45 minutes

## How to Install

```
/install module-installs/seo-kit
```

Claude will ask for your business details, generate everything, and walk you through deployment step by step.

## What You Get

| File | Purpose |
|------|---------|
| `worker.js` | Cloudflare Worker — prerender, SEO files, schema injection |
| `checklist.md` | Prioritised implementation checklist |
| `setup-guide.md` | Step-by-step deployment instructions |

## Proven Pattern

This exact setup is running in production on live client sites. The Worker handles prerendering, static SEO files, and schema markup injection — all without touching the hosting platform.
