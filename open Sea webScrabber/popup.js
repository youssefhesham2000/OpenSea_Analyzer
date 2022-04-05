//start button handler 
function startProcess(){
  console.log("clicked");
  chrome.runtime.sendMessage({Action:"startProgram"})
}
function scrabeByVersion(){
  chrome.runtime.sendMessage({Action:"scrabeByVersion"})
}
document.getElementById("start").addEventListener('click', startProcess);
document.getElementById("scrabeVersion").addEventListener('click',scrabeByVersion)
window.resizeBy(600,800)