const countDownClock = () => {
  let days = 0,
    hours = 0,
    minutes = 0,
    seconds = 0;
  let interval;
  let dateEnd;
  let timerDay, timerHour, timerMinute, timerSecond;
  const jetLag = new Date().getTimezoneOffset() * 60 * 1000;

  timerDay = document.getElementById("timer-days");
  timerHour = document.getElementById("timer-hours");
  timerMinute = document.getElementById("timer-minutes");
  timerSecond = document.getElementById("timer-seconds");
  // Set date of the end to timer
  dateEnd = +new Date("2023-12-31");

  interval = setInterval(timerDate, 1000);

  function timerDate() {
    // Time before the end of timer in second
    let currentTime = +new Date();
    let date = dateEnd + jetLag - currentTime;

    // Set value of date
    if (date > 0) {
      days = Math.floor(date / (3600 * 24 * 1000));
      hours = Math.floor((date / (3600 * 1000)) % 24);
      minutes = Math.floor((date / (60 * 1000)) % 60);
      seconds = Math.floor((date / 1000) % 60);
    } else {
      days = 0;
      hours = 0;
      minutes = 0;
      seconds = 0;
      clearInterval(interval);
    }

    timerDay.textContent = `${formatNumber(days)}`;
    timerHour.textContent = `${formatNumber(hours)}`;
    timerMinute.textContent = `${formatNumber(minutes)}`;
    timerSecond.textContent = `${formatNumber(seconds)}`;
  }

  function formatNumber(value) {
    return value.toLocaleString("en-US", {
      minimumIntegerDigits: 2,
      useGrouping: false,
    });
  }
};

countDownClock();
