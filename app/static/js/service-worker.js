// PartyTicket Nigeria - Service Worker for Offline Functionality

const CACHE_NAME = 'partyticket-v1';
const urlsToCache = [
  '/',
  '/static/css/style.css',
  '/static/js/script.js',
  '/static/images/logo.png',
  '/static/images/favicon.png',
  '/offline',
  '/events',
  '/blog'
];

// Install event - cache assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

// Fetch event - serve cached content when offline
self.addEventListener('fetch', event => {
  // Only cache GET requests
  if (event.request.method !== 'GET') {
    return;
  }
  
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Return cached version or fetch from network
        if (response) {
          return response;
        }
        
        // Clone the request because it's a stream and can only be consumed once
        const fetchRequest = event.request.clone();
        
        return fetch(fetchRequest).then(response => {
          // Check if we received a valid response
          if (!response || response.status !== 200 || response.type !== 'basic') {
            return response;
          }
          
          // Clone the response because it's a stream and can only be consumed once
          const responseToCache = response.clone();
          
          caches.open(CACHE_NAME)
            .then(cache => {
              cache.put(event.request, responseToCache);
            });
            
          return response;
        }).catch(() => {
          // Serve offline page for navigation requests
          if (event.request.mode === 'navigate') {
            return caches.match('/offline');
          }
          
          // For other requests, return cached version if available
          return caches.match(event.request);
        });
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Message event - handle messages from client
self.addEventListener('message', event => {
  if (event.data.action === 'skipWaiting') {
    self.skipWaiting();
  }
});

// Push notification event
self.addEventListener('push', event => {
  const title = 'PartyTicket Notification';
  const options = {
    body: event.data.text(),
    icon: '/static/images/logo.png',
    badge: '/static/images/favicon.png'
  };
  
  event.waitUntil(
    self.registration.showNotification(title, options)
  );
});

// Notification click event
self.addEventListener('notificationclick', event => {
  event.notification.close();
  
  // Open the app when notification is clicked
  event.waitUntil(
    clients.openWindow('/')
  );
});

// Sync event for background sync
self.addEventListener('sync', event => {
  if (event.tag === 'sync-events') {
    event.waitUntil(
      // Perform background sync operations
      syncEvents()
    );
  }
});

// Function to sync events (placeholder)
function syncEvents() {
  // This would contain logic to sync events when online
  return Promise.resolve();
}