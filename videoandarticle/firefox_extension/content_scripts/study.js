function createStudyWindow(){
  var win = document.createElement("div");
  win.className = "study-window";
  win.id = "study-window";
  win.innerHTML = `<h3>正在学习......</h3>`;
  win.style.width = "100%";
  win.style.height = "500px";

  var frame = document.createElement("iframe");
  frame.className = "study-window-iframe";
  frame.id = "study-window-iframe";
  frame.style.width = "100%";
  frame.style.height = "100%";
  win.append(frame);
  return win;
}

var studyWindow = createStudyWindow();


(function() {
  if (window.hasRun) {
    return;
  }
  window.hasRun = true;

  function start() { 
    //document.body.append(studyWindow);
    studyWindow.children[1].src = window.location.href; 
    

    var pages = document.getElementsByClassName("text-wrap");
    var buttons = document.getElementsByClassName("btn");

    for(var i=0; i < pages.length; i++){
      pages[i].children[0].click();
    }

    browser.runtime.sendMessage({command: "start"});

    setTimeout(function(){
      browser.runtime.sendMessage({command: "stop"});
    }, 1000*10);
  
  }

  function stop() {
    //document.body.remove(studyWindow);
  }

  browser.runtime.onMessage.addListener((message) => {
    if (message.command === "start") {
      start()
    } else if (message.command === "stop") {
      stop()
    }
  });
})();
