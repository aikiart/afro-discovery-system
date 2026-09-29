import { NextResponse } from "next/server";
import { db } from "../../../lib/firebase";
import { collection, addDoc } from "firebase/firestore";

export async function POST(req: Request) {
  try {
    const body = await req.json();

    // Validate required fields
    if (!body.name || !body.url) {
      return NextResponse.json(
        { error: "Missing required fields: name, url" },
        { status: 400 }
      );
    }

    const docRef = await addDoc(collection(db, "organizations"), {
      name: body.name,
      category: body.category || "Uncategorized",
      description: body.description || "",
      url: body.url,
      contact_email: body.contact_email || "",
      phone: body.phone || "",
      site_name: body.site_name || body.name,
      query: body.query || "",
      social_links: body.social_links || [],
    });

    return NextResponse.json({ id: docRef.id, ...body });
  } catch (error: any) {
    console.error("Error adding organization:", error);
    return NextResponse.json(
      { error: error.message || "Unknown error" },
      { status: 500 }
    );
  }
}
