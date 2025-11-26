// HIT Coach Pro Web App JavaScript - Redesigned

// ===== EXERCISE ICON IMAGES =====
// Gold circle icons with black silhouettes from Gemini

const ICON_PATH = './static/images/icons/';

// ===== EXERCISE DATABASE =====
// Complete mapping of exercise keys to icon filenames
const EXERCISE_ICONS = {
    // Primary exercises
    legPress: 'leg_press.png',
    pulldown: 'pull_up.png',
    chestPress: 'bench_press.png',
    benchPress: 'bench_press.png',
    overheadPress: 'overhead_press.png',
    legCurl: 'leg_curl.png',
    bicepCurl: 'bicep_curl.png',
    tricepExtension: 'tricep_extension.png',
    calfRaise: 'calf_raise.png',
    legExtension: 'leg_raise.png',
    seatedRow: 'barbell_row.png',
    inclinePress: 'incline_press.png',
    lateralRaise: 'lateral_raise.png',
    shrug: 'shrug.png',
    abCrunch: 'crunch.png',
    backExtension: 'good_morning.png',
    // Additional exercises
    squat: 'squat.png',
    deadlift: 'deadlift.png',
    barbellRow: 'barbell_row.png',
    pullUp: 'pull_up.png',
    dip: 'dip.png',
    lunge: 'lunge.png',
    frontRaise: 'front_raise.png',
    reverseFly: 'reverse_fly.png',
    dumbbellPress: 'dumbbell_press.png',
    declinePress: 'decline_press.png',
    arnoldPress: 'arnold_press.png',
    uprightRow: 'upright_row.png',
    facePull: 'face_pull.png',
    goodMorning: 'good_morning.png',
    romanianDeadlift: 'romanian_deadlift.png',
    sumoDeadlift: 'sumo_deadlift.png',
    hackSquat: 'hack_squat.png',
    bulgarianSplit: 'bulgarian_split.png',
    gluteBridge: 'glute_bridge.png',
    hipThrust: 'hip_thrust.png',
    plank: 'plank.png',
    crunch: 'crunch.png',
    legRaise: 'leg_raise.png',
    russianTwist: 'russian_twist.png',
    woodchopper: 'woodchopper.png',
    farmersWalk: 'farmers_walk.png',
    kettlebellSwing: 'kettlebell_swing.png',
    snatch: 'snatch.png',
    cleanAndJerk: 'clean_and_jerk.png'
};

// ===== DATA STRUCTURES =====

const WORKOUTS = {
    A: [
        { id: 'legPress', name: 'Leg Press', iconKey: 'legPress', muscle: 'Legs' },
        { id: 'pulldown', name: 'Pulldown', iconKey: 'pulldown', muscle: 'Back' },
        { id: 'chestPress', name: 'Chest Press', iconKey: 'chestPress', muscle: 'Chest' },
        { id: 'overheadPress', name: 'Overhead Press', iconKey: 'overheadPress', muscle: 'Shoulders' },
        { id: 'legCurl', name: 'Leg Curl', iconKey: 'legCurl', muscle: 'Hamstrings' },
        { id: 'bicepCurl', name: 'Bicep Curl', iconKey: 'bicepCurl', muscle: 'Biceps' },
        { id: 'tricepExtension', name: 'Tricep Extension', iconKey: 'tricepExtension', muscle: 'Triceps' },
        { id: 'calfRaise', name: 'Calf Raise', iconKey: 'calfRaise', muscle: 'Calves' }
    ],
    B: [
        { id: 'legExtension', name: 'Leg Extension', iconKey: 'legExtension', muscle: 'Quads' },
        { id: 'seatedRow', name: 'Seated Row', iconKey: 'seatedRow', muscle: 'Back' },
        { id: 'inclinePress', name: 'Incline Press', iconKey: 'inclinePress', muscle: 'Upper Chest' },
        { id: 'lateralRaise', name: 'Lateral Raise', iconKey: 'lateralRaise', muscle: 'Shoulders' },
        { id: 'legCurlB', name: 'Leg Curl', iconKey: 'legCurl', muscle: 'Hamstrings' },
        { id: 'shrug', name: 'Shrug', iconKey: 'shrug', muscle: 'Traps' },
        { id: 'abCrunch', name: 'Ab Crunch', iconKey: 'abCrunch', muscle: 'Abs' },
        { id: 'backExtension', name: 'Back Extension', iconKey: 'backExtension', muscle: 'Lower Back' }
    ]
};

// ===== DARDEN/HIT TRAINING LEVEL DATABASE =====
// Based on Dr. Ellington Darden's High Intensity Training research

const TRAINING_LEVELS = {
    beginner: {
        id: 'beginner',
        name: 'Beginner',
        icon: '🌱',
        description: 'New to HIT training (0-6 months)',
        weeklyFrequency: '2x per week',
        restBetweenWorkouts: '3-4 days',
        principles: [
            'Learn proper form before adding intensity',
            'Focus on mind-muscle connection',
            'Use lighter weights to master tempo',
            'Single set per exercise to near-failure'
        ],
        phaseTimings: {
            prep: 10,
            eccentric: 10,      // Slower eccentric for beginners
            concentric: 10,     // Slower concentric for control
            finalEccentric: 15  // Shorter final negative
        },
        restDuration: 90,
        routines: {
            A: [
                { id: 'legPress', name: 'Leg Press', iconKey: 'legPress', muscle: 'Legs', sets: 1, notes: 'Focus on full range of motion' },
                { id: 'chestPress', name: 'Chest Press', iconKey: 'chestPress', muscle: 'Chest', sets: 1, notes: 'Keep shoulders back' },
                { id: 'seatedRow', name: 'Seated Row', iconKey: 'seatedRow', muscle: 'Back', sets: 1, notes: 'Squeeze shoulder blades' },
                { id: 'overheadPress', name: 'Overhead Press', iconKey: 'overheadPress', muscle: 'Shoulders', sets: 1, notes: 'Control the negative' }
            ],
            B: [
                { id: 'legCurl', name: 'Leg Curl', iconKey: 'legCurl', muscle: 'Hamstrings', sets: 1, notes: 'Full contraction at top' },
                { id: 'pulldown', name: 'Pulldown', iconKey: 'pulldown', muscle: 'Back', sets: 1, notes: 'Lead with elbows' },
                { id: 'inclinePress', name: 'Incline Press', iconKey: 'inclinePress', muscle: 'Upper Chest', sets: 1, notes: 'Controlled movement' },
                { id: 'bicepCurl', name: 'Bicep Curl', iconKey: 'bicepCurl', muscle: 'Biceps', sets: 1, notes: 'No swinging' }
            ]
        }
    },
    intermediate: {
        id: 'intermediate',
        name: 'Intermediate',
        icon: '💪',
        description: '6+ months HIT experience',
        weeklyFrequency: '2-3x per week',
        restBetweenWorkouts: '2-3 days',
        principles: [
            'Increase time under tension',
            'Push closer to true muscular failure',
            'Add pre-exhaust techniques',
            'Longer negative phases for more stimulus'
        ],
        phaseTimings: {
            prep: 10,
            eccentric: 30,      // Standard Darden protocol
            concentric: 20,     // Powerful but controlled
            finalEccentric: 40  // Extended negative to failure
        },
        restDuration: 60,
        routines: {
            A: [
                { id: 'legPress', name: 'Leg Press', iconKey: 'legPress', muscle: 'Legs', sets: 1, notes: 'Deep range, 30-20-40 protocol' },
                { id: 'legCurl', name: 'Leg Curl', iconKey: 'legCurl', muscle: 'Hamstrings', sets: 1, notes: 'Pre-exhaust for legs' },
                { id: 'pulldown', name: 'Pulldown', iconKey: 'pulldown', muscle: 'Back', sets: 1, notes: 'Full stretch at top' },
                { id: 'chestPress', name: 'Chest Press', iconKey: 'chestPress', muscle: 'Chest', sets: 1, notes: 'Pause at bottom' },
                { id: 'overheadPress', name: 'Overhead Press', iconKey: 'overheadPress', muscle: 'Shoulders', sets: 1, notes: 'Strict form' },
                { id: 'bicepCurl', name: 'Bicep Curl', iconKey: 'bicepCurl', muscle: 'Biceps', sets: 1, notes: 'Squeeze at top' },
                { id: 'tricepExtension', name: 'Tricep Extension', iconKey: 'tricepExtension', muscle: 'Triceps', sets: 1, notes: 'Full lockout' },
                { id: 'calfRaise', name: 'Calf Raise', iconKey: 'calfRaise', muscle: 'Calves', sets: 1, notes: 'Pause at stretch' }
            ],
            B: [
                { id: 'legExtension', name: 'Leg Extension', iconKey: 'legExtension', muscle: 'Quads', sets: 1, notes: 'Pre-exhaust' },
                { id: 'squat', name: 'Squat', iconKey: 'squat', muscle: 'Legs', sets: 1, notes: 'After pre-exhaust' },
                { id: 'seatedRow', name: 'Seated Row', iconKey: 'seatedRow', muscle: 'Back', sets: 1, notes: 'Hold contraction' },
                { id: 'inclinePress', name: 'Incline Press', iconKey: 'inclinePress', muscle: 'Upper Chest', sets: 1, notes: 'Upper chest focus' },
                { id: 'lateralRaise', name: 'Lateral Raise', iconKey: 'lateralRaise', muscle: 'Shoulders', sets: 1, notes: 'Controlled tempo' },
                { id: 'shrug', name: 'Shrug', iconKey: 'shrug', muscle: 'Traps', sets: 1, notes: 'Hold at top 2 sec' },
                { id: 'abCrunch', name: 'Ab Crunch', iconKey: 'abCrunch', muscle: 'Abs', sets: 1, notes: 'Slow and controlled' },
                { id: 'backExtension', name: 'Back Extension', iconKey: 'backExtension', muscle: 'Lower Back', sets: 1, notes: 'No hyperextension' }
            ]
        }
    },
    advanced: {
        id: 'advanced',
        name: 'Advanced',
        icon: '🔥',
        description: '2+ years HIT experience',
        weeklyFrequency: '2x per week',
        restBetweenWorkouts: '3-4 days (more recovery needed)',
        principles: [
            'Maximum time under tension',
            'True muscular failure on every set',
            '30-10-30 Darden protocol',
            'Negative-accentuated training',
            'Inroad deeply into muscle reserves'
        ],
        phaseTimings: {
            prep: 10,
            eccentric: 30,      // 30-second negative (Darden 30-10-30)
            concentric: 10,     // 10 controlled reps
            finalEccentric: 30  // 30-second final negative
        },
        restDuration: 45,
        routines: {
            A: [
                { id: 'legExtension', name: 'Leg Extension', iconKey: 'legExtension', muscle: 'Quads', sets: 1, notes: 'Pre-exhaust, 30-10-30' },
                { id: 'legPress', name: 'Leg Press', iconKey: 'legPress', muscle: 'Legs', sets: 1, notes: 'Immediately after extension' },
                { id: 'legCurl', name: 'Leg Curl', iconKey: 'legCurl', muscle: 'Hamstrings', sets: 1, notes: '30-10-30 protocol' },
                { id: 'pulldown', name: 'Pulldown', iconKey: 'pulldown', muscle: 'Back', sets: 1, notes: 'Negative accentuated' },
                { id: 'seatedRow', name: 'Seated Row', iconKey: 'seatedRow', muscle: 'Back', sets: 1, notes: 'Compound back' },
                { id: 'chestPress', name: 'Chest Press', iconKey: 'chestPress', muscle: 'Chest', sets: 1, notes: '30-10-30' },
                { id: 'overheadPress', name: 'Overhead Press', iconKey: 'overheadPress', muscle: 'Shoulders', sets: 1, notes: 'Strict form' },
                { id: 'bicepCurl', name: 'Bicep Curl', iconKey: 'bicepCurl', muscle: 'Biceps', sets: 1, notes: 'Negative focus' },
                { id: 'tricepExtension', name: 'Tricep Extension', iconKey: 'tricepExtension', muscle: 'Triceps', sets: 1, notes: '30-10-30' },
                { id: 'calfRaise', name: 'Calf Raise', iconKey: 'calfRaise', muscle: 'Calves', sets: 1, notes: 'Deep stretch' }
            ],
            B: [
                { id: 'hipThrust', name: 'Hip Thrust', iconKey: 'hipThrust', muscle: 'Glutes', sets: 1, notes: 'Glute activation' },
                { id: 'deadlift', name: 'Deadlift', iconKey: 'deadlift', muscle: 'Back/Legs', sets: 1, notes: 'Controlled negative' },
                { id: 'legCurl', name: 'Leg Curl', iconKey: 'legCurl', muscle: 'Hamstrings', sets: 1, notes: 'After deadlift' },
                { id: 'inclinePress', name: 'Incline Press', iconKey: 'inclinePress', muscle: 'Upper Chest', sets: 1, notes: '30-10-30' },
                { id: 'dip', name: 'Dip', iconKey: 'dip', muscle: 'Chest/Triceps', sets: 1, notes: 'Negative accentuated' },
                { id: 'barbellRow', name: 'Barbell Row', iconKey: 'barbellRow', muscle: 'Back', sets: 1, notes: 'Squeeze at top' },
                { id: 'lateralRaise', name: 'Lateral Raise', iconKey: 'lateralRaise', muscle: 'Shoulders', sets: 1, notes: 'Pre-exhaust' },
                { id: 'shrug', name: 'Shrug', iconKey: 'shrug', muscle: 'Traps', sets: 1, notes: 'Heavy, controlled' },
                { id: 'abCrunch', name: 'Ab Crunch', iconKey: 'abCrunch', muscle: 'Abs', sets: 1, notes: 'Weighted' },
                { id: 'backExtension', name: 'Back Extension', iconKey: 'backExtension', muscle: 'Lower Back', sets: 1, notes: 'Hold contraction' }
            ]
        }
    }
};

// Darden's 30-10-30 Protocol explanation
const DARDEN_PROTOCOLS = {
    '30-10-30': {
        name: '30-10-30',
        description: 'Dr. Darden\'s signature protocol',
        phases: [
            '30-second negative (lowering)',
            '10 controlled reps (normal tempo)',
            '30-second final negative to failure'
        ],
        benefits: [
            'Maximum time under tension',
            'Deep muscle fiber recruitment',
            'Enhanced muscle growth stimulus',
            'Efficient - one set to failure'
        ]
    },
    'negative-accentuated': {
        name: 'Negative Accentuated',
        description: 'Emphasizes the eccentric phase',
        phases: [
            '1-second positive (concentric)',
            '4-6 second negative (eccentric)',
            'Repeat to failure'
        ],
        benefits: [
            'Greater muscle damage for growth',
            'Increased strength gains',
            'Improved muscle control'
        ]
    },
    'pre-exhaust': {
        name: 'Pre-Exhaust',
        description: 'Isolation before compound',
        phases: [
            'Isolation exercise to fatigue target muscle',
            'Immediately follow with compound movement',
            'No rest between exercises'
        ],
        benefits: [
            'Deeper fatigue in target muscle',
            'Less weight needed on compound',
            'Reduced joint stress'
        ]
    }
};

// Get routine based on user's experience level
function getRoutineForLevel(level, workoutType) {
    const levelData = TRAINING_LEVELS[level];
    if (levelData && levelData.routines && levelData.routines[workoutType]) {
        return levelData.routines[workoutType];
    }
    return TRAINING_LEVELS.intermediate.routines[workoutType]; // Default
}

// Apply level settings to app
function applyLevelSettings(level) {
    const levelData = TRAINING_LEVELS[level];
    if (!levelData) return;

    // Update phase timings
    const settings = JSON.parse(localStorage.getItem('hitCoachSettings')) || {};
    settings.phases = levelData.phaseTimings;
    settings.restDuration = levelData.restDuration;
    localStorage.setItem('hitCoachSettings', JSON.stringify(settings));

    // Update WORKOUTS with level-appropriate routines
    WORKOUTS.A = levelData.routines.A;
    WORKOUTS.B = levelData.routines.B;

    // Save to profile
    const profile = JSON.parse(localStorage.getItem('hitCoachProfile')) || {};
    profile.experience = level;
    localStorage.setItem('hitCoachProfile', JSON.stringify(profile));

    // Reload UI
    loadPhaseSettings();
    renderExerciseList();
}

// All available exercises for adding to workouts
const ALL_EXERCISES = [
    { id: 'legPress', name: 'Leg Press', iconKey: 'legPress', muscle: 'Legs' },
    { id: 'squat', name: 'Squat', iconKey: 'squat', muscle: 'Legs' },
    { id: 'deadlift', name: 'Deadlift', iconKey: 'deadlift', muscle: 'Back/Legs' },
    { id: 'benchPress', name: 'Bench Press', iconKey: 'benchPress', muscle: 'Chest' },
    { id: 'inclinePress', name: 'Incline Press', iconKey: 'inclinePress', muscle: 'Upper Chest' },
    { id: 'overheadPress', name: 'Overhead Press', iconKey: 'overheadPress', muscle: 'Shoulders' },
    { id: 'pullUp', name: 'Pull-up', iconKey: 'pullUp', muscle: 'Back' },
    { id: 'barbellRow', name: 'Barbell Row', iconKey: 'barbellRow', muscle: 'Back' },
    { id: 'bicepCurl', name: 'Bicep Curl', iconKey: 'bicepCurl', muscle: 'Biceps' },
    { id: 'tricepExtension', name: 'Tricep Extension', iconKey: 'tricepExtension', muscle: 'Triceps' },
    { id: 'lateralRaise', name: 'Lateral Raise', iconKey: 'lateralRaise', muscle: 'Shoulders' },
    { id: 'legCurl', name: 'Leg Curl', iconKey: 'legCurl', muscle: 'Hamstrings' },
    { id: 'legExtension', name: 'Leg Extension', iconKey: 'legExtension', muscle: 'Quads' },
    { id: 'calfRaise', name: 'Calf Raise', iconKey: 'calfRaise', muscle: 'Calves' },
    { id: 'shrug', name: 'Shrug', iconKey: 'shrug', muscle: 'Traps' },
    { id: 'dip', name: 'Dip', iconKey: 'dip', muscle: 'Chest/Triceps' },
    { id: 'lunge', name: 'Lunge', iconKey: 'lunge', muscle: 'Legs' },
    { id: 'hipThrust', name: 'Hip Thrust', iconKey: 'hipThrust', muscle: 'Glutes' },
    { id: 'crunch', name: 'Crunch', iconKey: 'crunch', muscle: 'Abs' },
    { id: 'plank', name: 'Plank', iconKey: 'plank', muscle: 'Core' },
    { id: 'goodMorning', name: 'Good Morning', iconKey: 'goodMorning', muscle: 'Lower Back' },
    { id: 'facePull', name: 'Face Pull', iconKey: 'facePull', muscle: 'Rear Delts' },
    { id: 'kettlebellSwing', name: 'Kettlebell Swing', iconKey: 'kettlebellSwing', muscle: 'Full Body' },
    { id: 'farmersWalk', name: "Farmer's Walk", iconKey: 'farmersWalk', muscle: 'Full Body' }
];

// Helper function to get icon image
function getExerciseIcon(iconKey) {
    const iconFile = EXERCISE_ICONS[iconKey];
    if (iconFile) {
        return `<img src="${ICON_PATH}${iconFile}" alt="${iconKey}" class="exercise-icon-img">`;
    }
    // Fallback gold circle
    return '<div class="exercise-icon-fallback"></div>';
}

// Default phase durations
const DEFAULT_PHASES = {
    PREP: 10,
    POSITIONING: 5,
    ECCENTRIC: 30,
    CONCENTRIC: 20,
    FINAL_ECCENTRIC: 40
};

// Timer phases (will be populated from settings or defaults)
let TIMER_PHASES = {
    PREP: { duration: 10, name: 'Prep', description: 'Get your weight ready' },
    POSITIONING: { duration: 5, name: 'Position', description: 'Get into eccentric position' },
    ECCENTRIC: { duration: 30, name: 'Eccentric', description: 'Slow, controlled lowering' },
    CONCENTRIC: { duration: 20, name: 'Concentric', description: 'Powerful lifting phase' },
    FINAL_ECCENTRIC: { duration: 40, name: 'Final Eccentric', description: 'Extended negative to failure' }
};

// ===== STATE MANAGEMENT =====

let currentWorkoutType = 'A';
let currentExerciseIndex = 0;
let currentPhase = null;
let timerInterval = null;
let restInterval = null;
let timeRemaining = 0;
let isPaused = false;
let workoutStartTime = null;
let currentWorkoutData = [];
let voiceEnabled = true;
let voiceGender = 'female';
let currentVoiceStyle = 'commander';
let synth = window.speechSynthesis;

// ===== VOICE/TRAINING STYLE DATABASE =====
const VOICE_STYLES = {
    commander: {
        id: 'commander',
        name: 'Commander',
        description: 'Intense military-style coaching',
        icon: '🎖️',
        isPro: true,
        hasAudio: true,
        phrases: {
            startWorkout: "Let's get to work, soldier!",
            prep: "Prepare yourself. Focus.",
            positioning: "Get into position. Lock it in.",
            eccentric: "Begin eccentric. Slow and controlled. Fight the weight.",
            concentric: "Drive it up! Power through!",
            finalEccentric: "Final eccentric. This is where champions are made. Push to failure!",
            complete: "Outstanding work. Exercise complete.",
            restStart: "Rest period. Recover and prepare.",
            restEnd: "Rest complete. Back to battle.",
            workoutComplete: "Mission accomplished. Excellent performance.",
            motivation: [
                "Pain is weakness leaving the body!",
                "Dig deep! Find that inner strength!",
                "This is what separates winners!",
                "Your body wants to quit. Your mind says no!",
                "Embrace the burn!"
            ]
        }
    },
    zen: {
        id: 'zen',
        name: 'Zen Master',
        description: 'Calm, mindful guidance',
        icon: '🧘',
        isPro: true,
        hasAudio: false,
        phrases: {
            startWorkout: "Let us begin. Breathe deeply.",
            prep: "Center yourself. Find your balance.",
            positioning: "Settle into position. Feel the connection.",
            eccentric: "Lower with intention. Feel every fiber.",
            concentric: "Rise with purpose. Breathe out.",
            finalEccentric: "Final descent. Stay present. Embrace it.",
            complete: "Well done. Take a breath.",
            restStart: "Rest now. Let your body recover.",
            restEnd: "Return to presence. We continue.",
            workoutComplete: "Your practice is complete. Namaste.",
            motivation: [
                "The mind leads, the body follows.",
                "In stillness, we find strength.",
                "Each rep is a meditation.",
                "Be present in this moment.",
                "Strength flows from inner peace."
            ]
        }
    },
    hype: {
        id: 'hype',
        name: 'Hype Coach',
        description: 'High-energy motivation',
        icon: '🔥',
        isPro: true,
        hasAudio: false,
        phrases: {
            startWorkout: "LET'S GOOO! Time to crush it!",
            prep: "Get hyped! This is YOUR moment!",
            positioning: "Lock it in! You got this!",
            eccentric: "Down we go! Control it! YEAHHH!",
            concentric: "PUSH IT! EXPLODE! LET'S GO!",
            finalEccentric: "FINAL REP! EVERYTHING YOU GOT!",
            complete: "YESSSS! Crushed it! Beast mode!",
            restStart: "Quick breather! Stay fired up!",
            restEnd: "Back at it! Energy UP!",
            workoutComplete: "INCREDIBLE! You're a MACHINE!",
            motivation: [
                "You're KILLING IT!",
                "Nobody can stop you!",
                "This is greatness!",
                "UNSTOPPABLE!",
                "Pure FIRE right now!"
            ]
        }
    },
    technical: {
        id: 'technical',
        name: 'Technical',
        description: 'Precise, form-focused',
        icon: '📐',
        isPro: false,
        hasAudio: false,
        phrases: {
            startWorkout: "Beginning workout. Focus on form.",
            prep: "Prepare. Check posture and grip.",
            positioning: "Position set. Engage core.",
            eccentric: "Eccentric phase. 3-second descent.",
            concentric: "Concentric phase. Drive through.",
            finalEccentric: "Final eccentric. Maintain form.",
            complete: "Exercise complete. Good execution.",
            restStart: "Rest interval initiated.",
            restEnd: "Rest complete. Next exercise.",
            workoutComplete: "Workout complete.",
            motivation: [
                "Perfect form, perfect results.",
                "Quality over quantity.",
                "Control is strength.",
                "Precision builds power.",
                "Master the basics."
            ]
        }
    },
    friendly: {
        id: 'friendly',
        name: 'Friendly',
        description: 'Encouraging and supportive',
        icon: '😊',
        isPro: false,
        hasAudio: false,
        phrases: {
            startWorkout: "Ready for a great workout?",
            prep: "Take your time, get comfortable.",
            positioning: "Looking good! Get set up.",
            eccentric: "Nice and slow. You're doing great!",
            concentric: "And push! Awesome job!",
            finalEccentric: "Last one! You can do it!",
            complete: "Fantastic! You did it!",
            restStart: "Take a breather. You earned it!",
            restEnd: "Ready? Let's keep going!",
            workoutComplete: "Amazing workout! So proud!",
            motivation: [
                "You're doing amazing!",
                "Every rep counts!",
                "I believe in you!",
                "Stronger than you think!",
                "Keep it up!"
            ]
        }
    },
    male: {
        id: 'male',
        name: 'Male',
        description: 'Standard male voice',
        icon: 'M',
        isPro: false,
        hasAudio: false,
        usesTTS: true,
        ttsVoice: 'male',
        phrases: null
    },
    female: {
        id: 'female',
        name: 'Female',
        description: 'Standard female voice',
        icon: 'F',
        isPro: false,
        hasAudio: false,
        usesTTS: true,
        ttsVoice: 'female',
        phrases: null
    }
};

// Get phrase for current voice style
function getVoicePhrase(phraseKey) {
    const style = VOICE_STYLES[currentVoiceStyle];
    if (style && style.phrases && style.phrases[phraseKey]) {
        return style.phrases[phraseKey];
    }
    return VOICE_STYLES.friendly.phrases[phraseKey] || '';
}

// Get random motivation phrase
function getMotivationalPhrase() {
    const style = VOICE_STYLES[currentVoiceStyle];
    if (style && style.phrases && style.phrases.motivation) {
        const phrases = style.phrases.motivation;
        return phrases[Math.floor(Math.random() * phrases.length)];
    }
    return "Keep going!";
}

// Set voice style
function setVoiceStyle(styleId) {
    if (VOICE_STYLES[styleId]) {
        currentVoiceStyle = styleId;
        const settings = JSON.parse(localStorage.getItem('hitCoachSettings')) || {};
        settings.voiceStyle = styleId;
        localStorage.setItem('hitCoachSettings', JSON.stringify(settings));
        updateVoiceStyleUI();

        // Enable/disable commander voice based on selection
        if (styleId === 'commander') {
            useCommanderVoice = true;
            // Try to play commander audio sample, fall back to TTS
            const audio = new Audio(AUDIO_PATH + AUDIO_FILES.workout.begin);
            audio.play().then(() => {
                console.log('Commander audio playing');
            }).catch(err => {
                console.log('Commander audio failed, using TTS:', err);
                speakTTS("Commander voice activated. Let's get to work, soldier!", true);
            });
        } else {
            useCommanderVoice = false;
            // Speak the style's start phrase as a sample
            const style = VOICE_STYLES[styleId];
            const samplePhrase = style.phrases ? style.phrases.startWorkout : `${style.name} voice selected`;
            speakTTS(samplePhrase, true);
        }

        console.log(`Voice style set to: ${styleId}`);
    }
}

// Update voice style UI
function updateVoiceStyleUI() {
    document.querySelectorAll('.voice-style-card').forEach(card => {
        card.classList.toggle('active', card.dataset.style === currentVoiceStyle);
    });

    // Also update the old commander card if it exists
    document.getElementById('voiceCommanderCard')?.classList.toggle('active', currentVoiceStyle === 'commander');
}

// ===== INITIALIZATION =====

document.addEventListener('DOMContentLoaded', () => {
    loadSettings();
    loadPhaseSettings();
    loadProfile();
    loadCustomWorkouts();
    loadProfiles();
    loadDuoModeSetting();
    renderExerciseList();
    loadStats();
    loadLog();

    // Load voices when available
    if (speechSynthesis.onvoiceschanged !== undefined) {
        speechSynthesis.onvoiceschanged = () => {
            speechSynthesis.getVoices();
        };
    }

    // Prevent screen sleep on mobile
    if ('wakeLock' in navigator) {
        navigator.wakeLock.request('screen').catch(err => {
            console.log('Wake lock error:', err);
        });
    }

    // Show install prompt after a delay
    setTimeout(showInstallPrompt, 5000);
});

// ===== EXERCISE LIST RENDERING =====

function renderExerciseList() {
    const list = document.getElementById('exerciseList');
    const exercises = WORKOUTS[currentWorkoutType];

    let html = exercises.map((exercise, index) => `
        <div class="exercise-item" onclick="showExerciseSetup(${index})">
            <div class="exercise-icon">${getExerciseIcon(exercise.iconKey)}</div>
            <div class="exercise-info">
                <div class="exercise-name">${exercise.name}</div>
                <div class="exercise-muscle">${exercise.muscle}</div>
            </div>
            <div class="exercise-chevron">›</div>
        </div>
    `).join('');

    // Add "Add Exercise" card
    html += `
        <div class="exercise-item add-exercise-item" onclick="showAddExercise()">
            <div class="exercise-icon add-exercise-icon">
                <span class="add-icon">+</span>
            </div>
            <div class="exercise-info">
                <div class="exercise-name">Add Exercise</div>
                <div class="exercise-muscle">Customize your workout</div>
            </div>
            <div class="exercise-chevron">›</div>
        </div>
    `;

    list.innerHTML = html;
}

// Show add exercise modal
function showAddExercise() {
    const modal = document.getElementById('addExerciseModal');
    if (modal) {
        populateExerciseSelector();
        modal.classList.add('active');
    }
}

function closeAddExerciseModal() {
    const modal = document.getElementById('addExerciseModal');
    if (modal) modal.classList.remove('active');
}

function populateExerciseSelector() {
    const list = document.getElementById('exerciseSelectorList');
    if (!list) return;

    // Filter out exercises already in current workout
    const currentExerciseIds = WORKOUTS[currentWorkoutType].map(e => e.id);
    const availableExercises = ALL_EXERCISES.filter(e => !currentExerciseIds.includes(e.id));

    list.innerHTML = availableExercises.map(exercise => `
        <div class="exercise-item" onclick="addExerciseToWorkout('${exercise.id}')">
            <div class="exercise-icon">${getExerciseIcon(exercise.iconKey)}</div>
            <div class="exercise-info">
                <div class="exercise-name">${exercise.name}</div>
                <div class="exercise-muscle">${exercise.muscle}</div>
            </div>
            <div class="exercise-chevron">+</div>
        </div>
    `).join('');
}

function addExerciseToWorkout(exerciseId) {
    const exercise = ALL_EXERCISES.find(e => e.id === exerciseId);
    if (exercise) {
        WORKOUTS[currentWorkoutType].push({ ...exercise });
        saveCustomWorkouts();
        renderExerciseList();
        closeAddExerciseModal();
    }
}

function saveCustomWorkouts() {
    localStorage.setItem('hitCoachCustomWorkouts', JSON.stringify(WORKOUTS));
}

function loadCustomWorkouts() {
    const saved = localStorage.getItem('hitCoachCustomWorkouts');
    if (saved) {
        const customWorkouts = JSON.parse(saved);
        WORKOUTS.A = customWorkouts.A || WORKOUTS.A;
        WORKOUTS.B = customWorkouts.B || WORKOUTS.B;
    }
}

// ===== WORKOUT TAB SWITCHING =====

function switchWorkoutTab(type) {
    currentWorkoutType = type;

    // Update tab UI
    document.getElementById('tabA').classList.toggle('active', type === 'A');
    document.getElementById('tabB').classList.toggle('active', type === 'B');

    // Re-render exercise list
    renderExerciseList();
}

// ===== BOTTOM NAVIGATION =====

function navigateTo(section) {
    // Update nav items
    document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));

    // Show/hide workout tabs
    const workoutTabs = document.getElementById('workoutTabs');

    switch (section) {
        case 'workouts':
            document.getElementById('navWorkouts').classList.add('active');
            workoutTabs.style.display = 'flex';
            showScreen('homeScreen');
            break;
        case 'stats':
            document.getElementById('navStats').classList.add('active');
            workoutTabs.style.display = 'none';
            loadStats();
            showScreen('statsScreen');
            break;
        case 'log':
            document.getElementById('navLog').classList.add('active');
            workoutTabs.style.display = 'none';
            loadLog();
            showScreen('logScreen');
            break;
        case 'settings':
            workoutTabs.style.display = 'none';
            loadSettingsUI();
            showScreen('settingsScreen');
            break;
        case 'profile':
            workoutTabs.style.display = 'none';
            loadProfileUI();
            showScreen('profileScreen');
            break;
        case 'siri':
            workoutTabs.style.display = 'none';
            loadSiriShortcuts();
            showScreen('siriScreen');
            break;
    }
}

// ===== SCREEN NAVIGATION =====

function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    document.getElementById(screenId).classList.add('active');

    // Show/hide workout tabs and bottom nav based on screen
    const workoutTabs = document.getElementById('workoutTabs');
    const bottomNav = document.getElementById('bottomNav');

    if (screenId === 'homeScreen') {
        workoutTabs.style.display = 'flex';
        bottomNav.style.display = 'flex';
    } else if (screenId === 'workoutScreen' || screenId === 'summaryScreen' || screenId === 'exerciseSetupScreen') {
        workoutTabs.style.display = 'none';
        bottomNav.style.display = 'none';
    } else if (screenId === 'settingsScreen' || screenId === 'profileScreen') {
        workoutTabs.style.display = 'none';
        bottomNav.style.display = 'flex';
    } else if (screenId === 'statsScreen' || screenId === 'logScreen') {
        workoutTabs.style.display = 'none';
        bottomNav.style.display = 'flex';
    }
}

// ===== WORKOUT MANAGEMENT =====

function showExerciseSetup(exerciseIndex) {
    currentExerciseIndex = exerciseIndex;

    // Initialize workout data if starting fresh
    if (workoutStartTime === null) {
        workoutStartTime = new Date();
        currentWorkoutData = [];
    }

    const exercises = WORKOUTS[currentWorkoutType];
    const exercise = exercises[currentExerciseIndex];

    // Update setup screen content
    document.getElementById('setupTitle').textContent = `Setup - ${exercise.name}`;
    document.getElementById('setupCounter').textContent = `${currentExerciseIndex + 1} / ${exercises.length}`;
    document.getElementById('setupExerciseName').textContent = exercise.name;
    document.getElementById('setupExerciseIcon').innerHTML = getExerciseIcon(exercise.iconKey);
    document.getElementById('setupMuscle').textContent = exercise.muscle;

    // Update Siri phrase display
    document.getElementById('siriExerciseName').textContent = exercise.name;
    document.getElementById('siriWorkoutName').textContent = currentWorkoutType === 'A' ? 'push' : 'pull';

    // Load last weight
    const lastWeight = getLastWeight(exercise.name);
    const setupWeightInput = document.getElementById('setupWeightInput');
    const setupLastWeight = document.getElementById('setupLastWeight');

    if (lastWeight) {
        setupLastWeight.textContent = `Last time: ${lastWeight} lbs`;
        setupWeightInput.value = lastWeight;
    } else {
        setupLastWeight.textContent = '';
        setupWeightInput.value = '';
    }

    // Hide workout tabs, show setup screen
    document.getElementById('workoutTabs').style.display = 'none';
    document.getElementById('bottomNav').style.display = 'none';
    showScreen('exerciseSetupScreen');
}

function startExerciseFromSetup() {
    // Get weight from setup screen
    const setupWeight = document.getElementById('setupWeightInput').value;

    // Transfer to workout screen
    document.getElementById('workoutTitle').textContent = `Workout ${currentWorkoutType}`;
    showScreen('workoutScreen');
    loadExercise();

    // Pre-fill the weight from setup
    if (setupWeight) {
        document.getElementById('weightInput').value = setupWeight;
    }

    // Start the exercise automatically
    startExercise();
}

function skipToNextExercise() {
    const exercises = WORKOUTS[currentWorkoutType];

    if (currentExerciseIndex < exercises.length - 1) {
        currentExerciseIndex++;
        showExerciseSetup(currentExerciseIndex);
        speak('Skipping to next exercise');
    } else {
        // No more exercises, go back to home
        speak('No more exercises in this workout');
        navigateTo('workouts');
    }
}

function addSiriShortcut(shortcutType) {
    const exercise = WORKOUTS[currentWorkoutType][currentExerciseIndex];
    let shortcutURL = '';
    let shortcutTitle = '';
    let shortcutPhrase = '';

    // Get the base URL (current page URL without query params)
    const baseURL = window.location.origin + window.location.pathname;

    switch (shortcutType) {
        case 'start-exercise':
            shortcutURL = `${baseURL}?action=start-exercise-${currentWorkoutType.toLowerCase()}-${currentExerciseIndex}`;
            shortcutTitle = `Start ${exercise.name}`;
            shortcutPhrase = `Start ${exercise.name}`;
            break;
        case 'start-workout':
            shortcutURL = `${baseURL}?action=start-workout-${currentWorkoutType.toLowerCase()}`;
            shortcutTitle = `Start Workout ${currentWorkoutType}`;
            shortcutPhrase = currentWorkoutType === 'A' ? 'Start my push workout' : 'Start my pull workout';
            break;
        case 'view-stats':
            shortcutURL = `${baseURL}?action=view-stats`;
            shortcutTitle = 'View Workout Stats';
            shortcutPhrase = 'Show my workout stats';
            break;
    }

    // Show instructions for adding to Siri
    const instructions = `To add "${shortcutTitle}" to Siri Shortcuts:

1. Open the Shortcuts app on your iPhone
2. Tap the + button to create a new shortcut
3. Search for "Open URL" and add it
4. Enter this URL: ${shortcutURL}
5. Tap the shortcut name and rename it
6. Tap "Add to Siri" and record: "${shortcutPhrase}"

Alternatively, you can bookmark this URL and say the phrase to Siri when the app is installed as a PWA.`;

    // Check if we can use the Web Share API
    if (navigator.share) {
        navigator.share({
            title: shortcutTitle,
            text: `Open HIT Coach Pro and ${shortcutTitle.toLowerCase()}`,
            url: shortcutURL
        }).catch(() => {
            // If share fails, show alert
            alert(instructions);
        });
    } else {
        // Copy URL to clipboard and show instructions
        navigator.clipboard.writeText(shortcutURL).then(() => {
            alert(`URL copied to clipboard!\n\n${instructions}`);
        }).catch(() => {
            alert(instructions);
        });
    }

    speak(`Adding ${shortcutTitle} shortcut`);
}

function startWorkoutFromExercise(exerciseIndex) {
    currentExerciseIndex = exerciseIndex;
    workoutStartTime = new Date();
    currentWorkoutData = [];

    document.getElementById('workoutTitle').textContent = `Workout ${currentWorkoutType}`;
    showScreen('workoutScreen');
    loadExercise();
}

function exitWorkout() {
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
    }
    if (restInterval) {
        clearInterval(restInterval);
        restInterval = null;
    }
    isPaused = false;
    navigateTo('workouts');
}

function loadExercise() {
    const exercises = WORKOUTS[currentWorkoutType];
    const exercise = exercises[currentExerciseIndex];

    document.getElementById('exerciseName').textContent = exercise.name;
    document.getElementById('exerciseCounter').textContent = `${currentExerciseIndex + 1} / ${exercises.length}`;
    document.getElementById('exerciseIconDisplay').innerHTML = getExerciseIcon(exercise.iconKey);

    // Load last weight for this exercise
    const lastWeight = getLastWeight(exercise.name);
    if (lastWeight) {
        document.getElementById('lastWeight').textContent = `Last time: ${lastWeight} lbs`;
        document.getElementById('weightInput').value = lastWeight;
    } else {
        document.getElementById('lastWeight').textContent = '';
        document.getElementById('weightInput').value = '';
    }

    // Reset UI
    resetExerciseUI();
}

function resetExerciseUI() {
    document.getElementById('phaseIndicator').textContent = 'Ready';
    document.getElementById('timerDisplay').textContent = '00:00';
    document.getElementById('phaseDescription').textContent = 'Tap START to begin';
    document.getElementById('progressBar').style.width = '0%';
    document.getElementById('startBtn').style.display = 'block';
    document.getElementById('pauseBtn').style.display = 'none';
    document.getElementById('resumeBtn').style.display = 'none';
    document.getElementById('completeSection').style.display = 'none';
    document.getElementById('restScreen').style.display = 'none';
    document.getElementById('failureCheck').checked = false;
}

function getLastWeight(exerciseName) {
    const history = JSON.parse(localStorage.getItem('workoutHistory')) || [];
    for (let i = history.length - 1; i >= 0; i--) {
        const workout = history[i];
        for (let exercise of workout.exercises) {
            if (exercise.name === exerciseName) {
                return exercise.weight;
            }
        }
    }
    return null;
}

// ===== TIMER FUNCTIONS =====

function startExercise() {
    document.getElementById('startBtn').style.display = 'none';
    document.getElementById('pauseBtn').style.display = 'block';

    const exercise = WORKOUTS[currentWorkoutType][currentExerciseIndex];

    // Play exercise name with commander voice
    if (useCommanderVoice) {
        playExerciseName(exercise.name);
        setTimeout(() => {
            startPhase('PREP');
        }, 1500); // Wait for exercise name to finish
    } else {
        speak(`Starting ${exercise.name}. ${getMotivationalPhrase()}`, true);
        startPhase('PREP');
    }
}

function startPhase(phaseName) {
    currentPhase = phaseName;
    const phase = TIMER_PHASES[phaseName];
    timeRemaining = phase.duration;

    document.getElementById('phaseIndicator').textContent = phase.name;
    document.getElementById('phaseDescription').textContent = phase.description;
    updateTimerDisplay();

    // Commander voice announcements
    if (useCommanderVoice) {
        if (phaseName === 'PREP') {
            playAudio(AUDIO_FILES.phases.prep);
        } else if (phaseName === 'POSITIONING') {
            playAudio(AUDIO_FILES.cues.getPosition);
        } else if (phaseName === 'ECCENTRIC') {
            playAudio(AUDIO_FILES.phases.eccentric);
        } else if (phaseName === 'CONCENTRIC') {
            playAudio(AUDIO_FILES.phases.concentric);
        } else if (phaseName === 'FINAL_ECCENTRIC') {
            playAudio(AUDIO_FILES.phases.finalEccentric);
        }
    } else {
        // Fallback TTS
        if (phaseName === 'POSITIONING') {
            speak('Get into position', true);
        } else if (phaseName === 'ECCENTRIC') {
            speak('Begin eccentric. Slow and controlled.', true);
        } else if (phaseName === 'CONCENTRIC') {
            speak('Begin concentric. Powerful lift.', true);
        } else if (phaseName === 'FINAL_ECCENTRIC') {
            speak('Final eccentric. Push to failure.', true);
        }
    }

    runTimer();
}

function runTimer() {
    const totalDuration = TIMER_PHASES[currentPhase].duration;

    timerInterval = setInterval(() => {
        if (isPaused) return;

        timeRemaining--;
        updateTimerDisplay();
        updateProgressBar(timeRemaining, totalDuration);

        // Continuous countdown for all voice styles
        // Skip 3 seconds after a cue to prevent any overlap
        const isCueMoment = (
            (currentPhase === 'ECCENTRIC' && timeRemaining === 15) ||
            (currentPhase === 'CONCENTRIC' && timeRemaining === 10) ||
            (currentPhase === 'FINAL_ECCENTRIC' && timeRemaining === 20) ||
            (currentPhase === 'FINAL_ECCENTRIC' && timeRemaining === 10)
        );
        const isSkipMoment = (
            // Skip 3 seconds after each cue for no overlap
            (currentPhase === 'ECCENTRIC' && [14, 13, 12].includes(timeRemaining)) ||
            (currentPhase === 'CONCENTRIC' && [9, 8, 7].includes(timeRemaining)) ||
            (currentPhase === 'FINAL_ECCENTRIC' && [19, 18, 17].includes(timeRemaining)) ||
            (currentPhase === 'FINAL_ECCENTRIC' && [9, 8, 7].includes(timeRemaining))
        );

        if (isCueMoment) {
            // Play cue only (no number) - gives full second for cue
            if (currentPhase === 'ECCENTRIC' && timeRemaining === 15) {
                if (useCommanderVoice) {
                    playEccentricCue();
                } else {
                    speak(getMotivationalPhrase());
                }
            } else if (currentPhase === 'CONCENTRIC' && timeRemaining === 10) {
                if (useCommanderVoice) {
                    playConcentricCue();
                } else {
                    speak('Push! Drive it up!');
                }
            } else if (currentPhase === 'FINAL_ECCENTRIC' && timeRemaining === 20) {
                if (useCommanderVoice) {
                    playAudio(AUDIO_FILES.time.halfway);
                } else {
                    speak('Halfway there!');
                }
            } else if (currentPhase === 'FINAL_ECCENTRIC' && timeRemaining === 10) {
                if (useCommanderVoice) {
                    playFinalCue();
                } else {
                    speak('Final ten! Give everything!');
                }
            }
        } else if (isSkipMoment) {
            // Skip this count to let cue finish (no overlap)
        } else if (timeRemaining >= 1 && timeRemaining <= 60) {
            // Normal counting
            if (useCommanderVoice) {
                playNumber(timeRemaining);
            } else {
                speak(String(timeRemaining));
            }
        }

        if (timeRemaining <= 0) {
            clearInterval(timerInterval);
            moveToNextPhase();
        }
    }, 1000);
}

function moveToNextPhase() {
    const phases = ['PREP', 'POSITIONING', 'ECCENTRIC', 'CONCENTRIC', 'FINAL_ECCENTRIC'];
    const currentIndex = phases.indexOf(currentPhase);

    if (currentIndex < phases.length - 1) {
        startPhase(phases[currentIndex + 1]);
    } else {
        finishExercise();
    }
}

function updateTimerDisplay() {
    const minutes = Math.floor(timeRemaining / 60);
    const seconds = timeRemaining % 60;
    document.getElementById('timerDisplay').textContent =
        `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}

function updateProgressBar(remaining, total) {
    const percentage = ((total - remaining) / total) * 100;
    document.getElementById('progressBar').style.width = percentage + '%';
}

function pauseExercise() {
    isPaused = true;
    document.getElementById('pauseBtn').style.display = 'none';
    document.getElementById('resumeBtn').style.display = 'block';
    speak('Paused', true);
}

function resumeExercise() {
    isPaused = false;
    document.getElementById('pauseBtn').style.display = 'block';
    document.getElementById('resumeBtn').style.display = 'none';
    speak('Resuming', true);
}

function finishExercise() {
    speak('Exercise complete!', true);
    document.getElementById('pauseBtn').style.display = 'none';
    document.getElementById('completeSection').style.display = 'block';
}

function redoExercise() {
    resetExerciseUI();
    speak("Let's try that again");
}

function completeExercise() {
    const exercise = WORKOUTS[currentWorkoutType][currentExerciseIndex];
    const weight = parseFloat(document.getElementById('weightInput').value) || 0;
    const reachedFailure = document.getElementById('failureCheck').checked;

    if (weight === 0) {
        alert('Please enter the weight used for this exercise');
        return;
    }

    // Save exercise data
    currentWorkoutData.push({
        name: exercise.name,
        weight: weight,
        failure: reachedFailure,
        timestamp: new Date()
    });

    // Move to next exercise or finish workout
    if (currentExerciseIndex < WORKOUTS[currentWorkoutType].length - 1) {
        currentExerciseIndex++;
        startRestPeriod();
    } else {
        finishWorkout();
    }
}

// ===== REST PERIOD =====

function startRestPeriod() {
    const settings = loadSettings();
    let restTime = settings.restDuration || 60;

    const nextExercise = WORKOUTS[currentWorkoutType][currentExerciseIndex];
    document.getElementById('nextExercise').textContent = nextExercise.name;
    document.getElementById('restScreen').style.display = 'block';
    document.getElementById('completeSection').style.display = 'none';
    document.getElementById('restTimer').textContent = restTime;

    speak(`Rest for ${restTime} seconds. Next: ${nextExercise.name}`);

    restInterval = setInterval(() => {
        restTime--;
        document.getElementById('restTimer').textContent = restTime;

        if (restTime === 5) {
            speak(`5 seconds. Next: ${nextExercise.name}`);
        }

        if (restTime <= 0) {
            clearInterval(restInterval);
            document.getElementById('restScreen').style.display = 'none';
            loadExercise();
            speak(`Let's do ${nextExercise.name}`);
        }
    }, 1000);
}

function skipRest() {
    if (restInterval) {
        clearInterval(restInterval);
        restInterval = null;
    }
    document.getElementById('restScreen').style.display = 'none';
    loadExercise();
}

// ===== WORKOUT SUMMARY =====

function finishWorkout() {
    const duration = Math.floor((new Date() - workoutStartTime) / 1000);
    const minutes = Math.floor(duration / 60);
    const seconds = duration % 60;

    const failureCount = currentWorkoutData.filter(ex => ex.failure).length;

    document.getElementById('summaryExercises').textContent = currentWorkoutData.length;
    document.getElementById('summaryDuration').textContent = `${minutes}:${String(seconds).padStart(2, '0')}`;
    document.getElementById('summaryFailures').textContent = failureCount;

    // Build exercise list
    const summaryList = document.getElementById('summaryExerciseList');
    summaryList.innerHTML = '<h3>Exercises Completed</h3>';

    currentWorkoutData.forEach(exercise => {
        const div = document.createElement('div');
        div.className = 'summary-exercise-item';
        div.innerHTML = `
            <span>${exercise.name}</span>
            <span>${exercise.weight} lbs ${exercise.failure ? '✓' : ''}</span>
        `;
        summaryList.appendChild(div);
    });

    // Save to history
    saveWorkoutToHistory();

    speak('Workout complete! Amazing job today!', true);
    showScreen('summaryScreen');
}

function saveWorkoutToHistory() {
    const history = JSON.parse(localStorage.getItem('workoutHistory')) || [];

    history.push({
        type: currentWorkoutType,
        date: new Date(),
        exercises: currentWorkoutData,
        duration: Math.floor((new Date() - workoutStartTime) / 1000)
    });

    localStorage.setItem('workoutHistory', JSON.stringify(history));
}

function finishAndGoHome() {
    navigateTo('workouts');
}

function shareWorkout() {
    const exercises = currentWorkoutData.map(ex =>
        `${ex.name}: ${ex.weight} lbs${ex.failure ? ' ✓' : ''}`
    ).join('\n');

    const text = `HIT Coach Pro - Workout ${currentWorkoutType}\n${exercises}\n\nCompleted with HIT Coach Pro`;

    if (navigator.share) {
        navigator.share({
            title: 'HIT Coach Pro Workout',
            text: text
        });
    } else {
        navigator.clipboard.writeText(text).then(() => {
            alert('Workout copied to clipboard!');
        });
    }
}

// ===== STATS SCREEN =====

function loadStats() {
    const history = JSON.parse(localStorage.getItem('workoutHistory')) || [];
    const statsContent = document.getElementById('statsContent');

    if (history.length === 0) {
        statsContent.innerHTML = `
            <div class="stats-empty">
                <div class="stats-empty-icon">📊</div>
                <p>No workout data yet.<br>Complete your first workout to see stats!</p>
            </div>
        `;
        return;
    }

    // Calculate stats
    const totalWorkouts = history.length;
    const totalExercises = history.reduce((sum, w) => sum + w.exercises.length, 0);
    const totalDuration = history.reduce((sum, w) => sum + (w.duration || 0), 0);
    const totalFailures = history.reduce((sum, w) => sum + w.exercises.filter(e => e.failure).length, 0);

    const avgDuration = Math.floor(totalDuration / totalWorkouts / 60);
    const failureRate = Math.round((totalFailures / totalExercises) * 100);

    statsContent.innerHTML = `
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">${totalWorkouts}</div>
                <div class="stat-label">Workouts</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${totalExercises}</div>
                <div class="stat-label">Exercises</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${avgDuration}m</div>
                <div class="stat-label">Avg Duration</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${failureRate}%</div>
                <div class="stat-label">Failure Rate</div>
            </div>
        </div>
    `;
}

// ===== LOG SCREEN =====

function loadLog() {
    const history = JSON.parse(localStorage.getItem('workoutHistory')) || [];
    const logList = document.getElementById('logList');

    if (history.length === 0) {
        logList.innerHTML = '<p style="text-align: center; color: var(--text-gray); padding: 2rem;">No workout history yet.</p>';
        return;
    }

    logList.innerHTML = '';

    // Reverse to show newest first
    [...history].reverse().forEach((workout) => {
        const date = new Date(workout.date);
        const dateStr = date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        const entry = document.createElement('div');
        entry.className = 'log-entry';
        entry.dataset.workout = workout.type;

        let exercisesHTML = workout.exercises.map(ex => `
            <div class="log-exercise">
                <span class="log-exercise-name">${ex.name}</span>
                <span>
                    <span class="log-exercise-weight">${ex.weight} lbs</span>
                    ${ex.failure ? '<span class="log-exercise-failure">✓</span>' : ''}
                </span>
            </div>
        `).join('');

        entry.innerHTML = `
            <div class="log-entry-header">
                <h3>Workout ${workout.type}</h3>
                <span class="log-entry-date">${dateStr}</span>
            </div>
            ${exercisesHTML}
        `;

        logList.appendChild(entry);
    });
}

function filterLog(filter) {
    document.querySelectorAll('.log-filters .filter-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');

    const entries = document.querySelectorAll('.log-entry');
    entries.forEach(entry => {
        if (filter === 'all' || entry.dataset.workout === filter) {
            entry.style.display = 'block';
        } else {
            entry.style.display = 'none';
        }
    });
}

function clearProgress() {
    if (confirm('Are you sure you want to clear all workout history? This cannot be undone.')) {
        localStorage.removeItem('workoutHistory');
        loadLog();
        loadStats();
    }
}

// ===== SETTINGS =====

function loadSettings() {
    const settings = JSON.parse(localStorage.getItem('hitCoachSettings')) || {
        voiceEnabled: true,
        voiceGender: 'female',
        restDuration: 60,
        theme: 'dark'
    };

    voiceEnabled = settings.voiceEnabled;
    voiceGender = settings.voiceGender;

    // Update rest duration input
    const restInput = document.getElementById('restDuration');
    if (restInput) restInput.value = settings.restDuration;

    // Update theme buttons
    updateThemeButtons(settings.theme);
    applyTheme(settings.theme);

    // Update voice buttons
    updateVoiceButtons(settings.voiceGender);

    return settings;
}

function saveSettings() {
    const settings = {
        voiceEnabled: voiceEnabled,
        voiceGender: voiceGender,
        restDuration: parseInt(document.getElementById('restDuration')?.value) || 60,
        theme: getCurrentTheme()
    };
    localStorage.setItem('hitCoachSettings', JSON.stringify(settings));
}

function getCurrentTheme() {
    if (document.getElementById('themeLight')?.classList.contains('active')) return 'light';
    if (document.getElementById('themeSystem')?.classList.contains('active')) return 'system';
    return 'dark';
}

// ===== THEME =====

function setTheme(theme) {
    updateThemeButtons(theme);
    applyTheme(theme);
    saveSettings();
}

function updateThemeButtons(theme) {
    document.getElementById('themeSystem')?.classList.toggle('active', theme === 'system');
    document.getElementById('themeDark')?.classList.toggle('active', theme === 'dark');
    document.getElementById('themeLight')?.classList.toggle('active', theme === 'light');
}

function applyTheme(theme) {
    if (theme === 'light') {
        document.body.classList.add('light-theme');
    } else if (theme === 'system') {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        document.body.classList.toggle('light-theme', !prefersDark);
    } else {
        document.body.classList.remove('light-theme');
    }
}

// ===== VOICE OPTIONS =====

function setVoice(gender) {
    voiceGender = gender;
    updateVoiceButtons(gender);
    saveSettings();
    speak('Voice updated', true);
}

function updateVoiceButtons(gender) {
    // Update old buttons if they exist
    document.getElementById('voiceM')?.classList.toggle('active', gender === 'male');
    document.getElementById('voiceF')?.classList.toggle('active', gender === 'female');
    document.getElementById('voiceD')?.classList.toggle('active', gender === 'default');

    // Update new voice cards
    document.getElementById('voiceMaleCard')?.classList.toggle('active', gender === 'male');
    document.getElementById('voiceFemaleCard')?.classList.toggle('active', gender === 'female');
    document.getElementById('voiceCommanderCard')?.classList.toggle('active', gender === 'commander');
}

// ===== NEW SETTINGS UI FUNCTIONS =====

function loadSettingsUI() {
    const settings = JSON.parse(localStorage.getItem('hitCoachSettings')) || {};

    // Update voice style selection
    currentVoiceStyle = settings.voiceStyle || 'commander';
    document.querySelectorAll('.voice-style-card').forEach(card => {
        card.classList.toggle('active', card.dataset.style === currentVoiceStyle);
    });

    // Update basic voice selection
    updateVoiceButtons(settings.voiceGender || 'female');

    // Update rest duration
    const restDuration = settings.restDuration || 90;
    document.getElementById('rest60')?.classList.toggle('active', restDuration === 60);
    document.getElementById('rest90')?.classList.toggle('active', restDuration === 90);
    document.getElementById('rest120')?.classList.toggle('active', restDuration === 120);

    // Update phase timing display
    const phases = settings.phases || { prep: 10, eccentric: 30, concentric: 20, finalEccentric: 40 };
    document.getElementById('prepValue').textContent = phases.prep + 's';
    document.getElementById('eccentricValue').textContent = phases.eccentric + 's';
    document.getElementById('concentricValue').textContent = phases.concentric + 's';
    document.getElementById('finalEccentricValue').textContent = phases.finalEccentric + 's';
}

function setRestDuration(seconds) {
    document.getElementById('rest60')?.classList.toggle('active', seconds === 60);
    document.getElementById('rest90')?.classList.toggle('active', seconds === 90);
    document.getElementById('rest120')?.classList.toggle('active', seconds === 120);

    const settings = JSON.parse(localStorage.getItem('hitCoachSettings')) || {};
    settings.restDuration = seconds;
    localStorage.setItem('hitCoachSettings', JSON.stringify(settings));
}

function adjustPhase(phase, delta) {
    const settings = JSON.parse(localStorage.getItem('hitCoachSettings')) || {};
    const defaults = { prep: 10, eccentric: 30, concentric: 20, finalEccentric: 40 };
    const phases = settings.phases || defaults;

    const currentVal = phases[phase] || defaults[phase] || 10;
    phases[phase] = Math.max(5, Math.min(90, currentVal + delta));
    settings.phases = phases;
    localStorage.setItem('hitCoachSettings', JSON.stringify(settings));

    // Update display
    document.getElementById(phase + 'Value').textContent = phases[phase] + 's';
}

// ===== NEW PROFILE UI FUNCTIONS =====

function loadProfileUI() {
    const profile = JSON.parse(localStorage.getItem('hitCoachProfile')) || {};

    // Load name
    const nameInput = document.getElementById('profileName');
    if (nameInput) nameInput.value = profile.name || '';

    // Load experience
    const experience = profile.experience || 'intermediate';
    document.getElementById('expBeginner')?.classList.toggle('active', experience === 'beginner');
    document.getElementById('expIntermediate')?.classList.toggle('active', experience === 'intermediate');
    document.getElementById('expAdvanced')?.classList.toggle('active', experience === 'advanced');

    // Load weight unit
    const weightUnit = profile.weightUnit || 'lbs';
    document.getElementById('unitLbs')?.classList.toggle('active', weightUnit === 'lbs');
    document.getElementById('unitKg')?.classList.toggle('active', weightUnit === 'kg');
}

function setExperience(level) {
    document.getElementById('expBeginner')?.classList.toggle('active', level === 'beginner');
    document.getElementById('expIntermediate')?.classList.toggle('active', level === 'intermediate');
    document.getElementById('expAdvanced')?.classList.toggle('active', level === 'advanced');

    // Apply Darden-based level settings
    applyLevelSettings(level);

    // Update recommended routine display
    updateRecommendedRoutine(level);
}

function updateRecommendedRoutine(level) {
    const levelData = TRAINING_LEVELS[level];
    if (!levelData) return;

    const routineTitle = document.querySelector('.routine-title');
    const routineDesc = document.querySelector('.routine-desc');

    if (routineTitle && routineDesc) {
        const exerciseCount = levelData.routines.A.length;
        routineTitle.textContent = `Full Body A/B Split (${exerciseCount} exercises)`;
        routineDesc.textContent = `${levelData.weeklyFrequency}, ${levelData.restBetweenWorkouts} rest`;
    }
}

function setWeightUnit(unit) {
    document.getElementById('unitLbs')?.classList.toggle('active', unit === 'lbs');
    document.getElementById('unitKg')?.classList.toggle('active', unit === 'kg');

    const profile = JSON.parse(localStorage.getItem('hitCoachProfile')) || {};
    profile.weightUnit = unit;
    localStorage.setItem('hitCoachProfile', JSON.stringify(profile));
}

function saveProfile() {
    const profile = JSON.parse(localStorage.getItem('hitCoachProfile')) || {};
    profile.name = document.getElementById('profileName')?.value || '';
    localStorage.setItem('hitCoachProfile', JSON.stringify(profile));

    // Save duo names if duo mode is enabled
    if (duoModeEnabled) {
        saveDuoNames();
    }
}

function confirmResetData() {
    if (confirm('Are you sure you want to reset all data? This cannot be undone.')) {
        localStorage.removeItem('hitCoachProgress');
        localStorage.removeItem('hitCoachProfile');
        localStorage.removeItem('hitCoachSettings');
        alert('All data has been reset.');
        navigateTo('workouts');
    }
}

// ===== SIRI SHORTCUTS =====

function loadSiriShortcuts() {
    const workoutAList = document.getElementById('siriWorkoutAList');
    const workoutBList = document.getElementById('siriWorkoutBList');

    if (workoutAList) {
        workoutAList.innerHTML = WORKOUTS.A.map(ex => `
            <div class="siri-shortcut-item" onclick="addSiriShortcut('${ex.id}', 'A')">
                <div class="siri-shortcut-info">
                    <span class="siri-shortcut-name">${ex.name} A</span>
                    <span class="siri-shortcut-phrase">Say: "Start ${ex.name.toLowerCase()} A"</span>
                </div>
                <button class="btn btn-primary siri-add-btn">+ Add to Siri</button>
            </div>
        `).join('');
    }

    if (workoutBList) {
        workoutBList.innerHTML = WORKOUTS.B.map(ex => `
            <div class="siri-shortcut-item" onclick="addSiriShortcut('${ex.id}', 'B')">
                <div class="siri-shortcut-info">
                    <span class="siri-shortcut-name">${ex.name} B</span>
                    <span class="siri-shortcut-phrase">Say: "Start ${ex.name.toLowerCase()} B"</span>
                </div>
                <button class="btn btn-primary siri-add-btn">+ Add to Siri</button>
            </div>
        `).join('');
    }
}

// ===== MULTI-PROFILE SUPPORT =====

let activeProfile = 1;
let profiles = {
    1: { name: 'Lifter 1', weights: {}, progress: [] },
    2: { name: 'Lifter 2', weights: {}, progress: [] }
};

function loadProfiles() {
    const saved = localStorage.getItem('hitCoachProfiles');
    if (saved) {
        profiles = JSON.parse(saved);
    }
    updateProfileDisplay();
}

function saveProfiles() {
    localStorage.setItem('hitCoachProfiles', JSON.stringify(profiles));
}

function switchActiveProfile(profileNum) {
    activeProfile = profileNum;

    // Update UI
    document.getElementById('profile1Tab')?.classList.toggle('active', profileNum === 1);
    document.getElementById('profile2Tab')?.classList.toggle('active', profileNum === 2);

    // Announce switch
    speak(`Switched to ${profiles[profileNum].name}`);

    // Re-render exercise list to show correct weights
    renderExerciseList();
}

function updateProfileDisplay() {
    document.getElementById('profile1Name').textContent = profiles[1].name || 'Lifter 1';
    document.getElementById('profile2Name').textContent = profiles[2].name || 'Lifter 2';
}

function enableDuoMode() {
    document.getElementById('profileSwitcher')?.classList.add('active');
}

function disableDuoMode() {
    document.getElementById('profileSwitcher')?.classList.remove('active');
    activeProfile = 1;
}

function setProfileName(profileNum, name) {
    profiles[profileNum].name = name;
    saveProfiles();
    updateProfileDisplay();
}

let duoModeEnabled = false;

function toggleDuoMode() {
    duoModeEnabled = !duoModeEnabled;

    const toggle = document.getElementById('duoModeToggle');
    const namesSection = document.getElementById('duoNamesSection');

    toggle?.classList.toggle('active', duoModeEnabled);

    if (namesSection) {
        namesSection.style.display = duoModeEnabled ? 'block' : 'none';
    }

    if (duoModeEnabled) {
        enableDuoMode();
        // Load existing names
        document.getElementById('lifter1Name').value = profiles[1].name || '';
        document.getElementById('lifter2Name').value = profiles[2].name || '';
    } else {
        disableDuoMode();
    }

    // Save setting
    localStorage.setItem('hitCoachDuoMode', duoModeEnabled);
}

function loadDuoModeSetting() {
    duoModeEnabled = localStorage.getItem('hitCoachDuoMode') === 'true';
    if (duoModeEnabled) {
        document.getElementById('duoModeToggle')?.classList.add('active');
        document.getElementById('duoNamesSection').style.display = 'block';
        enableDuoMode();
    }
}

function saveDuoNames() {
    const name1 = document.getElementById('lifter1Name')?.value || 'Lifter 1';
    const name2 = document.getElementById('lifter2Name')?.value || 'Lifter 2';
    setProfileName(1, name1);
    setProfileName(2, name2);
}

// Override getLastWeight to use active profile
function getLastWeightForProfile(exerciseName) {
    return profiles[activeProfile]?.weights?.[exerciseName] || null;
}

// Override saveWeight to use active profile
function saveWeightForProfile(exerciseName, weight) {
    if (!profiles[activeProfile].weights) {
        profiles[activeProfile].weights = {};
    }
    profiles[activeProfile].weights[exerciseName] = weight;
    saveProfiles();
}

function addSiriShortcut(exerciseId, workout) {
    // Generate URL scheme for the app
    const url = `hitcoach://start/${workout}/${exerciseId}`;

    // Copy to clipboard
    navigator.clipboard.writeText(url).then(() => {
        alert('URL copied! Opening Shortcuts app...\n\nPaste the URL in "Open URL" action.');
        // Try to open Shortcuts app
        window.location.href = 'shortcuts://';
    }).catch(() => {
        alert('URL: ' + url + '\n\nCopy this and add it to Shortcuts app.');
    });
}

// ===== COMMANDER AUDIO SYSTEM =====

const AUDIO_PATH = './static/audio/commander/commander/';
let currentAudio = null;
let audioQueue = [];
let isPlayingAudio = false;
let useCommanderVoice = true; // Toggle between commander voice and TTS

// Audio file mappings
const AUDIO_FILES = {
    // Numbers 1-60
    numbers: Object.fromEntries(
        Array.from({ length: 60 }, (_, i) => [i + 1, `num_${i + 1}.mp3`])
    ),
    // Phases
    phases: {
        prep: 'phase_get_ready.mp3',
        position: 'phase_position.mp3',
        eccentric: 'phase_eccentric.mp3',
        concentric: 'phase_concentric.mp3',
        finalEccentric: 'phase_final_eccentric.mp3',
        complete: 'phase_complete.mp3',
        rest: 'phase_rest.mp3'
    },
    // Exercise names
    exercises: {
        'Leg Press': 'ex_leg_press.mp3',
        'Pulldown': 'ex_pulldown.mp3',
        'Chest Press': 'ex_chest_press.mp3',
        'Overhead': 'ex_overhead_press.mp3',
        'Leg Curl': 'ex_leg_curl.mp3',
        'Bicep Curl': 'ex_bicep_curl.mp3',
        'Tricep Extension': 'ex_tricep_extension.mp3',
        'Calf Raise': 'ex_calf_raise.mp3',
        'Leg Extension': 'ex_leg_extension.mp3',
        'Seated Row': 'ex_seated_row.mp3',
        'Incline Press': 'ex_incline_press.mp3',
        'Lateral Raise': 'ex_lateral_raise.mp3',
        'Shrug': 'ex_shrug.mp3',
        'Ab Crunch': 'ex_ab_crunch.mp3',
        'Back Extension': 'ex_back_extension.mp3'
    },
    // Encouragement
    encouragement: [
        'enc_stay_strong.mp3',
        'enc_perfect.mp3',
        'enc_doing_great.mp3',
        'enc_great_work.mp3',
        'enc_excellent_form.mp3',
        'enc_keep_going.mp3',
        'enc_you_got_this.mp3',
        'enc_fantastic.mp3',
        'enc_almost_there.mp3',
        'enc_push_through.mp3',
        'enc_thats_it.mp3',
        'enc_well_done.mp3'
    ],
    // Final eccentric cues
    final: [
        'final_slow.mp3',
        'final_negative.mp3',
        'final_max_tension.mp3',
        'final_last_push.mp3',
        'final_fight.mp3',
        'final_dont_give_up.mp3',
        'final_control.mp3',
        'final_all_way.mp3'
    ],
    // Eccentric cues
    eccentric: [
        'ecc_smooth.mp3',
        'ecc_feel_stretch.mp3',
        'ecc_lower_slowly.mp3',
        'ecc_control_weight.mp3',
        'ecc_keep_tension.mp3',
        'ecc_resist.mp3',
        'ecc_nice_slow.mp3'
    ],
    // Concentric cues
    concentric: [
        'con_power.mp3',
        'con_push_now.mp3',
        'con_drive_up.mp3',
        'con_squeeze.mp3',
        'con_contract.mp3',
        'con_strong_push.mp3',
        'con_keep_pushing.mp3'
    ],
    // Time announcements
    time: {
        5: 'time_5_sec.mp3',
        10: 'time_10_sec.mp3',
        20: 'time_20_sec.mp3',
        30: 'time_30_sec.mp3',
        halfway: 'time_halfway.mp3',
        almost: 'time_almost.mp3'
    },
    // Rest
    rest: {
        starting: 'rest_starting.mp3',
        breathe: 'rest_breathe.mp3',
        recover: 'rest_recover.mp3',
        complete: 'rest_complete.mp3',
        getReady: 'rest_get_ready.mp3',
        nextComing: 'rest_next_coming.mp3',
        sec15: 'rest_15_sec.mp3',
        sec30: 'rest_30_sec.mp3'
    },
    // Workout
    workout: {
        starting: 'workout_starting.mp3',
        complete: 'workout_complete.mp3',
        greatSession: 'workout_great_session.mp3',
        seeYou: 'workout_see_you.mp3',
        begin: 'workout_begin.mp3',
        crushed: 'workout_crushed.mp3'
    },
    // Transitions
    trans: {
        prepare: 'trans_prepare.mp3',
        next: 'trans_next.mp3',
        moving: 'trans_moving.mp3'
    },
    // Cues
    cues: {
        startingWeight: 'cue_starting_weight.mp3',
        getPosition: 'cue_get_position.mp3',
        grip: 'cue_grip.mp3',
        posture: 'cue_posture.mp3',
        control: 'cue_control.mp3'
    }
};

// Initialize number audio files
for (let i = 1; i <= 60; i++) {
    AUDIO_FILES.numbers[i] = `num_${i}.mp3`;
}

// Play a single audio file
function playAudio(filename, callback) {
    if (!voiceEnabled || !useCommanderVoice) {
        if (callback) callback();
        return;
    }

    const audio = new Audio(AUDIO_PATH + filename);
    currentAudio = audio;

    audio.onended = () => {
        currentAudio = null;
        if (callback) callback();
        playNextInQueue();
    };

    audio.onerror = () => {
        console.log('Audio error:', filename);
        currentAudio = null;
        if (callback) callback();
        playNextInQueue();
    };

    audio.play().catch(err => {
        console.log('Audio play error:', err);
        if (callback) callback();
        playNextInQueue();
    });
}

// Queue audio for sequential playback
function queueAudio(filename) {
    audioQueue.push(filename);
    if (!isPlayingAudio) {
        playNextInQueue();
    }
}

function playNextInQueue() {
    if (audioQueue.length === 0) {
        isPlayingAudio = false;
        return;
    }

    isPlayingAudio = true;
    const filename = audioQueue.shift();
    playAudio(filename);
}

// Stop current audio
function stopAudio() {
    if (currentAudio) {
        currentAudio.pause();
        currentAudio = null;
    }
    audioQueue = [];
    isPlayingAudio = false;
}

// Play number countdown
function playNumber(num) {
    if (num >= 1 && num <= 60 && AUDIO_FILES.numbers[num]) {
        playAudio(AUDIO_FILES.numbers[num]);
    }
}

// Play exercise name
function playExerciseName(exerciseName) {
    if (AUDIO_FILES.exercises[exerciseName]) {
        playAudio(AUDIO_FILES.exercises[exerciseName]);
    }
}

// Play random encouragement
function playEncouragement() {
    const files = AUDIO_FILES.encouragement;
    const file = files[Math.floor(Math.random() * files.length)];
    playAudio(file);
}

// Play random eccentric cue
function playEccentricCue() {
    const files = AUDIO_FILES.eccentric;
    const file = files[Math.floor(Math.random() * files.length)];
    playAudio(file);
}

// Play random concentric cue
function playConcentricCue() {
    const files = AUDIO_FILES.concentric;
    const file = files[Math.floor(Math.random() * files.length)];
    playAudio(file);
}

// Play random final eccentric cue
function playFinalCue() {
    const files = AUDIO_FILES.final;
    const file = files[Math.floor(Math.random() * files.length)];
    playAudio(file);
}

// ===== VOICE SYNTHESIS (Fallback TTS) =====

// TTS-only speak function (bypasses commander audio)
function speakTTS(text, priority = false) {
    if (!voiceEnabled) return;

    if (priority) {
        synth.cancel();
    }

    const utterance = new SpeechSynthesisUtterance(text);
    const voices = synth.getVoices();
    let preferredVoice = null;

    if (voiceGender === 'male') {
        preferredVoice = voices.find(voice =>
            voice.name.toLowerCase().includes('male') ||
            voice.name.toLowerCase().includes('daniel') ||
            voice.name.toLowerCase().includes('alex')
        );
    } else if (voiceGender === 'female') {
        preferredVoice = voices.find(voice =>
            voice.name.toLowerCase().includes('female') ||
            voice.name.toLowerCase().includes('samantha') ||
            voice.name.toLowerCase().includes('victoria')
        );
    }

    if (preferredVoice) {
        utterance.voice = preferredVoice;
    }

    utterance.rate = 0.95;
    utterance.pitch = 1.0;
    utterance.volume = 1.0;

    synth.speak(utterance);
}

function speak(text, priority = false) {
    if (!voiceEnabled) return;

    // Use commander voice if available
    if (useCommanderVoice) {
        // Map text to audio files
        const textLower = text.toLowerCase();

        // Check for numbers
        const numMatch = text.match(/^(\d+)$/);
        if (numMatch) {
            playNumber(parseInt(numMatch[1]));
            return;
        }

        // Check for specific phrases
        if (textLower.includes('paused')) {
            return; // No audio for pause
        }
        if (textLower.includes('resuming')) {
            return; // No audio for resume
        }
        if (textLower.includes('exercise complete')) {
            playAudio(AUDIO_FILES.phases.complete);
            return;
        }
        if (textLower.includes('workout complete')) {
            playAudio(AUDIO_FILES.workout.complete);
            return;
        }

        // For other text, fall back to TTS
    }

    // Fallback to TTS
    if (priority) {
        synth.cancel();
    }

    const utterance = new SpeechSynthesisUtterance(text);
    const voices = synth.getVoices();
    let preferredVoice = null;

    if (voiceGender === 'male') {
        preferredVoice = voices.find(voice =>
            voice.name.toLowerCase().includes('male') ||
            voice.name.toLowerCase().includes('daniel') ||
            voice.name.toLowerCase().includes('alex')
        );
    } else if (voiceGender === 'female') {
        preferredVoice = voices.find(voice =>
            voice.name.toLowerCase().includes('female') ||
            voice.name.toLowerCase().includes('samantha') ||
            voice.name.toLowerCase().includes('victoria')
        );
    }

    if (preferredVoice) {
        utterance.voice = preferredVoice;
    }

    utterance.rate = 0.95;
    utterance.pitch = 1.0;
    utterance.volume = 1.0;

    synth.speak(utterance);
}

function getMotivationalPhrase() {
    const phrases = [
        "You've got this!",
        'Stay strong!',
        'Perfect form!',
        'Keep pushing!',
        'Excellent work!',
        'Stay focused!',
        "You're crushing it!",
        'Amazing control!',
        'Build that strength!',
        'Feel the burn!'
    ];
    return phrases[Math.floor(Math.random() * phrases.length)];
}

// ===== PHASE TIMING CUSTOMIZATION =====

function loadPhaseSettings() {
    const savedPhases = JSON.parse(localStorage.getItem('phaseTimings')) || DEFAULT_PHASES;

    // Update input fields
    const prepInput = document.getElementById('prepDuration');
    const posInput = document.getElementById('positioningDuration');
    const eccInput = document.getElementById('eccentricDuration');
    const conInput = document.getElementById('concentricDuration');
    const finInput = document.getElementById('finalEccentricDuration');

    if (prepInput) prepInput.value = savedPhases.PREP;
    if (posInput) posInput.value = savedPhases.POSITIONING;
    if (eccInput) eccInput.value = savedPhases.ECCENTRIC;
    if (conInput) conInput.value = savedPhases.CONCENTRIC;
    if (finInput) finInput.value = savedPhases.FINAL_ECCENTRIC;

    // Update TIMER_PHASES with custom durations
    TIMER_PHASES.PREP.duration = savedPhases.PREP;
    TIMER_PHASES.POSITIONING.duration = savedPhases.POSITIONING;
    TIMER_PHASES.ECCENTRIC.duration = savedPhases.ECCENTRIC;
    TIMER_PHASES.CONCENTRIC.duration = savedPhases.CONCENTRIC;
    TIMER_PHASES.FINAL_ECCENTRIC.duration = savedPhases.FINAL_ECCENTRIC;

    updateTotalPhaseTime();
}

function savePhaseSettings() {
    const phases = {
        PREP: parseInt(document.getElementById('prepDuration')?.value) || DEFAULT_PHASES.PREP,
        POSITIONING: parseInt(document.getElementById('positioningDuration')?.value) || DEFAULT_PHASES.POSITIONING,
        ECCENTRIC: parseInt(document.getElementById('eccentricDuration')?.value) || DEFAULT_PHASES.ECCENTRIC,
        CONCENTRIC: parseInt(document.getElementById('concentricDuration')?.value) || DEFAULT_PHASES.CONCENTRIC,
        FINAL_ECCENTRIC: parseInt(document.getElementById('finalEccentricDuration')?.value) || DEFAULT_PHASES.FINAL_ECCENTRIC
    };

    localStorage.setItem('phaseTimings', JSON.stringify(phases));

    TIMER_PHASES.PREP.duration = phases.PREP;
    TIMER_PHASES.POSITIONING.duration = phases.POSITIONING;
    TIMER_PHASES.ECCENTRIC.duration = phases.ECCENTRIC;
    TIMER_PHASES.CONCENTRIC.duration = phases.CONCENTRIC;
    TIMER_PHASES.FINAL_ECCENTRIC.duration = phases.FINAL_ECCENTRIC;

    updateTotalPhaseTime();
}

function updateTotalPhaseTime() {
    const total =
        parseInt(document.getElementById('prepDuration')?.value || 0) +
        parseInt(document.getElementById('positioningDuration')?.value || 0) +
        parseInt(document.getElementById('eccentricDuration')?.value || 0) +
        parseInt(document.getElementById('concentricDuration')?.value || 0) +
        parseInt(document.getElementById('finalEccentricDuration')?.value || 0);

    const totalEl = document.getElementById('totalPhaseTime');
    if (totalEl) totalEl.textContent = total;
}

function resetPhaseDefaults() {
    const prepInput = document.getElementById('prepDuration');
    const posInput = document.getElementById('positioningDuration');
    const eccInput = document.getElementById('eccentricDuration');
    const conInput = document.getElementById('concentricDuration');
    const finInput = document.getElementById('finalEccentricDuration');

    if (prepInput) prepInput.value = DEFAULT_PHASES.PREP;
    if (posInput) posInput.value = DEFAULT_PHASES.POSITIONING;
    if (eccInput) eccInput.value = DEFAULT_PHASES.ECCENTRIC;
    if (conInput) conInput.value = DEFAULT_PHASES.CONCENTRIC;
    if (finInput) finInput.value = DEFAULT_PHASES.FINAL_ECCENTRIC;

    savePhaseSettings();
    speak('Phase timings reset to defaults');
}

// ===== PROFILE =====

function loadProfile() {
    const profile = JSON.parse(localStorage.getItem('userProfile')) || {};

    const nameInput = document.getElementById('profileName');
    const ageInput = document.getElementById('profileAge');
    const weightInput = document.getElementById('profileWeight');
    const heightInput = document.getElementById('profileHeight');
    const genderSelect = document.getElementById('profileGender');
    const goalSelect = document.getElementById('profileGoal');
    const experienceSelect = document.getElementById('profileExperience');
    const commanderToggle = document.getElementById('commanderVoiceToggle');

    if (nameInput) nameInput.value = profile.name || '';
    if (ageInput) ageInput.value = profile.age || '';
    if (weightInput) weightInput.value = profile.weight || '';
    if (heightInput) heightInput.value = profile.height || '';
    if (genderSelect) genderSelect.value = profile.gender || 'prefer-not';
    if (goalSelect) goalSelect.value = profile.goal || 'strength';
    if (experienceSelect) experienceSelect.value = profile.experience || 'beginner';

    // Load commander voice preference
    if (profile.commanderVoice !== undefined) {
        useCommanderVoice = profile.commanderVoice;
    }
    if (commanderToggle) {
        commanderToggle.classList.toggle('active', useCommanderVoice);
    }
}

function saveProfile() {
    const profile = {
        name: document.getElementById('profileName')?.value || '',
        age: document.getElementById('profileAge')?.value || '',
        weight: document.getElementById('profileWeight')?.value || '',
        height: document.getElementById('profileHeight')?.value || '',
        gender: document.getElementById('profileGender')?.value || 'prefer-not',
        goal: document.getElementById('profileGoal')?.value || 'strength',
        experience: document.getElementById('profileExperience')?.value || 'beginner',
        commanderVoice: useCommanderVoice
    };
    localStorage.setItem('userProfile', JSON.stringify(profile));
}

// Toggle commander voice on/off
function toggleCommanderVoice() {
    useCommanderVoice = !useCommanderVoice;

    const toggle = document.getElementById('commanderVoiceToggle');
    if (toggle) {
        toggle.classList.toggle('active', useCommanderVoice);
    }

    // Save preference
    saveProfile();

    // Play feedback
    if (useCommanderVoice) {
        playAudio(AUDIO_FILES.encouragement[0]);
    } else {
        speak('Commander voice disabled');
    }
}

// ===== SIRI / VOICE COMMANDS =====

let recognition = null;
let isListening = false;

function initVoiceCommands() {
    // Check for Web Speech API support
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        console.log('Voice commands not supported in this browser');
        return;
    }

    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    recognition.onresult = (event) => {
        const command = event.results[0][0].transcript.toLowerCase().trim();
        console.log('Voice command:', command);
        processVoiceCommand(command);
    };

    recognition.onerror = (event) => {
        console.log('Voice recognition error:', event.error);
        isListening = false;
        updateVoiceCommandButton();
    };

    recognition.onend = () => {
        isListening = false;
        updateVoiceCommandButton();
    };
}

function toggleVoiceCommands() {
    if (!recognition) {
        initVoiceCommands();
        if (!recognition) {
            speak('Voice commands not supported');
            return;
        }
    }

    if (isListening) {
        recognition.stop();
        isListening = false;
    } else {
        recognition.start();
        isListening = true;
        speak('Listening');
    }
    updateVoiceCommandButton();
}

function updateVoiceCommandButton() {
    const btn = document.getElementById('voiceCommandBtn');
    if (btn) {
        btn.classList.toggle('active', isListening);
        btn.textContent = isListening ? '🎤' : '🎙️';
    }
}

function processVoiceCommand(command) {
    // Workout commands
    if (command.includes('start') && command.includes('workout')) {
        if (command.includes('a') || command.includes('one') || command.includes('1')) {
            switchWorkoutTab('A');
            speak('Starting Workout A');
        } else if (command.includes('b') || command.includes('two') || command.includes('2')) {
            switchWorkoutTab('B');
            speak('Starting Workout B');
        } else {
            speak('Starting workout');
        }
        return;
    }

    // Exercise control
    if (command.includes('start') || command.includes('begin') || command.includes('go')) {
        if (document.getElementById('startBtn')?.style.display !== 'none') {
            startExercise();
            return;
        }
    }

    if (command.includes('pause') || command.includes('stop') || command.includes('hold')) {
        if (document.getElementById('pauseBtn')?.style.display !== 'none') {
            pauseExercise();
            return;
        }
    }

    if (command.includes('resume') || command.includes('continue')) {
        if (document.getElementById('resumeBtn')?.style.display !== 'none') {
            resumeExercise();
            return;
        }
    }

    if (command.includes('next') || command.includes('done') || command.includes('complete')) {
        if (document.getElementById('completeSection')?.style.display !== 'none') {
            completeExercise();
            return;
        }
    }

    if (command.includes('skip') && command.includes('rest')) {
        if (document.getElementById('restScreen')?.style.display !== 'none') {
            skipRest();
            return;
        }
    }

    if (command.includes('redo') || command.includes('again') || command.includes('repeat')) {
        redoExercise();
        return;
    }

    // Navigation
    if (command.includes('settings') || command.includes('setting')) {
        showScreen('settingsScreen');
        speak('Opening settings');
        return;
    }

    if (command.includes('profile')) {
        showScreen('profileScreen');
        speak('Opening profile');
        return;
    }

    if (command.includes('stats') || command.includes('statistics')) {
        navigateTo('stats');
        speak('Showing stats');
        return;
    }

    if (command.includes('log') || command.includes('history')) {
        navigateTo('log');
        speak('Showing workout log');
        return;
    }

    if (command.includes('home') || command.includes('workouts')) {
        navigateTo('workouts');
        speak('Going home');
        return;
    }

    if (command.includes('back') || command.includes('exit')) {
        exitWorkout();
        return;
    }

    // Failure check
    if (command.includes('failure') || command.includes('failed')) {
        const checkbox = document.getElementById('failureCheck');
        if (checkbox) {
            checkbox.checked = true;
            speak('Marked as failure');
        }
        return;
    }

    speak("Sorry, I didn't understand that command");
}

// Initialize voice commands on load
document.addEventListener('DOMContentLoaded', () => {
    initVoiceCommands();
    initSiriShortcuts();
});

// ===== SIRI SHORTCUTS =====

function initSiriShortcuts() {
    // Check for Shortcuts support (iOS 12+ Safari)
    if ('shortcuts' in navigator || window.webkit?.messageHandlers?.shortcuts) {
        console.log('Siri Shortcuts may be available');
        registerShortcuts();
    }

    // Handle URL scheme for Siri Shortcuts
    handleShortcutURL();
}

function registerShortcuts() {
    // Define available shortcuts
    const shortcuts = [
        {
            id: 'start-workout-a',
            title: 'Start Workout A',
            phrase: 'Start my push workout',
            action: () => { switchWorkoutTab('A'); startWorkoutFromExercise(0); }
        },
        {
            id: 'start-workout-b',
            title: 'Start Workout B',
            phrase: 'Start my pull workout',
            action: () => { switchWorkoutTab('B'); startWorkoutFromExercise(0); }
        },
        {
            id: 'view-stats',
            title: 'View Workout Stats',
            phrase: 'Show my workout stats',
            action: () => navigateTo('stats')
        },
        {
            id: 'view-log',
            title: 'View Workout Log',
            phrase: 'Show my workout history',
            action: () => navigateTo('log')
        }
    ];

    // Store shortcuts for URL handling
    window.hitCoachShortcuts = shortcuts;
}

function handleShortcutURL() {
    // Handle deep links from Siri Shortcuts
    // URL format: hitcoachpro://action/start-workout-a
    const urlParams = new URLSearchParams(window.location.search);
    const action = urlParams.get('action');

    if (action) {
        executeShortcutAction(action);
    }

    // Also check hash for PWA
    if (window.location.hash) {
        const hashAction = window.location.hash.replace('#', '');
        executeShortcutAction(hashAction);
    }
}

function executeShortcutAction(actionId) {
    const shortcuts = window.hitCoachShortcuts || [];
    const shortcut = shortcuts.find(s => s.id === actionId);

    if (shortcut && shortcut.action) {
        // Small delay to ensure app is loaded
        setTimeout(() => {
            shortcut.action();
            speak(shortcut.title);
        }, 500);
    }
}

// Add to Home Screen with Shortcuts info
function showShortcutsInfo() {
    const info = `
Available Siri Shortcuts:

"Hey Siri, Start my push workout"
→ Starts Workout A

"Hey Siri, Start my pull workout"
→ Starts Workout B

"Hey Siri, Show my workout stats"
→ Opens Stats screen

"Hey Siri, Show my workout history"
→ Opens Workout Log

To add: Open Shortcuts app → Create New → Add Action → Search "HIT Coach Pro"
    `;
    alert(info);
}

// ===== UPGRADE MODAL =====

function showUpgradeModal() {
    document.getElementById('upgradeModal').classList.add('active');
}

function closeUpgradeModal() {
    document.getElementById('upgradeModal').classList.remove('active');
}

// ===== PWA / SERVICE WORKER =====

let deferredPrompt;
let isIOSDevice = false;

// Register service worker
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/service-worker.js')
            .then((registration) => {
                console.log('ServiceWorker registered:', registration.scope);
            })
            .catch((error) => {
                console.log('ServiceWorker registration failed:', error);
            });
    });
}

function detectIOS() {
    const ua = window.navigator.userAgent;
    const iOS = !!ua.match(/iPad/i) || !!ua.match(/iPhone/i);
    const webkit = !!ua.match(/WebKit/i);
    isIOSDevice = iOS && webkit && !ua.match(/CriOS/i);
    return isIOSDevice;
}

function isAppInstalled() {
    if (window.matchMedia('(display-mode: standalone)').matches) {
        return true;
    }
    if (window.navigator.standalone === true) {
        return true;
    }
    return false;
}

function showInstallPrompt() {
    if (isAppInstalled()) return;

    const dismissedTime = localStorage.getItem('installPromptDismissed');
    if (dismissedTime) {
        const daysSinceDismissed = (Date.now() - parseInt(dismissedTime)) / (1000 * 60 * 60 * 24);
        if (daysSinceDismissed < 7) return;
    }

    if (detectIOS()) {
        setTimeout(() => {
            document.getElementById('iosInstallPrompt').style.display = 'flex';
        }, 3000);
    } else if (deferredPrompt) {
        document.getElementById('installBanner').style.display = 'block';
    }
}

window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    showInstallPrompt();
});

document.addEventListener('DOMContentLoaded', () => {
    const installButton = document.getElementById('installButton');
    const dismissButton = document.getElementById('dismissInstall');

    if (installButton) {
        installButton.addEventListener('click', async () => {
            if (!deferredPrompt) return;

            deferredPrompt.prompt();
            const { outcome } = await deferredPrompt.userChoice;
            console.log(`User response to install prompt: ${outcome}`);

            deferredPrompt = null;
            document.getElementById('installBanner').style.display = 'none';
        });
    }

    if (dismissButton) {
        dismissButton.addEventListener('click', () => {
            document.getElementById('installBanner').style.display = 'none';
            localStorage.setItem('installPromptDismissed', Date.now().toString());
        });
    }
});

function closeIOSPrompt() {
    document.getElementById('iosInstallPrompt').style.display = 'none';
    localStorage.setItem('installPromptDismissed', Date.now().toString());
}

window.addEventListener('appinstalled', () => {
    console.log('PWA installed successfully');
    document.getElementById('installBanner').style.display = 'none';
    document.getElementById('iosInstallPrompt').style.display = 'none';
});

// Prevent accidental page close during workout
window.addEventListener('beforeunload', (e) => {
    if (timerInterval && !isPaused) {
        e.preventDefault();
        e.returnValue = '';
    }
});
