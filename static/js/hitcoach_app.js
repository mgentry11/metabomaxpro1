// HIT Coach Pro Web App JavaScript - Redesigned

// ===== SVG EXERCISE ICONS =====

const EXERCISE_ICONS = {
    legPress: `<svg viewBox="0 0 100 100" fill="currentColor"><path d="M25 70 L35 55 L45 65 L55 45 L50 35 L55 25 L60 25 L65 30 L60 40 L65 50 L75 40 L80 45 L70 60 L60 55 L50 70 L40 75 L25 70 Z M55 20 A8 8 0 1 1 55 21 Z"/><path d="M20 75 L30 80 L25 85 L15 80 Z"/><path d="M75 35 L90 25 L90 35 L75 45 Z" fill="currentColor" opacity="0.7"/></svg>`,

    pulldown: `<svg viewBox="0 0 100 100" fill="currentColor"><path d="M50 18 A8 8 0 1 1 50 19 Z"/><path d="M50 26 L50 50 M35 65 L50 50 L65 65 M40 35 L50 30 L60 35 M30 25 L40 35 M70 25 L60 35"/><path d="M25 15 L75 15 L75 20 L25 20 Z" opacity="0.7"/><line x1="50" y1="15" x2="50" y2="26" stroke="currentColor" stroke-width="3"/><circle cx="50" cy="18" r="8"/><path d="M42 28 L42 50 L38 65 M58 28 L58 50 L62 65" stroke="currentColor" stroke-width="4" fill="none"/><path d="M30 20 L30 35 L40 30 M70 20 L70 35 L60 30" stroke="currentColor" stroke-width="3" fill="none"/></svg>`,

    chestPress: `<svg viewBox="0 0 100 100" fill="currentColor"><rect x="15" y="45" width="70" height="8" rx="2"/><path d="M50 35 A7 7 0 1 1 50 36 Z"/><path d="M40 42 L40 60 L35 75 M60 42 L60 60 L65 75" stroke="currentColor" stroke-width="4" fill="none"/><path d="M40 50 L25 50 M60 50 L75 50" stroke="currentColor" stroke-width="4"/><ellipse cx="50" cy="60" rx="12" ry="6" opacity="0.5"/><rect x="10" y="42" width="8" height="14" rx="2"/><rect x="82" y="42" width="8" height="14" rx="2"/></svg>`,

    overheadPress: `<svg viewBox="0 0 100 100" fill="currentColor"><path d="M50 30 A8 8 0 1 1 50 31 Z"/><rect x="20" y="15" width="60" height="6" rx="2"/><rect x="15" y="12" width="10" height="12" rx="2"/><rect x="75" y="12" width="10" height="12" rx="2"/><path d="M42 38 L42 60 L38 80 M58 38 L58 60 L62 80" stroke="currentColor" stroke-width="4" fill="none"/><path d="M42 38 L35 18 M58 38 L65 18" stroke="currentColor" stroke-width="3" fill="none"/></svg>`,

    legCurl: `<svg viewBox="0 0 100 100" fill="currentColor"><path d="M65 35 A7 7 0 1 1 65 36 Z"/><path d="M20 50 L80 50 L80 60 L20 60 Z" opacity="0.5"/><path d="M55 42 L55 50 M75 50 L75 42" stroke="currentColor" stroke-width="4" fill="none"/><path d="M30 55 L30 75 L45 85" stroke="currentColor" stroke-width="5" fill="none"/><ellipse cx="48" cy="86" rx="5" ry="4"/><path d="M60 55 L75 55 L85 65" stroke="currentColor" stroke-width="4" fill="none" opacity="0.7"/></svg>`,

    bicepCurl: `<svg viewBox="0 0 100 100" fill="currentColor"><path d="M50 22 A8 8 0 1 1 50 23 Z"/><path d="M42 30 L42 55 L38 75 M58 30 L58 55 L62 75" stroke="currentColor" stroke-width="4" fill="none"/><path d="M42 45 L30 55 L28 45" stroke="currentColor" stroke-width="3" fill="none"/><path d="M58 45 L70 35 L72 45" stroke="currentColor" stroke-width="3" fill="none"/><rect x="24" y="42" width="8" height="16" rx="2"/><rect x="68" y="32" width="8" height="16" rx="2"/></svg>`,

    tricepExtension: `<svg viewBox="0 0 100 100" fill="currentColor"><path d="M50 25 A8 8 0 1 1 50 26 Z"/><path d="M42 33 L42 55 L38 75 M58 33 L58 55 L62 75" stroke="currentColor" stroke-width="4" fill="none"/><path d="M42 40 L50 20 L58 40" stroke="currentColor" stroke-width="3" fill="none"/><rect x="45" y="10" width="10" height="15" rx="2"/></svg>`,

    calfRaise: `<svg viewBox="0 0 100 100" fill="currentColor"><path d="M50 20 A8 8 0 1 1 50 21 Z"/><path d="M45 28 L45 55 L42 70 L42 78 M55 28 L55 55 L58 70 L58 78" stroke="currentColor" stroke-width="4" fill="none"/><path d="M38 78 L42 85 L58 85 L62 78" stroke="currentColor" stroke-width="3" fill="none"/><rect x="30" y="85" width="40" height="6" rx="2" opacity="0.5"/><path d="M40 40 L50 35 L60 40" stroke="currentColor" stroke-width="3" fill="none"/></svg>`,

    legExtension: `<svg viewBox="0 0 100 100" fill="currentColor"><path d="M35 35 A7 7 0 1 1 35 36 Z"/><path d="M20 45 L60 45 L60 55 L20 55 Z" opacity="0.5"/><path d="M30 42 L30 55 M45 42 L45 55" stroke="currentColor" stroke-width="4" fill="none"/><path d="M55 50 L80 40 L82 45 L58 55" stroke="currentColor" stroke-width="4" fill="none"/><ellipse cx="83" cy="42" rx="5" ry="4"/><rect x="15" y="55" width="10" height="25" rx="2" opacity="0.5"/></svg>`,

    seatedRow: `<svg viewBox="0 0 100 100" fill="currentColor"><path d="M30 35 A7 7 0 1 1 30 36 Z"/><path d="M25 42 L25 55 L20 75 M35 42 L40 55 L45 75" stroke="currentColor" stroke-width="4" fill="none"/><path d="M35 50 L55 50 L70 45" stroke="currentColor" stroke-width="3" fill="none"/><rect x="70" y="40" width="15" height="8" rx="2"/><rect x="15" y="55" width="35" height="5" rx="2" opacity="0.5"/><path d="M25 48 L15 48 L15 55" stroke="currentColor" stroke-width="3" fill="none" opacity="0.7"/></svg>`,

    inclinePress: `<svg viewBox="0 0 100 100" fill="currentColor"><path d="M55 30 A7 7 0 1 1 55 31 Z"/><path d="M20 75 L45 40 L70 75 Z" fill="none" stroke="currentColor" stroke-width="2" opacity="0.5"/><path d="M48 38 L48 55 L40 75 M62 38 L62 50 L70 70" stroke="currentColor" stroke-width="4" fill="none"/><path d="M48 45 L30 30 M62 45 L80 30" stroke="currentColor" stroke-width="3" fill="none"/><rect x="15" y="20" width="70" height="6" rx="2"/><rect x="10" y="18" width="10" height="10" rx="2"/><rect x="80" y="18" width="10" height="10" rx="2"/></svg>`,

    lateralRaise: `<svg viewBox="0 0 100 100" fill="currentColor"><path d="M50 22 A8 8 0 1 1 50 23 Z"/><path d="M45 30 L45 55 L40 78 M55 30 L55 55 L60 78" stroke="currentColor" stroke-width="4" fill="none"/><path d="M45 40 L20 35 M55 40 L80 35" stroke="currentColor" stroke-width="3" fill="none"/><rect x="12" y="32" width="12" height="8" rx="2"/><rect x="76" y="32" width="12" height="8" rx="2"/></svg>`,

    shrug: `<svg viewBox="0 0 100 100" fill="currentColor"><path d="M50 25 A8 8 0 1 1 50 26 Z"/><path d="M42 33 L42 60 L38 80 M58 33 L58 60 L62 80" stroke="currentColor" stroke-width="4" fill="none"/><path d="M42 40 L42 55 L30 55 L30 40" stroke="currentColor" stroke-width="3" fill="none"/><path d="M58 40 L58 55 L70 55 L70 40" stroke="currentColor" stroke-width="3" fill="none"/><rect x="25" y="55" width="10" height="25" rx="2"/><rect x="65" y="55" width="10" height="25" rx="2"/><path d="M35 33 L35 28 L42 33 M65 33 L65 28 L58 33" stroke="currentColor" stroke-width="2" fill="none"/></svg>`,

    abCrunch: `<svg viewBox="0 0 100 100" fill="currentColor"><path d="M30 45 A7 7 0 1 1 30 46 Z"/><path d="M35 50 L55 60 L75 55" stroke="currentColor" stroke-width="5" fill="none"/><path d="M55 60 L50 75 L55 85 M55 60 L65 75 L60 85" stroke="currentColor" stroke-width="4" fill="none"/><path d="M25 52 L20 60" stroke="currentColor" stroke-width="3" fill="none"/><ellipse cx="50" cy="65" rx="15" ry="8" opacity="0.3"/></svg>`,

    backExtension: `<svg viewBox="0 0 100 100" fill="currentColor"><path d="M70 35 A7 7 0 1 1 70 36 Z"/><path d="M65 42 L45 55 L25 52" stroke="currentColor" stroke-width="5" fill="none"/><path d="M45 55 L40 75 L45 85 M45 55 L55 72 L50 85" stroke="currentColor" stroke-width="4" fill="none"/><rect x="15" y="50" width="15" height="35" rx="3" opacity="0.5"/><path d="M75 40 L85 35" stroke="currentColor" stroke-width="3" fill="none"/></svg>`
};

// ===== DATA STRUCTURES =====

const WORKOUTS = {
    A: [
        { name: 'Leg Press', iconKey: 'legPress', muscle: 'Legs' },
        { name: 'Pulldown', iconKey: 'pulldown', muscle: 'Back' },
        { name: 'Chest Press', iconKey: 'chestPress', muscle: 'Chest' },
        { name: 'Overhead', iconKey: 'overheadPress', muscle: 'Shoulders' },
        { name: 'Leg Curl', iconKey: 'legCurl', muscle: 'Hamstrings' },
        { name: 'Bicep Curl', iconKey: 'bicepCurl', muscle: 'Biceps' },
        { name: 'Tricep Extension', iconKey: 'tricepExtension', muscle: 'Triceps' },
        { name: 'Calf Raise', iconKey: 'calfRaise', muscle: 'Calves' }
    ],
    B: [
        { name: 'Leg Extension', iconKey: 'legExtension', muscle: 'Quads' },
        { name: 'Seated Row', iconKey: 'seatedRow', muscle: 'Back' },
        { name: 'Incline Press', iconKey: 'inclinePress', muscle: 'Upper Chest' },
        { name: 'Lateral Raise', iconKey: 'lateralRaise', muscle: 'Shoulders' },
        { name: 'Leg Curl', iconKey: 'legCurl', muscle: 'Hamstrings' },
        { name: 'Shrug', iconKey: 'shrug', muscle: 'Traps' },
        { name: 'Ab Crunch', iconKey: 'abCrunch', muscle: 'Abs' },
        { name: 'Back Extension', iconKey: 'backExtension', muscle: 'Lower Back' }
    ]
};

// Helper function to get icon SVG
function getExerciseIcon(iconKey) {
    return EXERCISE_ICONS[iconKey] || '<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="30" fill="currentColor"/></svg>';
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
let synth = window.speechSynthesis;

// ===== INITIALIZATION =====

document.addEventListener('DOMContentLoaded', () => {
    loadSettings();
    loadPhaseSettings();
    loadProfile();
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

    list.innerHTML = exercises.map((exercise, index) => `
        <div class="exercise-item" onclick="showExerciseSetup(${index})">
            <div class="exercise-icon">${getExerciseIcon(exercise.iconKey)}</div>
            <div class="exercise-info">
                <div class="exercise-name">${exercise.name}</div>
                <div class="exercise-muscle">${exercise.muscle}</div>
            </div>
            <div class="exercise-chevron">›</div>
        </div>
    `).join('');
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
    speak(`Starting ${exercise.name}. ${getMotivationalPhrase()}`, true);

    startPhase('PREP');
}

function startPhase(phaseName) {
    currentPhase = phaseName;
    const phase = TIMER_PHASES[phaseName];
    timeRemaining = phase.duration;

    document.getElementById('phaseIndicator').textContent = phase.name;
    document.getElementById('phaseDescription').textContent = phase.description;
    updateTimerDisplay();

    // Voice announcements
    if (phaseName === 'POSITIONING') {
        speak('Get into position', true);
    } else if (phaseName === 'ECCENTRIC') {
        speak('Begin eccentric. Slow and controlled.', true);
    } else if (phaseName === 'CONCENTRIC') {
        speak('Begin concentric. Powerful lift.', true);
    } else if (phaseName === 'FINAL_ECCENTRIC') {
        speak('Final eccentric. Push to failure.', true);
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

        // Countdown announcements
        if (timeRemaining === 5) speak('5');
        else if (timeRemaining === 3) speak('3');
        else if (timeRemaining === 2) speak('2');
        else if (timeRemaining === 1) speak('1');

        // Motivational phrases at intervals
        if (currentPhase === 'ECCENTRIC' && timeRemaining === 15) {
            speak(getMotivationalPhrase());
        } else if (currentPhase === 'FINAL_ECCENTRIC' && timeRemaining === 20) {
            speak('Halfway there!');
        } else if (currentPhase === 'FINAL_ECCENTRIC' && timeRemaining === 10) {
            speak('10 seconds! Give it everything!');
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
    document.getElementById('voiceM')?.classList.toggle('active', gender === 'male');
    document.getElementById('voiceF')?.classList.toggle('active', gender === 'female');
    document.getElementById('voiceD')?.classList.toggle('active', gender === 'default');
}

// ===== VOICE SYNTHESIS =====

function speak(text, priority = false) {
    if (!voiceEnabled) return;

    if (priority) {
        synth.cancel();
    }

    const utterance = new SpeechSynthesisUtterance(text);

    // Set voice based on gender preference
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

    if (nameInput) nameInput.value = profile.name || '';
    if (ageInput) ageInput.value = profile.age || '';
    if (weightInput) weightInput.value = profile.weight || '';
    if (heightInput) heightInput.value = profile.height || '';
    if (genderSelect) genderSelect.value = profile.gender || 'prefer-not';
    if (goalSelect) goalSelect.value = profile.goal || 'strength';
    if (experienceSelect) experienceSelect.value = profile.experience || 'beginner';
}

function saveProfile() {
    const profile = {
        name: document.getElementById('profileName')?.value || '',
        age: document.getElementById('profileAge')?.value || '',
        weight: document.getElementById('profileWeight')?.value || '',
        height: document.getElementById('profileHeight')?.value || '',
        gender: document.getElementById('profileGender')?.value || 'prefer-not',
        goal: document.getElementById('profileGoal')?.value || 'strength',
        experience: document.getElementById('profileExperience')?.value || 'beginner'
    };
    localStorage.setItem('userProfile', JSON.stringify(profile));
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
