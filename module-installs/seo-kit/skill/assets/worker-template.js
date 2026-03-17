// =============================================================================
// __BUSINESS_NAME__ — Cloudflare Worker
// Handles: Prerender for bots, static SEO files, schema injection, upstream proxy
// Deploy to: Cloudflare Workers
// =============================================================================

// --- Static SEO Files (served directly by the worker) ---

const SITEMAP_XML = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <!-- __SITEMAP_ENTRIES__: Generate one <url> block per route -->
  <!-- Example:
  <url>
    <loc>https://__DOMAIN__/</loc>
    <lastmod>__DATE__</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  -->
</urlset>`;

const ROBOTS_TXT = `# __BUSINESS_NAME__ — robots.txt

User-agent: *
Allow: /

Sitemap: https://__DOMAIN__/sitemap.xml

# AI Crawler Info — see https://__DOMAIN__/llms.txt`;

const LLMS_TXT = `# __BUSINESS_NAME__

> __BUSINESS_DESCRIPTION__

## Services
<!-- __SERVICES__: One line per service, format: "- Name: Description (price if applicable)" -->

## Key Facts
<!-- __KEY_FACTS__: 3-5 bullet points about the business -->

## Contact
- Website: https://__DOMAIN__
- Email: __EMAIL__
- Phone: __PHONE__
- Book a call: https://__DOMAIN__/__CONTACT_PATH__`;

const STATIC_FILES = {
  "/sitemap.xml": { body: SITEMAP_XML, type: "application/xml" },
  "/robots.txt": { body: ROBOTS_TXT, type: "text/plain" },
  "/llms.txt": { body: LLMS_TXT, type: "text/plain" },
};

// --- Schema Markup (JSON-LD) ---
// Replace these with actual business data. See references/schema-patterns.md.

const SCHEMA_ORG = {
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://__DOMAIN__/#organization",
  "name": "__BUSINESS_NAME__",
  "url": "https://__DOMAIN__",
  "description": "__BUSINESS_DESCRIPTION__",
  "founder": {
    "@type": "Person",
    "name": "__FOUNDER_NAME__",
    "jobTitle": "__FOUNDER_TITLE__"
  },
  "foundingDate": "__FOUNDING_YEAR__",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "__STREET_ADDRESS__",
    "addressLocality": "__CITY__",
    "addressRegion": "__REGION__",
    "postalCode": "__POSTCODE__",
    "addressCountry": "__COUNTRY_CODE__"
  },
  "email": "__EMAIL__",
  "telephone": "__PHONE_E164__",
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "__PHONE_E164__",
    "contactType": "customer service",
    "email": "__EMAIL__",
    "availableLanguage": "English"
  },
  "sameAs": [/* "__LINKEDIN_URL__", "__TWITTER_URL__" */]
};

const SCHEMA_LOCAL = {
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "@id": "https://__DOMAIN__/#localbusiness",
  "name": "__BUSINESS_NAME__",
  "url": "https://__DOMAIN__",
  "description": "__BUSINESS_DESCRIPTION__",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "__STREET_ADDRESS__",
    "addressLocality": "__CITY__",
    "addressRegion": "__REGION__",
    "postalCode": "__POSTCODE__",
    "addressCountry": "__COUNTRY_CODE__"
  },
  "geo": { "@type": "GeoCoordinates", "latitude": "__LAT__", "longitude": "__LNG__" },
  "telephone": "__PHONE_E164__",
  "email": "__EMAIL__",
  "priceRange": "__PRICE_RANGE__",
  "openingHoursSpecification": [{
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
    "opens": "__OPENS__",
    "closes": "__CLOSES__"
  }],
  "areaServed": [
    /* { "@type": "Country", "name": "__COUNTRY__" } */
  ],
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "__CATALOG_NAME__",
    "itemListElement": [
      /* { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "__SERVICE__", "description": "__DESC__" }} */
    ]
  }
};

// __PERSON_SCHEMAS__: Add one const per team member
// const SCHEMA_PERSON_NAME = { "@context": "https://schema.org", "@type": "Person", ... };

// __FAQ_SCHEMAS__: Add one const per page with FAQs
// const SCHEMA_FAQ_PAGENAME = { "@context": "https://schema.org", "@type": "FAQPage", ... };

// Breadcrumb helper
function breadcrumb(items) {
  return {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": items.map((item, i) => ({
      "@type": "ListItem",
      "position": i + 1,
      "name": item.name,
      "item": item.url
    }))
  };
}

// Map paths to their schema arrays
// __SCHEMA_ROUTING__: Customise this for the site's actual routes
function getSchemasForPath(pathname) {
  const path = pathname.toLowerCase().replace(/\/$/, "") || "/";
  const home = { name: "Home", url: "https://__DOMAIN__" };

  switch (path) {
    case "/":
      return [SCHEMA_ORG, SCHEMA_LOCAL, breadcrumb([home])];
    // Add cases for each route — see references/schema-patterns.md for the mapping
    default:
      return [];
  }
}

function buildSchemaScripts(pathname) {
  const schemas = getSchemasForPath(pathname);
  if (schemas.length === 0) return "";
  return schemas
    .map(s => `<script type="application/ld+json">${JSON.stringify(s)}</script>`)
    .join("\n");
}

class SchemaInjector {
  constructor(pathname) {
    this.schemaHtml = buildSchemaScripts(pathname);
  }
  element(element) {
    if (this.schemaHtml) {
      element.prepend(this.schemaHtml, { html: true });
    }
  }
}

// --- Bot Detection ---

const BOT_AGENTS = [
  "googlebot","yahoo! slurp","bingbot","yandex","baiduspider","facebookexternalhit",
  "twitterbot","rogerbot","linkedinbot","embedly","quora link preview","showyoubot",
  "outbrain","pinterest/0.","developers.google.com/+/web/snippet","slackbot","vkshare",
  "w3c_validator","redditbot","applebot","whatsapp","flipboard","tumblr","bitlybot",
  "skypeuripreview","nuzzel","discordbot","google page speed","qwantify","pinterestbot",
  "bitrix link preview","xing-contenttabreceiver","chrome-lighthouse","telegrambot",
  "oai-searchbot","chatgpt","gptbot","claudebot","amazonbot","perplexity",
  "google-inspectiontool","integration-test",
];

const IGNORE_EXTENSIONS = [
  ".js",".css",".xml",".less",".png",".jpg",".jpeg",".gif",".pdf",".doc",".txt",".ico",
  ".rss",".zip",".mp3",".rar",".exe",".wmv",".avi",".ppt",".mpg",".mpeg",".tif",".wav",
  ".mov",".psd",".ai",".xls",".mp4",".m4a",".swf",".dat",".dmg",".iso",".flv",".m4v",
  ".torrent",".woff",".ttf",".svg",".webmanifest",
];

// --- Helper ---

function isRedirect(status) {
  return status === 301 || status === 302 || status === 303 || status === 307 || status === 308;
}

// --- Entry Point ---

export default {
  async fetch(request, env) {
    try {
      if (!env?.LOVABLE_UPSTREAM) {
        return new Response("Missing LOVABLE_UPSTREAM variable", { status: 500 });
      }
      if (!env?.PRERENDER_TOKEN) {
        return new Response("Missing PRERENDER_TOKEN secret", { status: 500 });
      }
      return await handleRequest(request, env);
    } catch (err) {
      return new Response(err?.stack || String(err), { status: 500 });
    }
  },
};                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           