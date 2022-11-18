// function qrCode()
// {
// 	fetch('/qrcode')
// 	.then(response=> {
//         if (response.ok) {
//             let date = new Date();
//             aliveSecond = date.getTime();
//             return response.json();
//         }
//     })
// }
function qrCode()
{
    fetch('/qrcode')
        .then(response=>{
            ("#mybutton").click(function (event) { event('/qrcode', { },
                function(data) { }); return false; });
        })
}