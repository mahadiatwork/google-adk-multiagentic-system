const defaultMinutes = 25;
const defaultSeconds = 0;

let timer;
let minutes = defaultMinutes;
let seconds = defaultSeconds;
let isRunning = false;

function updateTimer() {
    if (seconds === 0) {
        if (minutes === 0) {
            clearInterval(timer);
            isRunning = false; // Reset the running state
            notifyUser("Time's up!");
            return;
        }
        minutes--;
        seconds = 59;
    } else {
        seconds--;
    }
    document.getElementById("timer").textContent = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}

function notifyUser(message) {
    if (Notification.permission === "granted") {
        new Notification("Pomodoro Timer", { body: message });
    } else if (Notification.permission !== "denied") {
        Notification.requestPermission().then(permission => {
            if (permission === "granted") {
                new Notification("Pomodoro Timer", { body: message });
            }
        });
    } else {
        alert(message);
    }
}

function startTimer() {
    if (!isRunning) {
        timer = setInterval(updateTimer, 1000);
        isRunning = true;
    }
}

function resetTimer() {
    clearInterval(timer);
    minutes = defaultMinutes;
    seconds = defaultSeconds;
    document.getElementById("timer").textContent = "25:00";
    isRunning = false;
}

document.getElementById("start").addEventListener("click", startTimer);
document.getElementById("reset").addEventListener("click", resetTimer);