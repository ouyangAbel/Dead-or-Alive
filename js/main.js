
// Nav scroll effect
const nav = document.getElementById('main-nav');
window.addEventListener('scroll', () => {
  nav.classList.toggle('scrolled', window.scrollY > 50);
});

// Mobile nav toggle
const navToggle = document.getElementById('nav-toggle');
const navLinks = document.getElementById('nav-links');
if (navToggle) {
  navToggle.addEventListener('click', () => navLinks.classList.toggle('open'));
}
document.querySelectorAll('.nav-links a').forEach(l => {
  l.addEventListener('click', () => navLinks.classList.remove('open'));
});

// Reveal on scroll
document.querySelectorAll('.reveal').forEach(el => {
  new IntersectionObserver((entries, o) => {
    entries.forEach((e, i) => {
      if (e.isIntersecting) {
        setTimeout(() => e.target.classList.add('visible'), i * 80);
        o.unobserve(e.target);
      }
    });
  }, { threshold: .1, rootMargin: '0px 0px -50px 0px' }).observe(el);
});

// Combo tab switching
document.querySelectorAll('.combo-char-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const t = btn.dataset.target;
    document.querySelectorAll('.combo-char-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    document.querySelectorAll('.combo-panel').forEach(p => {
      p.classList.remove('active');
      if (p.id === `panel-${t}`) p.classList.add('active');
    });
  });
});

// Particles
const pc = document.getElementById('particles');
function cp() {
  if (!pc) return;
  const p = document.createElement('div');
  p.classList.add('particle');
  p.style.left = Math.random() * 100 + '%';
  p.style.animationDuration = (Math.random() * 6 + 4) + 's';
  p.style.animationDelay = Math.random() * 3 + 's';
  p.style.width = (Math.random() * 3 + 1) + 'px';
  p.style.height = p.style.width;
  const c = ['var(--accent-red)', 'var(--accent-cyan)', 'var(--accent-pink)', 'var(--accent-gold)'];
  p.style.background = c[Math.floor(Math.random() * c.length)];
  pc.appendChild(p);
  setTimeout(() => p.remove(), 10000);
}
setInterval(cp, 300);

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', function (e) {
    e.preventDefault();
    const t = document.querySelector(this.getAttribute('href'));
    if (t) t.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
});

// Active nav highlight for sections
const secs = document.querySelectorAll('section[id]');
window.addEventListener('scroll', () => {
  let cur = '';
  secs.forEach(s => {
    if (window.scrollY >= s.offsetTop - 100) cur = s.getAttribute('id');
  });
  document.querySelectorAll('.nav-links a').forEach(l => {
    l.style.color = '';
    if (l.getAttribute('href') === `#${cur}`) l.style.color = 'var(--accent-red)';
  });
});
