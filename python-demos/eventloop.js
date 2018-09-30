class App {
  main() {
    process.stdin.on('data', this.cpu_task);
    setInterval(this.timer_task, 3000);
  }

  cpu_task(data) {
    console.log('+ start cpu_task');
    const duration = Number.parseInt(data, 10);
    const start = Date.now();
    while (Date.now() - start < duration);
    console.log('+ finish cpu_task');
  }

  timer_task() {
    console.log('* timer_task');
  }
}

new App().main();
