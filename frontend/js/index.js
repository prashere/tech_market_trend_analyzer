// API Configuration
const API_BASE = "";

function createParticles() {
  const bgAnimation = document.getElementById("bg-animation");
  const particleCount = 15;

  for (let i = 0; i < particleCount; i++) {
    const particle = document.createElement("div");
    particle.className = "particle";

    const size = Math.random() * 6 + 2;
    particle.style.width = size + "px";
    particle.style.height = size + "px";

    particle.style.left = Math.random() * 100 + "%";

    particle.style.animationDelay = Math.random() * 20 + "s";

    particle.style.animationDuration = Math.random() * 10 + 15 + "s";

    bgAnimation.appendChild(particle);
  }
}

// Check API health and system status
async function checkSystemStatus() {
  try {
    const systemResponse = await fetch(`${API_BASE}/api/system/info`);
    const systemInfo = await systemResponse.json();
    updateButtonStatus(systemInfo);
    updateStatusIndicator(systemInfo);
  } catch (error) {
    console.warn("API not available:", error);
    updateButtonStatus(null);
    updateStatusIndicator(null);
  }
}

// Update the main CTA button based on system status
function updateButtonStatus(systemInfo) {
  const button = document.querySelector(".cta-button");
  if (!button) return;

  if (!systemInfo) {
    // API offline - keep default
    return;
  }

  if (
    systemInfo.system_status === "healthy" &&
    systemInfo.components.analysis_cache
  ) {
    // Analysis available
    button.innerHTML = `
      View Market Analysis
      <span class="arrow-icon">→</span>
    `;
  } else {
    // First time or needs setup
    button.innerHTML = `
      Start Market Analysis
      <span class="arrow-icon">→</span>
    `;
  }
}

// Add system status indicator
function addSystemStatusIndicator() {
  const statusIndicator = document.createElement("div");
  statusIndicator.id = "system-status";
  statusIndicator.style.cssText = `
    position: fixed;
    bottom: 20px;
    right: 20px;
    padding: 0.5rem 1rem;
    background: rgba(255, 255, 255, 0.9);
    border-radius: 25px;
    font-size: 0.8rem;
    color: #666;
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    z-index: 1000;
    opacity: 0;
    transition: opacity 0.3s ease;
  `;

  statusIndicator.innerHTML = `
    <span id="status-dot" style="
      display: inline-block;
      width: 8px;
      height: 8px;
      background: #ccc;
      border-radius: 50%;
      margin-right: 0.5rem;
    "></span>
    <span id="status-text">Checking system...</span>
  `;

  document.body.appendChild(statusIndicator);
  return statusIndicator;
}

// Update status indicator
function updateStatusIndicator(systemInfo) {
  const dot = document.getElementById("status-dot");
  const text = document.getElementById("status-text");
  const indicator = document.getElementById("system-status");

  if (!dot || !text || !indicator) return;

  if (!systemInfo) {
    dot.style.background = "#ff6b6b";
    text.textContent = "API Offline";
  } else if (systemInfo.system_status === "healthy") {
    dot.style.background = "#51cf66";
    text.textContent = "System Ready";
  } else {
    dot.style.background = "#ffd43b";
    text.textContent = "Setup Required";
  }

  // Show indicator briefly
  indicator.style.opacity = "1";
  setTimeout(() => {
    indicator.style.opacity = "0.7";
  }, 2000);

  setTimeout(() => {
    indicator.style.opacity = "0";
  }, 8000);
}

// Initialize particles and system check when page loads
window.addEventListener("load", () => {
  createParticles();
  addSystemStatusIndicator();

  // Check system status after a brief delay
  setTimeout(checkSystemStatus, 1000);
});
