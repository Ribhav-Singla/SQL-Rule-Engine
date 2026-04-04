"use client";

import { useState } from "react";
import styles from "./SchemaReference.module.css";
import { ecommerceSchema } from "@/lib/schema";

export default function SchemaReference() {
  const [expanded, setExpanded] = useState<Record<string, boolean>>({
    customers: true,
  });

  const toggle = (table: string) => {
    setExpanded((prev) => ({ ...prev, [table]: !prev[table] }));
  };

  return (
    <div className={styles.panel} id="schema-reference">
      <div className={styles.header}>
        <h3 className={styles.title}>
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <ellipse cx="12" cy="5" rx="9" ry="3" />
            <path d="M3 5V19A9 3 0 0 0 21 19V5" />
            <path d="M3 12A9 3 0 0 0 21 12" />
          </svg>
          Schema Reference
        </h3>
        <span className={styles.schemaBadge}>ecommerce</span>
      </div>

      <div className={styles.tables}>
        {ecommerceSchema.map((table) => (
          <div key={table.name} className={styles.tableGroup}>
            <button
              className={styles.tableHeader}
              onClick={() => toggle(table.name)}
              aria-expanded={!!expanded[table.name]}
              id={`schema-table-${table.name}`}
            >
              <span className={styles.tableIcon}>
                {expanded[table.name] ? "▾" : "▸"}
              </span>
              <span className={styles.tableName}>{table.name}</span>
              <span className={styles.colCount}>
                {table.columns.length} cols
              </span>
            </button>

            {expanded[table.name] && (
              <div className={styles.columns}>
                {table.columns.map((col) => (
                  <div key={col.name} className={styles.column}>
                    <span className={styles.colName}>{col.name}</span>
                    <span className={styles.colType}>{col.type}</span>
                    {col.constraint && (
                      <span className={styles.colConstraint}>
                        {col.constraint}
                      </span>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
