document.addEventListener('DOMContentLoaded', () => {
    const timerDisplay = document.getElementById('timer');
    const startButton = document.getElementById('start');
    const resetButton = document.getElementById('reset');

    let workMinutes = 25;
    let breakMinutes = 5;
    let isWorking = true;
    let timeLeft = workMinutes * 60;
    let timerInterval;

    function updateTimerDisplay() {
        const minutes = Math.floor(timeLeft / 60);
        let seconds = timeLeft % 60;
        seconds = seconds < 10 ? '0' + seconds : seconds;
        timerDisplay.textContent = `${minutes}:${seconds}`;
    }

    function startTimer() {
        timerInterval = setInterval(() => {
            timeLeft--;
            updateTimerDisplay();
            if (timeLeft === 0) {
                clearInterval(timerInterval);
                if (isWorking) {
                    isWorking = false;
                    timeLeft = breakMinutes * 60;
                    showNotification('Break Time!');
                } else {
                    isWorking = true;
                    timeLeft = workMinutes * 60;
                    showNotification('Work Time!');
                }
                startTimer();
            }
        }, 1000);
    }

    function resetTimer() {
        clearInterval(timerInterval);
        isWorking = true;
        timeLeft = workMinutes * 60;
        updateTimerDisplay();
    }

    function showNotification(message) {
        if ('Notification' in window) {
            Notification.requestPermission().then(permission => {
                if (permission === 'granted') {
                    new Notification(message);
                }
            });
        }
    }

    startButton.addEventListener('click', () => {
        clearInterval(timerInterval);
        startTimer();
    });

    resetButton.addEventListener('click', resetTimer);

    updateTimerDisplay();
});