// River's Toy Room — Fun, Mobile-First Educational Marvel Toy Gallery
// Easy to extend: simply add new objects to the episodes array below!

const episodes = [
  {
    id: 1,
    title: "Web of Teamwork",
    description: "Spider-Man and his heroic pals work together to rescue their friends from a tricky trap. Learn why teamwork makes every mission possible!",
    hero: "Spider-Man",
    skills: ["Teamwork", "Problem Solving"],
    thumbnail: "images/spidey-team.jpg",
    videoId: "jTnz3ktqkVo",
    duration: "5:14"
  },
  {
    id: 2,
    title: "Iron Man's Invention Lab",
    description: "Tony Stark's armor inspires kids to invent wild gadgets! Explore creativity and the joy of building anything you can imagine.",
    hero: "Iron Man",
    skills: ["Creativity", "Critical Thinking"],
    thumbnail: "images/ironman-invent.jpg",
    videoId: "rbGvDcRQeZ0",
    duration: "7:22"
  },
  {
    id: 3,
    title: "Hulk Learns Calm Power",
    description: "The big green guy teaches that strong feelings are okay — it's how we use them that matters. A story about emotional superpowers.",
    hero: "Hulk",
    skills: ["Empathy", "Perseverance"],
    thumbnail: "images/hulk-calm.jpg",
    videoId: "CcxSEqHR-jU",
    duration: "6:45"
  },
  {
    id: 4,
    title: "Captain America's Shield Circle",
    description: "Cap shows how passing the shield fairly builds trust and friendship. Great lessons in leadership and sharing with your whole team.",
    hero: "Captain America",
    skills: ["Leadership", "Teamwork"],
    thumbnail: "images/cap-shield.jpg",
    videoId: "o98-4q5DPY0",
    duration: "4:58"
  },
  {
    id: 5,
    title: "Black Panther's Wakanda Wisdom",
    description: "T'Challa explores clever inventions from Wakanda. Discover problem-solving through science, nature, and bold ideas.",
    hero: "Black Panther",
    skills: ["Problem Solving", "Creativity"],
    thumbnail: "images/blackpanther-wakanda.jpg",
    videoId: "9OWAvCp6ie4",
    duration: "8:10"
  },
  {
    id: 6,
    title: "Doctor Strange's Magic of Mistakes",
    description: "Even the Sorcerer Supreme gets spells wrong sometimes! Learn that mistakes are just portals to better learning and new ideas.",
    hero: "Doctor Strange",
    skills: ["Perseverance", "Critical Thinking"],
    thumbnail: "images/strange-magic.jpg",
    videoId: "J9EpClrYA5c",
    duration: "5:33"
  },
  {
    id: 7,
    title: "Guardians' Galaxy Groove",
    description: "The ragtag team of space heroes teach that every voice matters in a crew. A cosmic masterclass in communication and joyful teamwork.",
    hero: "Guardians of the Galaxy",
    skills: ["Communication", "Teamwork"],
    thumbnail: "images/guardians-groove.jpg",
    videoId: "z29loHu-lGo",
    duration: "6:07"
  },
  {
    id: 8,
    title: "Avengers Assemble: The Big Plan",
    description: "When the world needs heroes, they plan together. See how listening and combining powers creates unstoppable teamwork and friendship.",
    hero: "The Avengers",
    skills: ["Leadership", "Problem Solving"],
    thumbnail: "images/avengers-plan.jpg",
    videoId: "lBdbttgfmRw",
    duration: "9:15"
  }
];

// All unique skills for filters (auto-generated from data)
let allSkills = [...new Set(episodes.flatMap(ep => ep.skills))].sort();

// Robust skill class name generator (handles spaces, punctuation, case)
function getSkillClass(skill) {
  return 'skill-' + skill.toLowerCase().replace(/[^a-z0-9]+/g, '-');
}

// State
let activeFilters = new Set();
let displayedCount = 6; // Start with 6 for nice infinite feel
let filteredEpisodes = [...episodes];
let currentVideoEpisode = null;

// (Tailwind is loaded via CDN in index.html — no runtime config needed)

// Render skill filter pills
function renderSkillFilters() {
  const container = document.getElementById('skill-filters');
  container.innerHTML = '';

  // "All" pill
  const allPill = document.createElement('div');
  allPill.className = `filter-pill text-sm ${activeFilters.size === 0 ? 'active' : ''}`;
  allPill.textContent = 'All Adventures';
  allPill.onclick = () => {
    activeFilters.clear();
    applyFilters();
    renderSkillFilters();
  };
  container.appendChild(allPill);

  // Skill pills
  allSkills.forEach(skill => {
    const pill = document.createElement('div');
    const isActive = activeFilters.has(skill);
    pill.className = `filter-pill text-sm ${isActive ? 'active' : ''}`;
    pill.textContent = skill;

    pill.onclick = () => {
      if (activeFilters.has(skill)) {
        activeFilters.delete(skill);
      } else {
        activeFilters.add(skill);
      }
      applyFilters();
      renderSkillFilters();
    };
    container.appendChild(pill);
  });
}

// Apply current filters
function applyFilters() {
  if (activeFilters.size === 0) {
    filteredEpisodes = [...episodes];
  } else {
    filteredEpisodes = episodes.filter(ep =>
      ep.skills.some(skill => activeFilters.has(skill))
    );
  }

  // Reset infinite scroll when filters change
  displayedCount = Math.min(6, filteredEpisodes.length);
  renderGallery();
  updateEpisodeCount();
}

// Update the episode counter
function updateEpisodeCount() {
  const el = document.getElementById('episode-count');
  if (!el) return;
  const total = filteredEpisodes.length;
  const showing = Math.min(displayedCount, total);
  el.innerHTML = `<span class="font-bold">${showing}</span> / ${total} adventures`;
}

// Create a single episode card element
function createEpisodeCard(episode) {
  const card = document.createElement('div');
  card.className = 'episode-card group';
  card.setAttribute('data-id', episode.id);

  const skillBadges = episode.skills.map(skill => {
    return `<span class="skill-badge ${getSkillClass(skill)}">${skill}</span>`;
  }).join('');

  card.innerHTML = `
    <div class="thumb-wrap aspect-video relative">
      <img 
        src="${episode.thumbnail}" 
        alt="${episode.title} — ${episode.hero} educational episode thumbnail"
        loading="lazy"
      >
      <div class="play-overlay">
        <div class="play-badge">
          <span>▶</span>
          <span>WATCH</span>
        </div>
      </div>
    </div>

    <div class="p-5">
      <div class="flex items-start justify-between gap-3 mb-2">
        <h4 class="font-black text-[21px] leading-[1.05] tracking-[-0.4px] pr-1">${episode.title}</h4>
      </div>

      <p class="text-white/70 text-[13.5px] leading-snug line-clamp-3 mb-4">${episode.description}</p>

      <div class="flex items-center justify-between">
        <div class="flex flex-wrap gap-1.5">
          ${skillBadges}
        </div>
        <div class="text-right">
          <div class="font-mono text-[10px] text-white/50 tracking-widest">${episode.duration}</div>
          <div class="text-[11px] text-white/40 font-medium -mt-px">${episode.hero}</div>
        </div>
      </div>
    </div>
  `;

  // Click to open video
  card.addEventListener('click', () => openVideoModal(episode));

  // Keyboard support
  card.setAttribute('tabindex', '0');
  card.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      openVideoModal(episode);
    }
  });

  return card;
}

// Render (or re-render) the visible portion of the gallery
function renderGallery(append = false) {
  const gallery = document.getElementById('gallery');
  if (!gallery) return;

  if (!append) {
    gallery.innerHTML = '';
  }

  const toShow = filteredEpisodes.slice(0, displayedCount);

  toShow.forEach((ep, index) => {
    // Skip already rendered when appending
    if (append && gallery.querySelector(`[data-id="${ep.id}"]`)) return;

    const card = createEpisodeCard(ep);
    gallery.appendChild(card);
  });

  // End of results state
  updateScrollStatus();
  updateEpisodeCount();
}

// Update the infinite scroll helper text / state
function updateScrollStatus() {
  const statusEl = document.getElementById('scroll-status');
  const textEl = document.getElementById('scroll-text');
  if (!statusEl || !textEl) return;

  if (displayedCount >= filteredEpisodes.length) {
    statusEl.innerHTML = `
      <div class="px-5 py-2 text-xs rounded-3xl bg-white/5 border border-white/10 text-white/60">
        🌟 That's all for now! New episodes drop every week.
      </div>
    `;
  } else {
    statusEl.innerHTML = `
      <div class="flex items-center gap-x-2 text-white/50 text-sm">
        <div class="w-1.5 h-1.5 bg-white/40 rounded-full animate-pulse"></div>
        <span id="scroll-text">Scroll for more adventures...</span>
      </div>
    `;
  }
}

// Infinite scroll handler
let infiniteScrollObserver = null;

function setupInfiniteScroll() {
  const sentinel = document.getElementById('scroll-status');
  if (!sentinel) return;

  // Clean up previous observer when re-initializing after filters
  if (infiniteScrollObserver) {
    infiniteScrollObserver.disconnect();
  }

  infiniteScrollObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && displayedCount < filteredEpisodes.length) {
        displayedCount = Math.min(displayedCount + 4, filteredEpisodes.length);
        renderGallery(true);
      }
    });
  }, {
    rootMargin: '200px 0px',
    threshold: 0.1
  });

  infiniteScrollObserver.observe(sentinel);

  // Click fallback (guarded so we don't attach multiple listeners on filter changes)
  if (!sentinel.dataset.loadMoreAttached) {
    sentinel.dataset.loadMoreAttached = 'true';
    sentinel.addEventListener('click', () => {
      if (displayedCount < filteredEpisodes.length) {
        displayedCount = Math.min(displayedCount + 4, filteredEpisodes.length);
        renderGallery(true);
      }
    });
  }
}

// Open the beautiful video modal
function openVideoModal(episode) {
  const modal = document.getElementById('video-modal');
  const iframe = document.getElementById('video-iframe');
  const titleEl = document.getElementById('modal-title');
  const heroEl = document.getElementById('modal-hero');
  const descEl = document.getElementById('modal-desc');
  const durationEl = document.getElementById('modal-duration');
  const skillsContainer = document.getElementById('modal-skills');

  currentVideoEpisode = episode;

  // Populate content
  titleEl.textContent = episode.title;
  heroEl.textContent = episode.hero.toUpperCase();
  descEl.textContent = episode.description;
  durationEl.innerHTML = `<span class="font-semibold">${episode.duration}</span>`;

  // Skills badges in modal
  skillsContainer.innerHTML = episode.skills.map(skill => {
    return `<span class="skill-badge ${getSkillClass(skill)} text-xs px-3 py-px">${skill}</span>`;
  }).join('');

  // YouTube embed — autoplay muted to comply with modern browser policies
  iframe.src = `https://www.youtube.com/embed/${episode.videoId}?autoplay=1&mute=1&rel=0&modestbranding=1`;

  // Show modal
  modal.classList.remove('hidden');
  modal.classList.add('flex');

  // Trap focus roughly + escape support
  document.addEventListener('keydown', handleModalEsc, { once: true });
}

// Close video modal + cleanup iframe (stops video)
function closeVideoModal() {
  const modal = document.getElementById('video-modal');
  const iframe = document.getElementById('video-iframe');

  iframe.src = ''; // stop playback
  modal.classList.remove('flex');
  modal.classList.add('hidden');
  currentVideoEpisode = null;
}

function handleModalEsc(e) {
  if (e.key === 'Escape') {
    closeVideoModal();
  }
}

// Clear all filters
function clearFilters() {
  activeFilters.clear();
  applyFilters();
  renderSkillFilters();
}

// Scroll to gallery nicely
function scrollToGallery() {
  const el = document.getElementById('episodes');
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
}

// ========== CONTRIBUTE / ADD EPISODE FEATURE ==========

function showContributeModal() {
  const modal = document.getElementById('contribute-modal');
  const snippetBox = document.getElementById('snippet-output');
  snippetBox.classList.add('hidden');

  // Reset simple defaults each time (or keep previous)
  modal.classList.remove('hidden');
  modal.classList.add('flex');
}

function closeContributeModal() {
  const modal = document.getElementById('contribute-modal');
  modal.classList.remove('flex');
  modal.classList.add('hidden');
}

function generateEpisodeSnippet() {
  const title = document.getElementById('c-title').value.trim() || "Untitled Adventure";
  const hero = document.getElementById('c-hero').value.trim() || "Marvel Hero";
  const desc = document.getElementById('c-desc').value.trim() || "An amazing learning journey with toys.";
  const videoId = document.getElementById('c-video').value.trim() || "jTnz3ktqkVo";
  const duration = document.getElementById('c-duration').value.trim() || "4:20";
  const skillsRaw = document.getElementById('c-skills').value.trim();

  const skills = skillsRaw
    ? skillsRaw.split(',').map(s => s.trim()).filter(Boolean)
    : ["Teamwork"];

  // Generate a new ID (max + 1)
  const newId = Math.max(0, ...episodes.map(e => e.id)) + 1;

  // Create the object (note: thumbnail will be placeholder until user adds real image)
  const newEpisode = {
    id: newId,
    title,
    description: desc,
    hero,
    skills,
    thumbnail: "images/avengers-plan.jpg", // ← Replace with a real custom thumbnail for this episode
    videoId,
    duration
  };

  const json = JSON.stringify(newEpisode, null, 2);

  // Show output
  const output = document.getElementById('snippet-output');
  const codeEl = document.getElementById('snippet-code');

  codeEl.textContent = `{
  // Add this inside the episodes array in app.js
  // IMPORTANT: Replace the thumbnail with a custom image in /images
${json}
}`;

  output.classList.remove('hidden');

  // Also auto-copy for convenience
  navigator.clipboard?.writeText(json).catch(() => {});
}

function copySnippet() {
  const codeEl = document.getElementById('snippet-code');
  const text = codeEl.textContent.replace(/\{\s*\/\/ Add this[\s\S]*?\n/, '').trim();

  navigator.clipboard.writeText(text).then(() => {
    const btns = document.querySelectorAll('#contribute-modal button');
    const origText = [];
    btns.forEach(b => { origText.push(b.textContent); b.textContent = 'COPIED!'; });

    setTimeout(() => {
      btns.forEach((b, i) => b.textContent = origText[i] || 'COPY JSON');
    }, 1400);
  }).catch(() => {
    // Fallback select
    const range = document.createRange();
    range.selectNode(codeEl);
    window.getSelection().removeAllRanges();
    window.getSelection().addRange(range);
    alert('Select the code and press Ctrl/Cmd + C to copy');
  });
}

// Mobile menu (simple)
function setupMobileMenu() {
  const btn = document.getElementById('mobile-menu-btn');
  if (!btn) return;

  btn.addEventListener('click', () => {
    const nav = document.createElement('div');
    nav.className = 'fixed inset-0 z-[90] bg-black/95 md:hidden flex flex-col p-6';
    nav.innerHTML = `
      <div class="flex justify-between items-center mb-8">
        <div class="flex items-center gap-x-3">
          <div class="w-9 h-9 rounded-2xl bg-gradient-to-br from-[#FF2D55] to-[#00F5FF] flex items-center justify-center text-2xl">🦸</div>
          <span class="font-black text-2xl">River's Toy Room</span>
        </div>
        <button class="text-4xl text-white/70">×</button>
      </div>
      <div class="flex flex-col text-2xl gap-y-5 font-semibold">
        <a href="#episodes" class="py-2">Episodes</a>
        <a href="#skills" class="py-2">Skills</a>
        <a href="#about" class="py-2">About the Room</a>
        <button onclick="showContributeModal(); this.closest('.fixed').remove()" class="mt-4 text-left text-[#00F5FF]">✨ Add New Episode</button>
      </div>
      <div class="mt-auto text-xs text-white/40">Tap anywhere outside to close</div>
    `;

    document.body.appendChild(nav);

    const close = () => nav.remove();
    nav.querySelector('button').onclick = close;
    nav.addEventListener('click', (e) => {
      if (e.target === nav) close();
    });

    // Close on link click
    nav.querySelectorAll('a').forEach(a => a.addEventListener('click', close));
  });
}

// Keyboard shortcuts (fun)
function setupKeyboardShortcuts() {
  document.addEventListener('keydown', (e) => {
    // Press "?" to focus filter bar
    if (e.key === '?' && document.activeElement.tagName === 'BODY') {
      e.preventDefault();
      const filters = document.getElementById('skill-filters');
      filters?.scrollIntoView({ behavior: 'smooth' });
    }

    // Press "/" to open contribute
    if (e.key === '/' && document.activeElement.tagName === 'BODY') {
      e.preventDefault();
      showContributeModal();
    }
  });

  // Easter egg: type "marvel" anywhere for confetti burst (ignore when typing in forms)
  let typed = '';
  document.addEventListener('keypress', (e) => {
    const active = document.activeElement;
    if (active && (active.tagName === 'INPUT' || active.tagName === 'TEXTAREA' || active.isContentEditable)) {
      return;
    }
    typed += e.key.toLowerCase();
    if (typed.length > 6) typed = typed.slice(-6);
    if (typed.includes('marvel')) {
      burstConfetti();
      typed = '';
    }
  });
}

// Simple canvas confetti
function burstConfetti() {
  const colors = ['#FF2D55', '#FFD700', '#00F5FF', '#7B2CBF', '#00FF85'];
  const canvas = document.createElement('canvas');
  canvas.style.position = 'fixed';
  canvas.style.inset = '0';
  canvas.style.zIndex = '99999';
  canvas.style.pointerEvents = 'none';
  document.body.appendChild(canvas);

  const ctx = canvas.getContext('2d');
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  const particles = Array.from({ length: 160 }, () => ({
    x: Math.random() * canvas.width,
    y: Math.random() * -canvas.height * 0.6,
    r: Math.random() * 6 + 4,
    vx: (Math.random() - 0.5) * 4,
    vy: Math.random() * 4 + 2,
    color: colors[Math.floor(Math.random() * colors.length)]
  }));

  let frame = 0;
  const draw = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach(p => {
      p.x += p.vx;
      p.y += p.vy;
      p.vy += 0.06; // gravity
      ctx.fillStyle = p.color;
      ctx.fillRect(p.x, p.y, p.r, p.r * 0.6);
    });
    frame++;
    if (frame < 120) {
      requestAnimationFrame(draw);
    } else {
      canvas.remove();
    }
  };
  draw();
}

// Main bootstrap
function init() {
  // Initial render
  filteredEpisodes = [...episodes];
  renderSkillFilters();
  renderGallery();
  updateEpisodeCount();

  // Infinite scroll magic
  setupInfiniteScroll();

  // Nice interactions
  setupMobileMenu();
  setupKeyboardShortcuts();

  // Random fun tip in console
  console.log('%c[River\'s Toy Room] Pro tip: Type "marvel" anywhere for confetti. Press "?" on the filters. Press "/" to add episodes.', 'color:#555');

  // Optional: show a welcome toast on first load (desktop only)
  if (window.innerWidth > 900) {
    setTimeout(() => {
      const status = document.getElementById('scroll-status');
      if (status && displayedCount < filteredEpisodes.length) {
        // subtle nudge
      }
    }, 4200);
  }

  // Make sure initial count is correct
  setTimeout(updateEpisodeCount, 200);
}

// Kick everything off
window.addEventListener('DOMContentLoaded', init);

// Expose helpful globals for easy future customization (in console or scripts)
window.RIVERS_TOY_ROOM = {
  episodes,
  addEpisode(newEp) {
    episodes.push(newEp);
    // Rebuild derived data
    allSkills = [...new Set(episodes.flatMap(ep => ep.skills))].sort();
    filteredEpisodes = [...episodes];
    displayedCount = Math.min(displayedCount, filteredEpisodes.length);
    // Refresh UI without losing filter/scroll state
    renderSkillFilters();
    renderGallery();
    updateEpisodeCount();
  },
  clearFilters: () => {
    activeFilters.clear();
    applyFilters();
    renderSkillFilters();
  }
};
