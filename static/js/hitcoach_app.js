// HIT Coach Pro Web App JavaScript - Redesigned

// ===== DATA STRUCTURES =====

const WORKOUTS = {
    A: [
        { name: 'Leg Press', icon: '⬇️', muscle: 'Legs' },
        { name: 'Pulldown', icon: '⬆️', muscle: 'Back' },
        { name: 'Chest Press', icon: '➡️', muscle: 'Chest' },
        { name: 'Overhead', icon: '🔼', muscle: 'Shoulders' },
        { name: 'Leg Curl', icon: '🔄', muscle: 'Hamstrings' },
        { name: 'Bicep Curl', icon: '⤴️', muscle: 'Biceps' },
        { name: 'Tricep Extension', icon: '⤵️', muscle: 'Triceps' },
        { name: 'Calf Raise', icon: '📈', muscle: 'Calves' }
    ],
    B: [
        { name: 'Leg Extension', icon: '↗️', muscle: 'Quads' },
        { name: 'Seated Row', icon: '⬅️', muscle: 'Back' },
        { name: 'Incline Press', icon: '↖️', muscle: 'Upper Chest' },
        { name: 'Lateral Raise', icon: '↔️', muscle: 'Shoulders' },
        { name: 'Leg Curl', icon: '🔄', muscle: 'Hamstrings' },
        { name: 'Shrug', icon: '⏫', muscle: 'Traps' },
        { name: 'Ab Crunch', icon: '🎯', muscle: 'Abs' },
        { name: 'Back Extension', icon: '↩️', muscle: 'Lower Back' }
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
        <div class="exercise-item" onclick="startWorkoutFromExercise(${index})">
            <div class="exercise-icon">${exercise.icon}</div>
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
    } else if (screenId === 'workoutScreen' || screenId === 'summaryScreen') {
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
    document.getElementById('exerciseIconDisplay').textContent = exercise.icon;

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
});

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
