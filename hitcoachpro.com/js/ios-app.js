// HIT Coach Pro - iOS-Style Web App

// ============================================================================
// Data & State
// ============================================================================

const defaultExercises = {
    A: [
        { name: 'Leg Press', weight: null, completed: false },
        { name: 'Pulldown', weight: null, completed: false },
        { name: 'Chest Press', weight: null, completed: false },
        { name: 'Overhead Press', weight: null, completed: false },
        { name: 'Leg Curl', weight: null, completed: false },
        { name: 'Bicep Curl', weight: null, completed: false },
        { name: 'Tricep Extension', weight: null, completed: false },
        { name: 'Calf Raise', weight: null, completed: false }
    ],
    B: [
        { name: 'Leg Extension', weight: null, completed: false },
        { name: 'Seated Row', weight: null, completed: false },
        { name: 'Incline Press', weight: null, completed: false },
        { name: 'Lateral Raise', weight: null, completed: false },
        { name: 'Leg Curl', weight: null, completed: false },
        { name: 'Shrug', weight: null, completed: false },
        { name: 'Ab Crunch', weight: null, completed: false },
        { name: 'Back Extension', weight: null, completed: false }
    ]
};

let state = {
    currentWorkout: 'A',
    currentProfile: 0, // 0 or 1 for two profiles
    currentExerciseIndex: 0,
    settings: {
        voice: 'male',
        displaySize: 'normal',
        restDuration: 90,
        prep: 10,
        positioning: 8,
        eccentric: 30,
        concentric: 20,
        finalEccentric: 40
    },
    profiles: [
        {
            name: 'Profile 1',
            units: 'lbs',
            experience: 'intermediate',
            exercises: JSON.parse(JSON.stringify(defaultExercises)),
            workoutLogs: [],
            todayCompleted: []
        },
        {
            name: 'Profile 2',
            units: 'lbs',
            experience: 'intermediate',
            exercises: JSON.parse(JSON.stringify(defaultExercises)),
            workoutLogs: [],
            todayCompleted: []
        }
    ]
};

// Helper to get current profile
function getCurrentProfile() {
    return state.profiles[state.currentProfile];
}

// Helper to get exercises for current profile
function getExercises() {
    return getCurrentProfile().exercises;
}

// Helper to get today completed for current profile
function getTodayCompleted() {
    const profile = getCurrentProfile();
    if (!profile.todayCompletedSet) {
        profile.todayCompletedSet = new Set(profile.todayCompleted || []);
    }
    return profile.todayCompletedSet;
}

// Helper to get workout logs for current profile
function getWorkoutLogs() {
    return getCurrentProfile().workoutLogs;
}

// Timer state
let timerState = {
    phase: 'prep', // prep, positioning, eccentric, concentric, finalEccentric, complete
    seconds: 10,
    isRunning: false,
    intervalId: null
};

let restTimerState = {
    seconds: 90,
    isRunning: false,
    intervalId: null
};

// Speech synthesis
let synth = window.speechSynthesis;
let currentVoice = null;

// Audio files system
const audioCache = {};
let audioEnabled = false;
let audioQueue = [];
let isPlayingAudio = false;
let currentPlayingAudio = null;

// Map of speech text to audio file names
const audioFileMap = {
    // Phase announcements
    'get ready': 'phase_get_ready',
    'position yourself': 'phase_position',
    'get into position': 'cue_get_position',
    'eccentric phase': 'phase_eccentric',
    'eccentric phase. lower slowly': 'phase_eccentric',
    'concentric phase': 'phase_concentric',
    'concentric phase. push': 'phase_concentric',
    'final eccentric': 'phase_final_eccentric',
    'final eccentric. all the way down': 'phase_final_eccentric',
    'exercise complete': 'phase_complete',
    'rest period': 'phase_rest',

    // Countdown numbers 1-60
    '1': 'num_1', '2': 'num_2', '3': 'num_3', '4': 'num_4', '5': 'num_5',
    '6': 'num_6', '7': 'num_7', '8': 'num_8', '9': 'num_9', '10': 'num_10',
    '11': 'num_11', '12': 'num_12', '13': 'num_13', '14': 'num_14', '15': 'num_15',
    '16': 'num_16', '17': 'num_17', '18': 'num_18', '19': 'num_19', '20': 'num_20',
    '21': 'num_21', '22': 'num_22', '23': 'num_23', '24': 'num_24', '25': 'num_25',
    '26': 'num_26', '27': 'num_27', '28': 'num_28', '29': 'num_29', '30': 'num_30',
    '31': 'num_31', '32': 'num_32', '33': 'num_33', '34': 'num_34', '35': 'num_35',
    '36': 'num_36', '37': 'num_37', '38': 'num_38', '39': 'num_39', '40': 'num_40',
    '41': 'num_41', '42': 'num_42', '43': 'num_43', '44': 'num_44', '45': 'num_45',
    '46': 'num_46', '47': 'num_47', '48': 'num_48', '49': 'num_49', '50': 'num_50',
    '51': 'num_51', '52': 'num_52', '53': 'num_53', '54': 'num_54', '55': 'num_55',
    '56': 'num_56', '57': 'num_57', '58': 'num_58', '59': 'num_59', '60': 'num_60',

    // Time warnings
    'thirty seconds remaining': 'time_30_sec',
    'twenty seconds remaining': 'time_20_sec',
    'ten seconds remaining': 'time_10_sec',
    'five seconds remaining': 'time_5_sec',
    'halfway there': 'time_halfway',
    'almost done': 'time_almost',

    // Positioning cues
    'get into position': 'cue_get_position',
    'find your starting weight': 'cue_starting_weight',
    'grip the handles': 'cue_grip',
    'set your posture': 'cue_posture',
    'control the movement': 'cue_control',

    // Eccentric coaching
    'lower slowly': 'ecc_lower_slowly',
    'control the weight': 'ecc_control_weight',
    'feel the stretch': 'ecc_feel_stretch',
    'nice and slow': 'ecc_nice_slow',
    'keep tension on the muscle': 'ecc_keep_tension',
    'resist the weight': 'ecc_resist',
    'smooth and controlled': 'ecc_smooth',

    // Concentric coaching
    'push now': 'con_push_now',
    'drive up': 'con_drive_up',
    'squeeze at the top': 'con_squeeze',
    'power through': 'con_power',
    'strong push': 'con_strong_push',
    'keep pushing': 'con_keep_pushing',
    'contract the muscle': 'con_contract',
    'push': 'con_push_now',

    // Final eccentric coaching
    'final negative': 'final_negative',
    'all the way down': 'final_all_way',
    'maximum time under tension': 'final_max_tension',
    'fight the weight': 'final_fight',
    'slow as possible': 'final_slow',
    'control it': 'final_control',
    "don't give up": 'final_dont_give_up',
    'last push of effort': 'final_last_push',

    // Encouragement
    'great work': 'enc_great_work',
    'you got this': 'enc_you_got_this',
    'stay strong': 'enc_stay_strong',
    'keep going': 'enc_keep_going',
    'almost there': 'enc_almost_there',
    'excellent form': 'enc_excellent_form',
    "that's it": 'enc_thats_it',
    'perfect': 'enc_perfect',
    'well done': 'enc_well_done',
    'fantastic effort': 'enc_fantastic',
    'one more': 'enc_one_more',
    'push through': 'enc_push_through',
    "you're doing great": 'enc_doing_great',
    'strong finish': 'enc_strong_finish',
    'exercise complete. well done': 'enc_well_done',

    // Rest period
    'rest period starting': 'rest_starting',
    'take a breath': 'rest_breathe',
    'recover': 'rest_recover',
    'get ready for the next exercise': 'rest_get_ready',
    'thirty seconds of rest remaining': 'rest_30_sec',
    'fifteen seconds until next exercise': 'rest_15_sec',
    'next exercise coming up': 'rest_next_coming',
    'rest complete': 'rest_complete',

    // Exercise transitions
    'next exercise': 'trans_next',
    'moving on': 'trans_moving',
    'prepare for the next exercise': 'trans_prepare',

    // Workout start/end
    'workout starting': 'workout_starting',
    "let's begin": 'workout_begin',
    'workout complete': 'workout_complete',
    'great session': 'workout_great_session',
    'you crushed it': 'workout_crushed',
    'see you next time': 'workout_see_you',
    'workout complete! great job': 'workout_complete',

    // Exercise names
    'leg press': 'ex_leg_press',
    'pulldown': 'ex_pulldown',
    'chest press': 'ex_chest_press',
    'overhead press': 'ex_overhead_press',
    'leg curl': 'ex_leg_curl',
    'bicep curl': 'ex_bicep_curl',
    'tricep extension': 'ex_tricep_extension',
    'calf raise': 'ex_calf_raise',
    'leg extension': 'ex_leg_extension',
    'seated row': 'ex_seated_row',
    'incline press': 'ex_incline_press',
    'lateral raise': 'ex_lateral_raise',
    'shrug': 'ex_shrug',
    'ab crunch': 'ex_ab_crunch',
    'back extension': 'ex_back_extension'
};

// ============================================================================
// Storage
// ============================================================================

function loadState() {
    const saved = localStorage.getItem('hcp-ios-state');
    if (saved) {
        const parsed = JSON.parse(saved);
        state.settings = { ...state.settings, ...parsed.settings };
        state.currentProfile = parsed.currentProfile || 0;
        state.currentWorkout = parsed.currentWorkout || 'A';

        // Load profiles array
        if (parsed.profiles && parsed.profiles.length >= 2) {
            state.profiles = parsed.profiles;
        }

        // Migrate old data structure to new profiles
        if (parsed.exercises && !parsed.profiles) {
            state.profiles[0].exercises = parsed.exercises;
        }
        if (parsed.workoutLogs && !parsed.profiles) {
            state.profiles[0].workoutLogs = parsed.workoutLogs;
        }
        if (parsed.profile && !parsed.profiles) {
            state.profiles[0].name = parsed.profile.name || 'Profile 1';
            state.profiles[0].units = parsed.profile.units || 'lbs';
            state.profiles[0].experience = parsed.profile.experience || 'intermediate';
        }

        // Rebuild todayCompleted Sets for each profile
        const today = new Date().toDateString();
        state.profiles.forEach(profile => {
            profile.todayCompletedSet = new Set();
            (profile.workoutLogs || []).forEach(log => {
                if (new Date(log.date).toDateString() === today) {
                    profile.todayCompletedSet.add(log.exerciseName + '-' + log.workout);
                }
            });
            // Sync to array for storage
            profile.todayCompleted = Array.from(profile.todayCompletedSet);
        });
    }

    // Update profile switcher UI
    updateProfileSwitcher();
}

function saveState() {
    // Convert Sets to arrays before saving
    state.profiles.forEach(profile => {
        if (profile.todayCompletedSet) {
            profile.todayCompleted = Array.from(profile.todayCompletedSet);
        }
    });

    localStorage.setItem('hcp-ios-state', JSON.stringify({
        settings: state.settings,
        currentProfile: state.currentProfile,
        currentWorkout: state.currentWorkout,
        profiles: state.profiles
    }));
}

function switchProfile(profileIndex) {
    if (profileIndex === state.currentProfile) return;

    // Save current state
    saveState();

    // Switch profile
    state.currentProfile = profileIndex;

    // Update UI
    updateProfileSwitcher();
    renderExerciseList();

    // Announce profile switch
    const profileName = getCurrentProfile().name || `Profile ${profileIndex + 1}`;
    queueSpeak(`Switched to ${profileName}`);

    saveState();
}

function updateProfileSwitcher() {
    document.querySelectorAll('.profile-toggle').forEach(btn => {
        const profileIdx = parseInt(btn.dataset.profile);
        btn.classList.toggle('active', profileIdx === state.currentProfile);
    });
}

function updateWorkoutPicker() {
    document.querySelectorAll('.picker-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.workout === state.currentWorkout);
    });
}

// ============================================================================
// Voice & Audio
// ============================================================================

function initVoice() {
    // Initialize Web Speech API as fallback
    if (synth) {
        const loadVoices = () => {
            const voices = synth.getVoices();
            if (voices.length === 0) return;

            // Try to find appropriate voice based on settings
            const voiceType = state.settings.voice;
            let targetVoice = null;

            if (voiceType === 'male' || voiceType === 'male-pro') {
                targetVoice = voices.find(v => v.name.includes('Daniel') || v.name.includes('Alex') || v.name.includes('Male'));
            } else if (voiceType === 'female' || voiceType === 'female-pro') {
                targetVoice = voices.find(v => v.name.includes('Samantha') || v.name.includes('Karen') || v.name.includes('Female'));
            }

            currentVoice = targetVoice || voices[0];
        };

        loadVoices();
        synth.onvoiceschanged = loadVoices;
    }

    // Try to preload professional audio files
    preloadAudio();
}

function preloadAudio() {
    const voiceType = state.settings.voice;

    // Only preload for professional voices
    if (voiceType !== 'commander' && voiceType !== 'male-pro' && voiceType !== 'female-pro') {
        audioEnabled = false;
        return;
    }

    // Map voice types to folders
    const voiceFolders = {
        'commander': 'commander',
        'male-pro': 'male',
        'female-pro': 'female'
    };
    const voiceFolder = voiceFolders[voiceType] || 'commander';
    const audioPath = `audio/${voiceFolder}/`;

    // Test if audio files exist by loading one
    const testAudio = new Audio(`${audioPath}phase_get_ready.mp3`);
    testAudio.addEventListener('canplaythrough', () => {
        audioEnabled = true;
        console.log('Professional audio files available');

        // Preload commonly used audio files
        const priorityFiles = [
            'phase_get_ready', 'phase_eccentric', 'phase_concentric', 'phase_final_eccentric',
            'phase_complete', 'cue_get_position', 'enc_well_done',
            'num_5', 'num_4', 'num_3', 'num_2', 'num_1'
        ];

        priorityFiles.forEach(filename => {
            const audio = new Audio(`${audioPath}${filename}.mp3`);
            audio.preload = 'auto';
            audioCache[filename] = audio;
        });
    });

    testAudio.addEventListener('error', () => {
        audioEnabled = false;
        console.log('Professional audio files not found, using speech synthesis');
    });
}

function stopCurrentAudio() {
    if (currentPlayingAudio) {
        currentPlayingAudio.pause();
        currentPlayingAudio.currentTime = 0;
        currentPlayingAudio = null;
    }
    if (synth) {
        synth.cancel();
    }
}

function playAudio(filename) {
    return new Promise((resolve, reject) => {
        const voiceType = state.settings.voice;
        const voiceFolders = {
            'commander': 'commander',
            'male-pro': 'male',
            'female-pro': 'female'
        };
        const voiceFolder = voiceFolders[voiceType] || 'commander';

        // Stop any currently playing audio first
        stopCurrentAudio();

        // Check cache first
        if (audioCache[filename]) {
            const audio = audioCache[filename].cloneNode();
            currentPlayingAudio = audio;
            audio.addEventListener('ended', () => {
                currentPlayingAudio = null;
                resolve();
            });
            audio.addEventListener('error', () => {
                currentPlayingAudio = null;
                reject();
            });
            audio.play().then(() => {}).catch(reject);
            return;
        }

        // Load and play
        const audio = new Audio(`audio/${voiceFolder}/${filename}.mp3`);
        currentPlayingAudio = audio;
        audio.addEventListener('ended', () => {
            currentPlayingAudio = null;
            resolve();
        });
        audio.addEventListener('error', () => {
            currentPlayingAudio = null;
            reject();
        });
        audio.play().catch(reject);

        // Cache for future use
        audioCache[filename] = audio;
    });
}

// Queue-based speaking to prevent overlap
function queueSpeak(text) {
    audioQueue.push(text);
    processAudioQueue();
}

function processAudioQueue() {
    if (isPlayingAudio || audioQueue.length === 0) return;

    isPlayingAudio = true;
    const text = audioQueue.shift();

    speakWithCallback(text, () => {
        isPlayingAudio = false;
        processAudioQueue();
    });
}

function speakWithCallback(text, callback) {
    const normalizedText = text.toLowerCase().trim();
    const isProfessionalVoice = state.settings.voice === 'commander' || state.settings.voice === 'male-pro' || state.settings.voice === 'female-pro';

    // Try to play professional audio if enabled
    if (audioEnabled && isProfessionalVoice) {
        let audioFile = audioFileMap[normalizedText];

        if (!audioFile) {
            for (const [phrase, file] of Object.entries(audioFileMap)) {
                if (normalizedText.includes(phrase) || phrase.includes(normalizedText)) {
                    audioFile = file;
                    break;
                }
            }
        }

        if (audioFile) {
            playAudio(audioFile)
                .then(callback)
                .catch(() => {
                    // Fallback to speech synthesis if audio fails
                    console.log('Audio file failed, using speech:', audioFile);
                    speakWithSynthCallback(text, callback);
                });
            return;
        } else {
            // No audio mapping - use speech synthesis fallback
            console.log('No audio mapping, using speech:', normalizedText);
            speakWithSynthCallback(text, callback);
            return;
        }
    }

    // Use speech synthesis
    speakWithSynthCallback(text, callback);
}

function speakWithSynthCallback(text, callback) {
    if (!synth) {
        callback();
        return;
    }

    synth.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.voice = currentVoice;
    utterance.rate = 1.0;
    utterance.pitch = state.settings.voice === 'digital' ? 0.8 : 1.0;
    utterance.onend = callback;
    utterance.onerror = callback;
    synth.speak(utterance);
}

function speak(text, rate = 1.0) {
    // Don't interrupt if audio is currently playing (for countdown numbers)
    if (isPlayingAudio || currentPlayingAudio) {
        return;
    }

    const normalizedText = text.toLowerCase().trim();
    const isProfessionalVoice = state.settings.voice === 'commander' || state.settings.voice === 'male-pro' || state.settings.voice === 'female-pro';

    // Try to play professional audio if enabled
    if (audioEnabled && isProfessionalVoice) {
        // Look for exact match or partial match
        let audioFile = audioFileMap[normalizedText];

        // If no exact match, try to find partial matches
        if (!audioFile) {
            for (const [phrase, file] of Object.entries(audioFileMap)) {
                if (normalizedText.includes(phrase) || phrase.includes(normalizedText)) {
                    audioFile = file;
                    break;
                }
            }
        }

        if (audioFile) {
            playAudioNonInterrupting(audioFile).catch(() => {
                // Fallback to speech synthesis if audio fails
                console.log('Audio failed, using speech:', audioFile);
                speakWithSynth(text, rate);
            });
            return;
        }
    }

    // Use speech synthesis for all voices as fallback
    speakWithSynth(text, rate);
}

// Play audio without stopping current audio (for countdown)
function playAudioNonInterrupting(filename) {
    return new Promise((resolve, reject) => {
        // Don't play if something else is playing
        if (currentPlayingAudio) {
            resolve();
            return;
        }

        const voiceType = state.settings.voice;
        const voiceFolders = {
            'commander': 'commander',
            'male-pro': 'male',
            'female-pro': 'female'
        };
        const voiceFolder = voiceFolders[voiceType] || 'commander';

        const audio = new Audio(`audio/${voiceFolder}/${filename}.mp3`);
        audio.addEventListener('ended', resolve);
        audio.addEventListener('error', reject);
        audio.play().catch(reject);
    });
}

function speakWithSynth(text, rate = 1.0) {
    if (!synth) return;

    synth.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.voice = currentVoice;
    utterance.rate = rate;
    utterance.pitch = state.settings.voice === 'digital' ? 0.8 : 1.0;
    synth.speak(utterance);
}

// ============================================================================
// UI Rendering
// ============================================================================

function renderExerciseList() {
    const list = document.getElementById('exercise-list');
    const exercises = getExercises()[state.currentWorkout];
    
    list.innerHTML = exercises.map((ex, index) => {
        return `
            <div class="exercise-card" data-index="${index}">
                <div class="exercise-icon">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M20.57 14.86L22 13.43 20.57 12 17 15.57 8.43 7 12 3.43 10.57 2 9.14 3.43 7.71 2 5.57 4.14 4.14 2.71 2.71 4.14l1.43 1.43L2 7.71l1.43 1.43L2 10.57 3.43 12 7 8.43 15.57 17 12 20.57 13.43 22l1.43-1.43L16.29 22l2.14-2.14 1.43 1.43 1.43-1.43-1.43-1.43L22 16.29z"/>
                    </svg>
                </div>
                <div class="exercise-info">
                    <div class="exercise-name">${ex.name}</div>
                </div>
                <div class="exercise-status">
                    <span class="chevron">›</span>
                </div>
            </div>
        `;
    }).join('');

    // Add click handlers
    document.querySelectorAll('.exercise-card').forEach(card => {
        card.addEventListener('click', (e) => {
            const index = parseInt(card.dataset.index);
            // Open log modal instead of starting exercise directly
            openLogModal(index);
        });
    });

    updateProgress();
}

function updateProgress() {
    const exercises = getExercises()[state.currentWorkout];
    const todayCompleted = getTodayCompleted();
    const completed = exercises.filter(ex =>
        todayCompleted.has(ex.name + '-' + state.currentWorkout)
    ).length;
    document.getElementById('progress-text').textContent = `${completed}/${exercises.length} Completed Today`;
}

function updateSettingsUI() {
    // Voice
    document.querySelectorAll('#voice-control .voice-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.value === state.settings.voice);
    });

    // Rest duration
    document.querySelectorAll('#rest-control .seg-btn').forEach(btn => {
        btn.classList.toggle('active', parseInt(btn.dataset.value) === state.settings.restDuration);
    });

    // Phase durations
    document.getElementById('prep-value').textContent = state.settings.prep + 's';
    document.getElementById('eccentric-value').textContent = state.settings.eccentric + 's';
    document.getElementById('concentric-value').textContent = state.settings.concentric + 's';
    document.getElementById('finalEccentric-value').textContent = state.settings.finalEccentric + 's';
}

// ============================================================================
// Exercise & Timer Logic
// ============================================================================

function startExercise(index) {
    state.currentExerciseIndex = index;
    const exercise = getExercises()[state.currentWorkout][index];

    document.getElementById('timer-exercise-name').textContent = exercise.name;

    // Reset timer
    resetTimer();

    // Show timer view
    showView('timer-view');

    // Stop any playing audio, clear queue, and announce exercise
    stopCurrentAudio();
    audioQueue = [];
    isPlayingAudio = false;
    queueSpeak(exercise.name);
    queueSpeak('Get ready');

    // Auto-start voice control for hands-free operation
    if (!isVoiceListening) {
        autoStartVoice();
    }
}

// Siri helper: Start exercise by name
function startExerciseByName(name) {
    const exercises = getExercises()[state.currentWorkout];
    const index = exercises.findIndex(e =>
        e.name.toLowerCase() === name.toLowerCase() ||
        e.name.toLowerCase().includes(name.toLowerCase())
    );

    if (index >= 0) {
        startExercise(index);
        return true;
    }
    return false;
}

// Siri helper: Select workout A or B
function selectWorkout(workoutType) {
    const type = workoutType.toUpperCase();
    if (type === 'A' || type === 'B') {
        state.currentWorkout = type;
        renderExerciseList();
        updateWorkoutPicker();
        showView('workout-view');

        // Announce the workout selection
        queueSpeak(`Workout ${type} selected`);
        return true;
    }
    return false;
}

// Make functions available globally for Siri
window.startExerciseByName = startExerciseByName;
window.selectWorkout = selectWorkout;

function resetTimer() {
    clearInterval(timerState.intervalId);
    timerState.phase = 'prep';
    timerState.seconds = state.settings.prep;
    timerState.isRunning = false;

    updateTimerDisplay();
    updatePhaseIndicators();

    document.getElementById('play-icon').style.display = 'block';
    document.getElementById('pause-icon').style.display = 'none';
    document.getElementById('complete-buttons').style.display = 'none';
    document.querySelector('.timer-controls').style.display = 'flex';
}

function toggleTimer() {
    if (timerState.isRunning) {
        pauseTimer();
    } else {
        startTimer();
    }
}

function startTimer() {
    timerState.isRunning = true;
    document.getElementById('play-icon').style.display = 'none';
    document.getElementById('pause-icon').style.display = 'block';
    document.getElementById('timer-display').classList.add('running');

    timerState.intervalId = setInterval(() => {
        timerState.seconds--;

        // Countdown for prep phase (5, 4, 3, 2, 1)
        if (timerState.phase === 'prep' && timerState.seconds <= 5 && timerState.seconds > 0) {
            if (!isPlayingAudio && !currentPlayingAudio) {
                speak(timerState.seconds.toString(), 1.2);
            }
        }

        // Countdown for positioning phase (5, 4, 3, 2, 1) - starts after "Get into position" finishes
        if (timerState.phase === 'positioning' && timerState.seconds <= 5 && timerState.seconds > 0) {
            if (!isPlayingAudio && !currentPlayingAudio) {
                speak(timerState.seconds.toString(), 1.2);
            }
        }

        // FULL countdown for exercise phases - speak EVERY number after announcement finishes
        // This is essential for voice-commanded gym use
        const exercisePhases = ['eccentric', 'concentric', 'finalEccentric'];
        if (exercisePhases.includes(timerState.phase) && timerState.seconds > 0) {
            if (!isPlayingAudio && !currentPlayingAudio) {
                speak(timerState.seconds.toString(), 1.2);
            }
        }

        if (timerState.seconds <= 0) {
            advancePhase();
        }

        updateTimerDisplay();
    }, 1000);
}

function pauseTimer() {
    timerState.isRunning = false;
    clearInterval(timerState.intervalId);
    document.getElementById('play-icon').style.display = 'block';
    document.getElementById('pause-icon').style.display = 'none';
    document.getElementById('timer-display').classList.remove('running');
}

function advancePhase() {
    const phases = ['prep', 'positioning', 'eccentric', 'concentric', 'finalEccentric', 'complete'];
    const currentIndex = phases.indexOf(timerState.phase);

    if (currentIndex < phases.length - 1) {
        timerState.phase = phases[currentIndex + 1];

        // Don't interrupt audio when transitioning to positioning (let "Get into position" finish)
        if (timerState.phase !== 'positioning') {
            stopCurrentAudio();
            audioQueue = [];
            isPlayingAudio = false;
        }

        switch (timerState.phase) {
            case 'positioning':
                timerState.seconds = state.settings.positioning;
                // Say "Get into position" - countdown will start at 5 seconds (3 sec delay)
                queueSpeak('Get into position');
                break;
            case 'eccentric':
                timerState.seconds = state.settings.eccentric;
                queueSpeak('Eccentric phase');
                queueSpeak('Lower slowly');
                break;
            case 'concentric':
                timerState.seconds = state.settings.concentric;
                queueSpeak('Concentric phase');
                queueSpeak('Push');
                break;
            case 'finalEccentric':
                timerState.seconds = state.settings.finalEccentric;
                queueSpeak('Final eccentric');
                queueSpeak('All the way down');
                break;
            case 'complete':
                completeExercise();
                break;
        }

        updatePhaseIndicators();
    }
}

function completeExercise() {
    pauseTimer();
    stopCurrentAudio();
    audioQueue = [];
    isPlayingAudio = false;
    queueSpeak('Exercise complete');
    queueSpeak('Well done');

    // Mark as completed
    const exercise = getExercises()[state.currentWorkout][state.currentExerciseIndex];
    getTodayCompleted().add(exercise.name + '-' + state.currentWorkout);

    // Show complete buttons
    document.querySelector('.timer-controls').style.display = 'none';
    document.getElementById('complete-buttons').style.display = 'flex';
    document.getElementById('timer-display').classList.remove('running');

    // Update next exercise name
    const nextIndex = state.currentExerciseIndex + 1;
    const exercises = getExercises()[state.currentWorkout];
    if (nextIndex < exercises.length) {
        document.getElementById('next-exercise-name').textContent = exercises[nextIndex].name;
    } else {
        document.getElementById('next-exercise-name').textContent = 'Workout Complete!';
    }
}

function updateTimerDisplay() {
    document.getElementById('timer-display').textContent = timerState.seconds;

    const phaseLabels = {
        prep: 'Get Ready',
        positioning: 'Positioning',
        eccentric: 'Eccentric (Negative)',
        concentric: 'Concentric (Positive)',
        finalEccentric: 'Final Eccentric',
        complete: 'Complete!'
    };
    document.getElementById('phase-label').textContent = phaseLabels[timerState.phase];

    // Update timer glow
    const display = document.getElementById('timer-display');
    display.classList.remove('eccentric', 'concentric');
    if (timerState.phase === 'eccentric' || timerState.phase === 'finalEccentric') {
        display.classList.add('eccentric');
    } else if (timerState.phase === 'concentric') {
        display.classList.add('concentric');
    }
}

function updatePhaseIndicators() {
    const phases = ['eccentric', 'concentric', 'finalEccentric'];
    const phaseElements = ['phase-e', 'phase-c', 'phase-f'];
    const connectors = document.querySelectorAll('.phase-connector');

    let activeIndex = -1;
    if (timerState.phase === 'eccentric') activeIndex = 0;
    else if (timerState.phase === 'concentric') activeIndex = 1;
    else if (timerState.phase === 'finalEccentric' || timerState.phase === 'complete') activeIndex = 2;

    phaseElements.forEach((id, index) => {
        const el = document.getElementById(id);
        el.classList.toggle('active', index <= activeIndex);
    });

    connectors.forEach((conn, index) => {
        conn.classList.toggle('active', index < activeIndex);
    });
}

// ============================================================================
// Rest Timer
// ============================================================================

function startRestTimer() {
    showView('rest-view');
    restTimerState.seconds = state.settings.restDuration;
    restTimerState.isRunning = true;

    document.getElementById('rest-display').textContent = restTimerState.seconds;

    stopCurrentAudio();
    audioQueue = [];
    isPlayingAudio = false;
    queueSpeak('Rest period');
    queueSpeak('Recover');

    restTimerState.intervalId = setInterval(() => {
        restTimerState.seconds--;
        document.getElementById('rest-display').textContent = restTimerState.seconds;

        if (restTimerState.seconds <= 5 && restTimerState.seconds > 0 && !isPlayingAudio) {
            speak(restTimerState.seconds.toString(), 1.2);
        }

        if (restTimerState.seconds <= 0) {
            endRestTimer();
        }
    }, 1000);
}

function endRestTimer() {
    clearInterval(restTimerState.intervalId);
    restTimerState.isRunning = false;

    const nextIndex = state.currentExerciseIndex + 1;
    const exercises = getExercises()[state.currentWorkout];

    stopCurrentAudio();
    audioQueue = [];
    isPlayingAudio = false;

    if (nextIndex < exercises.length) {
        queueSpeak('Next exercise');
        // startExercise will queue the exercise name
        startExercise(nextIndex);
    } else {
        queueSpeak('Workout complete');
        queueSpeak('Great session');
        showView('workouts-view');
        renderExerciseList();
    }
}

function skipRest() {
    clearInterval(restTimerState.intervalId);
    endRestTimer();
}

// ============================================================================
// Modals & UI Helpers
// ============================================================================

function showView(viewId) {
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
    document.getElementById(viewId).classList.add('active');

    // Show/hide tab bar
    const tabBar = document.querySelector('.tab-bar');
    const tabViews = ['workouts-view', 'stats-view', 'log-view'];
    if (tabViews.includes(viewId)) {
        tabBar.style.display = 'flex';
    } else {
        tabBar.style.display = 'none';
    }
}

function openLogModal(index) {
    const exercise = getExercises()[state.currentWorkout][index];
    state.currentExerciseIndex = index;

    document.getElementById('modal-exercise-name').textContent = exercise.name;
    document.getElementById('weight-input').value = exercise.weight || '';
    document.getElementById('failure-checkbox').checked = false;

    // Update Siri button with exercise name
    const siriBtn = document.getElementById('siri-btn-text');
    if (siriBtn) {
        siriBtn.textContent = `Add "${exercise.name}" to Siri`;
    }
    const siriBtnEl = document.getElementById('add-siri-exercise-btn');
    if (siriBtnEl) {
        siriBtnEl.style.background = 'linear-gradient(135deg, #06b6d4, #3b82f6)';
    }

    document.getElementById('log-modal').classList.add('active');
}

function closeLogModal() {
    document.getElementById('log-modal').classList.remove('active');
}

function saveLog() {
    const weight = parseFloat(document.getElementById('weight-input').value);
    const reachedFailure = document.getElementById('failure-checkbox').checked;

    if (isNaN(weight) || weight <= 0) {
        closeLogModal();
        return;
    }

    const exercise = getExercises()[state.currentWorkout][state.currentExerciseIndex];
    exercise.weight = weight;

    // Log to history for current profile
    getWorkoutLogs().push({
        date: new Date().toISOString(),
        exerciseName: exercise.name,
        workout: state.currentWorkout,
        weight: weight,
        reachedFailure: reachedFailure
    });

    saveState();
    renderExerciseList();
    closeLogModal();
}

function openSettings() {
    try {
        updateSettingsUI();
        document.getElementById('settings-modal').classList.add('active');
    } catch (e) {
        alert('Settings error: ' + e.message);
    }
}

function closeSettings() {
    document.getElementById('settings-modal').classList.remove('active');
    saveState();
}

// Profile functions
function openProfile() {
    const profile = getCurrentProfile();
    document.getElementById('profile-name').value = profile.name || '';
    document.getElementById('profile-age').value = profile.age || '';
    document.getElementById('profile-weight').value = profile.weight || '';
    document.getElementById('profile-modal').classList.add('active');
}

function closeProfile() {
    const profile = getCurrentProfile();
    profile.name = document.getElementById('profile-name').value;
    profile.age = document.getElementById('profile-age').value;
    profile.weight = document.getElementById('profile-weight').value;
    document.getElementById('profile-modal').classList.remove('active');
    saveState();
}

function resetAllData() {
    if (confirm('Are you sure you want to reset all data for this profile? This cannot be undone.')) {
        const profile = getCurrentProfile();
        profile.exercises = JSON.parse(JSON.stringify(defaultExercises));
        profile.workoutLogs = [];
        profile.todayCompleted = [];
        profile.todayCompletedSet = new Set();
        profile.name = '';
        profile.age = '';
        profile.weight = '';
        saveState();
        renderExerciseList();
        closeProfile();
        alert('Profile data has been reset.');
    }
}

// Stats functions
function renderStats() {
    const logs = getWorkoutLogs();
    const profile = getCurrentProfile();

    // Total workouts (unique dates)
    const uniqueDates = new Set(logs.map(l => new Date(l.date).toDateString()));
    document.getElementById('stat-workouts').textContent = uniqueDates.size;

    // Total exercises
    document.getElementById('stat-exercises').textContent = logs.length;

    // Calculate streak
    const streak = calculateStreak();
    document.getElementById('stat-streak').textContent = streak;

    // This week
    const weekAgo = new Date();
    weekAgo.setDate(weekAgo.getDate() - 7);
    const thisWeek = logs.filter(l => new Date(l.date) >= weekAgo).length;
    document.getElementById('stat-thisweek').textContent = thisWeek;

    // Recent activity
    const recentLogs = logs.slice(-5).reverse();
    const recentDiv = document.getElementById('recent-activity');
    if (recentLogs.length === 0) {
        recentDiv.innerHTML = '<p class="no-data">Complete workouts to see stats</p>';
    } else {
        recentDiv.innerHTML = recentLogs.map(log => `
            <div class="log-entry">
                <div class="log-entry-header">
                    <span class="log-entry-date">${formatDate(log.date)}</span>
                    <span class="log-entry-workout">Workout ${log.workout}</span>
                </div>
                <div class="log-entry-exercise">${log.exerciseName}</div>
                <div class="log-entry-details">${log.weight} ${profile.units}${log.reachedFailure ? ' • Reached Failure' : ''}</div>
            </div>
        `).join('');
    }
}

function calculateStreak() {
    const logs = getWorkoutLogs();
    if (logs.length === 0) return 0;

    const uniqueDates = [...new Set(logs.map(l => new Date(l.date).toDateString()))].sort().reverse();
    let streak = 0;
    let checkDate = new Date();
    checkDate.setHours(0, 0, 0, 0);

    for (const dateStr of uniqueDates) {
        const logDate = new Date(dateStr);
        logDate.setHours(0, 0, 0, 0);

        const diffDays = Math.floor((checkDate - logDate) / (1000 * 60 * 60 * 24));

        if (diffDays <= 1) {
            streak++;
            checkDate = logDate;
        } else {
            break;
        }
    }

    return streak;
}

// Log functions
function renderLog() {
    const logs = getWorkoutLogs().slice().reverse();
    const profile = getCurrentProfile();
    const logList = document.getElementById('log-list');

    if (logs.length === 0) {
        logList.innerHTML = '<p class="no-data">No workouts logged yet</p>';
        return;
    }

    logList.innerHTML = logs.map(log => `
        <div class="log-entry">
            <div class="log-entry-header">
                <span class="log-entry-date">${formatDate(log.date)}</span>
                <span class="log-entry-workout">Workout ${log.workout}</span>
            </div>
            <div class="log-entry-exercise">${log.exerciseName}</div>
            <div class="log-entry-details">${log.weight} ${profile.units}${log.reachedFailure ? ' • Reached Failure' : ''}</div>
        </div>
    `).join('');
}

function formatDate(dateStr) {
    const date = new Date(dateStr);
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);

    if (date.toDateString() === today.toDateString()) {
        return 'Today ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } else if (date.toDateString() === yesterday.toDateString()) {
        return 'Yesterday';
    } else {
        return date.toLocaleDateString([], { month: 'short', day: 'numeric' });
    }
}

// ============================================================================
// QR Code Sync
// ============================================================================

function generateSyncData() {
    // Create a compact data object for QR code
    const exercises = getExercises();
    const syncData = {
        v: 1, // version
        w: state.currentWorkout,
        e: {
            A: exercises.A.map(ex => ({
                n: ex.name,
                w: ex.weight
            })),
            B: exercises.B.map(ex => ({
                n: ex.name,
                w: ex.weight
            }))
        },
        s: {
            v: state.settings.voice,
            r: state.settings.restDuration,
            p: state.settings.prep,
            ec: state.settings.eccentric,
            co: state.settings.concentric,
            fe: state.settings.finalEccentric
        }
    };

    return JSON.stringify(syncData);
}

function openSyncModal() {
    const modal = document.getElementById('sync-modal');
    modal.classList.add('active');

    // Generate QR code
    const canvas = document.getElementById('qr-canvas');
    const syncData = generateSyncData();

    // Create URL with data encoded
    const syncUrl = `hitcoachpro://sync?data=${encodeURIComponent(syncData)}`;

    if (typeof QRCode !== 'undefined') {
        QRCode.toCanvas(canvas, syncUrl, {
            width: 200,
            margin: 2,
            color: {
                dark: '#000000',
                light: '#ffffff'
            }
        }, function(error) {
            if (error) {
                console.error('QR Code error:', error);
                // Fallback: show the data as text
                canvas.style.display = 'none';
                const container = document.querySelector('.qr-container');
                container.innerHTML = `<p style="color:#000;font-size:10px;word-break:break-all;padding:10px;">${syncUrl}</p>`;
            }
        });
    }
}

function closeSyncModal() {
    document.getElementById('sync-modal').classList.remove('active');
}

function deleteExercise(index) {
    if (confirm('Delete this exercise?')) {
        getExercises()[state.currentWorkout].splice(index, 1);
        saveState();
        renderExerciseList();
    }
}

function addExercise() {
    const exercises = getExercises()[state.currentWorkout];
    if (exercises.length >= 8) {
        alert('Maximum 8 exercises per workout');
        return;
    }
    const name = prompt('Enter exercise name:');
    if (name && name.trim()) {
        exercises.push({
            name: name.trim(),
            weight: null,
            completed: false
        });
        saveState();
        renderExerciseList();
    }
}

// ============================================================================
// Event Listeners
// ============================================================================

function initEventListeners() {
    // Workout picker
    document.querySelectorAll('.picker-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.picker-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            state.currentWorkout = btn.dataset.workout;
            renderExerciseList();
        });
    });

    // Tab bar
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', () => {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            if (tab.dataset.tab === 'workouts') {
                showView('workouts-view');
            } else if (tab.dataset.tab === 'analytics') {
                renderStats();
                showView('stats-view');
            } else if (tab.dataset.tab === 'history') {
                renderLog();
                showView('log-view');
            }
        });
    });

    // Timer controls
    document.getElementById('play-pause-btn').addEventListener('click', toggleTimer);
    document.getElementById('reset-btn').addEventListener('click', resetTimer);
    document.getElementById('skip-btn').addEventListener('click', () => {
        resetTimer();
        startRestTimer();
    });
    document.getElementById('close-timer').addEventListener('click', () => {
        pauseTimer();
        hideMiniVoiceIndicator();
        showView('workouts-view');
        renderExerciseList();
    });

    // Complete buttons
    document.getElementById('start-rest-btn').addEventListener('click', startRestTimer);
    document.getElementById('another-set-btn').addEventListener('click', resetTimer);

    // Rest timer
    document.getElementById('skip-rest-btn').addEventListener('click', skipRest);
    document.getElementById('close-rest').addEventListener('click', () => {
        clearInterval(restTimerState.intervalId);
        hideMiniVoiceIndicator();
        showView('workouts-view');
        renderExerciseList();
    });

    // Log modal
    document.getElementById('cancel-log').addEventListener('click', closeLogModal);
    document.getElementById('save-log').addEventListener('click', saveLog);

    // Settings - use touchend for iOS WebView reliability
    const settingsBtn = document.getElementById('settings-btn');
    settingsBtn.addEventListener('touchend', function(e) {
        e.preventDefault();
        openSettings();
    });
    settingsBtn.addEventListener('click', openSettings);
    document.getElementById('close-settings').addEventListener('click', closeSettings);

    // Sync
    document.getElementById('sync-btn').addEventListener('click', openSyncModal);
    document.getElementById('close-sync').addEventListener('click', closeSyncModal);

    // Siri setup
    const siriBtn = document.getElementById('siri-btn');
    if (siriBtn) {
        siriBtn.addEventListener('click', openSiriSetup);
        siriBtn.addEventListener('touchend', (e) => {
            e.preventDefault();
            openSiriSetup();
        });
    }

    // Settings controls
    document.querySelectorAll('#voice-control .voice-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('#voice-control .voice-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            state.settings.voice = btn.dataset.value;
            initVoice();
        });
    });

    document.querySelectorAll('#rest-control .seg-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('#rest-control .seg-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            state.settings.restDuration = parseInt(btn.dataset.value);
        });
    });

    // Add exercise
    document.getElementById('add-exercise-btn').addEventListener('click', addExercise);

    // Profile button - use touchend for iOS WebView reliability
    const profileBtn = document.getElementById('profile-btn');
    profileBtn.addEventListener('touchend', function(e) {
        e.preventDefault();
        openProfile();
    });
    profileBtn.addEventListener('click', openProfile);

    // Profile modal
    document.getElementById('close-profile').addEventListener('click', closeProfile);
    document.getElementById('reset-data-btn').addEventListener('click', resetAllData);

    // Profile switcher toggle buttons
    document.querySelectorAll('.profile-toggle').forEach(btn => {
        btn.addEventListener('click', () => {
            const profileIdx = parseInt(btn.dataset.profile);
            switchProfile(profileIdx);
        });
        // iOS touch support
        btn.addEventListener('touchend', (e) => {
            e.preventDefault();
            const profileIdx = parseInt(btn.dataset.profile);
            switchProfile(profileIdx);
        });
    });
}

// ============================================================================
// Siri & Deep Link Handling
// ============================================================================

function handleDeepLink(url) {
    console.log('Handling deep link:', url);

    try {
        // Parse the URL - handle both URL objects and strings
        let path = url;
        let queryParams = {};

        if (typeof url === 'string') {
            if (url.startsWith('hitcoachpro://')) {
                const urlWithoutScheme = url.replace('hitcoachpro://', '');
                // Split path and query string
                const [pathPart, queryPart] = urlWithoutScheme.split('?');
                path = pathPart;

                // Parse query parameters
                if (queryPart) {
                    queryPart.split('&').forEach(param => {
                        const [key, value] = param.split('=');
                        queryParams[key] = decodeURIComponent(value || '');
                    });
                }
            }
        } else if (url.pathname) {
            path = url.pathname.replace(/^\//, '');
        }

        const parts = path.split('/').filter(p => p);
        const command = parts[0];

        switch (command) {
            case 'start':
                // Check query parameters first (new format: ?exercise=X&workout=A)
                if (queryParams.exercise) {
                    const workout = queryParams.workout?.toUpperCase() || state.currentWorkout;
                    console.log('Deep link: Starting exercise', queryParams.exercise, 'in workout', workout);
                    if (workout === 'A' || workout === 'B') {
                        state.currentWorkout = workout;
                        renderExerciseList();
                        showView('workout-view');
                    }
                    // Use longer timeout to ensure UI is ready
                    setTimeout(() => {
                        const exercises = getExercises()[state.currentWorkout];
                        const exerciseName = queryParams.exercise;
                        console.log('Looking for exercise:', exerciseName, 'in', exercises.map(e => e.name));
                        const index = exercises.findIndex(e =>
                            e.name.toLowerCase() === exerciseName.toLowerCase() ||
                            e.name.toLowerCase().includes(exerciseName.toLowerCase())
                        );
                        if (index >= 0) {
                            console.log('Found exercise at index:', index);
                            startExercise(index);
                        } else {
                            console.log('Exercise not found, starting first exercise');
                            startExercise(0);
                        }
                    }, 300);
                } else if (queryParams.workout) {
                    const workoutType = queryParams.workout.toUpperCase();
                    if (workoutType === 'A' || workoutType === 'B') {
                        state.currentWorkout = workoutType;
                        renderExerciseList();
                        showView('workout-view');
                        setTimeout(() => {
                            const exercises = getExercises()[workoutType];
                            if (exercises && exercises.length > 0) {
                                startExercise(0);
                                queueSpeak('Starting workout ' + workoutType);
                            }
                        }, 300);
                    }
                } else if (parts[1] === 'workout') {
                    // Old format: /start/workout/A
                    const workoutType = parts[2]?.toUpperCase();
                    if (workoutType === 'A' || workoutType === 'B') {
                        selectWorkout(workoutType);
                    }
                } else if (parts[1] === 'exercise') {
                    // Old format: /start/exercise/Leg%20Press
                    const exerciseName = decodeURIComponent(parts[2] || '').replace(/-/g, ' ');
                    if (exerciseName) {
                        startExerciseByName(exerciseName);
                    }
                } else {
                    // Just "start" - start first exercise of current workout
                    const exercises = getExercises()[state.currentWorkout];
                    if (exercises && exercises.length > 0) {
                        startExercise(0);
                        queueSpeak('Starting workout');
                    }
                }
                break;

            case 'pause':
                if (timerState.isRunning) {
                    pauseTimer();
                    queueSpeak('Paused');
                }
                break;

            case 'resume':
            case 'play':
                if (!timerState.isRunning && document.getElementById('timer-view').classList.contains('active')) {
                    startTimer();
                    queueSpeak('Resumed');
                }
                break;

            case 'skip':
                if (document.getElementById('timer-view').classList.contains('active')) {
                    resetTimer();
                    startRestTimer();
                }
                break;

            case 'stop':
                pauseTimer();
                showView('workouts-view');
                renderExerciseList();
                queueSpeak('Workout stopped');
                break;

            default:
                console.log('Unknown deep link command:', command);
        }
    } catch (e) {
        console.error('Error handling deep link:', e);
    }
}

// ============================================================================
// Voice Command Recognition
// ============================================================================

let voiceRecognition = null;
let isVoiceListening = false;

function initVoiceCommands() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        console.log('Speech recognition not supported');
        return false;
    }

    voiceRecognition = new SpeechRecognition();
    voiceRecognition.continuous = true;
    voiceRecognition.interimResults = false;
    voiceRecognition.lang = 'en-US';

    voiceRecognition.onresult = (event) => {
        const last = event.results.length - 1;
        const command = event.results[last][0].transcript.toLowerCase().trim();
        console.log('Voice command:', command);
        processVoiceCommand(command);
    };

    voiceRecognition.onerror = (event) => {
        console.log('Voice error:', event.error);
        if (event.error === 'no-speech' || event.error === 'aborted') {
            // Restart if still supposed to be listening
            if (isVoiceListening) {
                setTimeout(() => {
                    if (isVoiceListening) voiceRecognition.start();
                }, 100);
            }
        }
    };

    voiceRecognition.onend = () => {
        // Restart if still supposed to be listening
        if (isVoiceListening) {
            setTimeout(() => {
                if (isVoiceListening) {
                    try { voiceRecognition.start(); } catch(e) {}
                }
            }, 100);
        }
    };

    return true;
}

function processVoiceCommand(command) {
    // Normalize command
    const words = command.split(' ');

    // Check for commands
    if (command.includes('start') || command.includes('go') || command.includes('begin') || command.includes('play')) {
        if (timerState.isPaused) {
            startTimer();
            queueSpeak('Resuming');
        } else if (!timerState.isRunning) {
            // Start first incomplete exercise
            const exercises = getExercises()[state.currentWorkout];
            const todayCompleted = getTodayCompleted();
            const nextIndex = exercises.findIndex(ex => !todayCompleted.has(ex.name + '-' + state.currentWorkout));
            if (nextIndex >= 0) {
                startExercise(nextIndex);
            }
        }
    } else if (command.includes('pause') || command.includes('stop') || command.includes('wait') || command.includes('hold')) {
        if (timerState.isRunning && !timerState.isPaused) {
            pauseTimer();
            queueSpeak('Paused');
        }
    } else if (command.includes('resume') || command.includes('continue')) {
        if (timerState.isPaused) {
            startTimer();
            queueSpeak('Resuming');
        }
    } else if (command.includes('skip') || command.includes('next') || command.includes('done')) {
        if (timerState.isRunning) {
            skipToRest();
            queueSpeak('Skipping');
        }
    } else if (command.includes('workout a')) {
        selectWorkout('A');
    } else if (command.includes('workout b')) {
        selectWorkout('B');
    }
}

function toggleVoiceControl() {
    const btn = document.getElementById('siri-btn');

    if (!voiceRecognition) {
        if (!initVoiceCommands()) {
            alert('Voice commands not supported on this device');
            return;
        }
    }

    if (isVoiceListening) {
        // Stop listening
        isVoiceListening = false;
        voiceRecognition.stop();
        btn.classList.remove('voice-active');
        btn.innerHTML = `
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/>
                <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/>
            </svg>
            🎤 Voice
        `;
        hideVoiceHelper();
        hideMiniVoiceIndicator();
        queueSpeak('Voice off');
    } else {
        // Start listening
        isVoiceListening = true;
        try {
            voiceRecognition.start();
            btn.classList.add('voice-active');
            btn.innerHTML = `
                <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/>
                    <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/>
                </svg>
                Listening...
            `;
            showVoiceHelper();
            queueSpeak('Listening. Say Start, Pause, or Skip.');
        } catch (e) {
            isVoiceListening = false;
            console.error('Voice start error:', e);
        }
    }
}

// Show voice command helper overlay
function showVoiceHelper() {
    let helper = document.getElementById('voice-helper');
    if (!helper) {
        helper = document.createElement('div');
        helper.id = 'voice-helper';
        helper.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: #1a1a1a;
            color: #fff;
            padding: 24px;
            border-radius: 16px;
            font-size: 14px;
            z-index: 1000;
            text-align: center;
            box-shadow: 0 4px 30px rgba(0,0,0,0.5);
            border: 2px solid #10b981;
            max-width: 300px;
            width: 90%;
        `;
        helper.innerHTML = `
            <div style="font-size: 32px; margin-bottom: 12px;">🎤</div>
            <div style="font-size: 18px; font-weight: 700; color: #10b981; margin-bottom: 16px;">LISTENING...</div>
            <div style="font-size: 13px; color: #888; margin-bottom: 12px;">Say one of these commands:</div>
            <div style="background: #222; border-radius: 10px; padding: 16px; text-align: left;">
                <div style="margin-bottom: 10px; display: flex; align-items: center; gap: 10px;">
                    <span style="background: #10b981; color: #000; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 12px;">START</span>
                    <span style="color: #aaa; font-size: 12px;">Start or resume timer</span>
                </div>
                <div style="margin-bottom: 10px; display: flex; align-items: center; gap: 10px;">
                    <span style="background: #f59e0b; color: #000; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 12px;">PAUSE</span>
                    <span style="color: #aaa; font-size: 12px;">Pause the timer</span>
                </div>
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="background: #3b82f6; color: #fff; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 12px;">SKIP</span>
                    <span style="color: #aaa; font-size: 12px;">Skip to rest period</span>
                </div>
            </div>
            <div style="margin-top: 16px; font-size: 11px; color: #666;">Tap 🎤 Voice button again to stop</div>
        `;
        document.body.appendChild(helper);
    }
    helper.style.display = 'block';
}

function hideVoiceHelper() {
    const helper = document.getElementById('voice-helper');
    if (helper) {
        helper.style.display = 'none';
    }
}

// Auto-start voice control silently (no popup) for hands-free workout
function autoStartVoice() {
    if (!voiceRecognition) {
        if (!initVoiceCommands()) {
            return; // Voice not supported
        }
    }

    if (isVoiceListening) return; // Already listening

    isVoiceListening = true;
    try {
        voiceRecognition.start();
        const btn = document.getElementById('siri-btn');
        if (btn) {
            btn.classList.add('voice-active');
            btn.innerHTML = `
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/>
                    <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/>
                </svg>
                🎤 ON
            `;
        }
        // Show mini indicator instead of full popup
        showMiniVoiceIndicator();
    } catch (e) {
        isVoiceListening = false;
        console.error('Auto voice start error:', e);
    }
}

// Show small voice indicator during workout
function showMiniVoiceIndicator() {
    let indicator = document.getElementById('voice-mini-indicator');
    if (!indicator) {
        indicator = document.createElement('div');
        indicator.id = 'voice-mini-indicator';
        indicator.style.cssText = `
            position: fixed;
            top: 60px;
            right: 10px;
            background: rgba(16, 185, 129, 0.9);
            color: #000;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 600;
            z-index: 1000;
            display: flex;
            align-items: center;
            gap: 6px;
        `;
        indicator.innerHTML = `
            <span style="animation: blink 1s infinite;">●</span> Voice ON - Say "START", "PAUSE" or "SKIP"
        `;
        document.body.appendChild(indicator);

        // Add blink animation if not already added
        if (!document.getElementById('blink-style')) {
            const style = document.createElement('style');
            style.id = 'blink-style';
            style.textContent = `
                @keyframes blink {
                    0%, 50% { opacity: 1; }
                    51%, 100% { opacity: 0.3; }
                }
            `;
            document.head.appendChild(style);
        }
    }
    indicator.style.display = 'flex';
}

function hideMiniVoiceIndicator() {
    const indicator = document.getElementById('voice-mini-indicator');
    if (indicator) {
        indicator.style.display = 'none';
    }
}

// Legacy function - now just toggles voice
function openSiriSetup() {
    toggleVoiceControl();
}

function closeSiriSetup() {
    document.getElementById('siri-modal').classList.remove('active');
}

function showSiriModal() {
    // Close settings modal first
    document.getElementById('profile-modal').classList.remove('active');

    // Populate exercise list
    populateSiriExerciseList();

    // Open siri modal
    document.getElementById('siri-modal').classList.add('active');
}

// Populate the Siri exercise list with Add buttons (matching native app)
function populateSiriExerciseList() {
    const container = document.getElementById('siri-exercise-list');
    if (!container) return;

    container.innerHTML = '';

    // Get exercises from current profile
    const exercises = getExercises();
    const workoutAExercises = exercises.A || [];
    const workoutBExercises = exercises.B || [];

    // Add "Open App" shortcut first
    const openAppCard = createSiriExerciseRow('Open App', 'HIT', 'hitcoachpro://open', '');
    container.appendChild(openAppCard);

    if (workoutAExercises.length > 0) {
        const headerA = document.createElement('div');
        headerA.style.cssText = 'font-size: 11px; font-weight: 600; color: var(--neon-green); margin: 12px 0 6px; text-transform: uppercase;';
        headerA.textContent = 'Workout A';
        container.appendChild(headerA);

        workoutAExercises.forEach(ex => {
            const url = `hitcoachpro://start?exercise=${encodeURIComponent(ex.name)}&workout=A`;
            const siriPhrase = `HIT ${ex.name.toLowerCase()} A`;
            const card = createSiriExerciseRow(`${ex.name} A`, siriPhrase, url, 'A');
            container.appendChild(card);
        });
    }

    if (workoutBExercises.length > 0) {
        const headerB = document.createElement('div');
        headerB.style.cssText = 'font-size: 11px; font-weight: 600; color: var(--neon-green); margin: 12px 0 6px; text-transform: uppercase;';
        headerB.textContent = 'Workout B';
        container.appendChild(headerB);

        workoutBExercises.forEach(ex => {
            const url = `hitcoachpro://start?exercise=${encodeURIComponent(ex.name)}&workout=B`;
            const siriPhrase = `HIT ${ex.name.toLowerCase()} B`;
            const card = createSiriExerciseRow(`${ex.name} B`, siriPhrase, url, 'B');
            container.appendChild(card);
        });
    }
}

// Create a per-exercise Siri row (matching native app design)
function createSiriExerciseRow(title, siriPhrase, url, workout) {
    const row = document.createElement('div');
    row.style.cssText = `
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px;
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-radius: 10px;
    `;

    row.innerHTML = `
        <div style="flex: 1;">
            <div style="font-size: 14px; font-weight: 600; color: #fff;">${title}</div>
            <div style="font-size: 11px; color: rgba(255,255,255,0.6); margin-top: 2px;">Say: "${siriPhrase}"</div>
        </div>
        <button onclick="addSiriShortcut('${url}', '${title}')" style="
            background: #22c55e;
            color: #000;
            border: none;
            padding: 8px 14px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 4px;
        ">
            <span style="font-size: 14px;">+</span> Add
        </button>
    `;

    return row;
}

// Add shortcut - copies URL and opens Shortcuts app
function addSiriShortcut(url, title) {
    // Copy URL to clipboard
    navigator.clipboard.writeText(url).then(() => {
        // Show confirmation
        const btn = event.target.closest('button');
        const originalText = btn.innerHTML;
        btn.innerHTML = '✓ Copied!';
        btn.style.background = '#10b981';

        // Open Shortcuts app (on iOS)
        setTimeout(() => {
            if (window.Capacitor && window.Capacitor.Plugins.App) {
                window.Capacitor.Plugins.App.openUrl({ url: 'shortcuts://' });
            } else {
                window.open('shortcuts://', '_blank');
            }
        }, 300);

        // Reset button after delay
        setTimeout(() => {
            btn.innerHTML = originalText;
            btn.style.background = '#22c55e';
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy:', err);
        alert('URL: ' + url + '\n\nCopy this and paste in Shortcuts app');
    });
}

// Create a single exercise card for Siri setup
function createSiriExerciseCard(name, url, hint) {
    const card = document.createElement('div');
    card.style.cssText = 'display: flex; align-items: center; justify-content: space-between; background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 10px; padding: 10px 12px;';

    const info = document.createElement('div');
    info.style.cssText = 'flex: 1; min-width: 0;';

    const nameEl = document.createElement('div');
    nameEl.style.cssText = 'font-size: 13px; font-weight: 600; color: var(--text-primary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;';
    nameEl.textContent = name;

    const hintEl = document.createElement('div');
    hintEl.style.cssText = 'font-size: 10px; color: var(--text-muted); margin-top: 2px;';
    hintEl.textContent = hint;

    info.appendChild(nameEl);
    info.appendChild(hintEl);

    const copyBtn = document.createElement('button');
    copyBtn.style.cssText = 'background: var(--emerald); color: #000; border: none; border-radius: 6px; padding: 6px 12px; font-size: 11px; font-weight: 600; cursor: pointer; margin-left: 8px; white-space: nowrap;';
    copyBtn.textContent = 'Copy';
    copyBtn.onclick = async () => {
        try {
            await navigator.clipboard.writeText(url);
            copyBtn.textContent = 'Copied!';
            copyBtn.style.background = 'var(--neon-green)';
            setTimeout(() => {
                copyBtn.textContent = 'Copy';
                copyBtn.style.background = 'var(--emerald)';
            }, 2000);
        } catch (e) {
            // Fallback
            prompt('Copy this URL:', url);
        }
    };

    card.appendChild(info);
    card.appendChild(copyBtn);

    return card;
}

// Add current exercise to Siri (from log modal) - Uses native iOS Add to Siri sheet
async function addExerciseToSiri() {
    const exercise = getExercises()[state.currentWorkout][state.currentExerciseIndex];
    if (!exercise) return;

    const btn = document.getElementById('add-siri-exercise-btn');
    const btnText = document.getElementById('siri-btn-text');

    // Try native Siri plugin first
    if (window.Capacitor && window.Capacitor.Plugins && window.Capacitor.Plugins.Siri) {
        try {
            const result = await window.Capacitor.Plugins.Siri.addShortcut({
                title: `Start ${exercise.name}`,
                phrase: `Start ${exercise.name.toLowerCase()}`,
                exerciseName: exercise.name,
                workout: state.currentWorkout
            });

            if (result.success && !result.cancelled) {
                btnText.textContent = 'Added to Siri!';
                btn.style.background = 'linear-gradient(135deg, #10b981, #22c55e)';
                queueSpeak(`Siri shortcut added. Say: Hey Siri, ${result.phrase || 'start ' + exercise.name.toLowerCase()}`);

                setTimeout(() => {
                    btnText.textContent = `Add "${exercise.name}" to Siri`;
                    btn.style.background = 'linear-gradient(135deg, #06b6d4, #3b82f6)';
                }, 3000);
            }
            return;
        } catch (e) {
            console.log('Native Siri error:', e);
        }
    }

    // Fallback to copy URL approach
    const url = `hitcoachpro://start/exercise/${encodeURIComponent(exercise.name)}`;
    try {
        await navigator.clipboard.writeText(url);
        btnText.textContent = 'URL Copied!';
        btn.style.background = 'linear-gradient(135deg, #10b981, #22c55e)';
        alert(`URL copied!\n\nOpen Shortcuts app and create a new shortcut with "Open URLs" action.`);
        openShortcutsApp();
    } catch (e) {
        prompt(`Copy this URL:`, url);
    }
}

// Open Shortcuts app
async function openShortcutsApp() {
    const shortcutsUrl = 'shortcuts://';

    if (window.Capacitor && window.Capacitor.Plugins && window.Capacitor.Plugins.App) {
        try {
            await window.Capacitor.Plugins.App.openUrl({ url: shortcutsUrl });
            return;
        } catch (e) {
            console.log('Could not open Shortcuts:', e);
        }
    }

    window.location.href = shortcutsUrl;
}

// Open Siri Settings (where donated shortcuts appear)
async function openSiriSettings() {
    const settingsUrl = 'App-prefs:SIRI';

    // Use Capacitor App plugin to open external URL
    if (window.Capacitor && window.Capacitor.Plugins && window.Capacitor.Plugins.App) {
        try {
            await window.Capacitor.Plugins.App.openUrl({ url: settingsUrl });
            return;
        } catch (e) {
            console.log('Could not open settings URL:', e);
        }
    }

    // Fallback: try direct navigation
    window.location.href = settingsUrl;

    // Show manual instructions
    setTimeout(() => {
        alert('Go to:\n\nSettings > Siri & Search > Shortcuts\n\nFind "Start HIT Workout" and tap to add your voice phrase.');
    }, 500);
}

// Legacy function - kept for compatibility
async function setupSiriShortcut() {
    const appUrl = 'hitcoachpro://start';
    try {
        await navigator.clipboard.writeText(appUrl);
        alert('URL copied! Now open Shortcuts app to create your shortcut.');
        openShortcutsApp();
    } catch (error) {
        prompt('Copy this URL:', appUrl);
    }
}

// No-op function - native Siri donation not available without entitlement
function donateSiriShortcuts() {
    // Shortcuts-based approach doesn't require donation
}

// Initialize deep link handling for Capacitor
function initDeepLinks() {
    // Handle initial URL when app is opened via deep link
    if (window.Capacitor && window.Capacitor.Plugins && window.Capacitor.Plugins.App) {
        const App = window.Capacitor.Plugins.App;

        // Listen for app URL open events
        App.addListener('appUrlOpen', (event) => {
            console.log('App opened with URL:', event.url);
            handleDeepLink(event.url);
        });

        // Check if app was launched with a URL
        App.getLaunchUrl().then(result => {
            if (result && result.url) {
                console.log('App launched with URL:', result.url);
                handleDeepLink(result.url);
            }
        }).catch(err => {
            console.log('No launch URL or error:', err);
        });
    }

    // Also handle web-based URL parameters for testing
    const urlParams = new URLSearchParams(window.location.search);
    const action = urlParams.get('action');
    if (action) {
        handleDeepLink(action);
    }
}

// ============================================================================
// Initialization
// ============================================================================

function init() {
    loadState();
    initVoice();
    initEventListeners();
    initDeepLinks();
    renderExerciseList();
    applyDisplaySize();

    // Donate Siri shortcuts for suggestions
    donateSiriShortcuts();

    // Register service worker
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('service-worker.js');
    }

    // Add Siri modal event listeners
    const closeSiriBtn = document.getElementById('close-siri');
    if (closeSiriBtn) {
        closeSiriBtn.addEventListener('click', closeSiriSetup);
    }

    const siriSetupBtn = document.getElementById('siri-setup-btn');
    if (siriSetupBtn) {
        siriSetupBtn.addEventListener('click', showSiriModal);
        siriSetupBtn.addEventListener('touchend', (e) => {
            e.preventDefault();
            showSiriModal();
        });
    }
}

// Start the app
document.addEventListener('DOMContentLoaded', init);
