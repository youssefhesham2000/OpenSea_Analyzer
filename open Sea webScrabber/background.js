chrome.runtime.onMessage.addListener((response) => {
  if(response.Action.localeCompare("startProgram")==0){
    console.log("started");
    chrome.tabs.query({currentWindow: true,active:true}, function(tabs){
      console.log(tabs[0].url.toString());
     
      chrome.tabs.sendMessage(tabs[0].id,{Action:"startFiltering"} );  
  });
  }
});
chrome.runtime.onMessage.addListener((response) => {
  if(checkAction(response,"scrabeByVersion")){
    console.log("started scrabing");
    chrome.tabs.query({currentWindow: true,active:true}, function(tabs){
     
      chrome.tabs.sendMessage(tabs[0].id,{Action:"startScrabeByVersion"} );  
  });
  }
});
function checkAction(response,Action){
  return response.Action.localeCompare(Action)==0
}

