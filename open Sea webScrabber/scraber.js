console.log("i am here");
  chrome.runtime.onMessage.addListener(function (response) {
    if (checkAction(response,"startScrabeByVersion")) {
        chrome.storage.sync.get("version",({version})=>{
            console.log("startedin scraber");
            sendVersionToScrabe(version)
          });
        
    }
})
function checkAction(response,Action){
    return response.Action.localeCompare(Action)==0
  }
/**
 * 
 * @api {post} /scrabeByVersion/ send the entered version to scrabe 
 * @apiName sendVersionToSc
 * @apiGroup scrabing
 * @apiBody {Int} versionToSend
 * @apiSuccess {String} status
 * @apiParamExample Request-Example:
 * scrabeByVersion/
 */
 
function sendVersionToScrabe(versionToSend){
    return fetch("http://127.0.0.1:8000/scrabeByVersion/",
    {
     mode:'no-cors',
      method:'post',
              headers: { "Content-Type": "application/json",
              'Accept': 'application/json',
              'Access-Control-Allow-Origin':' *',
              'Access-Control-Allow-Headers': 'Accept'
              },
              
              body:JSON.stringify({version:versionToSend})
    }    
    )  
  }