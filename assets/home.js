// Homepage motion, ported from the Codex build's app.js (home block only; portal code dropped).
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
window.addEventListener('DOMContentLoaded',()=>{if(window.ScrollCraft)ScrollCraft.mount(document.body)});
const reduced=matchMedia('(prefers-reduced-motion:reduce)'),hero=$('.hero-product'),lock=$('.lock'),section=$('.intake');let px=0,py=0,scheduled=false;
const draw=()=>{scheduled=false;if(reduced.matches)return;
 const hr=$('.hero').getBoundingClientRect();if(hr.bottom>0){const y=Math.max(0,-hr.top);hero.style.transform=`translateY(${-y*.10}px) rotateX(${py*-5}deg) rotateY(${px*7}deg)`}
 const rect=section.getBoundingClientRect(),travel=section.offsetHeight-innerHeight,p=Math.max(0,Math.min(1,-rect.top/Math.max(1,travel))),t=Math.max(0,Math.min(1,(p-.12)/.78)),e=t*t*(3-2*t),small=innerWidth<680;
 $$('.scanner').forEach((el,i)=>{const x=(i%2===0?1:-1)*(small?65:105)*e,y=(i<2?1:-1)*(small?40:76)*e;el.style.transform=`translate(${x}px,${y}px) scale(${1-e*.34})`;el.style.opacity=String(1-e*.45)});
 $('.lock-mark').style.transform=`translate(-50%,-50%) scale(${1+e*.28})`;
};
const schedule=()=>{if(!scheduled){scheduled=true;requestAnimationFrame(draw)}};
addEventListener('scroll',schedule,{passive:true});addEventListener('resize',schedule);
$('.hero').addEventListener('pointermove',e=>{if(e.pointerType==='mouse'){const r=$('.hero').getBoundingClientRect();px=(e.clientX/r.width-.5)*2;py=((e.clientY-r.top)/r.height-.5)*2;schedule()}});
$('.hero').addEventListener('pointerleave',()=>{px=py=0;schedule()});
schedule();
