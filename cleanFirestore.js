import admin from "firebase-admin";
import { readFileSync } from "fs";

// Load service account JSON using standard FS read for ES Modules
const serviceAccount = JSON.parse(
  readFileSync(new URL("./serviceAccount.json", import.meta.url))
);

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

const db = admin.firestore();

// Aggressive scrubbing function targeting literal bad characters and Mojibake artifacts
function scrubText(str) {
  if (typeof str !== "string") return str;

  let cleaned = str;

  // 1. Direct string replacement for known Mojibake patterns
  cleaned = cleaned
    .replace(/â\u0080\u0094|â\u0080\u0093|â\u0080\u0090/g, " - ")
    .replace(/â\u0080\u0099|â\u0080\u0098/g, "'")
    .replace(/â\u0080\u009c|â\u0080\u009d/g, '"')
    .replace(/â\u0080\u00a6/g, "...")
    .replace(/\u00E2[^\x20-\x7E]+/g, " - ")
    .replace(/â[^\x20-\x7E]+/g, " - ")
    .replace(/\uFFFD/g, "")
    .replace(/â/g, " - ")
    .replace(/\s+/g, " ")
    .trim();

  return cleaned;
}

async function cleanDatabase() {
  console.log("Starting full Firestore database scan...");
  
  // List all collections in your Firestore database automatically
  const collections = await db.listCollections();
  
  if (collections.length === 0) {
    console.log("No collections found in this Firestore project.");
    process.exit(0);
  }

  for (const colRef of collections) {
    const colName = colRef.id;
    console.log(`\nScanning collection: '${colName}'...`);
    
    const snapshot = await colRef.get();
    let batch = db.batch();
    let count = 0;

    snapshot.forEach((doc) => {
      const data = doc.data();
      let updated = false;
      const updates = {};

      Object.keys(data).forEach((field) => {
        if (typeof data[field] === "string") {
          const original = data[field];
          const cleaned = scrubText(original);

          if (original !== cleaned) {
            console.log(` -> Found corrupted text in doc [${doc.id}], field [${field}]`);
            console.log(`    BEFORE: "${original}"`);
            console.log(`    AFTER:  "${cleaned}"`);
            updates[field] = cleaned;
            updated = true;
          }
        }
      });

      if (updated) {
        batch.update(doc.ref, updates);
        count++;
      }
    });

    if (count > 0) {
      await batch.commit();
      console.log(`Successfully cleaned and updated ${count} records in '${colName}'.`);
    } else {
      console.log(`No corrupted text detected in '${colName}'.`);
    }
  }

  console.log("\nDatabase cleanup complete!");
  process.exit(0);
}

cleanDatabase().catch((err) => {
  console.error("Migration failed:", err);
  process.exit(1);
});