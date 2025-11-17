// HIT Coach Pro Web App JavaScript

// ===== DATA STRUCTURES =====

const WORKOUTS = {
    FREE: [
        { name: 'Leg Press', icon: '🦵', muscle: 'Legs' },
        { name: 'Pulldown', icon: '💪', muscle: 'Back' },
        { name: 'Chest Press', icon: '💪', muscle: 'Chest' },
        { name: 'Overhead Press', icon: '💪', muscle: 'Shoulders' }
    ],
    A: [
        { name: 'Leg Press', icon: '🦵', muscle: 'Legs' },
        { name: 'Pulldown', icon: '💪', muscle: 'Back' },
        { name: 'Chest Press', icon: '💪', muscle: 'Chest' },
        { name: 'Overhead Press', icon: '💪', muscle: 'Shoulders' },
        { name: 'Leg Curl', icon: '🦵', muscle: 'Hamstrings' },
        { name: 'Bicep Curl', icon: '💪', muscle: 'Biceps' },
        { name: 'Tricep Extension', icon: '💪', muscle: 'Triceps' },
        { name: 'Calf Raise', icon: '🦵', muscle: 'Calves' }
    ],
    B: [
        { name: 'Leg Extension', icon: '🦵', muscle: 'Quads' },
        { name: 'Seated Row', icon: '💪', muscle: 'Back' },
        { name: 'Incline Press', icon: '💪', muscle: 'Chest' },
        { name: 'Lateral Raise', icon: '💪', muscle: 'Shoulders' },
        { name: 'Leg Curl', icon: '🦵', muscle: 'Hamstrings' },
        { name: 'Shrug', icon: '💪', muscle: 'Traps' },
        { name: 'Ab Crunch', icon: '🧘', muscle: 'Abs' },
        { name: 'Back Extension', icon: '🧘', muscle: 'Lower Back' }
    ]
};

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

let currentWorkout = null;
let currentExerciseIndex = 0;
let currentPhase = null;
let timerInterval = null;
let timeRemaining = 0;
let isPaused = false;
let workoutStartTime = null;
let currentWorkoutData = [];
let voiceEnabled = true;
let synth = window.speechSynthesis;

// ===== SETTINGS =====

function loadSettings() {
    const settings = JSON.parse(localStorage.getItem('hitCoachSettings')) || {
        voiceEnabled: true,
        voiceGender: 'female',
        restDuration: 60,
        coachingStyle: 'motivational',
        theme: 'dark',
        volume: 100
    };

    voiceEnabled = settings.voiceEnabled;
    document.getElementById('voiceToggle').checked = settings.voiceEnabled;
    document.getElementById('voiceGender').value = settings.voiceGender;
    document.getElementById('restDuration').value = settings.restDuration;
    document.getElementById('coachingStyle').value = settings.coachingStyle;
    document.getElementById('volumeSlider').value = settings.volume;
    document.getElementById('volumeDisplay').textContent = settings.volume + '%';

    if (settings.theme === 'light') {
        document.body.classList.add('light-theme');
    }

    return settings;
}

function saveSettings() {
    const settings = {
        voiceEnabled: document.getElementById('voiceToggle').checked,
        voiceGender: document.getElementById('voiceGender').value,
        restDuration: parseInt(document.getElementById('restDuration').value),
        coachingStyle: document.getElementById('coachingStyle').value,
        theme: document.body.classList.contains('light-theme') ? 'light' : 'dark',
        volume: parseInt(document.getElementById('volumeSlider').value)
    };
    localStorage.setItem('hitCoachSettings', JSON.stringify(settings));
}

function toggleVoice() {
    voiceEnabled = document.getElementById('voiceToggle').checked;
    saveSettings();
}

function changeVoiceGender() {
    saveSettings();
}

function setTheme(theme) {
    document.querySelectorAll('.theme-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');

    if (theme === 'light') {
        document.body.classList.add('light-theme');
    } else {
        document.body.classList.remove('light-theme');
    }
    saveSettings();
}

function updateVolume() {
    const volume = document.getElementById('volumeSlider').value;
    document.getElementById('volumeDisplay').textContent = volume + '%';
    saveSettings();
}

// ===== PHASE TIMING CUSTOMIZATION =====

function loadPhaseSettings() {
    const savedPhases = JSON.parse(localStorage.getItem('phaseTimings')) || DEFAULT_PHASES;

    // Update input fields
    document.getElementById('prepDuration').value = savedPhases.PREP;
    document.getElementById('positioningDuration').value = savedPhases.POSITIONING;
    document.getElementById('eccentricDuration').value = savedPhases.ECCENTRIC;
    document.getElementById('concentricDuration').value = savedPhases.CONCENTRIC;
    document.getElementById('finalEccentricDuration').value = savedPhases.FINAL_ECCENTRIC;

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
        PREP: parseInt(document.getElementById('prepDuration').value) || DEFAULT_PHASES.PREP,
        POSITIONING: parseInt(document.getElementById('positioningDuration').value) || DEFAULT_PHASES.POSITIONING,
        ECCENTRIC: parseInt(document.getElementById('eccentricDuration').value) || DEFAULT_PHASES.ECCENTRIC,
        CONCENTRIC: parseInt(document.getElementById('concentricDuration').value) || DEFAULT_PHASES.CONCENTRIC,
        FINAL_ECCENTRIC: parseInt(document.getElementById('finalEccentricDuration').value) || DEFAULT_PHASES.FINAL_ECCENTRIC
    };

    // Save to localStorage
    localStorage.setItem('phaseTimings', JSON.stringify(phases));

    // Update TIMER_PHASES
    TIMER_PHASES.PREP.duration = phases.PREP;
    TIMER_PHASES.POSITIONING.duration = phases.POSITIONING;
    TIMER_PHASES.ECCENTRIC.duration = phases.ECCENTRIC;
    TIMER_PHASES.CONCENTRIC.duration = phases.CONCENTRIC;
    TIMER_PHASES.FINAL_ECCENTRIC.duration = phases.FINAL_ECCENTRIC;

    updateTotalPhaseTime();
}

function updateTotalPhaseTime() {
    const total =
        parseInt(document.getElementById('prepDuration').value || 0) +
        parseInt(document.getElementById('positioningDuration').value || 0) +
        parseInt(document.getElementById('eccentricDuration').value || 0) +
        parseInt(document.getElementById('concentricDuration').value || 0) +
        parseInt(document.getElementById('finalEccentricDuration').value || 0);

    document.getElementById('totalPhaseTime').textContent = total;
}

function resetPhaseDefaults() {
    document.getElementById('prepDuration').value = DEFAULT_PHASES.PREP;
    document.getElementById('positioningDuration').value = DEFAULT_PHASES.POSITIONING;
    document.getElementById('eccentricDuration').value = DEFAULT_PHASES.ECCENTRIC;
    document.getElementById('concentricDuration').value = DEFAULT_PHASES.CONCENTRIC;
    document.getElementById('finalEccentricDuration').value = DEFAULT_PHASES.FINAL_ECCENTRIC;

    savePhaseSettings();

    // Give user feedback
    speak('Phase timings reset to defaults');
}

// ===== VOICE SYNTHESIS =====

function speak(text, priority = false) {
    if (!voiceEnabled) return;

    if (priority) {
        synth.cancel();
    }

    const settings = loadSettings();
    const utterance = new SpeechSynthesisUtterance(text);

    // Set voice based on gender preference
    const voices = synth.getVoices();
    const preferredVoice = voices.find(voice =>
        voice.name.toLowerCase().includes(settings.voiceGender === 'female' ? 'female' : 'male') ||
        voice.name.toLowerCase().includes(settings.voiceGender === 'female' ? 'samantha' : 'daniel')
    );

    if (preferredVoice) {
        utterance.voice = preferredVoice;
    }

    utterance.rate = 0.9;
    utterance.pitch = 1.0;
    utterance.volume = settings.volume / 100;

    synth.speak(utterance);
}

function getMotivationalPhrase() {
    const settings = loadSettings();

    if (settings.coachingStyle === 'minimal') return '';

    if (settings.coachingStyle === 'technical') {
        const phrases = [
            'Maintain constant tension',
            'Control the movement',
            'Focus on the muscle',
            'Perfect form',
            'Slow and controlled'
        ];
        return phrases[Math.floor(Math.random() * phrases.length)];
    }

    // Motivational
    const phrases = [
        'You\'ve got this!',
        'Stay strong!',
        'Perfect form!',
        'Keep pushing!',
        'Excellent work!',
        'Stay focused!',
        'You\'re crushing it!',
        'Amazing control!',
        'Build that strength!',
        'Feel the burn!'
    ];
    return phrases[Math.floor(Math.random() * phrases.length)];
}

// ===== SCREEN NAVIGATION =====

function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    document.getElementById(screenId).classList.add('active');

    if (screenId === 'settingsScreen') {
        loadSettings();
        loadPhaseSettings();
    }

    if (screenId === 'progressScreen') {
        loadProgressHistory();
    }
}

// ===== WORKOUT MANAGEMENT =====

function loadWorkout(workoutType) {
    currentWorkout = workoutType;
    currentExerciseIndex = 0;
    workoutStartTime = new Date();
    currentWorkoutData = [];

    document.getElementById('workoutTitle').textContent = `Workout ${workoutType}`;
    showScreen('workoutScreen');
    loadExercise();
}

function loadExercise() {
    const exercises = WORKOUTS[currentWorkout];
    const exercise = exercises[currentExerciseIndex];

    document.getElementById('exerciseName').textContent = exercise.name;
    document.getElementById('exerciseCounter').textContent = `${currentExerciseIndex + 1} / ${exercises.length}`;
    document.querySelector('.exercise-icon-display').textContent = exercise.icon;

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

    const exercise = WORKOUTS[currentWorkout][currentExerciseIndex];
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
        speak('You have 5 seconds to get into eccentric position', true);
    } else if (phaseName === 'ECCENTRIC') {
        speak('Begin eccentric. Slow and controlled. ' + getMotivationalPhrase(), true);
    } else if (phaseName === 'CONCENTRIC') {
        speak('Begin concentric. Powerful lift. ' + getMotivationalPhrase(), true);
    } else if (phaseName === 'FINAL_ECCENTRIC') {
        speak('Final eccentric. Push to failure. ' + getMotivationalPhrase(), true);
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
        if (timeRemaining === 5) {
            speak('5');
        } else if (timeRemaining === 3) {
            speak('3');
        } else if (timeRemaining === 2) {
            speak('2');
        } else if (timeRemaining === 1) {
            speak('1');
        }

        // Motivational phrases at intervals
        if (currentPhase === 'ECCENTRIC' && timeRemaining === 15) {
            speak(getMotivationalPhrase());
        } else if (currentPhase === 'CONCENTRIC' && timeRemaining === 10) {
            speak(getMotivationalPhrase());
        } else if (currentPhase === 'FINAL_ECCENTRIC' && timeRemaining === 20) {
            speak('Halfway there! ' + getMotivationalPhrase());
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
    speak('Exercise complete! Excellent work!', true);
    document.getElementById('pauseBtn').style.display = 'none';
    document.getElementById('completeSection').style.display = 'block';
}

function redoExercise() {
    resetExerciseUI();
    speak('Let\'s try that again');
}

function completeExercise() {
    const exercise = WORKOUTS[currentWorkout][currentExerciseIndex];
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
    if (currentExerciseIndex < WORKOUTS[currentWorkout].length - 1) {
        currentExerciseIndex++;
        startRestPeriod();
    } else {
        finishWorkout();
    }
}

// ===== REST PERIOD =====

function startRestPeriod() {
    const settings = loadSettings();
    let restTime = settings.restDuration;

    const nextExercise = WORKOUTS[currentWorkout][currentExerciseIndex];
    document.getElementById('nextExercise').textContent = nextExercise.name;
    document.getElementById('restScreen').style.display = 'block';

    speak(`Rest for ${restTime} seconds. Next exercise: ${nextExercise.name}`);

    const restInterval = setInterval(() => {
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
        type: currentWorkout,
        date: new Date(),
        exercises: currentWorkoutData,
        duration: Math.floor((new Date() - workoutStartTime) / 1000)
    });

    localStorage.setItem('workoutHistory', JSON.stringify(history));
}

function shareWorkout() {
    const exercises = currentWorkoutData.map(ex =>
        `${ex.name}: ${ex.weight} lbs${ex.failure ? ' ✓' : ''}`
    ).join('\n');

    const text = `HIT Coach Pro Workout ${currentWorkout}\n${exercises}\n\nCompleted with HIT Coach Pro`;

    if (navigator.share) {
        navigator.share({
            title: 'HIT Coach Pro Workout',
            text: text
        });
    } else {
        // Fallback: copy to clipboard
        navigator.clipboard.writeText(text).then(() => {
            alert('Workout copied to clipboard!');
        });
    }
}

// ===== PROGRESS TRACKING =====

function loadProgressHistory() {
    const history = JSON.parse(localStorage.getItem('workoutHistory')) || [];
    const progressList = document.getElementById('progressList');

    if (history.length === 0) {
        progressList.innerHTML = '<p style="text-align: center; color: var(--text-gray); padding: 2rem;">No workout history yet. Complete your first workout!</p>';
        return;
    }

    progressList.innerHTML = '';

    // Reverse to show newest first
    history.reverse().forEach((workout, index) => {
        const date = new Date(workout.date);
        const dateStr = date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});

        const entry = document.createElement('div');
        entry.className = 'progress-entry';
        entry.dataset.workout = workout.type;

        let exercisesHTML = '';
        workout.exercises.forEach(ex => {
            exercisesHTML += `
                <div class="progress-exercise">
                    <span class="progress-exercise-name">${ex.name}</span>
                    <div>
                        <span class="progress-exercise-weight">${ex.weight} lbs</span>
                        ${ex.failure ? '<span class="progress-exercise-failure">✓ Failure</span>' : ''}
                    </div>
                </div>
            `;
        });

        entry.innerHTML = `
            <div class="progress-entry-header">
                <h3>Workout ${workout.type}</h3>
                <span class="progress-entry-date">${dateStr}</span>
            </div>
            ${exercisesHTML}
        `;

        progressList.appendChild(entry);
    });
}

function filterProgress(filter) {
    document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');

    const entries = document.querySelectorAll('.progress-entry');
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
        loadProgressHistory();
    }
}

// ===== WORKOUT SELECTION & UPGRADE PROMPTS =====

function loadWorkout(workoutType) {
    // Check if valid workout type
    if (!WORKOUTS[workoutType]) {
        console.error('Invalid workout type:', workoutType);
        return;
    }

    // Set current workout and start it
    currentWorkout = workoutType;

    // Switch to workout selection screen
    showScreen('workoutScreen');

    // Display workout details
    document.getElementById('workoutType').textContent =
        workoutType === 'FREE' ? 'Quick Start' : `Workout ${workoutType}`;

    // Generate exercise list
    const exerciseListHTML = WORKOUTS[workoutType].map((exercise, index) => {
        return `
            <div class="exercise-item" onclick="selectExercise(${index})">
                <div class="exercise-icon">${exercise.icon}</div>
                <div class="exercise-info">
                    <div class="exercise-name">${exercise.name}</div>
                    <div class="exercise-muscle">${exercise.muscle}</div>
                </div>
                <div class="exercise-number">${index + 1}</div>
            </div>
        `;
    }).join('');

    document.getElementById('exerciseList').innerHTML = exerciseListHTML;

    // Reset current exercise index
    currentExerciseIndex = 0;
    currentWorkoutData = [];
    workoutStartTime = null;

    // Track workout start for free users (for upgrade prompts)
    if (workoutType === 'FREE') {
        trackFreeWorkoutStart();
    }
}

function trackFreeWorkoutStart() {
    // Track number of free workouts completed
    let freeWorkoutCount = parseInt(localStorage.getItem('freeWorkoutCount') || '0');
    freeWorkoutCount++;
    localStorage.setItem('freeWorkoutCount', freeWorkoutCount.toString());

    // Show upgrade prompt after 3-5 workouts
    if (freeWorkoutCount >= 3 && freeWorkoutCount % 2 === 1) {
        // Show on workout 3, 5, 7, etc.
        setTimeout(() => {
            showUpgradePromptModal();
        }, 2000); // Show after 2 seconds
    }
}

function showUpgradePrompt(workoutType) {
    // Show modal explaining this is a premium workout
    const modal = document.getElementById('upgradeModal');
    const modalContent = modal.querySelector('.upgrade-modal-content');

    // Update modal content based on which locked workout was clicked
    const workoutName = workoutType === 'A' ? 'Workout A (Push Focus)' : 'Workout B (Pull Focus)';

    modalContent.querySelector('h2').textContent = `Unlock ${workoutName}`;

    modal.classList.add('active');

    // Close modal when clicking outside
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeUpgradeModal();
        }
    });
}

function showUpgradePromptModal() {
    // Generic upgrade prompt for free users
    const modal = document.getElementById('upgradeModal');
    const modalContent = modal.querySelector('.upgrade-modal-content');

    modalContent.querySelector('h2').textContent = 'Ready for More Variety?';

    modal.classList.add('active');
}

function closeUpgradeModal() {
    document.getElementById('upgradeModal').classList.remove('active');
}

function selectExercise(index) {
    currentExerciseIndex = index;
    const exercise = WORKOUTS[currentWorkout][index];

    // Update UI with selected exercise
    document.getElementById('currentExercise').textContent = exercise.name;
    document.getElementById('currentMuscle').textContent = exercise.muscle;
    document.getElementById('exerciseIcon').textContent = exercise.icon;

    // Show weight entry screen
    showScreen('weightScreen');
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

// Detect iOS
function detectIOS() {
    const ua = window.navigator.userAgent;
    const iOS = !!ua.match(/iPad/i) || !!ua.match(/iPhone/i);
    const webkit = !!ua.match(/WebKit/i);
    isIOSDevice = iOS && webkit && !ua.match(/CriOS/i);
    return isIOSDevice;
}

// Check if app is already installed
function isAppInstalled() {
    // Check if running in standalone mode
    if (window.matchMedia('(display-mode: standalone)').matches) {
        return true;
    }
    // Check for iOS standalone
    if (window.navigator.standalone === true) {
        return true;
    }
    return false;
}

// Show install prompt
function showInstallPrompt() {
    // Don't show if already installed
    if (isAppInstalled()) {
        return;
    }

    // Check if user dismissed it recently
    const dismissedTime = localStorage.getItem('installPromptDismissed');
    if (dismissedTime) {
        const daysSinceDismissed = (Date.now() - parseInt(dismissedTime)) / (1000 * 60 * 60 * 24);
        if (daysSinceDismissed < 7) {
            return; // Don't show again for 7 days
        }
    }

    // Show iOS-specific instructions for Safari
    if (detectIOS()) {
        setTimeout(() => {
            document.getElementById('iosInstallPrompt').style.display = 'flex';
        }, 3000); // Show after 3 seconds
    } else if (deferredPrompt) {
        // Show banner for Android/Desktop
        document.getElementById('installBanner').style.display = 'block';
    }
}

// Capture install prompt event (Android/Desktop)
window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    showInstallPrompt();
});

// Handle install button click
document.addEventListener('DOMContentLoaded', () => {
    const installButton = document.getElementById('installButton');
    const dismissButton = document.getElementById('dismissInstall');

    if (installButton) {
        installButton.addEventListener('click', async () => {
            if (!deferredPrompt) {
                return;
            }

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

// Close iOS prompt
function closeIOSPrompt() {
    document.getElementById('iosInstallPrompt').style.display = 'none';
    localStorage.setItem('installPromptDismissed', Date.now().toString());
}

// Track successful install
window.addEventListener('appinstalled', () => {
    console.log('PWA installed successfully');
    document.getElementById('installBanner').style.display = 'none';
    document.getElementById('iosInstallPrompt').style.display = 'none';
});

// ===== INITIALIZATION =====

document.addEventListener('DOMContentLoaded', () => {
    loadSettings();
    loadPhaseSettings();

    // Load voices when available
    if (speechSynthesis.onvoiceschanged !== undefined) {
        speechSynthesis.onvoiceschanged = () => {
            speechSynthesis.getVoices();
        };
    }

    // Show settings button handler
    document.getElementById('settingsBtn').addEventListener('click', () => {
        showScreen('settingsScreen');
    });

    // Prevent screen sleep on mobile
    if ('wakeLock' in navigator) {
        navigator.wakeLock.request('screen').catch(err => {
            console.log('Wake lock error:', err);
        });
    }

    // Show install prompt after a delay
    setTimeout(showInstallPrompt, 5000);
});

// ===== UTILITY FUNCTIONS =====

function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${String(secs).padStart(2, '0')}`;
}

// Prevent accidental page close during workout
window.addEventListener('beforeunload', (e) => {
    if (timerInterval && !isPaused) {
        e.preventDefault();
        e.returnValue = '';
    }
});
