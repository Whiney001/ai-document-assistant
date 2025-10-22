<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Meta -->
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Winnie Kenneth — AI & Software Developer Portfolio</title>
  <meta name="description" content="Winnie Kenneth — Final-year Computer Science student. AI, Data & Software projects with live demos and real-world experience." />

  <!-- Fonts & Icons -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"/>

  <!-- AOS (Animate on Scroll) -->
  <link rel="stylesheet" href="https://unpkg.com/aos@2.3.4/dist/aos.css"/>

  <!-- Styles -->
  <style>
    :root{
      --bg:#0b0f16;
      --panel:#111625;
      --ink:#e9eef5;
      --muted:#9aa3b2;
      --accent:#ff6b9d;
      --accent-2:#e5527e;
      --edge:#1b2133;
      --shadow:0 10px 30px rgba(0,0,0,.35);
    }
    *{box-sizing:border-box}
    html,body{margin:0;padding:0;background:var(--bg);color:var(--ink);font-family:'Inter',sans-serif;scroll-behavior:smooth}
    a{text-decoration:none;color:inherit}

    /* Header / Nav */
    .nav{
      position:sticky;top:0;z-index:40;
      backdrop-filter: blur(6px);
      background:linear-gradient(180deg,rgba(11,15,22,.85),rgba(11,15,22,.3));
      border-bottom:1px solid var(--edge);
    }
    .nav-inner{max-width:1100px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;padding:0.9rem 1rem}
    .brand{font-weight:900;letter-spacing:.3px}
    .brand span{background: linear-gradient(135deg,var(--accent),var(--accent-2));-webkit-background-clip:text;background-clip:text;color:transparent}
    .nav a.link{color:var(--muted);margin-left:1rem;font-weight:600}
    .nav a.link:hover{color:var(--ink)}

    /* Hero */
    .hero{max-width:1100px;margin:0 auto;padding:4.5rem 1rem 3rem 1rem;display:grid;grid-template-columns:1.1fr .9fr;gap:2rem;align-items:center}
    .hero h1{font-size:2.6rem;margin:0 0 .5rem 0}
    .type{font-weight:900;background: linear-gradient(135deg,var(--accent),var(--accent-2));-webkit-background-clip:text;background-clip:text;color:transparent}
    .tag{color:var(--muted);margin:.35rem 0 1rem 0}
    .cta-row{display:flex;gap:.8rem;flex-wrap:wrap;margin-top:1rem}
    .btn{display:inline-flex;align-items:center;gap:.5rem;padding:.8rem 1.2rem;border-radius:10px;font-weight:700;transition:transform .15s ease, box-shadow .2s ease}
    .btn i{font-size:.95rem}
    .btn.primary{background:linear-gradient(135deg,var(--accent),var(--accent-2));color:#fff;box-shadow:0 6px 18px rgba(229,82,126,.35)}
    .btn.primary:hover{transform:translateY(-2px);box-shadow:0 10px 24px rgba(229,82,126,.45)}
    .btn.ghost{border:2px solid var(--accent);color:var(--accent);background:transparent}
    .btn.ghost:hover{transform:translateY(-2px);background:rgba(255,107,157,.08)}
    .hero-card{
      background: radial-gradient(1200px 400px at -10% -10%, rgba(255,107,157,.06), transparent 40%),
                  radial-gradient(900px 400px at 110% 110%, rgba(99,102,241,.08), transparent 40%),
                  var(--panel);
      border:1px solid var(--edge);border-radius:16px;padding:1.5rem;box-shadow:var(--shadow)
    }
    .hero-card ul{margin:.6rem 0 0 1.1rem;color:var(--muted)}
    .hero-card h3{margin:0 0 .6rem 0}

    /* Sections */
    section{max-width:1100px;margin:0 auto;padding:2.5rem 1rem}
    .section-title{text-align:center;margin:0 0 1.2rem 0;font-size:1.8rem}
    .section-sub{color:var(--muted);text-align:center;margin:-.6rem 0 2rem}

    /* Projects */
    .grid{display:grid;grid-template-columns:repeat(12,1fr);gap:1.1rem}
    .card{
      grid-column:span 12;background:var(--panel);border:1px solid var(--edge);
      border-radius:16px;padding:1.5rem;box-shadow:var(--shadow);position:relative;overflow:hidden
    }
    @media(min-width:840px){.card{grid-column:span 6}}
    .card:hover{transform:translateY(-3px)}
    .card h3{margin:.1rem 0 .4rem 0;color:#fff}
    .meta{display:flex;flex-wrap:wrap;gap:.6rem .8rem;margin:.6rem 0 1rem 0}
    .pill{font-size:.8rem;color:var(--muted);border:1px dashed #2a3148;border-radius:999px;padding:.25rem .6rem}
    .card .btn-row{display:flex;gap:.6rem;flex-wrap:wrap;margin-top:1rem}

    /* Experience */
    .xp{display:grid;grid-template-columns:repeat(12,1fr);gap:1.1rem}
    .xp .card{grid-column:span 12}
    @media(min-width:840px){.xp .card{grid-column:span 6}}
    .role{color:var(--muted);margin:.2rem 0 .8rem 0}
    .card ul{margin:.4rem 0 0 1.2rem;color:var(--muted)}

    /* Skills */
    .skills{display:grid;grid-template-columns:repeat(12,1fr);gap:1.1rem}
    .skills .card{grid-column:span 12}
    @media(min-width:840px){.skills .card{grid-column:span 6}}

    /* Footer */
    footer{border-top:1px solid var(--edge);padding:2rem 1rem;text-align:center;color:var(--muted)}
    .contact a{color:var(--accent)}
    .contact a:hover{text-decoration:underline}

    /* Back to top */
    .to-top{
      position:fixed;right:18px;bottom:18px;z-index:50;
      background:linear-gradient(135deg,var(--accent),var(--accent-2));
      width:44px;height:44px;border-radius:50%;
      display:flex;align-items:center;justify-content:center;color:#fff;
      box-shadow:0 8px 18px rgba(229,82,126,.35);
      transition:transform .2s ease, opacity .2s ease;opacity:.92
    }
    .to-top:hover{transform:translateY(-3px)}
  </style>
</head>
<body>

  <!-- NAV -->
  <nav class="nav">
    <div class="nav-inner">
      <div class="brand">Winnie <span>Kenneth</span></div>
      <div>
        <a class="link" href="#projects">Projects</a>
        <a class="link" href="#experience">Experience</a>
        <a class="link" href="#skills">Skills</a>
        <a class="link" href="#contact">Contact</a>
      </div>
    </div>
  </nav>

  <!-- HERO -->
  <section class="hero" id="home">
    <div data-aos="fade-right">
      <h1>Final-Year Computer Science Student</h1>
      <div class="tag">University of Hull — graduating 2026 (predicted 2:1)</div>
      <div class="type" id="typed"></div>
      <div class="cta-row">
        <a class="btn primary" href="#projects"><i class="fa-solid fa-rocket"></i> View Projects</a>
        <a class="btn ghost" href="mailto:kennethwinniefred746@gmail.com"><i class="fa-regular fa-envelope"></i> Email Me</a>
      </div>
    </div>

    <div class="hero-card" data-aos="fade-left">
      <h3>What I build</h3>
      <ul>
        <li>AI assistants that answer questions from your documents</li>
        <li>Data-driven tools with clean, simple UIs</li>
        <li>Deployed apps recruiters can click and use</li>
      </ul>
    </div>
  </section>

  <!-- PROJECTS -->
  <section id="projects">
    <h2 class="section-title" data-aos="fade-up">Featured Projects</h2>
    <p class="section-sub" data-aos="fade-up" data-aos-delay="80">AI, data and software projects with live demos and readable code.</p>

    <div class="grid">

      <!-- Project: AI Document Assistant -->
      <article class="card" data-aos="fade-up">
        <h3>AI-Powered Document Assistant (RAG)</h3>
        <p>Upload a PDF and ask natural questions. Uses embeddings + retrieval to find the most relevant sections, then answers with grounded context.</p>
        <div class="meta">
          <span class="pill">LangChain</span>
          <span class="pill">OpenAI API</span>
          <span class="pill">ChromaDB</span>
          <span class="pill">Streamlit</span>
          <span class="pill">Python</span>
        </div>
        <ul>
          <li>End-to-end pipeline: chunking, embeddings, semantic search, answer generation</li>
          <li>Deployed publicly — works without any setup</li>
          <li>Great for policies, reports, research and contracts</li>
        </ul>
        <div class="btn-row">
          <a class="btn primary" href="https://ai-document-assistant-gp7m7sxngzpyfxt46wjnnc.streamlit.app" target="_blank" rel="noopener">
            <i class="fa-solid fa-globe"></i> Live Demo
          </a>
          <a class="btn ghost" href="https://github.com/whiney001/ai-document-assistant" target="_blank" rel="noopener">
            <i class="fab fa-github"></i> View on GitHub
          </a>
        </div>
      </article>

      <!-- Project: Smart City Delivery -->
      <article class="card" data-aos="fade-up" data-aos-delay="60">
        <h3>Smart City Delivery Optimisation</h3>
        <p>Predictive routing across urban networks using regression/NN for cost estimation and A*, BFS, Dijkstra for paths.</p>
        <div class="meta">
          <span class="pill">Python</span>
          <span class="pill">Pandas</span>
          <span class="pill">Neural Nets</span>
          <span class="pill">A*, Dijkstra</span>
        </div>
        <ul>
          <li>Compared Polynomial Regression vs Neural Networks for travel cost</li>
          <li>Implemented multiple graph search algorithms with evaluation</li>
        </ul>
        <div class="btn-row">
          <a class="btn ghost" href="https://github.com/Whiney001/SmartCityDeliveryOptimization" target="_blank" rel="noopener">
            <i class="fab fa-github"></i> View on GitHub
          </a>
        </div>
      </article>

      <!-- Project: LightHR -->
      <article class="card" data-aos="fade-up" data-aos-delay="90">
        <h3>LightHR — AI Fairness & Bias Analysis</h3>
        <p>Explores bias in recruitment datasets with rule mining and fairness metrics; suggests mitigation approaches.</p>
        <div class="meta">
          <span class="pill">Python</span>
          <span class="pill">Pandas</span>
          <span class="pill">Fairlearn</span>
          <span class="pill">Data Viz</span>
        </div>
        <ul>
          <li>Measured statistical parity & disparate impact</li>
          <li>Produced interpretable visuals for stakeholders</li>
        </ul>
        <div class="btn-row">
          <a class="btn ghost" href="https://github.com/Whiney001/LightHR" target="_blank" rel="noopener">
            <i class="fab fa-github"></i> View on GitHub
          </a>
        </div>
      </article>

      <!-- Project: Engagement App -->
      <article class="card" data-aos="fade-up" data-aos-delay="120">
        <h3>Student Wellbeing Engagement App</h3>
        <p>C# console app with SQLite for tracking wellbeing activities; role-based access and data validation.</p>
        <div class="meta">
          <span class="pill">C#</span>
          <span class="pill">SQLite</span>
          <span class="pill">CLI UX</span>
        </div>
        <ul>
          <li>CRUD + auth + clean menu flows</li>
          <li>Lightweight and reliable for demos</li>
        </ul>
        <div class="btn-row">
          <a class="btn ghost" href="https://github.com/Whiney001/EngagementApp" target="_blank" rel="noopener">
            <i class="fab fa-github"></i> View on GitHub
          </a>
        </div>
      </article>

    </div>
  </section>

  <!-- EXPERIENCE -->
  <section id="experience">
    <h2 class="section-title" data-aos="fade-up">Experience</h2>
    <p class="section-sub" data-aos="fade-up" data-aos-delay="80">Commercial work where I applied my skills in real settings.</p>

    <div class="xp">

      <article class="card" data-aos="fade-up">
        <h3>Eagles Wing Limited</h3>
        <div class="role">Tech Associate (Software & AI) · Remote · Jan 2025 – Present</div>
        <ul>
          <li>Built lightweight internal tools and dashboards in Python/Flask/SQL</li>
          <li>Integrated OpenAI APIs for summaries and document workflows</li>
          <li>Delivered the AI Document Assistant for rapid policy search</li>
        </ul>
      </article>

      <article class="card" data-aos="fade-up" data-aos-delay="80">
        <h3>Step Recruitment</h3>
        <div class="role">Digital Transformation Intern (Entertainment) · Jul 2025 – Sep 2025</div>
        <ul>
          <li>Maintained and improved an entertainment website (HTML/CSS/JS)</li>
          <li>Added analytics for engagement and performance insights</li>
          <li>Worked cross-functionally on content and UX updates</li>
        </ul>
      </article>

    </div>
  </section>

  <!-- SKILLS -->
  <section id="skills">
    <h2 class="section-title" data-aos="fade-up">Skills</h2>
    <p class="section-sub" data-aos="fade-up" data-aos-delay="80">Strong engineering base with an AI/ML focus.</p>
    <div class="skills">
      <article class="card" data-aos="fade-up">
        <h3>Programming & Data</h3>
        <p class="role">Python, SQL, C#, JavaScript, Java · Pandas, NumPy, Scikit-learn</p>
      </article>
      <article class="card" data-aos="fade-up" data-aos-delay="80">
        <h3>AI & ML</h3>
        <p class="role">LangChain, OpenAI API, NLP, Neural Networks, Fairness & Evaluation</p>
      </article>
      <article class="card" data-aos="fade-up" data-aos-delay="120">
        <h3>Web & Cloud</h3>
        <p class="role">Streamlit, Flask, REST APIs, Docker (basics), Azure/AWS (basics), Git</p>
      </article>
      <article class="card" data-aos="fade-up" data-aos-delay="160">
        <h3>Collaboration</h3>
        <p class="role">Agile teamwork, documentation, stakeholder comms, demo-driven delivery</p>
      </article>
    </div>
  </section>

  <!-- CONTACT -->
  <section id="contact">
    <h2 class="section-title" data-aos="fade-up">Contact</h2>
    <p class="section-sub" data-aos="fade-up" data-aos-delay="80">I’m open to graduate roles in AI, Data and Software Engineering.</p>
    <div class="grid">
      <article class="card" data-aos="fade-up">
        <h3>Let’s talk</h3>
        <p class="role">Based in the UK · Remote-friendly</p>
        <div class="cta-row">
          <a class="btn primary" href="mailto:kennethwinniefred746@gmail.com"><i class="fa-regular fa-envelope"></i> Email</a>
          <a class="btn ghost" href="https://linkedin.com/in/winnie-kenneth-28a862287" target="_blank"><i class="fab fa-linkedin"></i> LinkedIn</a>
          <a class="btn ghost" href="https://github.com/Whiney001" target="_blank"><i class="fab fa-github"></i> GitHub</a>
        </div>
      </article>
    </div>
  </section>

  <footer>
    <div class="contact">
      © 2025 Winnie Kenneth · Final-Year BSc Computer Science · University of Hull ·
      <a href="mailto:kennethwinniefred746@gmail.com">kennethwinniefred746@gmail.com</a>
    </div>
  </footer>

  <!-- Back to top -->
  <a class="to-top" href="#home" aria-label="Back to top"><i class="fa-solid fa-arrow-up"></i></a>

  <!-- JS: Typed + AOS -->
  <script src="https://unpkg.com/aos@2.3.4/dist/aos.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/typed.js@2.0.12"></script>
  <script>
    AOS.init({ duration: 700, once: true, easing: 'ease-out' });

    new Typed('#typed', {
      strings: [
        'AI & Software Developer',
        'Data-driven problem solver',
        'I build useful, deployable tools'
      ],
      typeSpeed: 38,
      backSpeed: 20,
      backDelay: 1200,
      loop: true,
      showCursor: false
    });
  </script>
</body>
</html>
