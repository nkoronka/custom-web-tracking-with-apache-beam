/*<![CDATA[*/

/* 
	Base code for custom web tracking. trackEvent() used to send messages to microservice component ]]
	See more info on Git: https://github.com/nkoronka/custom-web-tracking-with-apache-beam
	author: Nick Koronka
	email: nick.koronka@gmail.com
*/

/* global sessionExpiry */
var sessionExpiry = 1800

/* retrieve cookie */
function retrieveCookie (name) {
  var name = name + "="
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';')
  for(var i = 0; i <ca.length; i++) {
    var c = ca[i]
    while (c.charAt(0) == ' ') {
      c = c.substring(1)
    }

    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length)
    }
  }
  return ""
}

/* set cookie */
function setCookie (name, value, expires_in_seconds) {
  var d = new Date()
  d.setTime(d.getTime() + (expires_in_seconds*1000))
  var expires = "expires="+ d.toUTCString()
  document.cookie = name + "=" + value + ";" + expires + ";path=/"
}

/*create new session cookie */
function createSession (){
  var vst = Math.round(new Date()/1000)
  setCookie("sessionCookie", vst, 1800)
  return vst
}

/* elongate session expiry time */
function updateSession (vst){
  setCookie("sessionCookie", vst, 1800)
}

/* retrieve session cookie */
function getSessionCookie (){
  return retrieveCookie("sessionCookie")
}

/* retrieve visitId */
function getVisitId (){
  var vst = getSessionCookie()
  if (vst == ""){
    return createSession()
  } else {
    updateSession(vst)
    return vst
  }
}

/* obtain client id */
function returnClientId (trackingId) {
  try {
    var trackers = ga.getAll()
    var i, len
    for (i = 0, len = trackers.length; i < len; i += 1) {
      if (trackers[i].get('trackingId') === trackingId) {
        return trackers[i].get('clientId')
      }
    }
  } catch(e) {
    return "null"
  }
  return "null"
}

/* obtain url */
function returnURL (){
  return encodeURIComponent(window.location.href)
}

/* obtain hostname */
function returnHostname (){
  return encodeURIComponent(window.location.hostname)
}

function returnPath (){
  return encodeURIComponent(window.location.pathname)
}

/* obtain time */
function returnTime (){
  var timestamp = (new Date).getTime()
  return timestamp
}

/* retrieve first visit start time */
function firstVisitStartTime (){
  return retrieveCookie("_ga").split(".")[3]
}

/* obtain request src */
function returnRequestSrc (trackingId, eventType){
  var location = 'https://web-tracker-210618.appspot.com'
  var cid = returnClientId(trackingId)
  var time = returnTime()
  var hostname = returnHostname()
  var url = returnURL()
  var path = returnPath()
  var fvst = firstVisitStartTime()
  var vst = getVisitId()

  var request = 
  	location + 
  	"?id="+trackingId + 
  	"&t="+time + 
  	"&cid="+cid +
  	"&fvst="+fvst + 
  	"&vst="+vst + 
  	"&eventType="+eventType + 
  	"&hostname="+hostname + 
  	"&url="+url +
  	"&path="+path
  return request
}

/* main tracking function */
function trackEvent (trackingId, eventType){
  var pixel = document.createElement("iframe")
  pixel.async = 'async'
  pixel.width = 1
  pixel.height = 1
  pixel.frameborder = 0
  pixel.style = "display=none"
  pixel.src = returnRequestSrc(trackingId, eventType)
  document.body.appendChild(pixel)
}
/*]]>*/


