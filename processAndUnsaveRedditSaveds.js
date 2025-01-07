async function processAndUnsaveRedditSaveds(checkNSFW = true, dateCheckText="", subredditCheckText="", sleepTime=5000) {

    savedElts = document.getElementsByClassName("saved")

    postsToUnsave = []

    for(element of savedElts) {
        nsfwCheck = (checkNSFW && element.getAttribute("data-nsfw") == "true") || (!checkNSFW && element.getAttribute("data-nsfw") == "false")

        dateText = element.querySelector("time").innerText
        dateCheck = dateText.includes(dateCheckText)

        subredditText = element.querySelector("a.subreddit").innerText
        subredditCheck = subredditText.includes(subredditCheckText)

        if (nsfwCheck && dateCheck && subredditCheck) {
            postsToUnsave.push(element)
        }
    }
    
    textLinks = ""
    
    for (unsavePost of postsToUnsave) {
        textLink = processSavedElt(unsavePost)
        textLinks += textLink + "\n"
        await sleep(sleepTime);
    }
    console.log(textLinks)

}

function processSavedElt(elt) {
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