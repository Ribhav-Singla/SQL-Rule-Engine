import styles from "./Footer.module.css";

export default function Footer() {
  return (
    <footer className={styles.footer} id="main-footer">
      <div className={styles.inner}>
        <p className={styles.text}>
          SQL Rule Engine — Practice SQL with instant feedback
        </p>
        <p className={styles.sub}>
          Built with FastAPI + Next.js
        </p>
      </div>
    </footer>
  );
}
