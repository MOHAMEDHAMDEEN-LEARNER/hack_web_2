import { Pool as NeonPool, neonConfig } from '@neondatabase/serverless';
import { drizzle as neonDrizzle } from 'drizzle-orm/neon-serverless';
import { drizzle as pgDrizzle } from 'drizzle-orm/node-postgres';
import { Pool as PgPool } from 'pg';
import ws from "ws";
import * as schema from "@shared/schema";

if (!process.env.DATABASE_URL) {
  throw new Error(
    "DATABASE_URL must be set. Did you forget to provision a database?",
  );
}

// Detect if we're using Neon or local PostgreSQL
const isNeon = process.env.DATABASE_URL.includes('neon.tech') || process.env.DATABASE_URL.includes('aws.neon');

let pool: any;
let db: any;

if (isNeon) {
  // Use Neon serverless
  neonConfig.webSocketConstructor = ws;
  pool = new NeonPool({ connectionString: process.env.DATABASE_URL });
  db = neonDrizzle({ client: pool, schema });
} else {
  // Use regular PostgreSQL
  pool = new PgPool({ connectionString: process.env.DATABASE_URL });
  db = pgDrizzle(pool, { schema });
}

export { pool, db };
