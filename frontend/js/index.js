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

// Initialize particles when page loads
window.addEventListener("load", createParticles);
