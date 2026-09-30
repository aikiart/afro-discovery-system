import React, { useState, useEffect, useMemo } from 'react';
import { db } from '../website/lib/firebase';
import { collection, onSnapshot, query } from 'firebase/firestore';

const TARGET_COLLECTION = 'afro_centric_apps';

// Helper function to extract domain name if title is missing or 'Untitled'
function cleanTitleFromUrl(url) {
  if (!url) return 'Afro Tech Platform';
  try {
    const formattedUrl = url.startsWith('http') ? url : `https://${url}`;
    const domain = new URL(formattedUrl).hostname.replace('www.', '');
    const baseName = domain.split('.')[0];
    return baseName ? baseName.charAt(0).toUpperCase() + baseName.slice(1) : 'Afro Tech Platform';
  } catch (e) {
    return 'Afro Tech Platform';
  }
}

export default function App() {
  const [platforms, setPlatforms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');

  useEffect(() => {
    setLoading(true);
    const collectionRef = collection(db, TARGET_COLLECTION);
    const q = query(collectionRef);

    const unsubscribe = onSnapshot(
      q,
      (snapshot) => {
        const loadedData = snapshot.docs
          .map((doc) => {
            const data = doc.data();
            const rawUrl = data.url || data.link || data.website || data.siteUrl || '';
            const rawTitle = data.title || data.platform_name || data.name || data.appName || '';

            // Clean title logic
            let finalTitle = rawTitle;
            if (!finalTitle || finalTitle.trim() === 'Untitled' || finalTitle.trim() === 'Untitled Platform') {
              finalTitle = cleanTitleFromUrl(rawUrl);
            }

            return {
              id: doc.id,
              ...data,
              title: finalTitle,
              summary: data.summary || data.description || data.overview || data.details || 'No description provided.',
              url: rawUrl,
              category: data.category || data.type || 'Literature and Publishing',
              location: data.location || null,
              tags: data.tags || ['#technology', '#mobile-app', '#digital-platform'],
              contactEmail: data.contactEmail || data.email || null,
            };
          })
          .filter((item) => {
            // Rule 1: Exclude non-HTTPS sites
            if (!item.url || !item.url.startsWith('https://')) return false;

            // Rule 2: Exclude any remaining 'Untitled Platform' records
            if (item.title === 'Untitled Platform' || item.title === 'Untitled') return false;

            return true;
          });

        setPlatforms(loadedData);
        setLoading(false);
        setError(null);
      },
      (err) => {
        console.error('Firestore Read Error:', err);
        setError(`Failed to read from collection '${TARGET_COLLECTION}'. Verify Firebase permissions.`);
        setLoading(false);
      }
    );

    return () => unsubscribe();
  }, []);

  const categories = useMemo(() => {
    const set = new Set(platforms.map((p) => p.category).filter(Boolean));
    return ['All', ...Array.from(set)];
  }, [platforms]);

  const filteredPlatforms = useMemo(() => {
    return platforms.filter((item) => {
      const titleMatch = (item.title || '').toLowerCase().includes(searchQuery.toLowerCase());
      const descMatch = (item.summary || '').toLowerCase().includes(searchQuery.toLowerCase());
      const locationMatch = (item.location || '').toLowerCase().includes(searchQuery.toLowerCase());
      const catMatch = selectedCategory === 'All' || item.category === selectedCategory;

      return (titleMatch || descMatch || locationMatch) && catMatch;
    });
  }, [platforms, searchQuery, selectedCategory]);

  return (
    <div style={styles.pageWrapper}>
      {/* Deep Forest Green Header Banner */}
      <header style={styles.header}>
        <div style={styles.headerContent}>
          <h1 style={styles.title}>Afro-Centric Digital Discovery Hub</h1>
          <p style={styles.subtitle}>
            This is a resource for all sites and apps Afro-Centric. To access a site, click the bolded title on each block.
          </p>
        </div>
      </header>

      {/* Main Container */}
      <div style={styles.container}>
        {/* Search & Filter Controls */}
        <section style={styles.controls}>
          <div style={styles.searchWrapper}>
            <span style={styles.searchIcon}>🔍</span>
            <input
              type="text"
              placeholder="Search platforms, descriptions, or locations..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              style={styles.searchInput}
            />
          </div>

          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            style={styles.categorySelect}
          >
            {categories.map((cat, idx) => (
              <option key={idx} value={cat}>
                {cat === 'All' ? 'All Categories' : cat}
              </option>
            ))}
          </select>
        </section>

        {/* Live Counter with Singular / Plural Logic */}
        <div style={styles.countText}>
          {loading
            ? 'Connecting to database...'
            : `Showing ${filteredPlatforms.length} ${
                filteredPlatforms.length === 1 ? 'platform' : 'platforms'
              }`}
        </div>

        {error && <div style={styles.errorBanner}>{error}</div>}

        {/* Directory Card Grid */}
        <main style={styles.grid}>
          {loading ? (
            <p style={styles.statusText}>Loading records from Firestore...</p>
          ) : filteredPlatforms.length === 0 ? (
            <p style={styles.statusText}>No platforms found matching your search.</p>
          ) : (
            filteredPlatforms.map((platform) => (
              <article key={platform.id} style={styles.card}>
                <div>
                  {/* Category & Location Badges */}
                  <div style={styles.badgeRow}>
                    <span style={styles.categoryBadge}>{platform.category}</span>
                    {platform.location && (
                      <span style={styles.locationBadge}>
                        📍 {platform.location}
                      </span>
                    )}
                  </div>

                  <h3 style={styles.cardTitle}>
                    {platform.url ? (
                      <a
                        href={platform.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        style={styles.titleLink}
                      >
                        {platform.title} <span style={styles.externalIcon}>↗</span>
                      </a>
                    ) : (
                      platform.title
                    )}
                  </h3>

                  <p style={styles.cardDescription}>{platform.summary}</p>

                  {/* Hashtags */}
                  {platform.tags && platform.tags.length > 0 && (
                    <div style={styles.tagContainer}>
                      {platform.tags.map((tag, idx) => (
                        <span key={idx} style={styles.tag}>
                          {tag.startsWith('#') ? tag : `#${tag}`}
                        </span>
                      ))}
                    </div>
                  )}
                </div>

                {/* Card Footer Info */}
                <div style={styles.cardFooter}>
                  <div style={styles.footerRow}>
                    {platform.contactEmail ? (
                      <span style={styles.emailText}>✉️ {platform.contactEmail}</span>
                    ) : (
                      <span style={styles.noEmailText}>✉️ No direct email listed</span>
                    )}
                  </div>
                  {platform.url && (
                    <div style={styles.footerRow}>
                      <span style={styles.linksLabel}>Links:</span>
                      <a
                        href={platform.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        style={styles.linkIcon}
                        title="Visit Link"
                      >
                        🔗
                      </a>
                    </div>
                  )}
                </div>
              </article>
            ))
          )}
        </main>
      </div>
    </div>
  );
}

const styles = {
  pageWrapper: {
    backgroundColor: '#f8f9fa',
    minHeight: '100vh',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif',
    color: '#212529',
    paddingBottom: '3rem',
  },
  header: {
    backgroundColor: '#0d5c46',
    color: '#ffffff',
    padding: '3rem 1rem',
    textAlign: 'center',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
  },
  headerContent: {
    maxWidth: '1200px',
    margin: '0 auto',
  },
  title: {
    fontSize: '2.25rem',
    fontWeight: '700',
    margin: '0 0 0.75rem 0',
    letterSpacing: '-0.02rem',
  },
  subtitle: {
    fontSize: '1rem',
    color: '#d1e7dd',
    margin: '0 auto',
    maxWidth: '800px',
    fontWeight: '400',
    lineHeight: '1.5',
  },
  container: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '2rem 1rem 0 1rem',
  },
  controls: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    gap: '1rem',
    marginBottom: '1rem',
    flexWrap: 'wrap',
  },
  searchWrapper: {
    position: 'relative',
    flex: '1',
    minWidth: '280px',
  },
  searchIcon: {
    position: 'absolute',
    left: '12px',
    top: '50%',
    transform: 'translateY(-50%)',
    color: '#6c757d',
    fontSize: '0.9rem',
  },
  searchInput: {
    width: '100%',
    padding: '0.65rem 1rem 0.65rem 2.2rem',
    borderRadius: '6px',
    border: '1px solid #ced4da',
    backgroundColor: '#ffffff',
    fontSize: '0.95rem',
    color: '#495057',
    outline: 'none',
    boxSizing: 'border-box',
  },
  categorySelect: {
    padding: '0.65rem 1rem',
    borderRadius: '6px',
    border: '1px solid #ced4da',
    backgroundColor: '#ffffff',
    fontSize: '0.95rem',
    color: '#495057',
    outline: 'none',
    minWidth: '200px',
  },
  countText: {
    fontSize: '0.875rem',
    color: '#495057',
    fontWeight: '600',
    marginBottom: '1.5rem',
  },
  errorBanner: {
    backgroundColor: '#f8d7da',
    color: '#842029',
    padding: '1rem',
    borderRadius: '6px',
    marginBottom: '1.5rem',
    border: '1px solid #f5c2c7',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(340px, 1fr))',
    gap: '1.5rem',
  },
  card: {
    backgroundColor: '#ffffff',
    borderRadius: '8px',
    border: '1px solid #e9ecef',
    padding: '1.5rem',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'space-between',
    boxShadow: '0 1px 3px rgba(0,0,0,0.03)',
  },
  badgeRow: {
    marginBottom: '0.85rem',
    display: 'flex',
    gap: '0.5rem',
    flexWrap: 'wrap',
    alignItems: 'center',
  },
  categoryBadge: {
    backgroundColor: '#e6f4ea',
    color: '#137333',
    padding: '0.25rem 0.65rem',
    borderRadius: '12px',
    fontSize: '0.75rem',
    fontWeight: '600',
    display: 'inline-block',
  },
  locationBadge: {
    backgroundColor: '#f1f3f5',
    color: '#495057',
    padding: '0.25rem 0.65rem',
    borderRadius: '12px',
    fontSize: '0.75rem',
    fontWeight: '600',
    display: 'inline-block',
    border: '1px solid #dee2e6',
  },
  cardTitle: {
    fontSize: '1.15rem',
    fontWeight: '700',
    color: '#212529',
    margin: '0 0 0.75rem 0',
    lineHeight: '1.35',
  },
  titleLink: {
    color: '#212529',
    textDecoration: 'none',
  },
  externalIcon: {
    fontSize: '0.8rem',
    color: '#6c757d',
  },
  cardDescription: {
    fontSize: '0.875rem',
    color: '#6c757d',
    lineHeight: '1.5',
    margin: '0 0 1rem 0',
  },
  tagContainer: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '0.4rem',
    marginBottom: '1.25rem',
  },
  tag: {
    backgroundColor: '#f1f3f5',
    color: '#6c757d',
    padding: '0.2rem 0.5rem',
    borderRadius: '4px',
    fontSize: '0.725rem',
  },
  cardFooter: {
    borderTop: '1px solid #f1f3f5',
    paddingTop: '0.85rem',
    display: 'flex',
    flexDirection: 'column',
    gap: '0.35rem',
    fontSize: '0.775rem',
    color: '#6c757d',
  },
  footerRow: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.4rem',
  },
  emailText: {
    color: '#0d5c46',
    fontWeight: '500',
  },
  noEmailText: {
    color: '#adb5bd',
  },
  linksLabel: {
    color: '#adb5bd',
  },
  linkIcon: {
    textDecoration: 'none',
    fontSize: '0.85rem',
  },
  statusText: {
    gridColumn: '1 / -1',
    textAlign: 'center',
    color: '#6c757d',
    padding: '3rem 0',
  },
};

import ReactDOM from "react-dom/client";
const rootElement = document.getElementById("root");
if (rootElement && !rootElement.hasChildNodes()) {
  ReactDOM.createRoot(rootElement).render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  );
}
