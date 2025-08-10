// Create animated background particles
function createParticles() {
  const bgAnimation = document.getElementById("bg-animation");
  const particleCount = 12;

  for (let i = 0; i < particleCount; i++) {
    const particle = document.createElement("div");
    particle.className = "particle";

    // Random size between 2px and 6px
    const size = Math.random() * 4 + 2;
    particle.style.width = size + "px";
    particle.style.height = size + "px";

    // Random horizontal position
    particle.style.left = Math.random() * 100 + "%";

    // Random animation delay
    particle.style.animationDelay = Math.random() * 25 + "s";

    // Random animation duration between 20-30 seconds
    particle.style.animationDuration = Math.random() * 10 + 20 + "s";

    bgAnimation.appendChild(particle);
  }
}

// Example data placeholder — replace with API data
const clusterAnalyses = [
  {
    title: "Cluster 1: AI Model Developments",
    key_developments:
      "Companies launched new models with improved accuracy and efficiency, including breakthrough developments in large language models and computer vision systems.",
    emerging_trends:
      "Growth in multi-modal AI and foundation models, with increased focus on efficiency and reduced computational requirements.",
    differences_in_viewpoints:
      "Some experts debate ethical implications of rapid AI deployment, while others advocate for accelerated development to maintain competitive advantage.",
    strategic_moves:
      "Major acquisitions by leading AI firms, increased investment in AI infrastructure, and partnerships between tech giants and research institutions.",
  },
  {
    title: "Cluster 2: Cloud Infrastructure",
    key_developments:
      "Significant expansions in cloud computing capabilities with new data centers and improved edge computing solutions across multiple regions.",
    emerging_trends:
      "Shift towards hybrid cloud architectures and increased adoption of serverless computing paradigms in enterprise environments.",
    differences_in_viewpoints:
      "Debates around data sovereignty and privacy regulations versus the benefits of centralized cloud services for scalability.",
    strategic_moves:
      "Strategic partnerships between cloud providers and enterprise software companies, aggressive pricing strategies to capture market share.",
  },
  {
    title: "Cluster 3: Cybersecurity Advances",
    key_developments:
      "New zero-trust security frameworks implemented across major organizations, with AI-powered threat detection becoming mainstream.",
    emerging_trends:
      "Increased focus on quantum-resistant encryption methods and proactive security measures rather than reactive approaches.",
    differences_in_viewpoints:
      "Disagreement on the balance between security measures and user experience, particularly in consumer applications.",
    strategic_moves:
      "Acquisitions of specialized security startups by major tech companies, increased investment in security research and development.",
  },
];

const container = document.getElementById("cluster-slider");

function renderClusters() {
  // Clear loading spinner
  container.innerHTML = "";

  if (clusterAnalyses.length === 0) {
    container.innerHTML = `
            <div class="empty-state">
              <h3>No Analysis Available</h3>
              <p>Cluster analysis data is currently being processed. Please check back later.</p>
            </div>
          `;
    return;
  }

  clusterAnalyses.forEach((cluster, index) => {
    const card = document.createElement("div");
    card.classList.add("card");
    card.style.animationDelay = `${index * 0.1}s`;

    card.innerHTML = `
            <h2>${cluster.title}</h2>
            <div class="section key_developments">
              <h3>
                <span class="section-icon">📈</span>
                Key Developments
              </h3>
              <p>${cluster.key_developments}</p>
            </div>
            <div class="section emerging_trends">
              <h3>
                <span class="section-icon">🚀</span>
                Emerging Trends
              </h3>
              <p>${cluster.emerging_trends}</p>
            </div>
            <div class="section differences_in_viewpoints">
              <h3>
                <span class="section-icon">💭</span>
                Different Viewpoints
              </h3>
              <p>${cluster.differences_in_viewpoints}</p>
            </div>
            <div class="section strategic_moves">
              <h3>
                <span class="section-icon">⚡</span>
                Strategic Moves
              </h3>
              <p>${cluster.strategic_moves}</p>
            </div>
          `;
    container.appendChild(card);
  });
}

// Initialize everything when page loads
window.addEventListener("load", () => {
  createParticles();
  // Simulate loading delay
  setTimeout(renderClusters, 800);
});
