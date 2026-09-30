import React from 'react';

export default function CountryFilter({ countries = [], selectedCountry, onSelectCountry }) {
  return (
    <div className="country-filter" style={{ marginBottom: '1.5rem' }}>
      <label 
        htmlFor="country-select" 
        style={{ 
          display: 'block', 
          marginBottom: '0.5rem', 
          fontWeight: '600',
          fontSize: '0.95rem' 
        }}
      >
        Filter by Country:
      </label>
      <select
        id="country-select"
        value={selectedCountry}
        onChange={(e) => onSelectCountry(e.target.value)}
        style={{
          width: '100%',
          maxWidth: '300px',
          padding: '0.6rem 0.8rem',
          borderRadius: '6px',
          border: '1px solid #ccc',
          fontSize: '1rem',
          backgroundColor: '#fff',
          cursor: 'pointer'
        }}
      >
        <option value="">All Countries ({countries.length})</option>
        {countries.map((country) => (
          <option key={country} value={country}>
            {country}
          </option>
        ))}
      </select>
    </div>
  );
}