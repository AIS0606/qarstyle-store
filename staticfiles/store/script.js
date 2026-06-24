document.addEventListener('DOMContentLoaded', () => {
  const hamburger = document.getElementById('hamburger');
  const navLinks = document.getElementById('nav-links');

  if (hamburger && navLinks) {
    hamburger.addEventListener('click', () => {
      navLinks.classList.toggle('active');
    });
  }

  // Accordion Logic
  const accHeaders = document.querySelectorAll('.accordion-header');
  accHeaders.forEach(header => {
    header.addEventListener('click', function () {
      // Toggle plus/minus icon
      const icon = this.querySelector('.icon');
      if (icon) {
        icon.textContent = icon.textContent === '+' ? '-' : '+';
      }

      const content = this.nextElementSibling;
      if (content.style.maxHeight) {
        content.style.maxHeight = null;
      } else {
        content.style.maxHeight = content.scrollHeight + "px";
      }
    });
  });

  // Infinite Slider Logic
  const sliderTrack = document.getElementById('sliderTrack');
  const prevBtn = document.getElementById('prevSlide');
  const nextBtn = document.getElementById('nextSlide');
  const dotsContainer = document.getElementById('sliderDots');

  if (sliderTrack && prevBtn && nextBtn) {
    let originalSlides = Array.from(sliderTrack.children);
    let N = originalSlides.length;

    if (N > 0) {
      // Build dots dynamically based on number of unique photos
      if (dotsContainer) {
        dotsContainer.innerHTML = '';
        for (let i = 0; i < N; i++) {
          const dot = document.createElement('span');
          dot.classList.add('dot');
          if (i === 0) dot.classList.add('active');
          dot.dataset.index = i;
          dotsContainer.appendChild(dot);
        }
      }

      const dots = document.querySelectorAll('.dot');

      // Clone slides to ensure we have enough for infinite scrolling (at least 10 sets)
      for (let i = 0; i < 10; i++) {
        originalSlides.forEach(slide => {
          sliderTrack.appendChild(slide.cloneNode(true));
        });
      }

      // Start at the 5th set to allow scrolling left immediately
      let currentIndex = N * 5;
      let isTransitioning = false;

      // Initial position
      sliderTrack.style.transform = `translateX(-${currentIndex * 33.33333}vw)`;

      function updateSlider(smooth = true) {
        if (smooth) {
          sliderTrack.style.transition = 'transform 0.5s cubic-bezier(0.25, 1, 0.5, 1)';
        } else {
          sliderTrack.style.transition = 'none';
        }
        sliderTrack.style.transform = `translateX(-${currentIndex * 33.33333}vw)`;

        // Update dots
        if (dots.length > 0) {
          dots.forEach(dot => dot.classList.remove('active'));
          let activeIndex = currentIndex % N;
          dots[activeIndex].classList.add('active');
        }
      }

      nextBtn.addEventListener('click', () => {
        if (isTransitioning) return;
        isTransitioning = true;
        currentIndex++;
        updateSlider(true);
      });

      prevBtn.addEventListener('click', () => {
        if (isTransitioning) return;
        isTransitioning = true;
        currentIndex--;
        updateSlider(true);
      });

      // Handle teleporting for infinite illusion
      sliderTrack.addEventListener('transitionend', () => {
        isTransitioning = false;
        // If we scrolled too far right, teleport back to center
        if (currentIndex >= N * 8) {
          currentIndex -= N * 3;
          updateSlider(false);
        }
        // If we scrolled too far left, teleport forward to center
        if (currentIndex <= N * 2) {
          currentIndex += N * 3;
          updateSlider(false);
        }
      });

      if (dots.length > 0) {
        dots.forEach((dot) => {
          dot.addEventListener('click', (e) => {
            if (isTransitioning) return;
            const targetIndex = parseInt(e.target.dataset.index);
            const currentMod = currentIndex % N;
            const diff = targetIndex - currentMod;
            currentIndex += diff;
            updateSlider(true);
          });
        });
      }
    }
  }
});

// Page Transition Manager
(function() {
  // Create transition elements and append to body
  const overlay = document.createElement('div');
  overlay.className = 'page-transition-overlay';
  
  const loadingBar = document.createElement('div');
  loadingBar.className = 'page-loading-bar';
  
  document.body.appendChild(overlay);
  document.body.appendChild(loadingBar);
  
  // Fade in the page content on load
  requestAnimationFrame(() => {
    overlay.classList.add('fade-out');
  });
  
  // Intercept links for smooth transition
  document.addEventListener('click', (e) => {
    const link = e.target.closest('a');
    if (!link) return;
    
    const href = link.getAttribute('href');
    
    // Filter out external URLs, hashes, javascript/tel/mailto/etc, targets like _blank
    if (!href || 
        href.startsWith('#') || 
        href.startsWith('javascript:') || 
        href.startsWith('mailto:') || 
        href.startsWith('tel:') ||
        link.getAttribute('target') === '_blank' ||
        link.hasAttribute('download') ||
        e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) {
      return;
    }
    
    // Check if it's the same origin
    try {
      const targetUrl = new URL(href, window.location.href);
      if (targetUrl.origin !== window.location.origin) {
        return;
      }
    } catch(err) {
      // If parsing fails, ignore
      return;
    }
    
    // Prevent default navigation to animate
    e.preventDefault();
    
    // Trigger loading bar
    loadingBar.classList.remove('complete');
    loadingBar.classList.add('active');
    
    // Fade in the overlay (fade out the page content)
    overlay.classList.remove('fade-out');
    
    // Navigate after animation completes
    setTimeout(() => {
      window.location.href = href;
    }, 300); // Matches CSS transition duration
  });
  
  // Reset state on pageshow (handles back/forward cache browser behavior)
  window.addEventListener('pageshow', (event) => {
    if (event.persisted) {
      overlay.classList.add('fade-out');
      loadingBar.classList.remove('active');
      loadingBar.classList.add('complete');
    }
  });
})();

function changeCardImage(swatchEl, imageUrl) {
  if (!imageUrl) return;
  const card = swatchEl.closest('.product-card');
  if (!card) return;
  const img = card.querySelector('.product-image');
  if (img) {
    img.src = imageUrl;
  }
  // Update active class
  const swatches = card.querySelectorAll('.swatch');
  swatches.forEach(sw => sw.classList.remove('active'));
  swatchEl.classList.add('active');
}

