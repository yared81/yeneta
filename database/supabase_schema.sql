-- Yeneta Database Schema for Supabase
-- Execute this SQL in your Supabase SQL Editor

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Users table
CREATE TABLE users (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    preferred_language VARCHAR(10) DEFAULT 'en',
    learning_level VARCHAR(20) DEFAULT 'beginner',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT true,
    profile_picture_url TEXT,
    country VARCHAR(100),
    timezone VARCHAR(50)
);

-- User sessions table
CREATE TABLE user_sessions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT true
);

-- Chat conversations table
CREATE TABLE conversations (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255),
    language VARCHAR(10) DEFAULT 'en',
    learning_level VARCHAR(20) DEFAULT 'beginner',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT true
);

-- Chat messages table
CREATE TABLE messages (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    language VARCHAR(10) DEFAULT 'en',
    learning_level VARCHAR(20) DEFAULT 'beginner',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'
);

-- Learning progress table
CREATE TABLE learning_progress (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    subject VARCHAR(100) NOT NULL,
    topic VARCHAR(100) NOT NULL,
    proficiency_level INTEGER DEFAULT 1 CHECK (proficiency_level BETWEEN 1 AND 10),
    questions_asked INTEGER DEFAULT 0,
    correct_answers INTEGER DEFAULT 0,
    time_spent_minutes INTEGER DEFAULT 0,
    last_studied TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User achievements table
CREATE TABLE user_achievements (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    achievement_type VARCHAR(50) NOT NULL,
    achievement_name VARCHAR(100) NOT NULL,
    description TEXT,
    points INTEGER DEFAULT 0,
    earned_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'
);

-- Study streaks table
CREATE TABLE study_streaks (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    current_streak INTEGER DEFAULT 0,
    longest_streak INTEGER DEFAULT 0,
    last_study_date DATE,
    streak_start_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Learning materials table
CREATE TABLE learning_materials (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    material_type VARCHAR(50) NOT NULL CHECK (material_type IN ('pdf', 'text', 'video', 'audio', 'image')),
    language VARCHAR(10) DEFAULT 'en',
    subject VARCHAR(100),
    difficulty_level VARCHAR(20) DEFAULT 'beginner',
    file_url TEXT,
    file_size INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_public BOOLEAN DEFAULT false
);

-- Quiz questions table
CREATE TABLE quiz_questions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    material_id UUID REFERENCES learning_materials(id) ON DELETE CASCADE,
    question TEXT NOT NULL,
    question_type VARCHAR(20) DEFAULT 'multiple_choice' CHECK (question_type IN ('multiple_choice', 'true_false', 'short_answer', 'essay')),
    options JSONB DEFAULT '[]',
    correct_answer TEXT NOT NULL,
    explanation TEXT,
    difficulty_level VARCHAR(20) DEFAULT 'beginner',
    language VARCHAR(10) DEFAULT 'en',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Quiz attempts table
CREATE TABLE quiz_attempts (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    quiz_id UUID,
    question_id UUID REFERENCES quiz_questions(id) ON DELETE CASCADE,
    user_answer TEXT,
    is_correct BOOLEAN,
    time_taken_seconds INTEGER,
    attempted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User preferences table
CREATE TABLE user_preferences (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    preference_key VARCHAR(100) NOT NULL,
    preference_value TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, preference_key)
);

-- Analytics events table
CREATE TABLE analytics_events (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    event_type VARCHAR(50) NOT NULL,
    event_data JSONB DEFAULT '{}',
    session_id VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);
CREATE INDEX idx_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_sessions_token ON user_sessions(session_token);
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_created_at ON conversations(created_at);
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_user_id ON messages(user_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
CREATE INDEX idx_learning_progress_user_id ON learning_progress(user_id);
CREATE INDEX idx_learning_progress_subject ON learning_progress(subject);
CREATE INDEX idx_achievements_user_id ON user_achievements(user_id);
CREATE INDEX idx_streaks_user_id ON study_streaks(user_id);
CREATE INDEX idx_materials_user_id ON learning_materials(user_id);
CREATE INDEX idx_materials_subject ON learning_materials(subject);
CREATE INDEX idx_questions_material_id ON quiz_questions(material_id);
CREATE INDEX idx_attempts_user_id ON quiz_attempts(user_id);
CREATE INDEX idx_attempts_question_id ON quiz_attempts(question_id);
CREATE INDEX idx_preferences_user_id ON user_preferences(user_id);
CREATE INDEX idx_analytics_user_id ON analytics_events(user_id);
CREATE INDEX idx_analytics_event_type ON analytics_events(event_type);
CREATE INDEX idx_analytics_created_at ON analytics_events(created_at);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Add updated_at triggers
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_conversations_updated_at BEFORE UPDATE ON conversations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_learning_progress_updated_at BEFORE UPDATE ON learning_progress FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_streaks_updated_at BEFORE UPDATE ON study_streaks FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_materials_updated_at BEFORE UPDATE ON learning_materials FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_questions_updated_at BEFORE UPDATE ON quiz_questions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_preferences_updated_at BEFORE UPDATE ON user_preferences FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample data
INSERT INTO users (email, password_hash, full_name, preferred_language, learning_level, country) VALUES
('demo@yeneta.ai', crypt('demo123', gen_salt('bf')), 'Demo User', 'en', 'beginner', 'Ethiopia'),
('student@yeneta.ai', crypt('student123', gen_salt('bf')), 'Student User', 'am', 'intermediate', 'Ethiopia'),
('teacher@yeneta.ai', crypt('teacher123', gen_salt('bf')), 'Teacher User', 'en', 'advanced', 'Nigeria');

-- Insert sample achievements
INSERT INTO user_achievements (user_id, achievement_type, achievement_name, description, points) 
SELECT id, 'first_question', 'First Question Asked', 'Asked your first question on Yeneta', 10 FROM users WHERE email = 'demo@yeneta.ai';

-- Insert sample learning materials
INSERT INTO learning_materials (user_id, title, content, material_type, language, subject, difficulty_level, is_public) 
SELECT id, 'Introduction to Mathematics', 'Basic mathematics concepts for beginners', 'text', 'en', 'Mathematics', 'beginner', true FROM users WHERE email = 'demo@yeneta.ai';

-- Create RLS (Row Level Security) policies
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE learning_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_achievements ENABLE ROW LEVEL SECURITY;
ALTER TABLE study_streaks ENABLE ROW LEVEL SECURITY;
ALTER TABLE learning_materials ENABLE ROW LEVEL SECURITY;
ALTER TABLE quiz_questions ENABLE ROW LEVEL SECURITY;
ALTER TABLE quiz_attempts ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_preferences ENABLE ROW LEVEL SECURITY;
ALTER TABLE analytics_events ENABLE ROW LEVEL SECURITY;

-- RLS Policies (users can only access their own data)
CREATE POLICY "Users can view own profile" ON users FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update own profile" ON users FOR UPDATE USING (auth.uid() = id);
CREATE POLICY "Users can insert own profile" ON users FOR INSERT WITH CHECK (auth.uid() = id);

CREATE POLICY "Users can view own sessions" ON user_sessions FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own sessions" ON user_sessions FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own sessions" ON user_sessions FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can view own conversations" ON conversations FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own conversations" ON conversations FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own conversations" ON conversations FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own conversations" ON conversations FOR DELETE USING (auth.uid() = user_id);

CREATE POLICY "Users can view own messages" ON messages FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own messages" ON messages FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can view own progress" ON learning_progress FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own progress" ON learning_progress FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own progress" ON learning_progress FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can view own achievements" ON user_achievements FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own achievements" ON user_achievements FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can view own streaks" ON study_streaks FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own streaks" ON study_streaks FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own streaks" ON study_streaks FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can view own materials" ON learning_materials FOR SELECT USING (auth.uid() = user_id OR is_public = true);
CREATE POLICY "Users can insert own materials" ON learning_materials FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own materials" ON learning_materials FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own materials" ON learning_materials FOR DELETE USING (auth.uid() = user_id);

CREATE POLICY "Users can view questions for accessible materials" ON quiz_questions FOR SELECT USING (
    EXISTS (SELECT 1 FROM learning_materials WHERE id = quiz_questions.material_id AND (user_id = auth.uid() OR is_public = true))
);

CREATE POLICY "Users can view own quiz attempts" ON quiz_attempts FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own quiz attempts" ON quiz_attempts FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can view own preferences" ON user_preferences FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own preferences" ON user_preferences FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own preferences" ON user_preferences FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can view own analytics" ON analytics_events FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own analytics" ON analytics_events FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Create views for common queries
CREATE VIEW user_stats AS
SELECT 
    u.id,
    u.email,
    u.full_name,
    u.preferred_language,
    u.learning_level,
    COUNT(DISTINCT c.id) as total_conversations,
    COUNT(DISTINCT m.id) as total_messages,
    COUNT(DISTINCT lp.id) as subjects_studied,
    COALESCE(ss.current_streak, 0) as current_streak,
    COALESCE(ss.longest_streak, 0) as longest_streak,
    COUNT(DISTINCT ua.id) as total_achievements
FROM users u
LEFT JOIN conversations c ON u.id = c.user_id
LEFT JOIN messages m ON u.id = m.user_id
LEFT JOIN learning_progress lp ON u.id = lp.user_id
LEFT JOIN study_streaks ss ON u.id = ss.user_id
LEFT JOIN user_achievements ua ON u.id = ua.user_id
GROUP BY u.id, u.email, u.full_name, u.preferred_language, u.learning_level, ss.current_streak, ss.longest_streak;

-- Create a function to get user dashboard data
CREATE OR REPLACE FUNCTION get_user_dashboard(user_uuid UUID)
RETURNS JSON AS $$
DECLARE
    result JSON;
BEGIN
    SELECT json_build_object(
        'user', (SELECT row_to_json(u) FROM users u WHERE u.id = user_uuid),
        'stats', (SELECT row_to_json(us) FROM user_stats us WHERE us.id = user_uuid),
        'recent_conversations', (
            SELECT json_agg(row_to_json(c)) 
            FROM conversations c 
            WHERE c.user_id = user_uuid 
            ORDER BY c.updated_at DESC 
            LIMIT 5
        ),
        'recent_achievements', (
            SELECT json_agg(row_to_json(ua)) 
            FROM user_achievements ua 
            WHERE ua.user_id = user_uuid 
            ORDER BY ua.earned_at DESC 
            LIMIT 5
        )
    ) INTO result;
    
    RETURN result;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Grant necessary permissions
GRANT USAGE ON SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL TABLES IN SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO anon, authenticated;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO anon, authenticated;
