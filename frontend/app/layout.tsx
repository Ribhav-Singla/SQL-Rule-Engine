import type { Metadata } from "next";
import "./globals.css";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

export const metadata: Metadata = {
  title: "SQL Rule Engine — Practice SQL with Instant Feedback",
  description:
    "Practice SQL queries and get instant feedback. Write SQL, run it against a real database, and learn from rule-based analysis. Built with FastAPI and Next.js.",
  keywords: ["SQL", "practice", "rule engine", "database", "PostgreSQL", "learning"],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body style={{ display: "flex", flexDirection: "column", minHeight: "100vh" }}>
        <Header />
        <main style={{ flex: 1 }}>{children}</main>
        <Footer />
      </body>
    </html>
  );
}
