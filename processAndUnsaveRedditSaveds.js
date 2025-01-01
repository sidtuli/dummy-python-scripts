
async function processAndUnsaveRedditSaveds() {

    savedElts = document.getElementsByClassName("saved") 

    nsfwElts = []

    // How to do for each loop - https://stackoverflow.com/questions/9329446/loop-for-each-over-an-array-in-javascript
    for(element of savedElts) {
        //console.log(element.getAttribute("data-nsfw"))
        //dateText = element.querySelector("time").innerText
        //dateCheck = dateText.includes("month")
        dateCheck = true
        if (element.getAttribute("data-nsfw") == "true" && dateCheck) {
            nsfwElts.push(element)
            //console.log(element.querySelector("time").innerText)
        }
    }
    
    textLinks = ""
    //console.log(nsfwElts[0])
    
    for (nsfwElt of nsfwElts) {
        textLink = processNSFWElt(nsfwElt)
        textLinks += textLink + "\n"
        await sleep(5000);
    }
    console.log(textLinks)

}


function processNSFWElt(elt) {
    /*firstLayerNodes = elt.childNodes;
    //console.log(firstLayerNodes)
    
    entryChild = "";
    
    for(child of firstLayerNodes) {
        // checking class list - https://stackoverflow.com/questions/5898656/check-if-an-element-contains-a-class-in-javascript
        // checking element type by node name - https://stackoverflow.com/questions/254302/how-can-i-determine-the-type-of-an-html-element-in-javascript
        if(child.nodeName == "DIV" && child.classList.contains("entry")) {
            entryChild = child;
        }
    }
    
    //console.log(entryChild)
    
    secondLayerNodes = entryChild.childNodes;
    
    topMatterChild = ""
    
    for(child of secondLayerNodes) {
        if(child.nodeName == "DIV" && child.classList.contains("top-matter")) {
            topMatterChild = child
        }
    }
    
    //console.log(topMatterChild)
    
    thirdLayerNodes = topMatterChild.childNodes;
    
    buttonsChild = ""
    
    for(child of thirdLayerNodes) {
        if(child.nodeName == "UL" && child.classList.contains("flat-list")) {
            buttonsChild = child;
        }
    }
    
    //console.log(buttonsChild)
    
    fourthLayerNodes = buttonsChild.childNodes;
    
    shareChild = "";
    
    for(child of fourthLayerNodes) {
        if(child.nodeName == "LI" && child.classList.contains("share")) {
            shareChild = child;
        }
    }
    
    //console.log(shareChild)
    
    fifthLayerNodes = shareChild.childNodes
    
    anchorButtonChild = ""
    
    for(child of fifthLayerNodes) {
        if(child.nodeName == "A" && child.classList.contains("post-sharing-button")) {
            anchorButtonChild = child;
        }
    }
    
    anchorButtonChild.click()
    
    // we then hit the unsave button
    
    unsaveChild = "";
    
    for(child of fourthLayerNodes) {
        if(child.nodeName == "LI" && child.classList.contains("link-unsave-button")) {
            unsaveChild = child;
        }
    }
    
    // using query selector to find sub child elements in html tree - https://bobbyhadz.com/blog/javascript-get-child-element-by-class
    unsaveChild.querySelector("a").click()
    
    
    
    // process the now visible shared post after clicking on share button
    
    thirdLayerNodes = topMatterChild.childNodes;
    
    sharePostChild = "";
    
    for(child of thirdLayerNodes) {
        if(child.nodeName == "DIV" && child.classList.contains("post-sharing")) {
            sharePostChild = child;
        }
    }
    
    //console.log(sharePostChild);
    sharingLinkTextElement = sharePostChild.querySelector("input.post-sharing-link-input")
    //console.log(sharingLinkTextElement.value)
    return sharingLinkTextElement.value*/
    clickUnsaveButton(elt)
    return clickShareButtonAndCollectTextLink(elt)
}

function clickShareButtonAndCollectTextLink(elt){
    shareButton = elt.querySelector("a.post-sharing-button")
    shareButton.click()
    
    sharingLinkTextElement = elt.querySelector("input.post-sharing-link-input")
    return sharingLinkTextElement.value
}

function clickUnsaveButton(elt) {
    unsaveButtonListElt = elt.querySelector("li.link-unsave-button")
    unsaveButtonListElt.querySelector("a").click()
}

// sleep function from here - https://stackoverflow.com/questions/951021/what-is-the-javascript-version-of-sleep
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
