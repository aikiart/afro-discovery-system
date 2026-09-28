import React, { useEffect, useState } from "react";
import ForceGraph2D from "react-force-graph-2d";
import { collection, onSnapshot } from "firebase/firestore";
import { db } from "../../website/lib/firebase";

// Native byte re-decoder with regex fallback to eliminate Mojibake artifacts
export function sanitizeText(str) {
  if (typeof str !== "string") return str || "";

  let cleaned = str;

  try {
    const bytes = Uint8Array.from(str, (char) => char.charCodeAt(0));
    const decoded = new TextDecoder("utf-8", { fatal: true }).decode(bytes);
    cleaned = decoded;
  } catch (e) {
    // Fallback if re-decoding fails
  }

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

export default function VisualGraph({ onSelectNode, onNodeCountChange }) {
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });

  useEffect(() => {
    // Subscribe to Firestore afro_centric_apps collection
    const unsubscribe = onSnapshot(collection(db, "afro_centric_apps"), (snapshot) => {
      const nodes = [];

      snapshot.forEach((doc) => {
        const data = doc.data();

        nodes.push({
          id: doc.id,
          title: sanitizeText(data.title || data.name || "Untitled"),
          description: sanitizeText(data.description || "No description available."),
          url: data.url || "#",
          category: data.category || "Ecosystem",
          tags: data.tags || []
        });
      });

      setGraphData({
        nodes,
        links: []
      });

      if (onNodeCountChange) {
        onNodeCountChange(nodes.length);
      }
    });

    return () => unsubscribe();
  }, [onNodeCountChange]);

  return (
    <div style={{ width: "100%", height: "100%", backgroundColor: "#111" }}>
      <ForceGraph2D
        graphData={graphData}
        nodeLabel={(node) => sanitizeText(node.title)}
        nodeAutoColorBy="category"
        onNodeClick={(node) => onSelectNode && onSelectNode(node)}
      />
    </div>
  );
}