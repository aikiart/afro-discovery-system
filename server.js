import express from "express";
import bodyParser from "body-parser";
import { initializeApp, cert } from "firebase-admin/app";
import { getFirestore } from "firebase-admin/firestore";
import { readFileSync } from "fs";

// Load local serviceAccount.json key directly
const serviceAccount = JSON.parse(
  readFileSync(new URL("./serviceAccount.json", import.meta.url))
);

// Initialize Firebase Admin with cert helper
initializeApp({
  credential: cert(serviceAccount)
});

const db = getFirestore();
const app = express();
app.use(bodyParser.json());

// Sanitization helper to fix character encoding glitches (Mojibake)
function sanitizeText(str) {
  if (typeof str !== 'string') return str;
  return str
    // Replace garbled UTF-8 dashes, quotes, and ellipses
    .replace(/â\u0080\u0094|â\u0080\u0093|â\u0080\u0090/g, " - ")
    .replace(/â\u0080\u0099|â\u0080\u0098/g, "'")
    .replace(/â\u0080\u009c|â\u0080\u009d/g, '"')
    .replace(/â\u0080\u00a6/g, "...")
    .replace(/\uFFFD/g, "")
    // Generic fallback for leftover garbled â sequences
    .replace(/â[^\s]+/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

// Endpoint to add organization
app.post("/api/add-organization", async (req, res) => {
  try {
    const org = req.body;

    // Sanitize text fields before saving
    if (org.title) org.title = sanitizeText(org.title);
    if (org.name) org.name = sanitizeText(org.name);
    if (org.description) org.description = sanitizeText(org.description);

    // Optional: deduplication by URL
    const existing = await db.collection("organizations")
      .where("url", "==", org.url)
      .get();

    if (!existing.empty) {
      return res.status(200).send({ message: "Organization already exists", org });
    }

    await db.collection("organizations").add(org);
    res.status(200).send({ message: "Organization added", org });
  } catch (error) {
    console.error(error);
    res.status(500).send({ error: "Failed to add organization" });
  }
});

// Health check endpoint
app.get("/", (req, res) => {
  res.send("Backend is running!");
});

// Start server
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});