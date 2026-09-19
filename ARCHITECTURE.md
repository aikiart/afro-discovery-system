# Afro Discovery System Architecture

## Goal

Discover Afro-centric websites, apps, organizations, media, educational resources, and businesses worldwide.

## Required Data

- URL
- Site Name
- Description
- Contact Email
- Phone Number
- Social Media Links
- Category
- Tags
- Date Discovered

## Agents

### Discovery Agent

Input:
- Search query

Output:
- URL
- Title
- Search Snippet

### Scraper Agent

Input:
- URL

Output:
- Site Metadata
- About Text
- Contact Information
- Social Links

### Categorizer Agent

Input:
- Scraped Content

Output:
- Category
- Tags

### Database Agent

Input:
- Categorized Data

Output:
- Firebase Record

### Update Agent

Runs Weekly

Tasks:
- Re-run discovery
- Check existing URLs
- Detect new resources
- Update records

## Future Search Providers

- Bing
- Brave
- SearchAPI.io
- Custom crawler