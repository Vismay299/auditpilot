-- Create inspections table
CREATE TABLE IF NOT EXISTS inspections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    org_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    site_location TEXT,
    site_address TEXT,
    inspector_id UUID REFERENCES users(id),
    status TEXT DEFAULT 'processing' CHECK (status IN ('processing', 'review', 'completed', 'failed')),
    risk_level TEXT CHECK (risk_level IN ('critical', 'high', 'medium', 'low', 'clear')),
    report_narrative TEXT,
    total_findings INTEGER DEFAULT 0,
    total_files INTEGER DEFAULT 0,
    processing_started_at TIMESTAMP,
    processing_completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_inspections_org_id ON inspections(org_id);
CREATE INDEX IF NOT EXISTS idx_inspections_inspector_id ON inspections(inspector_id);
CREATE INDEX IF NOT EXISTS idx_inspections_status ON inspections(status);
CREATE INDEX IF NOT EXISTS idx_inspections_created_at ON inspections(created_at DESC);
