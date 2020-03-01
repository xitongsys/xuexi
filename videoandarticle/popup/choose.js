// const hidePage = `body > :not(.study-window) {
//                     display: none;
//                   }`;

const hidePage = ``;

function listenForClicks() {
  document.addEventListener("click", (e) => {
    function start(tabs) {
      browser.tabs.insertCSS({code: hidePage}).then(() => {
        browser.tabs.sendMessage(tabs[0].id, {
          command: "start"
        });
      });
    }

    function stop(tabs) {
      browser.tabs.removeCSS({code: hidePage}).then(() => {
        browser.tabs.sendMessage(tabs[0].id, {
          command: "stop",
        });
      });
    }

    function reportError(error) {
      console.error(`Could not study: ${error}`);
    }

    if (e.target.classList.contains("start")) {
      browser.tabs.query({active: true, currentWindow: true})
        .then(start)
        .catch(reportError);
    }
    else if (e.target.classList.contains("stop")) {
      browser.tabs.query({active: true, currentWindow: true})
        .then(stop)
        .catch(reportError);
    }
  });
}

function reportExecuteScriptError(error) {
  document.querySelector("#popup-content").classList.add("hidden");
  document.querySelector("#error-content").classList.remove("hidden");
  console.error(`Failed to execute study content script: ${error.message}`);
}

browser.tabs.executeScript({file: "/content_scripts/study.js"})
.then(listenForClicks)
.catch(reportExecuteScriptError);

browser.runtime.onMessage.addListener((message) => {
  if (message.command === "start") {
    browser.tabs.query({currentWindow: true})
    .then((tabs)=>{
      var idx = 0;
      function nextTab(){
        browser.tabs.update(tabs[idx].id, {active: true});
        idx += 1;
        setTimeout(nextTab, 2000);
      }
      nextTab();
    });

  }else if(message.command === "stop") {
    browser.tabs.query({currentWindow: true})
    .then((tabs)=>{
      browser.tabs.remove(tabs.slice(1).map(t=>t.id));
    });
  }
});
