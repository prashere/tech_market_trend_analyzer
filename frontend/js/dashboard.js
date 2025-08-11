// API Configuration
const API_BASE = ""; 

// State management
let currentAnalysisData = null;
let isLoading = false;

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

// Show loading spinner with progress steps
function showLoading() {
  const container = document.getElementById("cluster-slider");
  container.innerHTML = `
          <div class="loading-container">
            <div class="loading-spinner">
              <div class="spinner"></div>
            </div>
            <div class="loading-text">Analyzing Market Trends</div>
            <div class="loading-subtitle">
              Our AI is processing the latest tech articles and generating comprehensive insights for you...
            </div>
            <div class="progress-steps" id="progress-steps">
              <div class="progress-step" id="step-1">
                <div class="step-icon">1</div>
                <div>
                  <div class="step-text">Loading article data</div>
                  <div class="step-detail">Reading latest tech articles and metadata</div>
                </div>
              </div>
              <div class="progress-step" id="step-2">
                <div class="step-icon">2</div>
                <div>
                  <div class="step-text">Clustering similar articles</div>
                  <div class="step-detail">Grouping related articles using AI embeddings</div>
                </div>
              </div>
              <div class="progress-step" id="step-3">
                <div class="step-icon">3</div>
                <div>
                  <div class="step-text">Generating AI analysis</div>
                  <div class="step-detail">Creating insights and trend analysis</div>
                </div>
              </div>
              <div class="progress-step" id="step-4">
                <div class="step-icon">4</div>
                <div>
                  <div class="step-text">Formatting results</div>
                  <div class="step-detail">Preparing your personalized dashboard</div>
                </div>
              </div>
            </div>
          </div>
        `;

  // Start progress animation
  startProgressAnimation();
}

// Start progress animation
function startProgressAnimation() {
  const steps = [
    {
      id: "step-1",
      messages: [
        "Reading article database...",
        "Loading RSS feed data...",
        "Indexing content...",
      ],
    },
    {
      id: "step-2",
      messages: [
        "Processing article embeddings...",
        "Running clustering algorithm...",
        "Identifying related articles...",
      ],
    },
    {
      id: "step-3",
      messages: [
        "Analyzing cluster 1...",
        "Analyzing cluster 2...",
        "Analyzing cluster 3...",
        "Generating insights...",
        "Creating trend analysis...",
      ],
    },
    {
      id: "step-4",
      messages: [
        "Formatting analysis data...",
        "Building dashboard...",
        "Almost ready!",
      ],
    },
  ];

  let currentStep = 0;
  let currentMessage = 0;

  function updateProgress() {
    if (currentStep >= steps.length) return;

    const step = steps[currentStep];
    const stepElement = document.getElementById(step.id);

    if (!stepElement) return;

    // Mark current step as active
    stepElement.classList.add("active");
    stepElement.classList.remove("completed");

    // Update detail text with current message
    const detailElement = stepElement.querySelector(".step-detail");
    if (detailElement && step.messages[currentMessage]) {
      detailElement.textContent = step.messages[currentMessage];
    }

    currentMessage++;

    // Move to next step when messages are exhausted
    if (currentMessage >= step.messages.length) {
      stepElement.classList.remove("active");
      stepElement.classList.add("completed");
      stepElement.querySelector(".step-icon").textContent = "✓";

      currentStep++;
      currentMessage = 0;
    }
  }

  // Update progress every 1.5 seconds
  const progressInterval = setInterval(updateProgress, 1500);

  // Store interval for cleanup
  window.currentProgressInterval = progressInterval;

  // Start immediately
  updateProgress();
}

// Stop progress animation
function stopProgressAnimation() {
  if (window.currentProgressInterval) {
    clearInterval(window.currentProgressInterval);
    window.currentProgressInterval = null;
  }
}

// Show error state
function showError(message) {
  const container = document.getElementById("cluster-slider");
  container.innerHTML = `
          <div class="empty-state">
            <h3>Error Loading Analysis</h3>
            <p>${message}</p>
            <button onclick="loadAnalysisData()" style="
              margin-top: 1rem;
              padding: 0.75rem 1.5rem;
              background: linear-gradient(135deg, #667eea, #764ba2);
              color: white;
              border: none;
              border-radius: 25px;
              cursor: pointer;
              font-weight: 500;
            ">Try Again</button>
          </div>
        `;
}

// Show empty state
function showEmptyState() {
  const container = document.getElementById("cluster-slider");
  container.innerHTML = `
          <div class="empty-state">
            <h3>No Analysis Available</h3>
            <p>No cluster analysis data is available. Please run the data pipeline first.</p>
            <button onclick="runPipeline()" style="
              margin-top: 1rem;
              padding: 0.75rem 1.5rem;
              background: linear-gradient(135deg, #667eea, #764ba2);
              color: white;
              border: none;
              border-radius: 25px;
              cursor: pointer;
              font-weight: 500;
            ">Run Data Pipeline</button>
          </div>
        `;
}

// Format analysis data for display
function formatAnalysisForDisplay(analysis) {
  // Handle both string arrays and plain strings
  const formatField = (field) => {
    if (Array.isArray(field)) {
      return field.map((item) => `• ${item}`).join("<br>");
    }
    return field || "No information available";
  };

  return {
    key_developments: formatField(analysis.key_developments),
    emerging_trends: formatField(analysis.emerging_trends),
    differences_in_viewpoints: formatField(analysis.differences_in_viewpoints),
    strategic_moves: formatField(analysis.strategic_moves),
  };
}

// Render clusters from API data
function renderClusters(analysisData) {
  const container = document.getElementById("cluster-slider");

  if (
    !analysisData ||
    !analysisData.clusters ||
    analysisData.clusters.length === 0
  ) {
    showEmptyState();
    return;
  }

  // Clear container
  container.innerHTML = "";

  analysisData.clusters.forEach((cluster, index) => {
    const card = document.createElement("div");
    card.classList.add("card");
    card.style.animationDelay = `${index * 0.1}s`;

    // Format the analysis data
    const formattedAnalysis = formatAnalysisForDisplay(cluster.analysis);

    // Create articles list for tooltip or expansion
    const articlesList = cluster.articles
      .map(
        (article) =>
          `<a href="${article.url}" target="_blank" style="color: #667eea; text-decoration: none;">
              ${article.title}
            </a>`
      )
      .join("<br><br>");

    card.innerHTML = `
            <h2>${
              cluster.analysis.title || `Cluster ${cluster.cluster_id + 1}`
            }</h2>
            
            <div class="section key_developments">
              <h3>
                <span class="section-icon">📈</span>
                Key Developments
              </h3>
              <p>${formattedAnalysis.key_developments}</p>
            </div>
            
            <div class="section emerging_trends">
              <h3>
                <span class="section-icon">🚀</span>
                Emerging Trends
              </h3>
              <p>${formattedAnalysis.emerging_trends}</p>
            </div>
            
            <div class="section differences_in_viewpoints">
              <h3>
                <span class="section-icon">💭</span>
                Different Viewpoints
              </h3>
              <p>${formattedAnalysis.differences_in_viewpoints}</p>
            </div>
            
            <div class="section strategic_moves">
              <h3>
                <span class="section-icon">⚡</span>
                Strategic Moves
              </h3>
              <p>${formattedAnalysis.strategic_moves}</p>
            </div>

            <div class="section" style="background: linear-gradient(135deg, #f8f9ff 0%, #e3f2fd 100%); margin-top: 1rem;">
              <h3>
                <span class="section-icon">📰</span>
                Source Articles (${cluster.article_count})
              </h3>
              <div style="max-height: 150px; overflow-y: auto; font-size: 0.85rem; line-height: 1.4;">
                ${articlesList}
              </div>
            </div>
          `;

    container.appendChild(card);
  });

  // Add refresh button
  const refreshButton = document.createElement("div");
  refreshButton.style.cssText = `
          position: fixed;
          top: 20px;
          right: 20px;
          z-index: 1000;
        `;
  refreshButton.innerHTML = `
          <button onclick="refreshAnalysis()" style="
            padding: 0.75rem 1rem;
            background: linear-gradient(135deg, #f093fb, #f5576c);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-weight: 500;
            box-shadow: 0 4px 15px rgba(240, 147, 251, 0.3);
          ">🔄 Refresh Analysis</button>
        `;
  document.body.appendChild(refreshButton);
}

// Load analysis data from API
async function loadAnalysisData() {
  if (isLoading) return;

  isLoading = true;
  showLoading();

  try {
    console.log("Fetching analysis data...");
    const response = await fetch(`${API_BASE}/api/analysis`);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    console.log("Analysis data received:", data);

    // Stop progress animation
    stopProgressAnimation();

    if (data.success) {
      currentAnalysisData = data;
      renderClusters(data);
    } else {
      showError(data.message || "Failed to load analysis data");
    }
  } catch (error) {
    console.error("Error loading analysis:", error);
    stopProgressAnimation();
    showError(`Failed to load analysis: ${error.message}`);
  } finally {
    isLoading = false;
  }
}

// Refresh analysis data
async function refreshAnalysis() {
  try {
    const response = await fetch(`${API_BASE}/api/analysis/refresh`, {
      method: "POST",
    });

    if (response.ok) {
      // Wait a moment then reload data
      setTimeout(() => {
        loadAnalysisData();
      }, 2000);
    }
  } catch (error) {
    console.error("Error refreshing analysis:", error);
  }
}

// Run data pipeline
async function runPipeline() {
  try {
    showLoading();

    const response = await fetch(`${API_BASE}/api/pipeline/run`, {
      method: "POST",
    });

    if (response.ok) {
      // Poll for completion
      checkPipelineStatus();
    } else {
      stopProgressAnimation();
      showError("Failed to start data pipeline");
    }
  } catch (error) {
    console.error("Error running pipeline:", error);
    stopProgressAnimation();
    showError(`Failed to run pipeline: ${error.message}`);
  }
}

// Check pipeline status and wait for completion
async function checkPipelineStatus() {
  try {
    const response = await fetch(`${API_BASE}/api/pipeline/status`);
    const status = await response.json();

    if (status.is_running) {
      // Still running, check again in 5 seconds
      setTimeout(checkPipelineStatus, 5000);
    } else if (status.status === "completed") {
      // Pipeline completed, load analysis
      setTimeout(() => {
        loadAnalysisData();
      }, 2000);
    } else if (status.status === "error") {
      stopProgressAnimation();
      showError(`Pipeline failed: ${status.message}`);
    }
  } catch (error) {
    console.error("Error checking pipeline status:", error);
    stopProgressAnimation();
  }
}

// Initialize everything when page loads
window.addEventListener("load", () => {
  createParticles();

  // Start loading analysis data
  setTimeout(() => {
    loadAnalysisData();
  }, 500);
});
