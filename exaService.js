import dotenv from "dotenv";
import Exa from "exa-js";
import fetch from "node-fetch";

dotenv.config();

const exa = new Exa(process.env.EXA_API_KEY);

async function runQuery() {
  const response = await exa.search("Afro-centric organizations", { numResults: 5 });
  console.log("Exa results:", response);

  for (const r of response.results) {
    const org = {
      name: r.title,
      description: r.highlight || "",
      url: r.url,
      source: "exa"
    };

    await fetch("http://localhost:3000/api/add-organization", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(org)
    });
  }
}

runQuery().catch(console.error);
