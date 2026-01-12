async function processAndUnsaveRedditSaveds(checkNSFW = null, dateCheckText = "", subredditCheckText = "", sleepTime = 60000) {

    savedElts = document.getElementsByClassName("saved")

    postsToUnsave = []

    for(element of savedElts) {
        nsfwCheck = makeNSFWCheck(checkNSFW, element)

        dateText = element.querySelector("time").innerText
        dateCheck = dateText.includes(dateCheckText)

        subredditText = element.querySelector("a.subreddit").innerText
        subredditCheck = subredditText.includes(subredditCheckText)

        if (nsfwCheck && dateCheck && subredditCheck) {
            postsToUnsave.push(element)
        }
    }
    
    textLinks = ""
    console.log("%d posts to process\nEstimated finish time: %s", 
        postsToUnsave.length,
        calculateEstimateFinishTime(postsToUnsave.length, sleepTime)
    )
    
    for (let i = 0; i < postsToUnsave.length; i++) {
        unsavePost = postsToUnsave[i]
        textLink = processSavedElt(unsavePost)
        textLinks += textLink + "\n"
        if (i + 1 < postsToUnsave.length) {
            await sleep(sleepTime);
        }
    }

    console.log("Processing done, finish time %s", 
        new Date().toString()
    )

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

function calculateEstimateFinishTime(unsavePostCount, sleepGap) {
    currentTime = Date.now();
    return new Date(currentTime + (unsavePostCount * sleepGap) - sleepGap).toString()
}

function makeNSFWCheck(checkNSFW, postElement) {
    if (checkNSFW == null) {
        return true;
    }
    if (checkNSFW) {
        return postElement.getAttribute("data-nsfw") == "true";
    } else {
        postElement.getAttribute("data-nsfw") == "false"
    }
}