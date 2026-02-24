const canvas = document.getElementById('c');
const ctx = canvas.getContext('2d');
function resize(){ canvas.width = window.innerWidth; canvas.height = window.innerHeight }
window.addEventListener('resize', resize); resize();

let ws_url = (location.protocol === 'https:' ? 'wss://' : 'ws://') + location.host + '/ws';
let ws = null;
let lastState = null;
let sendQueue = [];
let reconnectDelay = 500; // ms

function connect() {
  ws = new WebSocket(ws_url);

  ws.onopen = () => {
    console.log('ws open');
    reconnectDelay = 500;
    // flush send queue
    while(sendQueue.length > 0){
      const m = sendQueue.shift();
      try{ ws.send(m); }catch(e){ console.warn('send after open failed', e); }
    }
  };

  ws.onmessage = (ev) => {
    try{
      const msg = JSON.parse(ev.data);
      if(msg.type === 'state'){
        lastState = msg.payload;
      }
    }catch(e){ console.warn('ws parse error', e); }
  };

  ws.onclose = (ev) => {
    console.log('ws closed', ev.code, ev.reason);
    // attempt reconnect
    setTimeout(() => {
      reconnectDelay = Math.min(5000, reconnectDelay * 1.5);
      connect();
    }, reconnectDelay);
  };

  ws.onerror = (err) => { console.warn('ws error', err); };
}

connect();

function draw(){
  ctx.clearRect(0,0,canvas.width, canvas.height);
  if(!lastState) return;
  const bodies = lastState.bodies;
  for(const b of bodies){
    const pos = b.position;
    const col = b.color || [255,255,255];
    ctx.fillStyle = `rgb(${col[0]}, ${col[1]}, ${col[2]})`;
    if(b.vertices === null){
      ctx.beginPath(); ctx.arc(pos[0], canvas.height - pos[1], b.radius, 0, Math.PI*2); ctx.fill();
    } else {
      ctx.beginPath();
      const verts = b.vertices.map(v => [v[0]+pos[0], canvas.height - (v[1]+pos[1])]);
      ctx.moveTo(verts[0][0], verts[0][1]);
      for(let i=1;i<verts.length;i++) ctx.lineTo(verts[i][0], verts[i][1]);
      ctx.closePath(); ctx.fill();
    }
  }
}

canvas.addEventListener('mousedown', (e)=>{
  const x = e.clientX;
  const y = canvas.height - e.clientY;
  const msg = e.button === 0 ? {type:'add_circle', x:x, y:y} : {type:'add_polygon', x:x, y:y, n:4, size:50};
  const payload = JSON.stringify(msg);
  if(ws && ws.readyState === WebSocket.OPEN){
    ws.send(payload);
  } else {
    // queue message until websocket reconnects
    console.warn('WebSocket not open, queuing message');
    sendQueue.push(payload);
  }
});

canvas.addEventListener('contextmenu', (e)=>{ e.preventDefault(); });

function loop(){ draw(); requestAnimationFrame(loop); }
requestAnimationFrame(loop);
