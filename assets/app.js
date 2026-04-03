
const chips = document.querySelectorAll('[data-filter]');
const cards = document.querySelectorAll('[data-entry]');
const search = document.querySelector('#search');
function applyFilters(){
  const active = document.querySelector('.chip.active')?.dataset.filter || 'all';
  const q = (search?.value || '').trim().toLowerCase();
  cards.forEach(card=>{
    const hay = (card.dataset.title + ' ' + card.dataset.themes + ' ' + card.dataset.form + ' ' + card.dataset.year).toLowerCase();
    const okFilter = active === 'all' || card.dataset.form === active || card.dataset.themes.includes(active) || card.dataset.year === active;
    const okSearch = !q || hay.includes(q);
    card.classList.toggle('hidden', !(okFilter && okSearch));
  });
}
chips.forEach(chip=>chip.addEventListener('click', ()=>{
  chips.forEach(c=>c.classList.remove('active'));
  chip.classList.add('active');
  applyFilters();
}));
if(search){search.addEventListener('input', applyFilters);}
applyFilters();
