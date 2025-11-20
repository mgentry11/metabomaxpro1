# HIT Coach Pro Database Schema

This document outlines the database schema needed for HIT Coach Pro workout tracking and history.

## Required Supabase Tables

### 1. `workout_history` Table

Stores individual workout sessions.

```sql
CREATE TABLE workout_history (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    workout_type VARCHAR(50) NOT NULL, -- 'quick_start', 'workout_a', 'workout_b'
    completed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    total_duration_seconds INTEGER NOT NULL,
    exercises_completed INTEGER NOT NULL,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index for faster queries
CREATE INDEX idx_workout_history_user_id ON workout_history(user_id);
CREATE INDEX idx_workout_history_completed_at ON workout_history(completed_at DESC);
```

### 2. `exercise_sets` Table

Stores individual exercise sets within each workout.

```sql
CREATE TABLE exercise_sets (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    workout_id UUID NOT NULL REFERENCES workout_history(id) ON DELETE CASCADE,
    exercise_name VARCHAR(100) NOT NULL,
    exercise_order INTEGER NOT NULL, -- Order within the workout
    weight_lbs DECIMAL(6,2), -- Weight used (optional)
    reps INTEGER, -- Reps completed (optional)
    time_under_tension_seconds INTEGER, -- TUT duration
    difficulty_rating INTEGER CHECK (difficulty_rating BETWEEN 1 AND 10), -- 1-10 scale
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_exercise_sets_workout_id ON exercise_sets(workout_id);
CREATE INDEX idx_exercise_sets_exercise_name ON exercise_sets(exercise_name);
```

### 3. `user_workout_preferences` Table

Stores user preferences and custom timings.

```sql
CREATE TABLE user_workout_preferences (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID NOT NULL UNIQUE REFERENCES auth.users(id) ON DELETE CASCADE,
    default_prep_time INTEGER DEFAULT 5,
    default_positioning_time INTEGER DEFAULT 5,
    default_eccentric_time INTEGER DEFAULT 10,
    default_concentric_time INTEGER DEFAULT 1,
    default_final_eccentric_time INTEGER DEFAULT 10,
    voice_enabled BOOLEAN DEFAULT TRUE,
    voice_rate DECIMAL(3,2) DEFAULT 1.0 CHECK (voice_rate BETWEEN 0.5 AND 2.0),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index
CREATE INDEX idx_user_workout_preferences_user_id ON user_workout_preferences(user_id);
```

### 4. `workout_programs` Table (Optional - Future Enhancement)

Stores custom workout programs created by premium users.

```sql
CREATE TABLE workout_programs (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    program_name VARCHAR(100) NOT NULL,
    exercises JSONB NOT NULL, -- Array of exercise objects
    is_public BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_workout_programs_user_id ON workout_programs(user_id);
CREATE INDEX idx_workout_programs_is_public ON workout_programs(is_public);
```

## Row Level Security (RLS) Policies

Enable RLS and add policies to ensure users can only access their own data.

### `workout_history` Policies

```sql
-- Enable RLS
ALTER TABLE workout_history ENABLE ROW LEVEL SECURITY;

-- Users can view their own workout history
CREATE POLICY "Users can view own workout history"
ON workout_history FOR SELECT
USING (auth.uid() = user_id);

-- Users can insert their own workouts
CREATE POLICY "Users can insert own workouts"
ON workout_history FOR INSERT
WITH CHECK (auth.uid() = user_id);

-- Users can update their own workouts
CREATE POLICY "Users can update own workouts"
ON workout_history FOR UPDATE
USING (auth.uid() = user_id);

-- Users can delete their own workouts
CREATE POLICY "Users can delete own workouts"
ON workout_history FOR DELETE
USING (auth.uid() = user_id);
```

### `exercise_sets` Policies

```sql
-- Enable RLS
ALTER TABLE exercise_sets ENABLE ROW LEVEL SECURITY;

-- Users can view sets from their own workouts
CREATE POLICY "Users can view own exercise sets"
ON exercise_sets FOR SELECT
USING (
    EXISTS (
        SELECT 1 FROM workout_history
        WHERE workout_history.id = exercise_sets.workout_id
        AND workout_history.user_id = auth.uid()
    )
);

-- Users can insert sets for their own workouts
CREATE POLICY "Users can insert own exercise sets"
ON exercise_sets FOR INSERT
WITH CHECK (
    EXISTS (
        SELECT 1 FROM workout_history
        WHERE workout_history.id = exercise_sets.workout_id
        AND workout_history.user_id = auth.uid()
    )
);

-- Users can delete their own sets
CREATE POLICY "Users can delete own exercise sets"
ON exercise_sets FOR DELETE
USING (
    EXISTS (
        SELECT 1 FROM workout_history
        WHERE workout_history.id = exercise_sets.workout_id
        AND workout_history.user_id = auth.uid()
    )
);
```

### `user_workout_preferences` Policies

```sql
-- Enable RLS
ALTER TABLE user_workout_preferences ENABLE ROW LEVEL SECURITY;

-- Users can view their own preferences
CREATE POLICY "Users can view own preferences"
ON user_workout_preferences FOR SELECT
USING (auth.uid() = user_id);

-- Users can insert their own preferences
CREATE POLICY "Users can insert own preferences"
ON user_workout_preferences FOR INSERT
WITH CHECK (auth.uid() = user_id);

-- Users can update their own preferences
CREATE POLICY "Users can update own preferences"
ON user_workout_preferences FOR UPDATE
USING (auth.uid() = user_id);
```

## API Endpoints to Add

The following Flask routes should be added to integrate workout tracking:

### Save Workout
```python
@app.route('/api/workouts', methods=['POST'])
@login_required
def save_workout():
    # Save completed workout to database
    pass
```

### Get Workout History
```python
@app.route('/api/workouts', methods=['GET'])
@login_required
def get_workouts():
    # Retrieve user's workout history
    pass
```

### Get Workout Stats
```python
@app.route('/api/workouts/stats', methods=['GET'])
@login_required
def get_workout_stats():
    # Return aggregated statistics
    pass
```

### Save/Update Preferences
```python
@app.route('/api/preferences', methods=['GET', 'POST'])
@login_required
def workout_preferences():
    # Get or update user preferences
    pass
```

## Setup Instructions

1. **Access Supabase Dashboard**
   - Go to your Supabase project
   - Navigate to SQL Editor

2. **Run the SQL Scripts**
   - Copy and paste each CREATE TABLE statement
   - Run the RLS policies
   - Verify tables are created in the Table Editor

3. **Test the Schema**
   - Try inserting test data
   - Verify RLS policies work correctly
   - Check that indexes are in place

## Future Enhancements

- **Analytics Dashboard**: Add charts showing progress over time
- **Exercise Library**: Expand with video demonstrations
- **Social Features**: Share workouts with other users
- **AI Coaching**: Integrate OpenAI for form tips and progression suggestions
- **Wearable Integration**: Connect with Apple Health, Fitbit, etc.
