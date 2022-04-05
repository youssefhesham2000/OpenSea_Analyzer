let filterAtt;
let URLS=[];
chrome.runtime.onMessage.addListener(async function (response) {
    if (response.Action.localeCompare("startFiltering") == 0) {
        
        while (true) {
            let ele = getElementsByClass("AssetSearchView--results")
            console.log(ele[0].children[1]);
            getWindowViewElements(ele[0].children[1])
            scroll()
            await sleep(10000)
        }
    }
})



function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
function setSearchAttribute() {
    chrome.storage.sync.get("filterAttribute", ({ filterAttribute }) => {
        filterAtt = filterAttribute
        console.log(filterAtt);
        let elements = getElementsByClass("browser-default Input--input")
        elements[0].value = filterAtt.min;
        elements[1].value = filterAtt.max;
    })

}
const getScrollPosition = (el = window) => ({
    x: el.pageXOffset !== undefined ? el.pageXOffset : el.scrollLeft,
    y: el.pageYOffset !== undefined ? el.pageYOffset : el.scrollTop
});
function scroll() {
    let temp = getScrollPosition()
    window.scrollTo({
        top: temp.y + 1000,
        behavior: 'smooth'
    });
}
function getElement(ID) {
    return document.getElementById(ID);
}

function getElementsByClass(Class) {
    return document.getElementsByClassName(Class);
}
/**
 * 
 *  @api {post} /recieveUrls/ send all the fetched Urls to the python scrabber
 * @apiName sendUrls
 * @apiGroup Urls
 * @apiBody {String[]} Urls
 * @apiSuccess {String} status
 * @apiParamExample Request-Example:
 * recieveUrls/
 */
async function sendUrls(){
    
    return fetch("http://127.0.0.1:8000/recieveUrls/",
    {
    mode: 'no-cors',
      method:'post',
              headers: { "Content-Type": "application/json",
              'Accept': 'application/json',
              'Access-Control-Allow-Origin':'*',
              'Access-Control-Allow-Headers': 'Accept'
              },
              
              body:JSON.stringify(URLS)
    }    
    )  
}

function getWindowViewElements(windowElements) {
    let elements = [];
    console.log(windowElements);
    let childrenDivs = windowElements.children[1].children[0].children[0].children
    for (let i = 0; i < childrenDivs.length; i++) {
        elements[i] = getHref(childrenDivs[i])    
        URLS.push(elements[i])
    }
    console.log(URLS.length);
    if(URLS.length>=100){
        //call the fetch to send the urls to back end and sync the DB
        
        sendUrls()
        console.log(URLS);
        URLS.splice(0, URLS.length)
    }
}
function getHref(element){
    return element.children[0].children[1].children[0].href 
}