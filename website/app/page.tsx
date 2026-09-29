"use client";

import { useEffect, useState } from "react";

interface Organization {
  id: string;
  name?: string;
  category?: string;
  description?: string;
  url?: string;
  contact_email?: string;
  phone?: string;
  site_name?: string;
  query?: string;
  social_links?: string[];
}

export default function HomePage() {
  const [organizations, setOrganizations] = useState<Organization[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchOrganizations() {
      try {
        const res = await fetch("/api/organizations");
        const data = await res.json();
        setOrganizations(data);
      } catch (err) {
        console.error("Failed to fetch organizations:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchOrganizations();
  }, []);

  if (loading) {
    return <p className="p-4">Loading organizations…</p>;
  }

  return (
    <main className="p-6">
      <h1 className="text-2xl font-bold mb-4">Afro Discovery Directory</h1>
      {organizations.length === 0 ? (
        <p>No organizations found.</p>
      ) : (
        <ul className="space-y-4">
          {organizations.map((org) => (
            <li key={org.id} className="border p-4 rounded">
              <h2 className="text-lg font-semibold">
                {org.site_name || org.name || "Untitled"}
              </h2>
              {org.description && (
                <p className="text-sm text-gray-700">{org.description}</p>
              )}
              {org.url && (
                <a
                  href={org.url.trim()}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 underline"
                >
                  Visit site
                </a>
              )}
              {org.contact_email && (
                <p className="text-sm">📧 {org.contact_email.trim()}</p>
              )}
              {org.phone && <p className="text-sm">📞 {org.phone}</p>}
              {org.social_links && org.social_links.length > 0 && (
                <div className="mt-2">
                  <p className="font-medium">Social Links:</p>
                  <ul className="list-disc list-inside">
                    {org.social_links.map((link, i) => (
                      <li key={i}>
                        <a
                          href={link.trim()}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-blue-600 underline"
                        >
                          {link.trim()}
                        </a>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}
