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
    html += `<tr><th>Sun</th><th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th><th>Sat</th></tr>`
    
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
                if (day === currentDay && month === currentMonth && year === currentYear){
                    classNames.push('today');
                }
                html += `<td class="${classNames.join('')}">${day}</td>`;
                day++;
            }
        }
        html += `</tr>`;
    }
    html += `</table>`;

    calendar.innerHTML = html;
}

createCalendar(currentMonth, currentYear);
/*
document.addEventListener('mouseover', function(event){
    if (event.target.tagName=== 'TD'){
    event.target.classList.add('highlight');
    }
});

document.addEventListener('mouseout', function(event){
    if (event.target.tagName==='TD') {
    event.target.classList.remove('highlight');
    }
});
*/