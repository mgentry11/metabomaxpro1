// HIT Coach Pro - Service Worker v2
const CACHE_NAME = 'hitcoachpro-v2';
const AUDIO_CACHE = 'hitcoachpro-audio-v1';

// Core app files to cache
const coreFiles = [
    '/',
    '/ios-app.html',
    '/ios-app.js',
    '/ios-app.css',
    '/manifest.json',
    '/icons/icon-192.png',
    '/icons/icon-512.png'
];

// Audio files for Commander voice (cache on first use)
const audioFiles = [
    // Phase announcements
    '/audio/commander/phase_get_ready.mp3',
    '/audio/commander/phase_eccentric.mp3',
    '/audio/commander/phase_concentric.mp3',
    '/audio/commander/phase_final_eccentric.mp3',
    '/audio/commander/phase_complete.mp3',
    '/audio/commander/phase_rest.mp3',
    // Cues
    '/audio/commander/cue_get_position.mp3',
    // Numbers 1-60
    '/audio/commander/num_1.mp3',
    '/audio/commander/num_2.mp3',
    '/audio/commander/num_3.mp3',
    '/audio/commander/num_4.mp3',
    '/audio/commander/num_5.mp3',
    '/audio/commander/num_6.mp3',
    '/audio/commander/num_7.mp3',
    '/audio/commander/num_8.mp3',
    '/audio/commander/num_9.mp3',
    '/audio/commander/num_10.mp3',
    '/audio/commander/num_11.mp3',
    '/audio/commander/num_12.mp3',
    '/audio/commander/num_13.mp3',
    '/audio/commander/num_14.mp3',
    '/audio/commander/num_15.mp3',
    '/audio/commander/num_16.mp3',
    '/audio/commander/num_17.mp3',
    '/audio/commander/num_18.mp3',
    '/audio/commander/num_19.mp3',
    '/audio/commander/num_20.mp3',
    '/audio/commander/num_21.mp3',
    '/audio/commander/num_22.mp3',
    '/audio/commander/num_23.mp3',
    '/audio/commander/num_24.mp3',
    '/audio/commander/num_25.mp3',
    '/audio/commander/num_26.mp3',
    '/audio/commander/num_27.mp3',
    '/audio/commander/num_28.mp3',
    '/audio/commander/num_29.mp3',
    '/audio/commander/num_30.mp3',
    '/audio/commander/num_31.mp3',
    '/audio/commander/num_32.mp3',
    '/audio/commander/num_33.mp3',
    '/audio/commander/num_34.mp3',
    '/audio/commander/num_35.mp3',
    '/audio/commander/num_36.mp3',
    '/audio/commander/num_37.mp3',
    '/audio/commander/num_38.mp3',
    '/audio/commander/num_39.mp3',
    '/audio/commander/num_40.mp3',
    '/audio/commander/num_41.mp3',
    '/audio/commander/num_42.mp3',
    '/audio/commander/num_43.mp3',
    '/audio/commander/num_44.mp3',
    '/audio/commander/num_45.mp3',
    '/audio/commander/num_46.mp3',
    '/audio/commander/num_47.mp3',
    '/audio/commander/num_48.mp3',
    '/audio/commander/num_49.mp3',
    '/audio/commander/num_50.mp3',
    '/audio/commander/num_51.mp3',
    '/audio/commander/num_52.mp3',
    '/audio/commander/num_53.mp3',
    '/audio/commander/num_54.mp3',
    '/audio/commander/num_55.mp3',
    '/audio/commander/num_56.mp3',
    '/audio/commander/num_57.mp3',
    '/audio/commander/num_58.mp3',
    '/audio/commander/num_59.mp3',
    '/audio/commander/num_60.mp3',
    // Encouragement & coaching
    '/audio/commander/enc_well_done.mp3',
    '/audio/commander/enc_great_work.mp3',
    '/audio/commander/ecc_lower_slowly.mp3',
    '/audio/commander/con_push_now.mp3',
    '/audio/commander/final_all_way.mp3',
    '/audio/commander/rest_recover.mp3'
];

// Install event - cache core files
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('Caching core files');
                return cache.addAll(coreFiles);
            })
            .catch(err => console.log('Core cache failed:', err))
    );
    self.skipWaiting();
});

// Fetch event - serve from cache, cache audio on demand
self.addEventListener('fetch', event => {
    const url = new URL(event.request.url);

    // Handle audio files separately
    if (url.pathname.includes('/audio/')) {
        event.respondWith(
            caches.open(AUDIO_CACHE).then(cache => {
                return cache.match(event.request).then(response => {
                    if (response) {
                        return response;
                    }
                    return fetch(event.request).then(networkResponse => {
                        // Cache audio file for offline use
                        cache.put(event.request, networkResponse.clone());
                        return networkResponse;
                    });
                });
            })
        );
        return;
    }

    // Handle other requests
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                if (response) {
                    return response;
                }
                return fetch(event.request)
                    .then(response => {
                        if (!response || response.status !== 200 || response.type !== 'basic') {
                            return response;
                        }
                        const responseToCache = response.clone();
                        caches.open(CACHE_NAME)
                            .then(cache => cache.put(event.request, responseToCache));
                        return response;
                    });
            })
            .catch(() => caches.match('/ios-app.html'))
    );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
    const cacheWhitelist = [CACHE_NAME, AUDIO_CACHE];
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (!cacheWhitelist.includes(cacheName)) {
                        console.log('Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    self.clients.claim();
});

// Background sync for preloading audio
self.addEventListener('message', event => {
    if (event.data === 'preloadAudio') {
        caches.open(AUDIO_CACHE).then(cache => {
            audioFiles.forEach(url => {
                cache.match(url).then(response => {
                    if (!response) {
                        fetch(url).then(res => cache.put(url, res));
                    }
                });
            });
        });
    }
});
