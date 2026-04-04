import Link from "next/link";
import styles from "./ProblemCard.module.css";
import { patternColors } from "@/lib/problems";

interface ProblemCardProps {
  problemId: string;
  title: string;
  pattern: string;
  schema: string;
  index: number;
}

export default function ProblemCard({
  problemId,
  title,
  pattern,
  schema,
  index,
}: ProblemCardProps) {
  const patternColor = patternColors[pattern] || "#F97316";

  return (
    <Link href={`/practice/${problemId}`} className={styles.card} style={{ animationDelay: `${index * 60}ms` }} id={`problem-card-${problemId}`}>
      <div className={styles.cardTop}>
        <span className={styles.problemId}>{problemId}</span>
        <svg className={styles.arrow} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M5 12h14" />
          <path d="m12 5 7 7-7 7" />
        </svg>
      </div>

      <h3 className={styles.title}>{title}</h3>

      <div className={styles.tags}>
        <span
          className={styles.patternTag}
          style={{
            backgroundColor: `${patternColor}12`,
            color: patternColor,
            borderColor: `${patternColor}30`,
          }}
        >
          {pattern}
        </span>
        <span className={styles.schemaTag}>{schema}</span>
      </div>
    </Link>
  );
}
