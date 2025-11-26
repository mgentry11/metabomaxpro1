// HIT Coach Pro Web App JavaScript - Redesigned

// ===== EXERCISE ICON IMAGES =====
// Gold circle icons with black silhouettes from Gemini

const ICON_PATH = './static/images/icons/';

const EXERCISE_ICONS = {
    legPress: 'leg_press.png',
    pulldown: 'pull_up.png',
    chestPress: 'bench_press.png',
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
    backExtension: 'good_morning.png'
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

        // Commander voice countdown and cues
        if (useCommanderVoice) {
            // Countdown at 5, 3, 2, 1
            if (timeRemaining === 5) playNumber(5);
            else if (timeRemaining === 3) playNumber(3);
            else if (timeRemaining === 2) playNumber(2);
            else if (timeRemaining === 1) playNumber(1);

            // Phase-specific cues
            if (currentPhase === 'ECCENTRIC' && timeRemaining === 15) {
                playEccentricCue();
            } else if (currentPhase === 'CONCENTRIC' && timeRemaining === 10) {
                playConcentricCue();
            } else if (currentPhase === 'FINAL_ECCENTRIC' && timeRemaining === 20) {
                playAudio(AUDIO_FILES.time.halfway);
            } else if (currentPhase === 'FINAL_ECCENTRIC' && timeRemaining === 10) {
                playFinalCue();
            }
        } else {
            // Fallback TTS countdown
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

// ===== COMMANDER AUDIO SYSTEM =====

const AUDIO_PATH = './static/audio/commander/';
let currentAudio = null;
let audioQueue = [];
let isPlayingAudio = false;
let useCommanderVoice = true; // Toggle between commander voice and TTS

// Audio file mappings
const AUDIO_FILES = {
    // Numbers 1-60
    numbers: {},
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
