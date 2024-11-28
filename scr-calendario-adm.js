const calendar = document.getElementById('calendar');
const today = new Date();
const currentMonth = today.getMonth();
const currentYear = today.getFullYear();
const currentDay= today.getDate();

function createCalendar(month, year){
    const monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    const totalDays = new Date(year, month + 1,0).getDate();
    const firstDayIndex = new Date(year, month, 1).getDay();

let html = `<section id="menu-calendario"><h2 id="month-year">${monthNames[month]} ${year}</h2>`;
    html += `<div id="botao-mes"><button type="button" id="b1"></button><button type="button" id="b2"></button></div></section>`;
    html += `<table>`;
    html += `<tr><th>Dom</th><th>Seg</th><th>Ter</th><th>Qua</th><th>Qui</th><th>Sex</th><th>Sab</th></tr>`
    
    let day = 1;
    for(let i=0; i < 6; i++) {
        html += `<tr>`;
        for(let j = 0; j < 7; j++){
            const classNames = [];
            if (i === 0 && j < firstDayIndex) {
                html += `<td></td>`;
            }else if (day > totalDays){
                break;
            }else {
                const date = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
                html += `<td class="calendar-day" data-date="${date}">${day}</td>`;
                //html += `<td class="${classNames.join('')}">${day}</td>`;
                day++;
            }
        }
        html += `</tr>`;
    }
    html += `</table>`;

    calendar.innerHTML = html;

    document.querySelectorAll('.calendar-day').forEach(day => {
        day.addEventListener('click', function () {
            const date = this.getAttribute('data-date');
            // Redireciona para a página desejada
            window.location.href = `horarios-administrador.html`;
        });
    });
}

createCalendar(currentMonth, currentYear);