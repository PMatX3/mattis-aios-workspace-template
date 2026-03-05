# Schema Markup Patterns (JSON-LD)

Reference for generating schema.org JSON-LD objects. All schemas are injected as `<script type="application/ld+json">` in `<head>`.

## Organization

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://__DOMAIN__/#organization",
  "name": "__BUSINESS_NAME__",
  "url": "https://__DOMAIN__",
  "description": "__DESCRIPTION__",
  "founder": {
    "@type": "Person",
    "name": "__FOUNDER_NAME__",
    "jobTitle": "__FOUNDER_TITLE__"
  },
  "foundingDate": "__YEAR__",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "__STREET__",
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
  "sameAs": ["__LINKEDIN_URL__", "__TWITTER_URL__"]
}
```

## LocalBusiness / ProfessionalService

```json
{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "@id": "https://__DOMAIN__/#localbusiness",
  "name": "__BUSINESS_NAME__",
  "url": "https://__DOMAIN__",
  "description": "__DESCRIPTION__",
  "address": { "...same as Organization..." },
  "geo": { "@type": "GeoCoordinates", "latitude": __LAT__, "longitude": __LNG__ },
  "telephone": "__PHONE_E164__",
  "email": "__EMAIL__",
  "priceRange": "__PRICE_RANGE__",
  "openingHoursSpecification": [{
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
    "opens": "__OPEN__",
    "closes": "__CLOSE__"
  }],
  "areaServed": [
    { "@type": "Country", "name": "__COUNTRY__" }
  ],
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "__CATALOG_NAME__",
    "itemListElement": [
      {
        "@type": "Offer",
        "itemOffered": {
          "@type": "Service",
          "name": "__SERVICE_NAME__",
          "description": "__SERVICE_DESC__"
        }
      }
    ]
  }
}
```

## Person

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "@id": "https://__DOMAIN__/__TEAM_PATH__#__SLUG__",
  "name": "__PERSON_NAME__",
  "jobTitle": "__JOB_TITLE__",
  "worksFor": {
    "@type": "Organization",
    "@id": "https://__DOMAIN__/#organization",
    "name": "__BUSINESS_NAME__"
  },
  "url": "https://__DOMAIN__/__TEAM_PATH__",
  "knowsAbout": ["__SKILL_1__", "__SKILL_2__"],
  "sameAs": ["__LINKEDIN_URL__"]
}
```

## FAQPage

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "__QUESTION__",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "__ANSWER__ (under 300 words for rich result eligibility)"
      }
    }
  ]
}
```

Generate 3-5 FAQs per page. Source from service descriptions, pricing, process, and common objections.

## BreadcrumbList

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://__DOMAIN__" },
    { "@type": "ListItem", "position": 2, "name": "__PAGE_NAME__", "item": "https://__DOMAIN__/__PATH__" }
  ]
}
```

Every page should have breadcrumbs. Depth matches the URL hierarchy.

## Route-to-Schema Mapping

| Route Pattern | Schemas |
|---------------|---------|
| `/` (homepage) | Organization + LocalBusiness + Breadcrumb |
| `/about` | Organization + FAQ + Breadcrumb |
| `/services` | FAQ (service questions) + Breadcrumb |
| `/services/*` | Breadcrumb (Services > Specific Service) |
| `/team` or `/our-team` | Person (each team member) + Breadcrumb |
| `/team/*` | Person (individual) + Breadcrumb |
| `/contact` | Breadcrumb |
| `/blog` | Breadcrumb |
| `/blog/*` | Breadcrumb (Blog > Post Title) |
| `/case-studies` | Breadcrumb |

Implement via `getSchemasForPath(pathname)` function in the Worker, returning an array of schema objects per path.
