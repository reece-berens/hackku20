'use strict';
const http = require('http');

// Route the incoming request based on type (LaunchRequest, IntentRequest,
// etc.) The JSON body of the request is provided in the event parameter.
exports.handler = function (event, context, callback) {
    try {
        console.log("event.session.application.applicationId=" + event.session.application.applicationId);

        /**
         * Uncomment this if statement and populate with your skill's application ID to
         * prevent someone else from configuring a skill that sends requests to this function.
         */

        if (event.session.new) {
            onSessionStarted({requestId: event.request.requestId}, event.session);
        }

        if (event.request.type === "LaunchRequest") {
            onLaunch(event.request,
                event.session,
                function callback(sessionAttributes, speechletResponse) {
                    context.succeed(buildResponse(sessionAttributes, speechletResponse));
                });
        } else if (event.request.type === "IntentRequest") {
            onIntent(event.request, event.session, callback);
        } else if (event.request.type === "SessionEndedRequest") {
            onSessionEnded(event.request, event.session);
            context.succeed();
        }
    } catch (e) {
        context.fail("Exception: " + e);
    }
};

/**
 * Called when the session starts.
 */
function onSessionStarted(sessionStartedRequest, session) {
    console.log("onSessionStarted requestId=" + sessionStartedRequest.requestId
        + ", sessionId=" + session.sessionId);

    // add any session init logic here
}

/**
 * Called when the user invokes the skill without specifying what they want.
 */
function onLaunch(launchRequest, session, callback) {
    console.log("onLaunch requestId=" + launchRequest.requestId
        + ", sessionId=" + session.sessionId);

    var cardTitle = "Hello, World!";
    var speechOutput = "You can ask for all parking available or for parking at a specific address. What would you like?";
    callback(session.attributes,
        buildSpeechletResponse(cardTitle, speechOutput, "", false));
}

/**
 * Called when the user specifies an intent for this skill.
 */
function onIntent(intentRequest, session, callback) {
    console.log("onIntent requestId=" + intentRequest.requestId
        + ", sessionId=" + session.sessionId);

    var intent = intentRequest.intent,
        intentName = intentRequest.intent.name;

    // dispatch custom intents to handlers here
    if (intentName == 'TestIntent') {
        handleTestRequest(intent, session, callback);
    }
    else if (intentName == 'helloWorld') {
        handleHelloWorldRequest(intent,session,callback);
    }
    else if(intentName == 'AMAZON.StopIntent' || intentName == 'AMAZON.CancelIntent') {
        callback(session.attributes,
                getAlexaSkillSetResponse("Goodbye!", true));
    }
    else if(intentName == 'parkingIntent') {
        handleGarageRequest(intent, session, callback);
    }
    else if(intentName == 'ChuckNorrisIntent') {
        GetChuckNorrisFactIntent(callback);
    }
    else {
        throw "Invalid intent";
    }
}

function handleGarageRequest(intent, session, callback)
{
    var streetName = intent.slots.street.value;
    if(streetName)
    {
        GetOpenSpacesByStreet(callback, streetName);
    }
    else
    {
        GetGarageFactIntent(callback);
    }
}

/**
 * Called when the user ends the session.
 * Is not called when the skill returns shouldEndSession=true.
 */
function onSessionEnded(sessionEndedRequest, session) {
    console.log("onSessionEnded requestId=" + sessionEndedRequest.requestId
        + ", sessionId=" + session.sessionId);

    // Add any cleanup logic here
}


function handleHelloWorldRequest(intent, session, callback) {
    var personName = intent.slots.name.value;
    if(personName) {
        callback(session.attributes,getAlexaSkillSetResponse("I hope you have a wonderful day " + personName + "!", false));
    }
    else {
        callback(session.attributes, getAlexaSkillSetResponse("Have a great day!", false));
    }
}

function handleTestRequest(intent, session, callback) {
    callback(session.attributes,
        getAlexaSkillSetResponse("Hello, world!", true));
}

// ------- Helper functions to build responses -------

function buildSpeechletResponse(title, output, repromptText, shouldEndSession) {
    return {
        outputSpeech: {
            type: "PlainText",
            text: output
        },
        card: {
            type: "Simple",
            title: title,
            content: output
        },
        reprompt: {
            outputSpeech: {
                type: "PlainText",
                text: repromptText
            }
        },
        shouldEndSession: shouldEndSession
    };
}

function buildResponse(sessionAttributes, speechletResponse) {
    return {
        version: "1.0",
        sessionAttributes: sessionAttributes,
        response: speechletResponse
    };
}

function httpGet(query, callback) {
    var options = {
        host: 'hack-ku-2020.appspot.com',
        path: '/garage/allGarages',
        method: 'GET',
    };

    var req = http.request(options, res => {
        res.setEncoding('utf8');
        var responseString = "";

        //accept incoming data asynchronously
        res.on('data', chunk => {
            responseString = responseString + chunk;
        });

        //return the data when streaming is complete
        res.on('end', () => {
            console.log(responseString);
            callback(responseString);
        });

    });
    req.end();
}

function httpGetOpenSpacesByStreet(theStreet, callback) {
    var streetParsed = theStreet.replace(/ /g, '%20');
    var newPath = '/garage/getOpenSpaces?streetLocation=' + streetParsed;
    var options = {
        host: 'hack-ku-2020.appspot.com',
        path: newPath,
        method: 'GET',
    };

    var req = http.request(options, res => {
        res.setEncoding('utf8');
        var responseString = "";

        //accept incoming data asynchronously
        res.on('data', chunk => {
            responseString = responseString + chunk;
        });

        //return the data when streaming is complete
        res.on('end', () => {
            console.log(responseString);
            callback(responseString);
        });

    });
    req.end();
}

function httpGetCN(query, callback) {
    var options = {
        host: 'api.icndb.com',
        path: '/jokes/random',
        method: 'GET',
    };

    var req = http.request(options, res => {
        res.setEncoding('utf8');
        var responseString = "";

        //accept incoming data asynchronously
        res.on('data', chunk => {
            responseString = responseString + chunk;
        });

        //return the data when streaming is complete
        res.on('end', () => {
            console.log(responseString);
            callback(responseString);
        });

    });
    req.end();
}

function GetChuckNorrisFactIntent(callback) {
    httpGetCN('',  (theResult) => {
                console.log("received : " + theResult);
                var obj = JSON.parse(theResult);
                var fact = obj.value.joke
                console.log("Now received: " + fact);
                callback(null,getAlexaSkillSetResponse(fact, true));
            });
}

function GetGarageFactIntent(callback) {
        httpGet('',  (theResult) => {
                console.log("received : " + theResult);
                var dictionary = JSON.parse(theResult);
                var theFact = '';
                for (var key in dictionary) {
                    theFact += 'At ' + key + ' there are ' + dictionary[key] + ' spots available. ';
                }
                callback(null,getAlexaSkillSetResponse(theFact, true));
            });
    }

function GetOpenSpacesByStreet(callback,streetName) {
        httpGetOpenSpacesByStreet(streetName,  (theResult) => {
                console.log("received : " + theResult);
                var obj = JSON.parse(theResult);
                var output = "At " + streetName + ' there are ' + obj + ' spaces available.';
                callback(null,getAlexaSkillSetResponse(output, true));
            });
    }

function getAlexaSkillSetResponse(text, doesEnd) {
    return  {
        version: "1.0",
        response: {
            outputSpeech: {
                type: "PlainText",
                text: text,
            },
            shouldEndSession: doesEnd
        },
        sessionAttributes: {}
    };
}
