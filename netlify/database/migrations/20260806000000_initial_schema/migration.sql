-- Initial schema for Dunn & Waite Cleaning Co. business app

CREATE TABLE clients (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  address TEXT DEFAULT '',
  phone TEXT DEFAULT '',
  notes TEXT DEFAULT '',
  access_code TEXT NOT NULL UNIQUE,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE jobs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  time TEXT NOT NULL,
  type TEXT NOT NULL,
  price NUMERIC(10,2) NOT NULL DEFAULT 0,
  status TEXT NOT NULL DEFAULT 'requested' CHECK (status IN ('requested', 'scheduled', 'in_progress', 'done')),
  notes TEXT DEFAULT '',
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE invoices (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  job_id UUID NOT NULL UNIQUE REFERENCES jobs(id) ON DELETE CASCADE,
  client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
  number TEXT NOT NULL UNIQUE,
  subtotal NUMERIC(10,2) NOT NULL DEFAULT 0,
  tax NUMERIC(10,2) NOT NULL DEFAULT 0,
  payment_method TEXT NOT NULL DEFAULT 'Cash' CHECK (payment_method IN ('Cash', 'Check', 'Card')),
  paid BOOLEAN NOT NULL DEFAULT FALSE,
  created_date DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE invoice_sequence (
  id INTEGER PRIMARY KEY DEFAULT 1,
  next_number INTEGER NOT NULL DEFAULT 1,
  CONSTRAINT single_row CHECK (id = 1)
);
INSERT INTO invoice_sequence (id, next_number) VALUES (1, 1);

-- Owner login: single business account (email + hashed password)
CREATE TABLE owner_account (
  id INTEGER PRIMARY KEY DEFAULT 1,
  email TEXT NOT NULL,
  password_hash TEXT NOT NULL,
  CONSTRAINT single_owner CHECK (id = 1)
);

CREATE INDEX idx_jobs_client_id ON jobs(client_id);
CREATE INDEX idx_invoices_client_id ON invoices(client_id);
CREATE INDEX idx_clients_access_code ON clients(access_code);
