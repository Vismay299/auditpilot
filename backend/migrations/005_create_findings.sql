-- Create findings table with pgvector support
CREATE TABLE IF NOT EXISTS findings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    inspection_id UUID REFERENCES inspections(id) ON DELETE CASCADE,
    file_id UUID REFERENCES files(id) ON DELETE CASCADE,
    category TEXT NOT NULL,
    severity TEXT CHECK (severity IN ('critical', 'high', 'medium', 'low', 'clear')),
    confidence_score FLOAT CHECK (confidence_score >= 0 AND confidence_score <= 1),
    needs_review BOOLEAN DEFAULT false,
    description TEXT,
    ai_caption TEXT,
    transcription TEXT,
    location_code TEXT,
    equipment_id TEXT,
    extra_metadata JSONB DEFAULT '{}'::jsonb,
    embedding VECTOR(384),  -- pgvector column
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_findings_inspection_id ON findings(inspection_id);
CREATE INDEX IF NOT EXISTS idx_findings_file_id ON findings(file_id);
CREATE INDEX IF NOT EXISTS idx_findings_category ON findings(category);
CREATE INDEX IF NOT EXISTS idx_findings_severity ON findings(severity);
CREATE INDEX IF NOT EXISTS idx_findings_needs_review ON findings(needs_review) WHERE needs_review = true;

-- Vector similarity index (HNSW for fast approximate search)
CREATE INDEX IF NOT EXISTS idx_findings_embedding ON findings USING hnsw (embedding vector_cosine_ops);
