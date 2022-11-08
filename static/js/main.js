let aliveSecond = 0;
let heartbeatRate = 100;
    let myChannel = "sergejs_sd3b_pi_channel";
let pubnub;

const setupPubNub = () =>{
    pubnub = new PubNub({
        publishKey: 'sub-c-f0b1216d-3419-4c2c-bb29-9d7389a11e21',
        subscribeKey: 'pub-c-07659b0d-b4ed-4fed-a636-dabd418f94f3',
        userId: "sergejz"
    });

        const listener = {
        status: (statusEvent) => {
            if(statusEvent.category === "PNConnectedCategory"){
                console.log("Connected");
            }
        },
        message: (messageEvent) => {
            console.log(messageEvent);
        },
        presence: (presenceEvent) => {
            //Handle presence
        }
    };
    pubnub.addListener(listener);

    //subscribe to a channel
    pubnub.subscribe({channels: [myChannel]});
};

const publishMessage = async (message) => {
    const publishPayload = {
        channel : myChannel,
        message: {
            title: "Sensor values",
            description: message
        }
    };
    await pubnub.publish(publishPayload);
}


function keepAlive()
{
	fetch('/keep_alive')
	.then(response=>{
		if(response.ok){
			let date = new Date();
			aliveSecond = date.getTime();
			return response.json();
		}
		throw new Error("Server offline")
	})
	.then(responseJson => {
		if(responseJson.motion == 1){
			document.getElementById("motion_id").innerHTML = "Motion Detected";
		}
		else
		{

			document.getElementById("motion_id").innerHTML = "No Motion Detected";
		}

		console.log(responseJson)})
	.catch(error => console.log(error));
	setTimeout('keepAlive()', heartbeatRate);
}


function time()
{
	let d = new Date();
	let currentSec = d.getTime();
	console.log(currentSec - aliveSecond)
	if(currentSec - aliveSecond > heartbeatRate + 1000)
	{

		document.getElementById("Connection_id").innerHTML = "DEAD";
	}
	else
	{
		document.getElementById("Connection_id").innerHTML = "ALIVE";
	}
	setTimeout('time()', 1000);
}

function handleClick(cb){
	if(cb.checked){
		value = "ON";
	}else{
		value = "OFF";
	}
	publishMessage(cb.id+"-"+value);
}