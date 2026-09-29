// Native byte re-decoder with regex fallback to eliminate Mojibake artifacts
function sanitizeText(str) {
  if (typeof str !== "string") return str || "";

  let cleaned = str;

  // 1. Attempt true UTF-8 re-decoding from Latin-1/Windows-1252 byte stream
  try {
    const bytes = Uint8Array.from(str, (char) => char.charCodeAt(0));
    const decoded = new TextDecoder("utf-8", { fatal: true }).decode(bytes);
    cleaned = decoded;
  } catch (e) {
    // Fallback if re-decoding is not applicable
  }

  // 2. Comprehensive pattern replacement to scrub residual garbled sequences
  return cleaned
    .replace(/â\u0080\u0094|â\u0080\u0093|â\u0080\u0090/g, " - ")
    .replace(/â\u0080\u0099|â\u0080\u0098/g, "'")
    .replace(/â\u0080\u009c|â\u0080\u009d/g, '"')
    .replace(/\u00E2[^\x20-\x7E]+/g, " - ")
    .replace(/â[^\x20-\x7E]+/g, " - ")
    .replace(/\uFFFD/g, "")
    .replace(/â(?=\s|[\:\-\_]|$)/g, " - ")
    .replace(/\s+/g, " ")
    .trim();
}

function renderPlatforms(platforms) {
  cardsGrid.innerHTML = "";
  
  // Updated display text: "Showing X platforms" (removed "(s)")
  resultsCount.textContent = `Showing ${platforms.length} platforms`;

  platforms.forEach((platform) => {
    const card = document.createElement("div");
    card.className = "platform-card";

    const cleanTitle = sanitizeText(platform.title || platform.name || "Untitled");
    const cleanDescription = sanitizeText(platform.description || "No description available.");

    card.innerHTML = `
      <h3>${cleanTitle}</h3>
      <p>${cleanDescription}</p>
      ${
        platform.url && platform.url !== "#"
          ? `<a href="${platform.url}" target="_blank" rel="noopener noreferrer">Visit Resource ↗</a>`
          : ""
      }
    `;

    cardsGrid.appendChild(card);
  });
}