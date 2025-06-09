const CACHE_NAME = 'ai-doc-library-v1';
const urlsToCache = [
  '/tech_documents/',
  '/tech_documents/data/documents.json',
  '/tech_documents/_astro/',
  'https://cdn.tailwindcss.com',
  'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap'
];

// Install event - cache resources
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
      .catch((error) => {
        console.log('Cache install failed:', error);
      })
  );
});

// Fetch event - serve from cache when offline
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        // Return cached version or fetch from network
        if (response) {
          return response;
        }
        
        // Clone the request because it's a stream
        const fetchRequest = event.request.clone();
        
        return fetch(fetchRequest).then((response) => {
          // Check if we received a valid response
          if (!response || response.status !== 200 || response.type !== 'basic') {
            return response;
          }
          
          // Clone the response because it's a stream
          const responseToCache = response.clone();
          
          caches.open(CACHE_NAME)
            .then((cache) => {
              cache.put(event.request, responseToCache);
            });
          
          return response;
        }).catch(() => {
          // Return offline page or cached content
          if (event.request.destination === 'document') {
            return caches.match('/tech_documents/');
          }
        });
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Background sync for document updates
self.addEventListener('sync', (event) => {
  if (event.tag === 'background-sync') {
    event.waitUntil(
      fetch('/tech_documents/data/documents.json')
        .then((response) => response.json())
        .then((data) => {
          // Update cache with new documents
          caches.open(CACHE_NAME).then((cache) => {
            cache.put('/tech_documents/data/documents.json', new Response(JSON.stringify(data)));
          });
        })
        .catch((error) => {
          console.log('Background sync failed:', error);
        })
    );
  }
});

// Push notifications (for future use)
self.addEventListener('push', (event) => {
  const options = {
    body: event.data ? event.data.text() : 'New documents available!',
    icon: '/tech_documents/favicon.svg',
    badge: '/tech_documents/favicon.svg',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'explore',
        title: 'View Documents',
        icon: '/tech_documents/favicon.svg'
      },
      {
        action: 'close',
        title: 'Close',
        icon: '/tech_documents/favicon.svg'
      }
    ]
  };
  
  event.waitUntil(
    self.registration.showNotification('AI Document Library', options)
  );
});

// Handle notification clicks
self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  
  if (event.action === 'explore') {
    event.waitUntil(
      clients.openWindow('/tech_documents/')
    );
  }
});
