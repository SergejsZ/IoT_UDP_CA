let aliveSecond = 0;
let heartbeatRate = 1000;
let myChannel = "sergejs_sd3b_pi_channel";
let pubnub;

let previous_message= "";
let current_message = "";
let count = 0;

const setupPubNub = () =>{
    pubnub = new PubNub({
        publishKey: 'pub-c-07659b0d-b4ed-4fed-a636-dabd418f94f3',
        subscribeKey: 'sub-c-f0b1216d-3419-4c2c-bb29-9d7389a11e21',
        userId: "sergejz"
    });

    const listener = {
        status: (statusEvent) => {
            if(statusEvent.category === "PNConnectedCategory"){
                console.log("Connected");
            }
        },
        message: (messageEvent) => {

            console.log(messageEvent.message);
            console.log(messageEvent.timetoken);
            current_message = messageEvent.message;
            if((previous_message === "dawids_motion_detected") && (current_message === "sergejs_motion_detected"))
            {
            count++;
               // document.getElementById(motion_id).innerHTML = "Need to increase count";
                console.log("Increasing count " + count);
            }
            else if((previous_message === "sergejs_motion_detected") && (current_message === "dawids_motion_detected"))
            {
            count--;
                //document.getElementById(motion_id).innerHTML = "Need to decrease count";
                console.log("Decreasing count " + count);
            }
            document.getElementById("motion_id").innerHTML = "Current count " +count;
            previous_message = current_message;
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

			document.getElementById("motion_id").innerHTML = "Current count "+ count;
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