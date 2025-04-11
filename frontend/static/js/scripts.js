/* 
  Main JavaScript file for HBNB frontend
  Enhanced with register functionality, random data and animations
*/

document.addEventListener('DOMContentLoaded', () => {
  // Apply animations to elements
  applyAnimations();
  
  // Helper function to get cookie value by name
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
  }
  
  // Check if user is logged in
  function isLoggedIn() {
    return getCookie('token') !== null;
  }
  
  // Update UI based on login status
  function updateUIForLoggedInUser() {
    const loginButton = document.querySelector('.login-button');
    if (!loginButton) return;
    
    if (isLoggedIn()) {
      // Update login button to show "Logout" instead
      loginButton.textContent = 'Logout';
      loginButton.href = '#';
      loginButton.addEventListener('click', (e) => {
        e.preventDefault();
        // Clear the token cookie
        document.cookie = 'token=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
        // Redirect to login page
        window.location.href = 'login.html';
      });
    } else {
      // Ensure login button is visible and properly labeled
      loginButton.textContent = 'Login';
      loginButton.href = 'login.html';
    }
  }
  
  // Apply animations to elements
  function applyAnimations() {
    // Add animation classes to header elements
    const header = document.querySelector('header');
    if (header) {
      header.classList.add('animated', 'fade-in');
      
      const logo = header.querySelector('.logo');
      if (logo) logo.classList.add('animated', 'slide-left');
      
      const nav = header.querySelector('nav');
      if (nav) nav.classList.add('animated', 'slide-right');
    }
    
    // Add animation classes to main content
    const main = document.querySelector('main');
    if (main) main.classList.add('animated', 'fade-in');
    
    // Add animation classes to forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
      form.classList.add('animated', 'slide-up');
    });
    
    // Add animation classes to place cards with staggered delay
    const placeCards = document.querySelectorAll('.place-card');
    placeCards.forEach((card, index) => {
      card.classList.add('animated', 'slide-up');
      card.style.animationDelay = `${0.1 * (index % 5)}s`;
    });
    
    // Add animation classes to review cards with staggered delay
    const reviewCards = document.querySelectorAll('.review-card');
    reviewCards.forEach((card, index) => {
      card.classList.add('animated', 'slide-up');
      card.style.animationDelay = `${0.1 * (index % 3)}s`;
    });
  }
  
  // Generate a random integer between min and max (inclusive)
  function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }
  
  // Generate a random price between 10 and 2500 dollars
  function getRandomPrice() {
    return getRandomInt(10, 2500);
  }
  
  // Generate a consistent random price based on place ID
  function getConsistentRandomPrice(id) {
    // Use the place ID to generate a consistent random number
    let hash = 0;
    for (let i = 0; i < id.length; i++) {
      hash = ((hash << 5) - hash) + id.charCodeAt(i);
      hash |= 0; // Convert to 32bit integer
    }
    
    // Use the hash to generate a price between 10 and 2500
    const normalizedHash = Math.abs(hash) / 2147483647; // Normalize to 0-1
    return Math.floor(normalizedHash * (2500 - 10 + 1)) + 10;
  }
  
  // Fetch places from API
  async function fetchPlaces() {
    try {
      const headers = {
        'Content-Type': 'application/json'
      };
      
      // Add authorization header if user is logged in
      const token = getCookie('token');
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }
      
      // Add cache-busting parameter to prevent caching
      const cacheBuster = Date.now();
      const response = await fetch(`http://localhost:5000/api/v1/places/?_=${cacheBuster}`, {
        method: 'GET',
        headers: headers,
        cache: 'no-store' // Tell browser not to cache this request
      });
      
      if (response.ok) {
        const places = await response.json();
        return places;
      } else {
        console.error('Failed to fetch places:', response.statusText);
        return [];
      }
    } catch (error) {
      console.error('Error fetching places:', error);
      return [];
    }
  }
  
  // Generate a realistic place name based on place ID
  function generatePlaceName(id) {
    // Use the place ID to generate a consistent random number
    let hash = 0;
    for (let i = 0; i < id.length; i++) {
      hash = ((hash << 5) - hash) + id.charCodeAt(i);
      hash |= 0; // Convert to 32bit integer
    }
    
    // Use the hash to select from arrays of adjectives, types, and locations
    const adjectives = [
      'Luxurious', 'Cozy', 'Modern', 'Rustic', 'Charming', 'Elegant', 
      'Stunning', 'Peaceful', 'Scenic', 'Historic', 'Stylish', 'Quaint',
      'Contemporary', 'Traditional', 'Secluded', 'Bright', 'Spacious'
    ];
    
    const types = [
      'Villa', 'Apartment', 'Cottage', 'Cabin', 'Loft', 'House', 
      'Penthouse', 'Bungalow', 'Chalet', 'Studio', 'Condo', 'Retreat',
      'Mansion', 'Townhouse', 'Suite', 'Farmhouse', 'Estate'
    ];
    
    const locations = [
      'by the Beach', 'in the Mountains', 'Downtown', 'with Ocean View', 
      'with Lake View', 'in the Forest', 'in the City Center', 'with Garden',
      'with Pool', 'near the Park', 'in the Countryside', 'with Terrace',
      'in the Historic District', 'with Panoramic Views', 'in Wine Country',
      'on the Waterfront', 'in the Arts District', 'with Private Beach'
    ];
    
    // Use the hash to select items from each array
    const normalizedHash = Math.abs(hash) / 2147483647; // Normalize to 0-1
    const adjIndex = Math.floor(normalizedHash * adjectives.length);
    const typeIndex = Math.floor((normalizedHash * 13.37) % types.length);
    const locIndex = Math.floor((normalizedHash * 42.42) % locations.length);
    
    // Combine the selected items to create a place name
    return `${adjectives[adjIndex]} ${types[typeIndex]} ${locations[locIndex]}`;
  }
  
  // Generate a real city name based on coordinates
  function getCityFromCoordinates(latitude, longitude, id) {
    // Map of coordinates to city names
    const cityMap = {
      // Europe
      '48.8566,2.3522': 'Paris, France',
      '51.5074,-0.1278': 'London, UK',
      '41.9028,12.4964': 'Rome, Italy',
      '52.5200,13.4050': 'Berlin, Germany',
      '40.4168,-3.7038': 'Madrid, Spain',
      '55.7558,37.6173': 'Moscow, Russia',
      '52.3676,4.9041': 'Amsterdam, Netherlands',
      '59.3293,18.0686': 'Stockholm, Sweden',
      '55.6761,12.5683': 'Copenhagen, Denmark',
      '48.2082,16.3738': 'Vienna, Austria',
      
      // North America
      '40.7128,-74.0060': 'New York City, USA',
      '34.0522,-118.2437': 'Los Angeles, USA',
      '41.8781,-87.6298': 'Chicago, USA',
      '29.7604,-95.3698': 'Houston, USA',
      '43.6532,-79.3832': 'Toronto, Canada',
      '45.5017,-73.5673': 'Montreal, Canada',
      '19.4326,-99.1332': 'Mexico City, Mexico',
      
      // Asia
      '35.6762,139.6503': 'Tokyo, Japan',
      '22.3193,114.1694': 'Hong Kong',
      '1.3521,103.8198': 'Singapore',
      '25.2048,55.2708': 'Dubai, UAE',
      '39.9042,116.4074': 'Beijing, China',
      '31.2304,121.4737': 'Shanghai, China',
      '37.5665,126.9780': 'Seoul, South Korea',
      '28.6139,77.2090': 'New Delhi, India',
      '13.7563,100.5018': 'Bangkok, Thailand',
      
      // Australia/Oceania
      '-33.8688,151.2093': 'Sydney, Australia',
      '-37.8136,144.9631': 'Melbourne, Australia',
      '-41.2865,174.7762': 'Wellington, New Zealand',
      
      // South America
      '-34.6037,-58.3816': 'Buenos Aires, Argentina',
      '-23.5505,-46.6333': 'São Paulo, Brazil',
      '-33.4489,-70.6693': 'Santiago, Chile',
      
      // Africa
      '-33.9249,18.4241': 'Cape Town, South Africa',
      '30.0444,31.2357': 'Cairo, Egypt',
      '6.5244,3.3792': 'Lagos, Nigeria'
    };
    
    // Round coordinates to 4 decimal places for matching
    const roundedLat = latitude.toFixed(4);
    const roundedLng = longitude.toFixed(4);
    const coordKey = `${roundedLat},${roundedLng}`;
    
    // Try to find an exact match
    if (cityMap[coordKey]) {
      return cityMap[coordKey];
    }
    
    // If no exact match, find the closest city
    // Calculate distance between two points using Haversine formula
    function getDistance(lat1, lon1, lat2, lon2) {
      const R = 6371; // Radius of the earth in km
      const dLat = (lat2 - lat1) * Math.PI / 180;
      const dLon = (lon2 - lon1) * Math.PI / 180;
      const a = 
        Math.sin(dLat/2) * Math.sin(dLat/2) +
        Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * 
        Math.sin(dLon/2) * Math.sin(dLon/2);
      const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
      return R * c; // Distance in km
    }
    
    let closestCity = null;
    let minDistance = Infinity;
    
    for (const coords in cityMap) {
      const [lat, lng] = coords.split(',').map(Number);
      const distance = getDistance(latitude, longitude, lat, lng);
      
      if (distance < minDistance) {
        minDistance = distance;
        closestCity = cityMap[coords];
      }
    }
    
    // If we found a city within 500km, use it
    if (closestCity && minDistance < 500) {
      return closestCity;
    }
    
    // Generate a city name based on the place ID if no match found
    // Use the place ID to generate a consistent random number
    let hash = 0;
    for (let i = 0; i < id.length; i++) {
      hash = ((hash << 5) - hash) + id.charCodeAt(i);
      hash |= 0; // Convert to 32bit integer
    }
    
    // Arrays of city names and countries
    const cities = [
      'Lakeside', 'Riverdale', 'Mountainview', 'Seaside', 'Valleytown',
      'Pinecrest', 'Oakridge', 'Maplewood', 'Cedarville', 'Elmwood',
      'Brookside', 'Highland', 'Meadowbrook', 'Sunset', 'Bayview',
      'Harborview', 'Oceanside', 'Cliffside', 'Hillcrest', 'Westwood'
    ];
    
    const countries = [
      'USA', 'Canada', 'France', 'Italy', 'Spain', 'Germany', 'UK',
      'Australia', 'Japan', 'Brazil', 'Mexico', 'South Africa', 'Sweden',
      'Norway', 'Switzerland', 'Portugal', 'Greece', 'Thailand', 'New Zealand'
    ];
    
    // Use the hash to select a city and country
    const normalizedHash = Math.abs(hash) / 2147483647; // Normalize to 0-1
    const cityIndex = Math.floor(normalizedHash * cities.length);
    const countryIndex = Math.floor((normalizedHash * 13.37) % countries.length);
    
    return `${cities[cityIndex]}, ${countries[countryIndex]}`;
  }
  
  // Generate a realistic place description based on place name and ID
  function generatePlaceDescription(name, id) {
    // Use the place ID to generate a consistent random number
    let hash = 0;
    for (let i = 0; i < id.length; i++) {
      hash = ((hash << 5) - hash) + id.charCodeAt(i);
      hash |= 0; // Convert to 32bit integer
    }
    
    // Parse the name to extract components
    const nameParts = name.split(' ');
    const adjective = nameParts[0].toLowerCase();
    const type = nameParts[1].toLowerCase();
    const location = nameParts.slice(2).join(' ').toLowerCase();
    
    // Arrays of description templates
    const templates = [
      `This ${adjective} ${type} ${location} offers a perfect getaway for your next vacation.`,
      `Experience the beauty of this ${adjective} ${type} ${location}, ideal for relaxation and adventure.`,
      `Enjoy your stay in our ${adjective} ${type} ${location}, featuring all the comforts of home.`,
      `Welcome to this ${adjective} ${type} ${location}, where comfort meets style.`,
      `Discover the charm of our ${adjective} ${type} ${location}, perfect for your next trip.`,
      `Escape to this ${adjective} ${type} ${location} and enjoy a memorable stay.`,
      `Relax and unwind in this ${adjective} ${type} ${location}, designed for your comfort.`,
      `This ${adjective} ${type} ${location} provides the perfect setting for an unforgettable experience.`
    ];
    
    // Use the hash to select a template
    const normalizedHash = Math.abs(hash) / 2147483647; // Normalize to 0-1
    const templateIndex = Math.floor(normalizedHash * templates.length);
    
    return templates[templateIndex];
  }
  
  // Create place card element with random price
  function createPlaceCard(place) {
    const placeCard = document.createElement('div');
    placeCard.className = 'place-card';
    placeCard.dataset.id = place.id;
    
    // Generate a realistic place name if the title is "Test Place" or missing
    let placeName = place.title;
    if (!placeName || placeName === 'Test Place' || placeName === 'Unnamed Place') {
      placeName = generatePlaceName(place.id);
    }
    
    const title = document.createElement('h3');
    title.textContent = placeName;
    
    const description = document.createElement('p');
    // Generate a realistic description based on the place name and location
    const generatedDesc = generatePlaceDescription(placeName, place.id);
    
    // Get city name from coordinates if available
    if (place.latitude && place.longitude) {
      const cityName = getCityFromCoordinates(place.latitude, place.longitude, place.id);
      description.textContent = `${generatedDesc} Located in ${cityName}.`;
    } else {
      description.textContent = generatedDesc;
    }
    
    const price = document.createElement('p');
    price.className = 'price';
    // Generate a consistent random price based on place ID
    const randomPrice = getConsistentRandomPrice(place.id);
    price.textContent = `$${randomPrice} per night`;
    
    const detailsButton = document.createElement('a');
    detailsButton.href = `place.html?id=${place.id}`;
    detailsButton.className = 'details-button';
    detailsButton.textContent = 'View Details';
    
    placeCard.appendChild(title);
    placeCard.appendChild(description);
    placeCard.appendChild(price);
    placeCard.appendChild(detailsButton);
    
    // Add animation class
    placeCard.classList.add('animated', 'slide-up');
    
    return placeCard;
  }
  
  // Shuffle array (Fisher-Yates algorithm)
  function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
  }
  
  // Populate places list with randomized order
  async function populatePlacesList() {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;
    
    // Clear existing content
    placesList.innerHTML = '';
    
    // Show loading indicator
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'loading';
    placesList.appendChild(loadingDiv);
    
    try {
      // Fetch places from API
      let places = await fetchPlaces();
      
      // Remove loading indicator
      placesList.removeChild(loadingDiv);
      
      if (places.length === 0) {
        const noPlacesMessage = document.createElement('p');
        noPlacesMessage.textContent = 'No places found.';
        placesList.appendChild(noPlacesMessage);
        return;
      }
      
      // Randomize the order of places
      places = shuffleArray(places);
      
      // Create and append place cards with staggered animation delay
      places.forEach((place, index) => {
        const placeCard = createPlaceCard(place);
        placeCard.style.animationDelay = `${0.1 * (index % 5)}s`;
        placesList.appendChild(placeCard);
      });
      
      // Initialize price filter after places are loaded
      initializePriceFilter();
    } catch (error) {
      // Remove loading indicator
      placesList.removeChild(loadingDiv);
      
      // Show error message
      const errorMessage = document.createElement('p');
      errorMessage.textContent = 'Error loading places. Please try again later.';
      errorMessage.style.color = 'red';
      placesList.appendChild(errorMessage);
      
      console.error('Error populating places list:', error);
    }
  }
  
  // Initialize price filter
  function initializePriceFilter() {
    const priceFilter = document.getElementById('price-filter');
    if (!priceFilter) return;
    
    priceFilter.addEventListener('change', () => {
      const maxPrice = priceFilter.value;
      const placeCards = document.querySelectorAll('.place-card');
      
      // If "All Prices" is selected, show all places
      if (maxPrice === 'all') {
        placeCards.forEach(card => {
          card.style.display = 'block';
        });
        return;
      }
      
      // Otherwise, filter places by price
      placeCards.forEach(card => {
        const priceText = card.querySelector('.price').textContent;
        const price = parseInt(priceText.replace(/\D/g, ''));
        
        if (price <= parseInt(maxPrice)) {
          card.style.display = 'block';
        } else {
          card.style.display = 'none';
        }
      });
    });
  }
  
  // Initialize layout controls
  function initializeLayoutControls() {
    const placesList = document.getElementById('places-list');
    const layoutButtons = document.querySelectorAll('.layout-btn');
    
    if (!placesList || !layoutButtons.length) return;
    
    // Load saved layout preference from localStorage
    const savedLayout = localStorage.getItem('preferredLayout') || 'grid';
    
    // Apply saved layout
    changeLayout(savedLayout);
    
    // Add event listeners to layout buttons
    layoutButtons.forEach(button => {
      button.addEventListener('click', () => {
        const layout = button.getAttribute('data-layout');
        changeLayout(layout);
      });
      
      // Set active state based on saved preference
      if (button.getAttribute('data-layout') === savedLayout) {
        button.classList.add('active');
      } else {
        button.classList.remove('active');
      }
    });
    
    // Add shine effect to place cards
    const placeCards = document.querySelectorAll('.place-card');
    placeCards.forEach(card => {
      const shine = document.createElement('div');
      shine.className = 'shine';
      card.appendChild(shine);
    });
  }
  
  // Change layout of places list
  function changeLayout(layout) {
    const placesList = document.getElementById('places-list');
    const layoutButtons = document.querySelectorAll('.layout-btn');
    
    if (!placesList || !layoutButtons.length) return;
    
    // Remove all layout classes
    placesList.classList.remove('grid-layout', 'list-layout', 'compact-layout', 'masonry-layout');
    
    // Add the selected layout class
    placesList.classList.add(`${layout}-layout`);
    
    // Update active state of layout buttons
    layoutButtons.forEach(button => {
      if (button.getAttribute('data-layout') === layout) {
        button.classList.add('active');
      } else {
        button.classList.remove('active');
      }
    });
    
    // Save preference to localStorage
    localStorage.setItem('preferredLayout', layout);
    
    // Add animation to places list
    placesList.classList.add('animated', 'fade-in');
    setTimeout(() => {
      placesList.classList.remove('animated', 'fade-in');
    }, 1000);
  }
  
  // Add scroll to top button
  function addScrollToTopButton() {
    // Create the button
    const scrollTopButton = document.createElement('div');
    scrollTopButton.className = 'scroll-top';
    scrollTopButton.innerHTML = '↑';
    scrollTopButton.title = 'Scroll to top';
    document.body.appendChild(scrollTopButton);
    
    // Add theme toggle button
    const themeToggle = document.createElement('div');
    themeToggle.className = 'theme-toggle';
    themeToggle.innerHTML = '☀';
    themeToggle.title = 'Toggle theme';
    document.body.appendChild(themeToggle);
    
    // Show/hide scroll button based on scroll position
    window.addEventListener('scroll', () => {
      if (window.pageYOffset > 300) {
        scrollTopButton.classList.add('visible');
      } else {
        scrollTopButton.classList.remove('visible');
      }
    });
    
    // Scroll to top when clicked
    scrollTopButton.addEventListener('click', () => {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
    
    // Toggle theme when clicked
    themeToggle.addEventListener('click', () => {
      document.body.classList.toggle('dark-theme');
      
      // Save theme preference
      const isDarkTheme = document.body.classList.contains('dark-theme');
      localStorage.setItem('darkTheme', isDarkTheme);
      
      // Update icon
      themeToggle.innerHTML = isDarkTheme ? '☀' : '☾';
    });
    
    // Apply saved theme preference
    if (localStorage.getItem('darkTheme') === 'true') {
      document.body.classList.add('dark-theme');
      themeToggle.innerHTML = '☀';
    }
  }
  
  // Helper function to display messages
  function displayMessage(containerId, message, type = 'error') {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    // Clear previous messages
    container.innerHTML = '';
    
    // Create message element
    const messageElement = document.createElement('div');
    messageElement.className = type === 'error' ? 'error-message' : 'success-message';
    messageElement.textContent = message;
    
    // Add animation class
    messageElement.classList.add('animated', 'slide-up');
    
    // Add message to container
    container.appendChild(messageElement);
  }
  
  // Handle login form submission
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
      
      try {
        console.log('Login attempt with:', { email, password: '***' });
        
        // Make API request to login endpoint
        console.log('Sending request to:', 'http://localhost:5000/api/v1/auth/login');
        const response = await fetch('http://localhost:5000/api/v1/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ email, password })
        });
        
        if (response.ok) {
          // If login is successful, store JWT token in cookie
          const data = await response.json();
          document.cookie = `token=${data.access_token}; path=/; max-age=86400`; // 24 hours
          
          // Show success message with animation
          displayMessage('login-messages', 'Login successful! Redirecting...', 'success');
          
          // Redirect to index page after a short delay
          setTimeout(() => {
            window.location.href = 'index.html';
          }, 1500);
        } else {
          // If login fails, display error message
          const errorData = await response.json();
          displayMessage('login-messages', errorData.error || 'Login failed. Please check your credentials.');
        }
      } catch (error) {
        // Handle network errors
        console.error('Login error:', error);
        displayMessage('login-messages', 'Network error. Please check if the API server is running and try again.');
      }
    });
  }
  
  // Handle register form submission
  const registerForm = document.getElementById('register-form');
  if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      const firstName = document.getElementById('first_name').value;
      const lastName = document.getElementById('last_name').value;
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
      const confirmPassword = document.getElementById('confirm_password').value;
      
      // Validate input
      if (!firstName || !lastName || !email || !password) {
        displayMessage('register-messages', 'All fields are required.');
        return;
      }
      
      // Validate email format
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email)) {
        displayMessage('register-messages', 'Please enter a valid email address.');
        return;
      }
      
      // Validate password length
      if (password.length < 6) {
        displayMessage('register-messages', 'Password must be at least 6 characters long.');
        return;
      }
      
      // Check if passwords match
      if (password !== confirmPassword) {
        displayMessage('register-messages', 'Passwords do not match.');
        return;
      }
      
      // Show loading message
      displayMessage('register-messages', 'Creating your account...', 'success');
      
      try {
        // Make API request to register endpoint
        const response = await fetch('http://localhost:5000/api/v1/users/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            first_name: firstName,
            last_name: lastName,
            email: email,
            password: password
          })
        });
        
        if (response.ok) {
          // If registration is successful, show success message
          displayMessage('register-messages', 'Account created successfully! Redirecting to login page...', 'success');
          
          // Redirect to login page after a short delay
          setTimeout(() => {
            window.location.href = 'login.html';
          }, 2000);
        } else {
          // Handle different error responses
          if (response.status === 400) {
            const errorData = await response.json();
            if (errorData.error && errorData.error.includes('Email already registered')) {
              displayMessage('register-messages', 'This email is already registered. Please use a different email or login.');
            } else {
              displayMessage('register-messages', errorData.error || 'Registration failed. Please check your information.');
            }
          } else {
            displayMessage('register-messages', 'Registration failed. Please try again later.');
          }
        }
      } catch (error) {
        console.error('Registration error:', error);
        displayMessage('register-messages', 'Network error. Please check if the API server is running and try again.');
      }
    });
  }
  
  // Generate random user names for reviews
  function getRandomUserName() {
    const firstNames = [
      'Emma', 'Liam', 'Olivia', 'Noah', 'Ava', 'William', 'Sophia', 'James',
      'Isabella', 'Logan', 'Charlotte', 'Benjamin', 'Amelia', 'Mason', 'Mia',
      'Elijah', 'Harper', 'Oliver', 'Evelyn', 'Jacob', 'Abigail', 'Lucas',
      'Emily', 'Michael', 'Elizabeth', 'Alexander', 'Sofia', 'Ethan', 'Avery'
    ];
    
    const lastNames = [
      'Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller',
      'Wilson', 'Moore', 'Taylor', 'Anderson', 'Thomas', 'Jackson', 'White',
      'Harris', 'Martin', 'Thompson', 'Garcia', 'Martinez', 'Robinson', 'Clark',
      'Rodriguez', 'Lewis', 'Lee', 'Walker', 'Hall', 'Allen', 'Young', 'King'
    ];
    
    const firstName = firstNames[Math.floor(Math.random() * firstNames.length)];
    const lastName = lastNames[Math.floor(Math.random() * lastNames.length)];
    
    return `${firstName} ${lastName}`;
  }
  
  // Generate random review text
  function getRandomReviewText() {
    const positiveAdjectives = [
      'amazing', 'wonderful', 'fantastic', 'excellent', 'great', 'perfect',
      'lovely', 'beautiful', 'comfortable', 'clean', 'spacious', 'cozy',
      'charming', 'delightful', 'peaceful', 'relaxing', 'convenient'
    ];
    
    const features = [
      'location', 'view', 'amenities', 'host', 'neighborhood', 'decor',
      'kitchen', 'bathroom', 'bedroom', 'living room', 'balcony', 'patio',
      'pool', 'garden', 'parking', 'WiFi', 'TV', 'air conditioning'
    ];
    
    const positiveVerbs = [
      'enjoyed', 'loved', 'appreciated', 'liked', 'adored'
    ];
    
    const recommendations = [
      'Highly recommend!',
      'Would definitely stay again!',
      'Can\'t wait to come back!',
      'Perfect for a vacation!',
      'Great value for the price!',
      'You won\'t be disappointed!',
      'Five stars all around!',
      'A hidden gem!',
      'Exceeded our expectations!'
    ];
    
    // Generate a random review with 2-3 sentences
    let review = '';
    
    // First sentence - general impression
    const adj1 = positiveAdjectives[Math.floor(Math.random() * positiveAdjectives.length)];
    const adj2 = positiveAdjectives[Math.floor(Math.random() * positiveAdjectives.length)];
    if (Math.random() > 0.5) {
      review += `This place was ${adj1} and ${adj2}! `;
    } else {
      review += `We had an ${adj1} stay at this ${adj2} place! `;
    }
    
    // Second sentence - specific features
    const feature1 = features[Math.floor(Math.random() * features.length)];
    const feature2 = features[Math.floor(Math.random() * features.length)];
    const verb = positiveVerbs[Math.floor(Math.random() * positiveVerbs.length)];
    if (feature1 !== feature2) {
      review += `We really ${verb} the ${feature1} and the ${feature2}. `;
    } else {
      const feature3 = features[Math.floor(Math.random() * features.length)];
      if (feature1 !== feature3) {
        review += `We really ${verb} the ${feature1} and the ${feature3}. `;
      } else {
        review += `The ${feature1} was outstanding. `;
      }
    }
    
    // Third sentence - recommendation
    if (Math.random() > 0.3) {
      const recommendation = recommendations[Math.floor(Math.random() * recommendations.length)];
      review += recommendation;
    }
    
    return review;
  }
  
  // Generate random reviews for a place
  function generateRandomReviews(placeId, count = 3) {
    const reviews = [];
    
    // Use the place ID to seed the random number generator for consistent reviews
    let seed = 0;
    for (let i = 0; i < placeId.length; i++) {
      seed = ((seed << 5) - seed) + placeId.charCodeAt(i);
      seed |= 0;
    }
    
    // Generate random reviews
    for (let i = 0; i < count; i++) {
      // Use a combination of the place ID and index to generate a consistent random seed
      const reviewSeed = seed + i;
      
      // Use the seed to generate a consistent random rating (3-5 stars, weighted towards higher ratings)
      const ratingRandom = Math.abs(reviewSeed) / 2147483647; // Normalize to 0-1
      let rating;
      if (ratingRandom < 0.2) {
        rating = 3;
      } else if (ratingRandom < 0.5) {
        rating = 4;
      } else {
        rating = 5;
      }
      
      reviews.push({
        id: `fake-${placeId}-${i}`,
        user_name: getRandomUserName(),
        rating: rating,
        text: getRandomReviewText(),
        created_at: new Date(Date.now() - getRandomInt(1, 90) * 24 * 60 * 60 * 1000).toISOString().split('T')[0] // Random date in the last 90 days
      });
    }
    
    return reviews;
  }
  
  // Populate add review page with place info
  async function populateAddReviewPage() {
    // Check if user is logged in, redirect to index if not
    if (!isLoggedIn()) {
      displayMessage('review-messages', 'You must be logged in to add a review.', 'error');
      // Redirect to index page after a short delay
      setTimeout(() => {
        window.location.href = 'index.html';
      }, 2000);
      return;
    }
    
    const placeInfoSection = document.querySelector('#place-info');
    if (!placeInfoSection) return;
    
    // Get place ID from URL query parameter
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');
    
    if (!placeId) {
      placeInfoSection.innerHTML = '<p>No place ID provided.</p>';
      return;
    }
    
    try {
      // Fetch all places and find the one we need
      const places = await fetchPlaces();
      const place = places.find(p => p.id === placeId);
      
      if (!place) {
        placeInfoSection.innerHTML = '<p>Place not found. Please try another place.</p>';
        return;
      }
      
      // Update the place info section
      const placeTitle = placeInfoSection.querySelector('h2');
      if (placeTitle) {
        const titleSpan = placeTitle.querySelector('#place-title');
        if (titleSpan) {
          titleSpan.textContent = place.title || 'Unnamed Place';
        }
      }
      
      // Update the location info if it exists
      const locationInfo = placeInfoSection.querySelector('#place-location');
      if (locationInfo && place.latitude && place.longitude) {
        const cityName = getCityFromCoordinates(place.latitude, place.longitude, place.id);
        locationInfo.textContent = cityName;
      }
      
      // Update the back link to point to the correct place
      const backLink = document.querySelector('#back-to-place');
      if (backLink) {
        backLink.href = `place.html?id=${placeId}`;
      }
    } catch (error) {
      console.error('Error populating add review page:', error);
      placeInfoSection.innerHTML = '<p>Error loading place information. Please try again later.</p>';
    }
  }
  
  // Handle review form submission
  const reviewForm = document.getElementById('review-form');
  if (reviewForm) {
    reviewForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      // Check if user is logged in
      if (!isLoggedIn()) {
        displayMessage('review-messages', 'You must be logged in to add a review.', 'error');
        // Redirect to index page after a short delay
        setTimeout(() => {
          window.location.href = 'index.html';
        }, 2000);
        return;
      }
      
      const rating = document.getElementById('rating').value;
      const reviewText = document.getElementById('review').value;
      
      // Validate input
      if (!rating) {
        displayMessage('review-messages', 'Please select a rating.', 'error');
        return;
      }
      
      if (!reviewText.trim()) {
        displayMessage('review-messages', 'Please enter a review.', 'error');
        return;
      }
      
      // Get place ID from URL query parameter
      const urlParams = new URLSearchParams(window.location.search);
      const placeId = urlParams.get('id');
      
      if (!placeId) {
        displayMessage('review-messages', 'No place ID provided.', 'error');
        return;
      }
      
      // Show loading message
      displayMessage('review-messages', 'Submitting your review...', 'success');
      
      try {
        // Get JWT token
        const token = getCookie('token');
        
      // Prepare request data
      const reviewData = {
        text: reviewText,
        rating: parseInt(rating),
        place_id: placeId,
        user_id: "placeholder" // Backend will replace this with the actual user ID from JWT token
      };
        
        console.log('Submitting review:', reviewData);
        
        // Send request to API
        const response = await fetch('http://localhost:5000/api/v1/reviews/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify(reviewData)
        });
        
        if (response.ok) {
          // Show success message
          displayMessage('review-messages', 'Thank you for your review!', 'success');
          
          // Clear form
          reviewForm.reset();
          
          // Redirect to place details page after a short delay and force refresh
          setTimeout(() => {
            // Add a timestamp parameter to force a fresh page load
            window.location.href = `place.html?id=${placeId}&t=${Date.now()}`;
          }, 2000);
        } else {
          // Handle API error
          const errorData = await response.json();
          let errorMessage = 'Failed to submit review.';
          
          if (errorData && errorData.message) {
            errorMessage = errorData.message;
          } else if (response.status === 400) {
            errorMessage = 'Invalid review data. Please check your input.';
          } else if (response.status === 401) {
            errorMessage = 'You must be logged in to add a review.';
          } else if (response.status === 403) {
            errorMessage = 'You cannot review your own place or add multiple reviews for the same place.';
          }
          
          displayMessage('review-messages', errorMessage, 'error');
        }
      } catch (error) {
        console.error('Error submitting review:', error);
        displayMessage('review-messages', 'Network error. Please check if the API server is running and try again.', 'error');
      }
    });
  }
  
  // Fetch place details from API
  async function fetchPlaceDetails(placeId) {
    try {
      const headers = {
        'Content-Type': 'application/json'
      };
      
      // Add authorization header if user is logged in
      const token = getCookie('token');
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }
      
      const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}/`, {
        method: 'GET',
        headers: headers
      });
      
      if (response.ok) {
        const place = await response.json();
        return place;
      } else {
        console.error('Failed to fetch place details:', response.statusText);
        // Add more detailed error information
        const errorInfo = {
          error: true,
          status: response.status,
          statusText: response.statusText,
          url: response.url
        };
        return errorInfo;
      }
    } catch (error) {
      console.error('Error fetching place details:', error);
      return null;
    }
  }
  
  // Fetch reviews for a place from API
  async function fetchPlaceReviews(placeId) {
    try {
      const headers = {
        'Content-Type': 'application/json'
      };
      
      // Add authorization header if user is logged in
      const token = getCookie('token');
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }
      
      // Add cache-busting parameter to prevent caching
      const cacheBuster = Date.now();
      const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}/reviews/?_=${cacheBuster}`, {
        method: 'GET',
        headers: headers,
        cache: 'no-store' // Tell browser not to cache this request
      });
      
      if (response.ok) {
        const reviews = await response.json();
        return reviews;
      } else {
        console.error('Failed to fetch reviews:', response.statusText);
        return [];
      }
    } catch (error) {
      console.error('Error fetching reviews:', error);
      return [];
    }
  }
  
  // Create review element
  function createReviewElement(review) {
    const reviewCard = document.createElement('div');
    reviewCard.className = 'review-card';
    
    const userName = document.createElement('h4');
    userName.textContent = review.user_name || 'Anonymous';
    
    const rating = document.createElement('div');
    rating.className = 'rating';
    rating.textContent = '★'.repeat(review.rating) + '☆'.repeat(5 - review.rating);
    
    const date = document.createElement('p');
    date.className = 'review-date';
    date.textContent = review.created_at || 'Recently';
    
    const comment = document.createElement('p');
    comment.className = 'review-text';
    comment.textContent = review.text;
    
    reviewCard.appendChild(userName);
    reviewCard.appendChild(rating);
    reviewCard.appendChild(date);
    reviewCard.appendChild(comment);
    
    // Add animation class
    reviewCard.classList.add('animated', 'slide-up');
    
    return reviewCard;
  }
  
  // Populate place details page
  async function populatePlaceDetails() {
    const placeDetails = document.getElementById('place-details');
    const reviewsSection = document.getElementById('reviews');
    
    if (!placeDetails || !reviewsSection) return;
    
    // Get place ID from URL query parameter
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');
    
    if (!placeId) {
      placeDetails.innerHTML = '<p>No place ID provided.</p>';
      return;
    }
    
    // Show loading indicator
    placeDetails.innerHTML = '<div class="loading"></div>';
    reviewsSection.innerHTML = '<h2>Reviews</h2><div class="loading"></div>';
    
    try {
      // Since the specific place endpoint doesn't work, fetch all places and find the one we need
      const places = await fetchPlaces();
      const place = places.find(p => p.id === placeId);
      
      if (!place) {
        placeDetails.innerHTML = '<p>Place not found. Please try another place.</p>';
        reviewsSection.innerHTML = '<h2>Reviews</h2><p>No reviews available.</p>';
        return;
      }
      
      // Generate a consistent random price based on place ID
      const randomPrice = getConsistentRandomPrice(place.id);
      
      // Get place name and city
      const placeName = place.title || generatePlaceName(place.id);
      let cityName = 'Location not specified';
      if (place.latitude && place.longitude) {
        cityName = getCityFromCoordinates(place.latitude, place.longitude, place.id);
      }
      
      // Populate place details with available data and animations
      placeDetails.innerHTML = `
        <h1 class="animated fade-in">${placeName}</h1>
        
        <div class="place-info animated slide-up">
          <p><strong>Host:</strong> John Doe</p>
          <p><strong>Price:</strong> <span class="price">$${randomPrice} per night</span></p>
          <p><strong>Location:</strong> ${cityName}</p>
          <p><strong>Description:</strong> ${place.description || 
            generatePlaceDescription(placeName, place.id)}</p>
        </div>
        
        <div class="amenities animated slide-up delay-1">
          <h3>Amenities</h3>
          <div class="amenity">
            <img src="../static/images/icon_wifi.png" alt="WiFi">
            <span>WiFi</span>
          </div>
          <div class="amenity">
            <img src="../static/images/icon_bed.png" alt="Comfortable Beds">
            <span>Comfortable Beds</span>
          </div>
          <div class="amenity">
            <img src="../static/images/icon_bath.png" alt="Private Bathroom">
            <span>Private Bathroom</span>
          </div>
        </div>
      `;
      
      // Reset reviews section
      reviewsSection.innerHTML = '<h2 class="animated fade-in">Reviews</h2>';
      
      // Try to fetch real reviews first
      let reviews = await fetchPlaceReviews(placeId);
      
      // If no real reviews, generate random ones
      if (reviews.length === 0) {
        reviews = generateRandomReviews(placeId, getRandomInt(2, 5));
      }
      
      if (reviews.length === 0) {
        const noReviewsMessage = document.createElement('p');
        noReviewsMessage.textContent = 'No reviews yet. Be the first to leave a review!';
        noReviewsMessage.classList.add('animated', 'fade-in');
        reviewsSection.appendChild(noReviewsMessage);
      } else {
        // Create and append review cards with staggered animation delay
        reviews.forEach((review, index) => {
          const reviewCard = createReviewElement(review);
          reviewCard.style.animationDelay = `${0.2 * (index + 1)}s`;
          reviewsSection.appendChild(reviewCard);
        });
      }
      
      // Add "Add a Review" button if user is logged in
      const addReviewButton = document.createElement('a');
      addReviewButton.href = `add_review.html?id=${placeId}`;
      addReviewButton.className = 'details-button animated slide-up';
      addReviewButton.style.animationDelay = '0.5s';
      addReviewButton.textContent = 'Add a Review';
      
      // Only show the button if the user is logged in
      if (isLoggedIn()) {
        reviewsSection.appendChild(addReviewButton);
      } else {
        const loginMessage = document.createElement('p');
        loginMessage.textContent = 'Please log in to add a review.';
        loginMessage.style.fontStyle = 'italic';
        loginMessage.classList.add('animated', 'fade-in');
        loginMessage.style.animationDelay = '0.5s';
        reviewsSection.appendChild(loginMessage);
      }
      
    } catch (error) {
      console.error('Error populating place details:', error);
      placeDetails.innerHTML = '<p>An error occurred while loading place details. Please try again later.</p>';
      reviewsSection.innerHTML = '<h2>Reviews</h2><p>Failed to load reviews.</p>';
    }
  }
  
  // Initialize the page based on the current page
  updateUIForLoggedInUser();
  
  // Populate the appropriate page
  if (window.location.pathname.includes('place.html')) {
    populatePlaceDetails();
  } else if (window.location.pathname.includes('add_review.html')) {
    populateAddReviewPage();
  } else if (window.location.pathname.includes('register.html')) {
    // Nothing special needed for register page initialization
  } else if (document.getElementById('places-list')) {
    populatePlacesList();
    // Initialize layout controls after places are loaded
    setTimeout(() => {
      initializeLayoutControls();
    }, 500);
  }
  
  // Add scroll to top button and theme toggle
  addScrollToTopButton();
  
  // Apply animations after a short delay to ensure DOM is fully loaded
  setTimeout(applyAnimations, 100);
  
  // Add page transition effect
  document.body.classList.add('page-transition');
});