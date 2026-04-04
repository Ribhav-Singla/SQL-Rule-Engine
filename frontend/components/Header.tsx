import Link from "next/link";
import styles from "./Header.module.css";

export default function Header() {
  return (
    <header className={styles.header} id="main-header">
      <div className={styles.inner}>
        <Link href="/" className={styles.logo}>
          <span className={styles.logoIcon}>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="16 18 22 12 16 6" />
              <polyline points="8 6 2 12 8 18" />
            </svg>
          </span>
          <span className={styles.logoText}>
            SQL Rule Engine
          </span>
        </Link>

        <nav className={styles.nav}>
          <Link href="/" className={styles.navLink}>
            Problems
          </Link>
          <a
            href="http://localhost:8000/docs"
            target="_blank"
            rel="noopener noreferrer"
            className={styles.navLink}
          >
            API Docs
          </a>
          <span className={styles.badge}>v1.0</span>
        </nav>
      </div>
    </header>
  );
}
