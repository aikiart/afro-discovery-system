'use client';

import React, { useState, useEffect } from 'react';
import { initializeApp, getApps, getApp } from 'firebase/app';
import { getFirestore, collection, getDocs, query, orderBy } from 'firebase/firestore';

// Firebase Client Configuration
// (Replace these environment variables or strings with your actual Firebase web config)
const firebaseConfig = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY,
  authDomain: "afro-discovery-system.firebaseapp.com",
  projectId: "afro-discovery-system",
  storageBucket: "afro-discovery-system.appspot.com",
  messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID
};

// Initialize Firebase
const app = !getApps().length ? initializeApp(firebaseConfig) : getApp();
const db = getFirestore(app);

interface DiscoveryItem {
  id: string;
  title?: string;
  name?: string;
  description?: string;
  country?: string;
  category?: string;
  url?: string;
}

export default function AfroDiscoveryHub() {
  const [items, setItems] = useState<DiscoveryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCountry, setSelectedCountry] = useState('All');

  // List of countries for the dropdown filter
  const countries = [
    'All',
    'Costa Rica',
    'Georgia (US)',
    'United States',
    'Ghana',
    'Nigeria',
    'Brazil',
    'Colombia',
    'Jamaica',
    'United Kingdom'
  ];

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);
        // Fetch scraped items from your Firestore collection
        const querySnapshot = await getDocs(collection(db, 'organizations'));
        const docsData: DiscoveryItem[] = querySnapshot.docs.map(doc => ({
          id: doc.id,
          ...doc.data()
        }));
        setItems(docsData);
      } catch (error) {
        console.error("Error fetching Firestore records:", error);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  // Filter items based on search query & selected country dropdown
  const filteredItems = items.filter(item => {
    const itemTitle = (item.title || item.name || '').toLowerCase();
    const itemDesc = (item.description || '').toLowerCase();
    const itemCountry = item.country || '';

    const matchesSearch = itemTitle.includes(searchQuery.toLowerCase()) || itemDesc.includes(searchQuery.toLowerCase());
    const matchesCountry = selectedCountry === 'All' || itemCountry.toLowerCase() === selectedCountry.toLowerCase();

    return matchesSearch && matchesCountry;
  });

  return (
    <div className="min-h-screen bg-stone-950 text-stone-100 font-sans p-6 md:p-12">
      {/* Header Section */}
      <header className="max-w-6xl mx-auto mb-10 text-center md:text-left border-b border-amber-900/40 pb-6">
        <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight text-amber-500 mb-2">
          Afro Discovery System
        </h1>
        <p className="text-stone-400 text-lg">
          Web discovery platform and literature recommendation portal.
        </p>
      </header>

      {/* Control Bar: Search Input & Country Dropdown */}
      <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        
        {/* Search Input */}
        <div className="md:col-span-2">
          <label className="block text-xs uppercase tracking-wider text-amber-500 mb-1 font-semibold">
            Search Portal
          </label>
          <input
            type="text"
            placeholder="Search organizations, topics, or literature..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-stone-900 border border-stone-800 focus:border-amber-500 rounded-lg px-4 py-3 text-stone-200 outline-none transition"
          />
        </div>

        {/* Country Filter Dropdown */}
        <div>
          <label className="block text-xs uppercase tracking-wider text-amber-500 mb-1 font-semibold">
            Filter by Country
          </label>
          <select
            value={selectedCountry}
            onChange={(e) => setSelectedCountry(e.target.value)}
            className="w-full bg-stone-900 border border-stone-800 focus:border-amber-500 rounded-lg px-4 py-3 text-stone-200 outline-none cursor-pointer transition"
          >
            {countries.map((country) => (
              <option key={country} value={country} className="bg-stone-900 text-stone-200">
                {country}
              </option>
            ))}
          </select>
        </div>

      </div>

      {/* Content Grid */}
      <main className="max-w-6xl mx-auto">
        {loading ? (
          <div className="py-20 text-center text-stone-500 animate-pulse">
            Loading discovery records from Firestore...
          </div>
        ) : filteredItems.length === 0 ? (
          <div className="py-16 text-center border border-dashed border-stone-800 rounded-xl text-stone-500">
            No discovery records match your search or selected country.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredItems.map((item) => (
              <div 
                key={item.id} 
                className="bg-stone-900/60 border border-stone-800 hover:border-amber-600/50 rounded-xl p-6 flex flex-col justify-between transition-all duration-200 hover:-translate-y-1"
              >
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-xs font-semibold px-2.5 py-1 bg-amber-950/80 text-amber-400 border border-amber-800/40 rounded-full">
                      {item.country || 'Global'}
                    </span>
                    {item.category && (
                      <span className="text-xs text-stone-500">{item.category}</span>
                    )}
                  </div>
                  <h2 className="text-xl font-bold text-stone-100 mb-2">
                    {item.title || item.name || 'Untitled Entry'}
                  </h2>
                  <p className="text-stone-400 text-sm line-clamp-3 mb-4">
                    {item.description || 'No description provided.'}
                  </p>
                </div>

                {item.url && (
                  <a
                    href={item.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center justify-center w-full py-2.5 px-4 bg-stone-800 hover:bg-amber-600 text-stone-200 hover:text-stone-950 text-sm font-semibold rounded-lg transition"
                  >
                    Visit Link
                  </a>
                )}
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}