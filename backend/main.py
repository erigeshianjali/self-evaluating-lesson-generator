from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional

from lesson_generator import generate_lesson
from agent import run_agent
from memory import get_evaluations, create_table

app = FastAPI(
    title="Self-Evaluating Lesson Content Generator",
    description="Generate, evaluate, improve, and record beginner-friendly lessons.",
    version="1.0.1",
)

class GenerateRequest(BaseModel):
    topic: str = Field(min_length=2, max_length=120)
    lesson: Optional[str] = None
    human_verified: bool = False
    source_url: Optional[str] = None

@app.on_event("startup")
def startup():
    create_table()

@app.get("/", response_class=HTMLResponse)
def home():
    return r"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Self-Evaluating Lesson Generator</title>
<style>
:root{font-family:Inter,Segoe UI,Arial,sans-serif;color:#172033;background:#f4f7fb}
*{box-sizing:border-box}body{margin:0}.wrap{max-width:1050px;margin:34px auto;padding:0 20px}
header{background:linear-gradient(120deg,#172554,#2563eb);color:white;padding:30px;border-radius:18px;margin-bottom:22px}
header h1{margin:0 0 8px;font-size:clamp(25px,4vw,36px)}header p{margin:0;color:#dbeafe;line-height:1.6}
.panel,.card{background:white;border:1px solid #e2e8f0;border-radius:14px;padding:22px;margin:18px 0;box-shadow:0 4px 16px #0f172a0a}
label{display:block;font-weight:650;margin:14px 0 6px}
input[type=text],input[type=url],textarea{width:100%;padding:12px 13px;border:1px solid #cbd5e1;border-radius:9px;font:inherit}
textarea{min-height:115px;resize:vertical}
.check{display:flex;gap:9px;align-items:flex-start;font-weight:500;line-height:1.5}.check input{margin-top:5px}
button{background:#2563eb;color:white;border:0;border-radius:9px;padding:13px 18px;font:inherit;font-weight:700;cursor:pointer;width:100%;margin-top:16px}
button:disabled{opacity:.6;cursor:wait}.muted{color:#64748b;font-size:14px}.hidden{display:none}
.result-head{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
.pill{display:inline-block;padding:6px 11px;border-radius:999px;font-size:13px;font-weight:750;background:#e2e8f0;color:#334155}
.APPROVED,.PASS{background:#dcfce7;color:#166534}.REJECTED,.FAIL{background:#fee2e2;color:#991b1b}.PENDING,.NEEDS_IMPROVEMENT{background:#fef3c7;color:#92400e}
.lesson{white-space:normal;line-height:1.75;font-size:16px}.lesson h3{margin:22px 0 6px;color:#1e3a8a;font-size:19px}.lesson p{margin:6px 0 12px}.lesson ol,.lesson ul{padding-left:24px}
.criteria{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px}
.criterion{border:1px solid #e2e8f0;border-radius:10px;padding:14px}.criterion strong{display:block;margin-bottom:8px;overflow-wrap:anywhere}.criterion p{margin:8px 0 0;color:#475569;font-size:14px;line-height:1.5}
.logitem{padding:12px;border-left:3px solid #93c5fd;background:#f8fafc;margin:9px 0;border-radius:5px}
.note{background:#fffbeb;border:1px solid #fde68a;padding:13px;border-radius:10px;color:#854d0e;line-height:1.5}
.error{color:#991b1b;background:#fef2f2;padding:12px;border-radius:9px}
footer{text-align:center;color:#64748b;font-size:13px;padding:20px}
@media(max-width:600px){.wrap{padding:0 12px;margin:16px auto}header,.panel,.card{padding:17px}}
</style>
</head>
<body>
<div class="wrap">
<header>
<h1>Self-Evaluating Lesson Content Generator</h1>
<p>Create a beginner-friendly lesson, evaluate it against six criteria, improve failed sections, and keep an evaluation history.</p>
</header>
<section class="panel">
<h2>Generate a lesson</h2>
<label for="topic">Topic</label>
<input id="topic" type="text" value="Introduction to RAG" placeholder="Enter a lesson topic">
<label for="lesson">Optional: paste your own lesson</label>
<textarea id="lesson" placeholder="Leave blank to use the built-in RAG demonstration lesson."></textarea>
<label class="check"><input id="verified" type="checkbox"> I have personally checked the factual claims against the source below.</label>
<label for="source">Source URL (required when confirming verification)</label>
<input id="source" type="url" placeholder="https://...">
<button id="generate" onclick="run()">Generate and evaluate lesson</button>
<p class="muted">For this demonstration, the built-in lesson generator currently supports Introduction to RAG.</p>
</section>
<div id="result" class="hidden" aria-live="polite"></div>
<div class="note">Accuracy is marked PASS only when a user explicitly confirms that they checked the factual claims against a supplied source. This application does not independently prove factual correctness.</div>
<footer>Self-Evaluating Lesson Content Generator · FastAPI demonstration</footer>
</div>
<script>
function escapeHtml(value){
 return String(value ?? '').replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
}
function renderLesson(text){
 const lines=String(text||'').trim().split(/\r?\n/);
 let html='', inList=false, listType='';
 const headings=['Introduction','Definition','Importance','How It Works','Example','Advantages','Limitations','Conclusion','Accuracy Verification Required'];
 function closeList(){if(inList){html+=listType==='ol'?'</ol>':'</ul>';inList=false;}}
 for(const raw of lines){
  const line=raw.trim();
  if(!line){closeList();continue;}
  const heading=headings.find(h=>line.toLowerCase()===h.toLowerCase()+':');
  if(heading){closeList();html+='<h3>'+escapeHtml(heading)+'</h3>';continue;}
  const numbered=line.match(/^\d+[\.)]\s+(.*)$/);
  const bullet=line.match(/^[-•]\s+(.*)$/);
  if(numbered||bullet){
   const type=numbered?'ol':'ul';
   if(!inList||listType!==type){closeList();html+=type==='ol'?'<ol>':'<ul>';inList=true;listType=type;}
   html+='<li>'+escapeHtml((numbered||bullet)[1])+'</li>';continue;
  }
  closeList();html+='<p>'+escapeHtml(line)+'</p>';
 }
 closeList();return html;
}
function renderResult(data){
 const result=data.result||{};
 const status=result.status||'UNKNOWN';
 const results=result.results||{};
 let criteria='';
 for(const [name,item] of Object.entries(results)){
  const s=item.status||'PENDING';
  const label=name.replaceAll('_',' ').replace(/\b\w/g,c=>c.toUpperCase());
  criteria+=`<div class="criterion"><strong>${escapeHtml(label)} <span class="pill ${escapeHtml(s)}">${escapeHtml(s)}</span></strong><p>${escapeHtml(item.feedback||'')}</p></div>`;
 }
 const attempts=result.attempts??'—';
 const logs=(result.rejection_log||[]).map(x=>`<div class="logitem"><b>Attempt ${escapeHtml(x.attempt)}</b><br>Failed: ${escapeHtml((x.failures||[]).join(', ')||'None')}</div>`).join('')||'<p class="muted">No rejected attempts.</p>';
 const hints=(result.learning_hints||[]).map(x=>`<li><b>${escapeHtml(x[0])}</b>: ${escapeHtml(x[2])}</li>`).join('');
 const lesson=renderLesson(result.final_lesson||'No lesson content was returned.');
 return `<section class="card"><div class="result-head"><h2>Lesson result</h2><span class="pill ${escapeHtml(status)}">${escapeHtml(status)}</span></div>
 <p class="muted">Topic: ${escapeHtml(data.topic||'')} · Evaluation attempts: ${escapeHtml(attempts)}</p>
 <h2>Generated lesson</h2><article class="lesson">${lesson}</article>
 <h2>Evaluation scorecard</h2><div class="criteria">${criteria||'<p>No evaluation details available.</p>'}</div>
 <h2>Improvement history</h2>${logs}
 ${hints?`<h2>Learning suggestions</h2><ul>${hints}</ul>`:''}
 <div class="note"><b>Accuracy note:</b> ${escapeHtml(data.accuracy_note||'Review factual claims against trusted sources.')}</div>
 </section>`;
}
async function run(){
 const button=document.getElementById('generate'), box=document.getElementById('result');
 button.disabled=true;button.textContent='Generating lesson...';box.classList.remove('hidden');box.innerHTML='<section class="card">Generating and evaluating your lesson. Please wait...</section>';
 const body={topic:document.getElementById('topic').value,lesson:document.getElementById('lesson').value||null,human_verified:document.getElementById('verified').checked,source_url:document.getElementById('source').value||null};
 try{
  const response=await fetch('/generate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
  const data=await response.json();
  if(!response.ok){box.innerHTML='<section class="card error">'+escapeHtml(data.detail||'Request failed.')+'</section>';return;}
  box.innerHTML=renderResult(data);
 }catch(error){box.innerHTML='<section class="card error">Could not contact the backend: '+escapeHtml(error.message)+'</section>';}
 finally{button.disabled=false;button.textContent='Generate and evaluate lesson';}
}
</script>
</body>
</html>
"""

@app.get("/health")
def health():
    return {"status": "ok", "project": "Self-Evaluating Lesson Content Generator"}

@app.post("/generate")
def generate(request: GenerateRequest):
    topic = request.topic.strip()
    if not topic:
        raise HTTPException(status_code=400, detail="Topic cannot be empty.")
    if request.human_verified and not request.source_url:
        raise HTTPException(status_code=400, detail="Provide the source URL when confirming human verification.")
    try:
        lesson = request.lesson.strip() if request.lesson and request.lesson.strip() else generate_lesson(topic)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    accuracy_status = "PASS" if request.human_verified and request.source_url else "PENDING"
    result = run_agent(lesson, topic=topic, accuracy_status=accuracy_status, max_retries=2)
    return {
        "topic": topic,
        "result": result,
        "accuracy_note": (
            "Human verification was declared by the requester. The application does not independently validate the source."
            if accuracy_status == "PASS"
            else "Accuracy is PENDING. Keyword matching and source retrieval do not prove factual correctness."
        ),
    }

@app.get("/history")
def history():
    return {"records": get_evaluations(limit=100)}
