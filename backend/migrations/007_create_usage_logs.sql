-- Create usage_logs table
CREATE TABLE IF NOT EXISTS usage_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    inspection_id UUID REFERENCES inspections(id) ON DELETE CASCADE,
    file_id UUID REFERENCES files(id) ON DELETE SET NULL,
    model_name TEXT NOT NULL,
    task_type TEXT NOT NULL,
    input_tokens INTEGER,
    output_tokens INTEGER,
    processing_time_ms INTEGER,
    cost_usd DECIMAL(10, 6),
    timestamp TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_usage_logs_inspection_id ON usage_logs(inspection_id);
CREATE INDEX IF NOT EXISTS idx_usage_logs_timestamp ON usage_logs(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_usage_logs_model_name ON usage_logs(model_name);
