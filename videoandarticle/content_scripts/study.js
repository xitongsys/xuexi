function createStudyWindow(id, title){
  var win = document.createElement("div");
  win.className = "study-window";
  win.id = id;
  win.innerHTML = `<h3>` + title + `</h3>`;
  win.style.width = "100%";
  win.style.height = "400px";

  var frame = document.createElement("iframe");
  frame.className = "study-window-iframe";
  frame.id = id + "-iframe";
  frame.style.width = "100%";
  frame.style.height = "400px";
  win.append(frame);
  return win;
}

var videoWindow = createStudyWindow("video-window", "视频学习");
var articleWindow = createStudyWindow("article-window", "文章学习");


(function() {
  if (window.hasRun) {
    return;
  }
  window.hasRun = true;

  var cssurl = browser.extension.getURL("resources/style.css");
  alert(cssurl);

  //videoWin.src = cssurl;
  //document.write('<link rel="stylesheet" type="text/css" href="' + cssurl + '">');

  function start() { 
    document.body.append(videoWindow);
    document.body.append(articleWindow);
  }

  function stop() {
    document.body.remove(videoWindow);
    document.body.remove(articleWindow);
  }

  browser.runtime.onMessage.addListener((message) => {
    if (message.command === "start") {
      start()
    } else if (message.command === "stop") {
      stop()
    }
  });
})();
