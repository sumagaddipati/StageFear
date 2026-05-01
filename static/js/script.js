let recorder, chunks = [], scores = [];

document.getElementById("gen").onclick = () => {
    const t = ["AI future", "Dream life", "Success meaning"];
    document.getElementById("topic").innerText = t[Math.floor(Math.random() * t.length)];
};

document.getElementById("prep").onclick = () => timer(60, () => alert("Start speaking"));

document.getElementById("speak").onclick = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    recorder = new MediaRecorder(stream);

    recorder.ondataavailable = e => chunks.push(e.data);
    recorder.start();

    timer(60, () => recorder.stop());

    recorder.onstop = () => {
        const blob = new Blob(chunks);
        document.getElementById("audio").src = URL.createObjectURL(blob);
    };

    // 🔊 Silence detection
    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    const ctx = new AudioContextClass();
    const analyser = ctx.createAnalyser();
    const mic = ctx.createMediaStreamSource(stream);
    mic.connect(analyser);

    function detect() {
        let data = new Uint8Array(analyser.frequencyBinCount);
        analyser.getByteFrequencyData(data);
        let vol = data.reduce((a, b) => a + b) / data.length;
        if (vol < 5) console.log("Silence...");
        requestAnimationFrame(detect);
    }
    detect();
};

document.getElementById("pause").onclick = () => recorder && recorder.pause();
document.getElementById("resume").onclick = () => recorder && recorder.resume();

document.getElementById("analyze").onclick = async () => {
    try {
        if (chunks.length === 0) {
            alert("Please record audio first");
            return;
        }
        
        const blob = new Blob(chunks, { type: "audio/webm" });
        const fd = new FormData();
        fd.append("audio", blob, "recording.webm");
        fd.append("topic", document.getElementById("topic").innerText || "General");
        fd.append("category", document.getElementById("category").value || "Tech");
        fd.append("difficulty", document.getElementById("difficulty").value || "Medium");
        fd.append("duration", 60);

        const token = localStorage.getItem("access_token");
        const res = await fetch("/api/sessions/analyze", {
            method: "POST",
            headers: {
                "Authorization": "Bearer " + token
            },
            body: fd
        });
        
        if (!res.ok) {
            throw new Error("Failed to analyze: " + res.statusText);
        }
        
        const d = await res.json();
        console.log("Analysis result:", d);
        displayResults(d);
    } catch (error) {
        console.error("Error:", error);
        alert("Error analyzing audio: " + error.message);
    }
};

function displayResults(data) {
    // Display results on page
    if (document.getElementById("results")) {
        document.getElementById("results").innerHTML = `
            <h3>Analysis Results</h3>
            <p>Word Count: ${data.word_count}</p>
            <p>WPM: ${data.wpm}</p>
            <p>Confidence: ${data.confidence_score}</p>
            <p>Clarity: ${data.clarity_score}</p>
            <p>Structure: ${data.structure_score}</p>
            <p>Overall Score: ${data.overall_score}</p>
            <p>Transcript: ${data.transcript}</p>
        `;
    }
}

    scores.push(d.confidence);

    new Chart(document.getElementById("chart"),{
        type:"line",
        data:{labels:scores.map((_,i)=>i+1),datasets:[{data:scores}]}
    });

    document.getElementById("result").innerHTML=`
    <h3>Results</h3>
    <p>Confidence: ${d.confidence}</p>
    <p>Clarity: ${d.clarity}</p>
    <p>Structure: ${d.structure}</p>
    <p>WPM: ${d.wpm}</p>
    <p>${d.text}</p>
    <ul>${d.coach.map(c=>`<li>${c}</li>`).join("")}</ul>
    `;
};

// 🌙 dark mode
document.getElementById("toggleTheme").onclick=()=>{
    document.body.classList.toggle("dark");
};

// ⏱ timer
function timer(sec,cb){
    let t=sec;
    const i=setInterval(()=>{
        t--;
        document.getElementById("circle").innerText=t;
        let p=((sec-t)/sec)*100;
        document.getElementById("circle").style.background=
        `conic-gradient(#2563eb ${p}%,#ddd 0)`;
        if(t<=0){clearInterval(i);cb();}
    },1000);
}

// 📂 PDF
document.getElementById("download").onclick=()=>{
    const content=document.getElementById("result").innerText;
    const blob=new Blob([content],{type:"text/plain"});
    const a=document.createElement("a");
    a.href=URL.createObjectURL(blob);
    a.download="report.txt";
    a.click();
};