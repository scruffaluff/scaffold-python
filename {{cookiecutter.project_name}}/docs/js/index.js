// Initialize mermaid.js library.
mermaid.initialize({ startOnLoad: true });

// Instantiate Termynal instances
const termynals = document.querySelectorAll("div.termynal");
termynals.forEach((container) => new Termynal(container));
