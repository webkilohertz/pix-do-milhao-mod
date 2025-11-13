const timerEl = document.getElementById("timer");
const resultEl = document.getElementById("result");

// função pra gerar 6 dezenas aleatórias de 0 a 100
function gerarDezenas() {
  const numeros = [];
  while (numeros.length < 6) {
    const n = Math.floor(Math.random() * 101);
    if (!numeros.includes(n)) numeros.push(n);
  }
  return numeros;
}

// retorna o próximo horário de reset (meia-noite)
function getNextResetTime() {
  const now = new Date();
  const next = new Date();
  next.setHours(24, 0, 0, 0);
  return next;
}

// atualiza o contador na tela
function updateTimer() {
  const now = new Date();
  const diff = nextReset - now;

  if (diff <= 0) {
    // virou o dia — novo sorteio
    sortearHoje();
    nextReset = getNextResetTime();
  } else {
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const minutes = Math.floor((diff / (1000 * 60)) % 60);
    const seconds = Math.floor((diff / 1000) % 60);
    timerEl.textContent =
      `${hours.toString().padStart(2, "0")}:` +
      `${minutes.toString().padStart(2, "0")}:` +
      `${seconds.toString().padStart(2, "0")}`;
  }
}

// sorteia e salva o resultado do dia
function sortearHoje() {
  const hoje = new Date().toDateString();
  const dezenas = gerarDezenas();
  localStorage.setItem("ultimaData", hoje);
  localStorage.setItem("resultadoHoje", JSON.stringify(dezenas));
  exibirResultado(dezenas);
}

// mostra na tela o resultado do dia
function exibirResultado(dezenas) {
  resultEl.textContent = "Resultado de hoje: " + dezenas.join(" - ");
}

// inicialização
let nextReset = getNextResetTime();
const salvoData = localStorage.getItem("ultimaData");
const hojeData = new Date().toDateString();

if (salvoData === hojeData) {
  // já tem sorteio do dia
  const dezenasSalvas = JSON.parse(localStorage.getItem("resultadoHoje"));
  exibirResultado(dezenasSalvas);
} else {
  // faz novo sorteio
  sortearHoje();
}

// atualiza cronômetro a cada segundo
setInterval(updateTimer, 1000);

