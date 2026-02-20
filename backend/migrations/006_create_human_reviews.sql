-- Create human_reviews table
CREATE TABLE IF NOT EXISTS human_reviews (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    finding_id UUID REFERENCES findings(id) ON DELETE CASCADE,
    reviewer_id UUID REFERENCES users(id),
    original_category TEXT NOT NULL,
    corrected_category TEXT NOT NULL,
    original_severity TEXT,
    corrected_severity TEXT,
    notes TEXT,
    review_duration_seconds INTEGER,
    reviewed_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_human_reviews_finding_id ON human_reviews(finding_id);
CREATE INDEX IF NOT EXISTS idx_human_reviews_reviewer_id ON human_reviews(reviewer_id);
CREATE INDEX IF NOT EXISTS idx_human_reviews_reviewed_at ON human_reviews(reviewed_at DESC);
