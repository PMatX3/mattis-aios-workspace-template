# SEO/GEO Implementation Checklist — __DOMAIN__

> Generated for __BUSINESS_NAME__. Work through priorities in order.

## Priority 1: CRITICAL — Fix JS Rendering

Without this, Google and AI crawlers see an empty page.

- [ ] Sign up for Prerender.io and get API token
- [ ] Move DNS to Cloudflare (change nameservers at registrar)
- [ ] Remove custom domain from hosting platform (Lovable/Vercel/etc.)
- [ ] Create Cloudflare Worker (`lovable-prerender`)
- [ ] Add secrets: `PRERENDER_TOKEN` + `LOVABLE_UPSTREAM`
- [ ] Paste and deploy worker code
- [ ] Attach custom domains to Worker (root + www)
- [ ] Set Cloudflare SSL/TLS to Full (strict)
- [ ] Test: `curl -A "googlebot" https://__DOMAIN__ | head -50` — should show full HTML
- [ ] Test: visit `https://__DOMAIN__` in browser — should load normally

## Priority 2: HIGH — Search Console + Sitemap

- [ ] Verify site in Google Search Console (DNS TXT record via Cloudflare)
- [ ] Verify robots.txt is clean: `curl https://__DOMAIN__/robots.txt`
- [ ] Disable Cloudflare managed robots.txt (Security → Bots → AI Crawl Control)
- [ ] Allow all AI crawlers in Cloudflare AI Crawl Control
- [ ] Submit sitemap: `https://__DOMAIN__/sitemap.xml`
- [ ] Verify llms.txt: `curl https://__DOMAIN__/llms.txt`
- [ ] Set up Bing Webmaster Tools (import from Search Console)

## Priority 3: HIGH — Schema Markup

- [ ] Verify schema injection: `curl -s https://__DOMAIN__/ | grep -c 'ld+json'`
- [ ] Validate with Google Rich Results Test: https://search.google.com/test/rich-results
- [ ] Test each page type (homepage, services, about, team, contact)

## Priority 4: MEDIUM — Google My Business

- [ ] Create Google Business Profile
- [ ] Set categories, address, phone, email, website, hours
- [ ] Upload logo + cover photo + team photos (min 5 images)
- [ ] Add all services with descriptions
- [ ] Complete verification (postcard/phone/video)
- [ ] Post first Google Business update
- [ ] Begin review collection

## Priority 5: MEDIUM — Content Pages

- [ ] Deploy service pages (content provided in kit)
- [ ] Deploy team bio pages
- [ ] Set up blog section
- [ ] Publish initial blog posts
- [ ] Update Worker sitemap with new URLs
- [ ] Request indexing for each new page in Search Console

## Priority 6: LOW-MEDIUM — Backlink Cleanup

- [ ] Export backlinks from Search Console
- [ ] Identify toxic/spammy links
- [ ] Send removal requests
- [ ] Create and submit Google Disavow file

## Priority 7: ONGOING — Monitoring

### Weekly
- [ ] Check Search Console for crawl errors
- [ ] Check Prerender.io dashboard for cache health

### Monthly
- [ ] Review Search Console Performance (clicks, impressions, CTR)
- [ ] Publish 2 blog posts
- [ ] Collect Google reviews
- [ ] Test AI search citations (search for business in ChatGPT/Perplexity)

### Quarterly
- [ ] Full technical SEO audit (Core Web Vitals, mobile, schema validation)
- [ ] Update llms.txt with any new services
- [ ] Refresh underperforming content

## Expected Timeline

| Timeframe | Expected Outcome |
|-----------|-----------------|
| Week 1 | Site crawlable, sitemap submitted, Search Console active |
| Week 2-3 | Pages indexed, schema live |
| Month 2 | GMB active, blog publishing started |
| Month 3 | 10+ indexed pages, AI search citations appearing |
| Month 6 | Meaningful organic traffic, GEO score improved |
