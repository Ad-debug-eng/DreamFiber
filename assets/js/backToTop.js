/**
 * Back to Top with Scroll Progress Circle
 * Handles zoom: 0.9, responsive viewports, and auto-injection if markup is missing.
 */
(function () {
  'use strict';

  function initBackToTop() {
    let wrap = document.querySelector('.progress-wrap');
    if (!wrap) {
      wrap = document.createElement('div');
      wrap.className = 'progress-wrap';
      wrap.innerHTML = '<svg class="progress-circle svg-content" width="100%" height="100%" viewBox="-1 -1 102 102"><path d="M50,1 a49,49 0 0,1 0,98 a49,49 0 0,1 0,-98"/></svg>';
      document.body.appendChild(wrap);
    }

    const path = wrap.querySelector('path');
    if (!path) return;

    const pathLength = path.getTotalLength();
    path.style.transition = path.style.WebkitTransition = 'none';
    path.style.strokeDasharray = pathLength + ' ' + pathLength;
    path.style.strokeDashoffset = pathLength;
    path.getBoundingClientRect();
    path.style.transition = path.style.WebkitTransition = 'stroke-dashoffset 10ms linear';

    function updateProgress() {
      const scrollY = window.pageYOffset || document.documentElement.scrollTop || 0;
      const maxScroll = document.documentElement.scrollHeight - window.innerHeight;

      let progress = 0;
      if (maxScroll > 0) {
        progress = scrollY / maxScroll;
      }

      if (progress > 1 || (maxScroll > 0 && scrollY >= maxScroll - 5)) {
        progress = 1;
      }
      if (progress < 0) {
        progress = 0;
      }

      const offset = pathLength * (1 - progress);
      path.style.strokeDashoffset = offset;

      if (scrollY > 50) {
        wrap.classList.add('active-progress');
      } else {
        wrap.classList.remove('active-progress');
      }
    }

    window.addEventListener('scroll', updateProgress, { passive: true });
    window.addEventListener('resize', updateProgress);
    updateProgress();

    wrap.addEventListener('click', function (e) {
      e.preventDefault();
      try {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      } catch (err) {}
      return false;
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initBackToTop);
  } else {
    initBackToTop();
  }
})();
