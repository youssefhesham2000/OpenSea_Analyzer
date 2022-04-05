
let submitButton=document.getElementById("save");
let scrabeVersionButton=document.getElementById("scrabeVersion")
class filterAttributes{
  constructor(min,max){
    this.min=min;
    this.max=max;
  }
}
function scrabeByVersion(){
  let version= document.getElementById("version").value
  console.log(version);
  chrome.storage.sync.set({ version });
}
function saveFilterAttributes(){
  let min=document.getElementById("Min").value
  let max=document.getElementById("Max").value
  let filterAttribute=new filterAttributes(min,max);
  chrome.storage.sync.set({ filterAttribute });
  console.log(filterAttribute);
}


// combinig handlers
scrabeVersionButton.addEventListener('click',scrabeByVersion)
submitButton.addEventListener('click',saveFilterAttributes)