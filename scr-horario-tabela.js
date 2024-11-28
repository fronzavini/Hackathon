const horario = document.getElementById('horario');
const horas = ["08:00", "08:45", "09:45", "10:30", "11:15", "", "13:30", "14:15", "15:00", "16:00", "16:45"];

function criarHorario(){
    
let html = `<section id="menu-calendario"><h2 id="month-year">
    <select name="Labs" id="labs">
        <option value="LabA03" class="select">Lab A03</option>
        <option value="LabA04" class="select">Lab A04</option>
    </select>
    </h2>`;
    html += `<div id="botao-mes"><button type="button" id="b1"></button><button type="button" id="b2"></button></div></section>`;
    html += `<table>`;
html += `<tr><th></th><th>Seg</th><th>Ter</th><th>Qua</th><th>Qui</th><th>Sex</th><th>Sab</th></tr>`;

for(let i=0; i < 11; i++) {
    html += `<tr>`;
    for(let j = 0; j < 7; j++){
        if(j === 0){
            html += `<td class="horario-celula" id="hora">${horas[i]}</td>`;
        }
        else{
            html += `<td class="horario-celula" id="i${i}j${j-1} "></td>`;
        }
    }
    html += `</tr>`;
}
html += `</table>`;

horario.innerHTML = html;
}

criarHorario();