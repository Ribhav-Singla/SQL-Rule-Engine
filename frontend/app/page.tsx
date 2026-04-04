import ProblemCard from "@/components/ProblemCard";
import { problems } from "@/lib/problems";
import styles from "./page.module.css";

export default function HomePage() {
  return (
    <div className={styles.page}>
      {/* Hero Section */}
      <section className={styles.hero}>
        <div className={styles.heroContent}>
          <div className={styles.heroBadge}>
            <span className={styles.heroBadgeDot} />
            Open Source SQL Practice Platform
          </div>

          <h1 className={styles.heroTitle}>
            Master SQL with
            <span className={styles.heroAccent}> Instant Feedback</span>
          </h1>

          <p className={styles.heroSubtitle}>
            Write SQL queries, execute them against a real PostgreSQL database,
            and get intelligent feedback from our rule engine — all in your
            browser.
          </p>

          <div className={styles.heroStats}>
            <div className={styles.stat}>
              <span className={styles.statNumber}>{problems.length}</span>
              <span className={styles.statLabel}>Problems</span>
            </div>
            <div className={styles.statDivider} />
            <div className={styles.stat}>
              <span className={styles.statNumber}>5</span>
              <span className={styles.statLabel}>Patterns</span>
            </div>
            <div className={styles.statDivider} />
            <div className={styles.stat}>
              <span className={styles.statNumber}>6</span>
              <span className={styles.statLabel}>Tables</span>
            </div>
            <div className={styles.statDivider} />
            <div className={styles.stat}>
              <span className={styles.statNumber}>5</span>
              <span className={styles.statLabel}>Lint Rules</span>
            </div>
          </div>
        </div>
      </section>

      {/* Problems Grid */}
      <section className={styles.problems} id="problems-section">
        <div className={styles.sectionHeader}>
          <h2 className={styles.sectionTitle}>SQL Problems</h2>
          <p className={styles.sectionSubtitle}>
            Choose a problem to start practicing. Each tests a different SQL
            pattern.
          </p>
        </div>

        <div className={styles.grid}>
          {problems.map((problem, index) => (
            <ProblemCard
              key={problem.problem_id}
              problemId={problem.problem_id}
              title={problem.title}
              pattern={problem.pattern}
              schema={problem.schema}
              index={index}
            />
          ))}
        </div>
      </section>

      {/* Pipeline Section */}
      <section className={styles.pipeline}>
        <h2 className={styles.sectionTitle}>How It Works</h2>
        <div className={styles.pipelineSteps}>
          {[
            {
              step: "01",
              title: "Write SQL",
              desc: "Use our CodeMirror editor with syntax highlighting and auto-formatting",
              icon: "✍️",
            },
            {
              step: "02",
              title: "Normalize & Lint",
              desc: "Your query is parsed, normalized, and checked against 5 best-practice rules",
              icon: "🔍",
            },
            {
              step: "03",
              title: "Execute & Compare",
              desc: "Run safely against PostgreSQL and compare results with expected output",
              icon: "⚡",
            },
            {
              step: "04",
              title: "Get Feedback",
              desc: "See correctness, data preview, rule violations, and improvement suggestions",
              icon: "📊",
            },
          ].map((item) => (
            <div key={item.step} className={styles.pipelineStep}>
              <div className={styles.pipelineIcon}>{item.icon}</div>
              <div className={styles.pipelineStepNum}>{item.step}</div>
              <h3 className={styles.pipelineTitle}>{item.title}</h3>
              <p className={styles.pipelineDesc}>{item.desc}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
