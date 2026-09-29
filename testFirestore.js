import admin from "firebase-admin";

admin.initializeApp({
  credential: admin.credential.applicationDefault()
});

const db = admin.firestore();

async function run() {
  const docRef = await db.collection("test").add({
    name: "Dummy Org",
    url: "http://example.com",
    created: new Date()
  });
  console.log("Document written with ID:", docRef.id);
}

run();
