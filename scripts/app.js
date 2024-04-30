setInterval(myFunction, 1000);

function myFunction() {
  let d = new Date();
  document.getElementById("time").innerHTML=
  d.getHours() + ":" +
  d.getMinutes() + ":" +
  d.getSeconds();
}
