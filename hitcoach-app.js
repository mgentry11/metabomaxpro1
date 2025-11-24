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
let exerciseStartTime = null;
let totalExerciseDuration = 0;

// ===== SETTINGS =====

function loadSettings() {
    const settings = JSON.parse(localStorage.getItem('hitCoachSettings')) || {
        voiceEnabled: true,
        voiceGender: 'female',
        restDuration: 60,
        coachingStyle: 'motivational',
        theme: 'dark',
        volume: 100,
        notificationsEnabled: false,
        reminderInterval: 72,
        autoComplete: false
    };

    voiceEnabled = settings.voiceEnabled;
    document.getElementById('voiceToggle').checked = settings.voiceEnabled;
    document.getElementById('voiceGender').value = settings.voiceGender;
    document.getElementById('restDuration').value = settings.restDuration;
    document.getElementById('coachingStyle').value = settings.coachingStyle;
    document.getElementById('volumeSlider').value = settings.volume;
    document.getElementById('volumeDisplay').textContent = settings.volume + '%';
    document.getElementById('notificationsToggle').checked = settings.notificationsEnabled;
    document.getElementById('reminderInterval').value = settings.reminderInterval;
    document.getElementById('autoCompleteToggle').checked = settings.autoComplete;

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
        volume: parseInt(document.getElementById('volumeSlider').value),
        notificationsEnabled: document.getElementById('notificationsToggle').checked,
        reminderInterval: parseInt(document.getElementById('reminderInterval').value),
        autoComplete: document.getElementById('autoCompleteToggle').checked
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

function setTheme(theme, event) {
    document.querySelectorAll('.theme-btn').forEach(btn => btn.classList.remove('active'));
    if (event && event.target) {
        event.target.classList.add('active');
    }

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

function toggleAutoComplete() {
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

    // Load last weight for this exercise and show stats
    const lastWeight = getLastWeight(exercise.name);
    const stats = getExerciseStats(exercise.name);

    if (lastWeight) {
        let statsText = `Last time: ${lastWeight} lbs`;
        if (stats && stats.personalRecord) {
            statsText += ` | PR: ${stats.personalRecord} lbs`;
        }
        document.getElementById('lastWeight').textContent = statsText;
        document.getElementById('weightInput').value = lastWeight;
    } else {
        document.getElementById('lastWeight').textContent = '';
        document.getElementById('weightInput').value = '';
    }

    // Display weight recommendation
    displayWeightRecommendation(exercise.name);

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
    document.getElementById('completeExerciseBtn').style.display = 'none';
    document.getElementById('completeSection').style.display = 'none';
    document.getElementById('restScreen').style.display = 'none';
    document.getElementById('failureCheck').checked = false;
    document.getElementById('exerciseStatus').textContent = '';
    document.getElementById('exerciseStatus').className = 'exercise-completion-status';
    exerciseStartTime = null;
    totalExerciseDuration = 0;
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

    // Track exercise start time
    exerciseStartTime = Date.now();

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
    // Calculate total exercise duration
    if (exerciseStartTime) {
        totalExerciseDuration = Math.floor((Date.now() - exerciseStartTime) / 1000);
    }

    const settings = loadSettings();

    speak('You are done! Excellent work!', true);
    document.getElementById('pauseBtn').style.display = 'none';

    // Change the START button to COMPLETE EXERCISE button with green styling
    const completeBtn = document.getElementById('completeExerciseBtn');
    completeBtn.style.display = 'block';
    completeBtn.style.backgroundColor = '#10b981'; // Green success state
    completeBtn.style.borderColor = '#10b981';

    // Visual confirmation in exercise status
    const statusEl = document.getElementById('exerciseStatus');
    statusEl.textContent = 'TIMER COMPLETE';
    statusEl.className = 'exercise-completion-status completed';
    statusEl.style.color = '#10b981';
    statusEl.style.fontWeight = 'bold';
    statusEl.style.fontSize = '1.1rem';
    statusEl.style.marginTop = '1rem';

    // If auto-complete is enabled, automatically move to next
    if (settings.autoComplete) {
        const weight = parseFloat(document.getElementById('weightInput').value) || 0;
        if (weight > 0) {
            // Auto-complete after 2 seconds
            setTimeout(() => {
                completeExercise();
            }, 2000);
            speak('Auto completing exercise');
        } else {
            // Show completion section if no weight entered
            showCompleteSection();
        }
    }
}

function showCompleteSection() {
    const weight = parseFloat(document.getElementById('weightInput').value) || 0;

    // Show or hide weight input in complete section based on whether it's already entered
    const completeWeightSection = document.getElementById('completeWeightSection');
    const completeWeightInput = document.getElementById('completeWeightInput');

    if (weight === 0) {
        completeWeightSection.style.display = 'block';
        completeWeightInput.value = '';
        // Copy last weight suggestion if available
        const lastWeight = getLastWeight(WORKOUTS[currentWorkout][currentExerciseIndex].name);
        if (lastWeight) {
            completeWeightInput.placeholder = `Last: ${lastWeight} lbs`;
        }
    } else {
        completeWeightSection.style.display = 'none';
    }

    document.getElementById('completeSection').style.display = 'block';
}

function redoExercise() {
    resetExerciseUI();
    speak('Let\'s try that again');
}

function completeExercise() {
    const exercise = WORKOUTS[currentWorkout][currentExerciseIndex];

    // Get weight from either the main input or the complete section input
    let weight = parseFloat(document.getElementById('weightInput').value) || 0;
    if (weight === 0) {
        weight = parseFloat(document.getElementById('completeWeightInput').value) || 0;
    }

    const reachedFailure = document.getElementById('failureCheck').checked;

    if (weight === 0) {
        alert('Please enter the weight used for this exercise');
        return;
    }

    // Calculate duration if not already set
    if (totalExerciseDuration === 0 && exerciseStartTime) {
        totalExerciseDuration = Math.floor((Date.now() - exerciseStartTime) / 1000);
    }

    // Get current date and time
    const now = new Date();
    const dateStr = now.toISOString().split('T')[0]; // YYYY-MM-DD format
    const timeStr = now.toTimeString().split(' ')[0]; // HH:MM:SS format

    // Save exercise data with detailed logging including duration
    const exerciseData = {
        exerciseName: exercise.name,
        name: exercise.name, // Keep for backwards compatibility
        weight: weight,
        failure: reachedFailure,
        date: dateStr,
        time: timeStr,
        timestamp: now,
        workout: currentWorkout,
        duration: totalExerciseDuration
    };

    currentWorkoutData.push(exerciseData);

    // Log to detailed exercise history
    logExerciseData(exerciseData);

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

    const workoutRecord = {
        type: currentWorkout,
        date: new Date(),
        exercises: currentWorkoutData,
        duration: Math.floor((new Date() - workoutStartTime) / 1000)
    };

    history.push(workoutRecord);
    localStorage.setItem('workoutHistory', JSON.stringify(history));

    // Update last workout timestamp for notifications
    localStorage.setItem('lastWorkoutTimestamp', Date.now().toString());

    // Schedule next workout reminder
    scheduleWorkoutReminder();
}

// ===== EXERCISE DATA LOGGING =====

function logExerciseData(exerciseData) {
    // Get existing exercise log
    const exerciseLog = JSON.parse(localStorage.getItem('exerciseLog')) || {};

    // Initialize exercise array if it doesn't exist
    if (!exerciseLog[exerciseData.name]) {
        exerciseLog[exerciseData.name] = [];
    }

    // Add this exercise session with all data including duration
    exerciseLog[exerciseData.name].push({
        weight: exerciseData.weight,
        failure: exerciseData.failure,
        timestamp: exerciseData.timestamp,
        date: exerciseData.date,
        time: exerciseData.time,
        workout: exerciseData.workout,
        duration: exerciseData.duration || 0
    });

    // Save back to localStorage
    localStorage.setItem('exerciseLog', JSON.stringify(exerciseLog));
}

function getExerciseHistory(exerciseName) {
    const exerciseLog = JSON.parse(localStorage.getItem('exerciseLog')) || {};
    return exerciseLog[exerciseName] || [];
}

function getExerciseStats(exerciseName) {
    const history = getExerciseHistory(exerciseName);

    if (history.length === 0) {
        return null;
    }

    const weights = history.map(entry => entry.weight);
    const maxWeight = Math.max(...weights);
    const avgWeight = weights.reduce((a, b) => a + b, 0) / weights.length;
    const lastWeight = weights[weights.length - 1];

    return {
        totalSessions: history.length,
        maxWeight: maxWeight,
        avgWeight: avgWeight,
        lastWeight: lastWeight,
        personalRecord: maxWeight
    };
}

// ===== WEIGHT RECOMMENDATION SYSTEM =====

function getWeightRecommendation(exerciseName) {
    const history = getExerciseHistory(exerciseName);

    if (history.length === 0) {
        return null;
    }

    const lastSession = history[history.length - 1];
    const last3Sessions = history.slice(-3);
    const last4Sessions = history.slice(-4);

    let recommendedWeight = lastSession.weight;
    let reasoning = '';
    let category = 'maintain'; // maintain, increase, deload, plateau

    // RULE 1: If last session reached failure, suggest 2.5% increase (rounded to nearest 5 lbs)
    if (lastSession.failure) {
        const increase = lastSession.weight * 0.025;
        recommendedWeight = roundToNearest5(lastSession.weight + increase);
        reasoning = 'You reached failure last time - time to increase!';
        category = 'increase';
    }
    // RULE 2: If last session didn't reach failure, suggest same weight
    else if (!lastSession.failure) {
        recommendedWeight = lastSession.weight;
        reasoning = 'Didn\'t reach failure last time - aim for failure at this weight';
        category = 'maintain';
    }

    // RULE 3: Check for plateau (3+ sessions with no PR)
    if (last3Sessions.length >= 3) {
        const weights = last3Sessions.map(s => s.weight);
        const allSameWeight = weights.every(w => w === weights[0]);
        const noFailures = last3Sessions.every(s => !s.failure);

        if (allSameWeight && noFailures) {
            // Plateau detected - suggest deload
            recommendedWeight = roundToNearest5(lastSession.weight * 0.90);
            reasoning = 'Plateau detected (3 sessions, no failure) - deload 10% and rebuild';
            category = 'deload';
        }
    }

    // RULE 4: Extended plateau detection (4+ sessions with minimal progress)
    if (last4Sessions.length >= 4) {
        const weights = last4Sessions.map(s => s.weight);
        const maxWeight = Math.max(...weights);
        const currentWeight = lastSession.weight;

        // If no progress in last 4 sessions
        if (currentWeight < maxWeight * 0.95) {
            // Suggest deload
            recommendedWeight = roundToNearest5(maxWeight * 0.85);
            reasoning = 'Extended plateau - deload to 85% of recent peak and rebuild';
            category = 'deload';
        }
    }

    return {
        weight: recommendedWeight,
        reasoning: reasoning,
        category: category,
        lastWeight: lastSession.weight,
        lastFailure: lastSession.failure
    };
}

function roundToNearest5(num) {
    return Math.round(num / 5) * 5;
}

function displayWeightRecommendation(exerciseName) {
    const recommendation = getWeightRecommendation(exerciseName);
    const recommendationEl = document.getElementById('weightRecommendation');

    if (!recommendation) {
        recommendationEl.style.display = 'none';
        return;
    }

    recommendationEl.style.display = 'block';

    // Set category class for styling
    recommendationEl.className = 'weight-recommendation';
    recommendationEl.classList.add(`recommendation-${recommendation.category}`);

    // Build recommendation HTML
    let icon = '💪';
    if (recommendation.category === 'increase') {
        icon = '📈';
    } else if (recommendation.category === 'deload') {
        icon = '🔄';
    } else if (recommendation.category === 'plateau') {
        icon = '⚠️';
    }

    const changeIndicator = recommendation.weight > recommendation.lastWeight ? '↗️' :
                           recommendation.weight < recommendation.lastWeight ? '↘️' : '➡️';

    recommendationEl.innerHTML = `
        <div class="recommendation-header">
            <span class="recommendation-icon">${icon}</span>
            <div class="recommendation-content">
                <div class="recommendation-weight">
                    <span class="recommended-label">Recommended:</span>
                    <span class="recommended-value">${recommendation.weight} lbs</span>
                    <span class="weight-change">${changeIndicator}</span>
                </div>
                <div class="recommendation-reason">${recommendation.reasoning}</div>
                <div class="recommendation-last">
                    Last time: ${recommendation.lastWeight} lbs
                    ${recommendation.lastFailure ? '<span class="failure-badge">✓ Failure</span>' : '<span class="no-failure-badge">No Failure</span>'}
                </div>
            </div>
        </div>
        <button class="btn-use-recommended" onclick="useRecommendedWeight(${recommendation.weight})">
            Use Recommended Weight
        </button>
    `;
}

function useRecommendedWeight(weight) {
    document.getElementById('weightInput').value = weight;
    speak(`Weight set to ${weight} pounds`);
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
            // Get stats for this exercise
            const stats = getExerciseStats(ex.name);
            const isPR = stats && ex.weight === stats.personalRecord;

            // Format duration if available
            let durationText = '';
            if (ex.duration) {
                const mins = Math.floor(ex.duration / 60);
                const secs = ex.duration % 60;
                durationText = `<span class="progress-exercise-duration" style="color: var(--text-gray); font-size: 0.85rem;">${mins}:${String(secs).padStart(2, '0')}</span>`;
            }

            exercisesHTML += `
                <div class="progress-exercise">
                    <div style="display: flex; flex-direction: column; gap: 0.25rem;">
                        <span class="progress-exercise-name">${ex.name}</span>
                        ${durationText}
                    </div>
                    <div style="display: flex; gap: 0.5rem; align-items: center;">
                        <span class="progress-exercise-weight">${ex.weight} lbs</span>
                        ${ex.failure ? '<span class="progress-exercise-failure">✓ Failure</span>' : ''}
                        ${isPR ? '<span class="progress-exercise-pr">🏆 PR</span>' : ''}
                    </div>
                </div>
            `;
        });

        const duration = workout.duration;
        const minutes = Math.floor(duration / 60);
        const seconds = duration % 60;
        const durationStr = `${minutes}:${String(seconds).padStart(2, '0')}`;

        entry.innerHTML = `
            <div class="progress-entry-header">
                <h3>Workout ${workout.type}</h3>
                <div style="display: flex; flex-direction: column; align-items: flex-end; gap: 0.25rem;">
                    <span class="progress-entry-date">${dateStr}</span>
                    <span class="progress-entry-duration">${durationStr}</span>
                </div>
            </div>
            ${exercisesHTML}
        `;

        progressList.appendChild(entry);
    });
}

function filterProgress(filter, event) {
    document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
    if (event && event.target) {
        event.target.classList.add('active');
    }

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

// ===== WORKOUT NOTIFICATIONS =====

function toggleNotifications() {
    const enabled = document.getElementById('notificationsToggle').checked;

    if (enabled) {
        requestNotificationPermission();
    } else {
        cancelWorkoutReminder();
    }

    saveSettings();
}

function requestNotificationPermission() {
    if (!('Notification' in window)) {
        alert('This browser does not support notifications');
        document.getElementById('notificationsToggle').checked = false;
        saveSettings();
        return;
    }

    if (Notification.permission === 'granted') {
        scheduleWorkoutReminder();
    } else if (Notification.permission !== 'denied') {
        Notification.requestPermission().then(permission => {
            if (permission === 'granted') {
                scheduleWorkoutReminder();
                showNotification('Workout Reminders Enabled', 'You will be notified when it\'s time for your next workout!');
            } else {
                document.getElementById('notificationsToggle').checked = false;
                saveSettings();
            }
        });
    } else {
        alert('Notifications are blocked. Please enable them in your browser settings.');
        document.getElementById('notificationsToggle').checked = false;
        saveSettings();
    }
}

function scheduleWorkoutReminder() {
    const settings = loadSettings();

    if (!settings.notificationsEnabled) {
        return;
    }

    // Cancel any existing reminder
    cancelWorkoutReminder();

    const lastWorkoutTime = parseInt(localStorage.getItem('lastWorkoutTimestamp') || '0');

    if (lastWorkoutTime === 0) {
        // No workouts yet, don't schedule
        return;
    }

    const reminderInterval = settings.reminderInterval * 60 * 60 * 1000; // Convert hours to milliseconds
    const nextReminderTime = lastWorkoutTime + reminderInterval;
    const now = Date.now();
    const timeUntilReminder = nextReminderTime - now;

    if (timeUntilReminder > 0) {
        const reminderTimeoutId = setTimeout(() => {
            showNotification(
                'Time for Your Next Workout!',
                'It\'s been ' + settings.reminderInterval + ' hours since your last workout. Ready to build more strength?'
            );
            // Don't update timestamp or reschedule - let the next actual workout trigger the next reminder
            // This prevents infinite notification loops
        }, timeUntilReminder);

        localStorage.setItem('reminderTimeoutId', reminderTimeoutId.toString());
    }
}

function cancelWorkoutReminder() {
    const timeoutId = localStorage.getItem('reminderTimeoutId');
    if (timeoutId) {
        clearTimeout(parseInt(timeoutId));
        localStorage.removeItem('reminderTimeoutId');
    }
}

function showNotification(title, body) {
    if (!('Notification' in window) || Notification.permission !== 'granted') {
        return;
    }

    const notification = new Notification(title, {
        body: body,
        icon: '/icons/icon-192.png',
        badge: '/icons/icon-72.png',
        tag: 'workout-reminder',
        requireInteraction: false,
        vibrate: [200, 100, 200]
    });

    notification.onclick = () => {
        window.focus();
        notification.close();
    };
}

function checkWorkoutReminders() {
    const settings = loadSettings();

    if (!settings.notificationsEnabled) {
        return;
    }

    const lastWorkoutTime = parseInt(localStorage.getItem('lastWorkoutTimestamp') || '0');

    if (lastWorkoutTime === 0) {
        return;
    }

    const reminderInterval = settings.reminderInterval * 60 * 60 * 1000;
    const now = Date.now();
    const timeSinceLastWorkout = now - lastWorkoutTime;

    if (timeSinceLastWorkout >= reminderInterval) {
        showNotification(
            'Time for Your Next Workout!',
            'It\'s been ' + Math.floor(timeSinceLastWorkout / (60 * 60 * 1000)) + ' hours since your last workout. Ready to build more strength?'
        );
    }
}

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

    // Check for workout reminders on load
    checkWorkoutReminders();

    // Schedule workout reminder if enabled
    const settings = loadSettings();
    if (settings.notificationsEnabled) {
        scheduleWorkoutReminder();
    }
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
