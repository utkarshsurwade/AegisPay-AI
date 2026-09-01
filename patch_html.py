import re

with open("web_prototype/templates/index.html", "r") as f:
    content = f.read()

# 1. Add multimodal container
container_html = """
            <!-- Multimodal Asset Generation Container -->
            <div id="multimodal-asset-container" class="hidden border-t border-slate-800 pt-2 space-y-1">
              <span class="text-[10px] text-slate-400 uppercase font-bold block">Live GenAI Asset (Intercepted):</span>
              <div id="multimodal-asset-content" class="p-2 bg-slate-900 border border-slate-800 rounded flex justify-center items-center">
              </div>
            </div>

            <!-- TreeSHAP Feature Contributions Container -->"""
content = content.replace("<!-- TreeSHAP Feature Contributions Container -->", container_html)

# 2. Add functions
funcs = """
    async function generateDeepfakeImage(txId) {
      const container = document.getElementById('multimodal-asset-container');
      const content = document.getElementById('multimodal-asset-content');
      container.classList.remove('hidden');
      content.innerHTML = '<div class="flex items-center space-x-2 text-slate-400"><i class="fa-solid fa-spinner fa-spin text-mc-orange"></i><span>Generating live deepfake artifact...</span></div>';
      
      try {
        const res = await fetch('/api/generate/image', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ prompt: "A hyper-realistic selfie of a person holding a fake ID card, deepfake artifacting, cybersecurity forensics style", seed: Math.floor(Math.random() * 1000000) })
        });
        const data = await res.json();
        if (data.status === 'success') {
          content.innerHTML = `<img src="${data.url}" class="max-h-48 rounded object-cover border border-mc-red/50 shadow-lg shadow-mc-red/20" alt="Generated Deepfake">`;
        } else {
          content.innerHTML = '<span class="text-mc-red">Failed to generate image.</span>';
        }
      } catch (e) {
        content.innerHTML = '<span class="text-mc-red">Failed to generate image.</span>';
      }
    }

    async function generateSyntheticAudio(txId) {
      const container = document.getElementById('multimodal-asset-container');
      const content = document.getElementById('multimodal-asset-content');
      container.classList.remove('hidden');
      content.innerHTML = '<div class="flex items-center space-x-2 text-slate-400"><i class="fa-solid fa-spinner fa-spin text-cyan-400"></i><span>Synthesizing voice clone...</span></div>';
      
      try {
        const script = "Hello, this is fraud prevention calling from your bank. We noticed a suspicious charge of 4850 dollars. Please verify your identity by speaking your full name and social security number loudly and clearly.";
        const res = await fetch('/api/generate/audio', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ script: script })
        });
        const data = await res.json();
        if (data.status === 'success') {
          content.innerHTML = `
            <div class="flex items-center space-x-4 w-full">
              <i class="fa-solid fa-microphone-lines text-2xl text-cyan-400 animate-pulse"></i>
              <audio controls class="w-full h-8" autoplay>
                <source src="${data.url}" type="audio/mpeg">
              </audio>
            </div>
          `;
        } else {
          content.innerHTML = '<span class="text-mc-red">Failed to generate audio.</span>';
        }
      } catch (e) {
        content.innerHTML = '<span class="text-mc-red">Failed to generate audio.</span>';
      }
    }

    // Trigger Sandbox Simulation"""

content = content.replace("// Trigger Sandbox Simulation", funcs)

# 3. Call functions inside triggerSimulation
call_logic = """
        if (isFraud) {
          if (vectorId === 'ADV-05') {
            generateDeepfakeImage(tx.tx_id);
          } else if (vectorId === 'ADV-07' || vectorId === 'ADV-21') {
            generateSyntheticAudio(tx.tx_id);
          } else {
            document.getElementById('multimodal-asset-container').classList.add('hidden');
          }
        } else {
          document.getElementById('multimodal-asset-container').classList.add('hidden');
        }
        
        // Render TreeSHAP Feature Contributions
"""
content = content.replace("// Render TreeSHAP Feature Contributions", call_logic)

with open("web_prototype/templates/index.html", "w") as f:
    f.write(content)

